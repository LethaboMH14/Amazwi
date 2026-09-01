"""Deterministic, advisory Council specialists.

These functions consume redacted persisted facts only. They never mutate
contribution, consent, audio, reward, or model-alias authority state.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib, json
from typing import Any, Protocol, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import CouncilOutput, CouncilOutputState, OutboxEvent

@dataclass(frozen=True)
class ResolutionFacts:
    contribution_id: str
    language: str
    peer_understood: bool
    audio_quality_passed: bool
    model_consent_active: bool
    source_class: str = "AMAZWI_OPTED_IN"

@dataclass(frozen=True)
class SpecialistResult:
    code: str
    evidence: dict[str, Any]
    confidence: float | None = None

class CouncilSpecialist(Protocol):
    name: str
    version: str
    def run(self, facts: ResolutionFacts) -> SpecialistResult: ...

def canonical_sha256(value: dict[str, Any]) -> str:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()

class DataStewardRulesV1:
    name="DATA_STEWARD"; version="rules-1"
    def run(self, facts):
        if not facts.model_consent_active: return SpecialistResult("BLOCKED_CONSENT", {"reason":"training consent absent"})
        if facts.source_class not in {"AMAZWI_OPTED_IN","EXTERNAL_LICENSED"}: return SpecialistResult("BLOCKED_LICENCE", {"source_class":facts.source_class})
        return SpecialistResult("TRAINING_READY", {"source_class":facts.source_class})
class SoundSentinelRulesV1:
    name="SOUND_SENTINEL"; version="rules-1"
    def run(self, facts): return SpecialistResult("RECORDING_OK" if facts.audio_quality_passed else "RE_RECORD_RISK", {"audio_quality_passed":facts.audio_quality_passed})
class LanguageScoutRulesV1:
    name="LANGUAGE_SCOUT"; version="rules-1"
    def run(self, facts): return SpecialistResult("LANGUAGE_REVIEW", {"language":facts.language, "peer_label_preserved":True})
class ExplainerRulesV1:
    name="EXPLAINER"; version="rules-1"
    def run(self, facts): return SpecialistResult("ADVISORY_ONLY", {"authority":"peer_resolution"})

def run_council_event(session: Session, event: OutboxEvent, specialists: Sequence[CouncilSpecialist], now: datetime | None = None) -> list[CouncilOutput]:
    now=now or datetime.now(timezone.utc); payload=event.payload_json
    facts=ResolutionFacts(contribution_id=str(payload["contribution_id"]), language=str(payload.get("language","zu")), peer_understood=bool(payload.get("peer_understood",False)), audio_quality_passed=bool(payload.get("audio_quality_passed",False)), model_consent_active=bool(payload.get("model_consent_active",False)), source_class=str(payload.get("source_class","AMAZWI_OPTED_IN")))
    redacted={"contribution_id":facts.contribution_id,"language":facts.language,"peer_understood":facts.peer_understood,"audio_quality_passed":facts.audio_quality_passed,"model_consent_active":facts.model_consent_active,"source_class":facts.source_class}; input_hash=canonical_sha256(redacted); outputs=[]
    for specialist in specialists:
        existing=session.scalar(select(CouncilOutput).where(CouncilOutput.event_id==event.id,CouncilOutput.specialist==specialist.name,CouncilOutput.model_version==specialist.version))
        if existing and existing.state == CouncilOutputState.SUCCEEDED: outputs.append(existing); continue
        row=existing or CouncilOutput(event_id=event.id,specialist=specialist.name,model_version=specialist.version,state=CouncilOutputState.RUNNING,input_sha256=input_hash,started_at=now)
        if existing is None: session.add(row)
        try:
            result=specialist.run(facts); row.state=CouncilOutputState.SUCCEEDED; row.output_json={"code":result.code,"evidence":result.evidence}; row.confidence=result.confidence; row.completed_at=now
        except Exception as exc:
            row.state=CouncilOutputState.FAILED; row.failure_reason=str(exc)[:2000]; row.retry_count += 1
        outputs.append(row)
    session.commit(); return outputs
