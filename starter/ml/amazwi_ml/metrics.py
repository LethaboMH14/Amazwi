"""Deterministic ASR metrics and immutable evaluation slice reports."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass


class InvalidReference(ValueError):
    """A non-empty hypothesis cannot be scored without reference material."""


@dataclass(frozen=True)
class TokenSpan:
    start: int
    end: int
    language: str


@dataclass(frozen=True)
class AsrCase:
    case_id: str
    reference: str
    hypothesis: str
    language: str
    speaker_id: str
    domain: str = "unknown"
    acoustic_condition: str = "unknown"
    spans: tuple[TokenSpan, ...] = ()


@dataclass(frozen=True)
class MetricSlice:
    name: str
    case_count: int
    reference_count: int
    errors: int
    rate: float
    wer: float
    cer: float
    embedded_span_error: float


@dataclass(frozen=True)
class AsrMetricReport:
    case_count: int
    slices: tuple[MetricSlice, ...]


def normalise_transcript(text: str) -> str:
    text = unicodedata.normalize("NFC", text).casefold()
    text = "".join(
        " " if unicodedata.category(char).startswith("P") else char
        for char in text
        if not unicodedata.category(char).startswith("M")
    )
    return " ".join(text.split())


def _alignment(reference: Sequence[str], hypothesis: Sequence[str]) -> tuple[int, list[tuple[str, int | None, int | None]]]:
    rows, cols = len(reference), len(hypothesis)
    costs = [[0] * (cols + 1) for _ in range(rows + 1)]
    ops: list[list[str]] = [["eq"] * (cols + 1) for _ in range(rows + 1)]
    for i in range(1, rows + 1):
        costs[i][0], ops[i][0] = i, "delete"
    for j in range(1, cols + 1):
        costs[0][j], ops[0][j] = j, "insert"
    priority = {"eq": 0, "substitute": 1, "delete": 2, "insert": 3}
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            candidates = [
                (costs[i - 1][j - 1] + (reference[i - 1] != hypothesis[j - 1]), "eq" if reference[i - 1] == hypothesis[j - 1] else "substitute"),
                (costs[i - 1][j] + 1, "delete"),
                (costs[i][j - 1] + 1, "insert"),
            ]
            costs[i][j], ops[i][j] = min(candidates, key=lambda item: (item[0], priority[item[1]]))
    aligned: list[tuple[str, int | None, int | None]] = []
    i, j = rows, cols
    while i or j:
        op = ops[i][j]
        if op in {"eq", "substitute"}:
            aligned.append((op, i - 1, j - 1)); i -= 1; j -= 1
        elif op == "delete":
            aligned.append((op, i - 1, None)); i -= 1
        else:
            aligned.append((op, None, j - 1)); j -= 1
    return costs[rows][cols], list(reversed(aligned))


def _tokens(text: str) -> list[str]:
    value = normalise_transcript(text)
    return value.split() if value else []


def word_error_rate(reference: str, hypothesis: str) -> float:
    ref, hyp = _tokens(reference), _tokens(hypothesis)
    if not ref:
        if not hyp:
            return 0.0
        raise InvalidReference("reference must be non-empty")
    return _alignment(ref, hyp)[0] / len(ref)


def character_error_rate(reference: str, hypothesis: str) -> float:
    ref = normalise_transcript(reference).replace(" ", "")
    hyp = normalise_transcript(hypothesis).replace(" ", "")
    if not ref:
        if not hyp:
            return 0.0
        raise InvalidReference("reference must be non-empty")
    return _alignment(list(ref), list(hyp))[0] / len(ref)


def embedded_span_error(reference: str, hypothesis: str, spans: Sequence[TokenSpan]) -> float:
    ref, hyp = _tokens(reference), _tokens(hypothesis)
    if not ref:
        if not hyp:
            return 0.0
        raise InvalidReference("reference must be non-empty")
    alignment = _alignment(ref, hyp)[1]
    selected = {(index, span.language) for span in spans for index in range(span.start, span.end)}
    denominator = sum(1 for index, _ in selected if 0 <= index < len(ref))
    if not denominator:
        return 0.0
    errors = 0
    for op, ref_index, _ in alignment:
        if op in {"substitute", "delete"} and ref_index is not None and any(ref_index == index for index, _ in selected):
            errors += 1
        elif op == "insert":
            left = (ref_index if ref_index is not None else 0)
            if any(left == index for index, _ in selected):
                errors += 1
    return errors / denominator


def _slice(name: str, cases: Sequence[AsrCase]) -> MetricSlice:
    ref_words = sum(len(_tokens(case.reference)) for case in cases)
    errors = sum(_alignment(_tokens(case.reference), _tokens(case.hypothesis))[0] for case in cases)
    ref_chars = sum(len(normalise_transcript(case.reference).replace(" ", "")) for case in cases)
    char_errors = sum(_alignment(list(normalise_transcript(case.reference).replace(" ", "")), list(normalise_transcript(case.hypothesis).replace(" ", "")))[0] for case in cases)
    spans = [span for case in cases for span in case.spans]
    embedded = sum(embedded_span_error(case.reference, case.hypothesis, case.spans) for case in cases) / len(cases) if cases else 0.0
    return MetricSlice(name, len(cases), ref_words, errors, errors / ref_words if ref_words else 0.0, errors / ref_words if ref_words else 0.0, char_errors / ref_chars if ref_chars else 0.0, embedded)


def evaluate_asr(cases: Sequence[AsrCase]) -> AsrMetricReport:
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("duplicate case IDs")
    if any(not case.language or not case.speaker_id for case in cases):
        raise ValueError("language and speaker IDs are required")
    groups: dict[str, list[AsrCase]] = {"aggregate": list(cases)}
    for attr, prefix in (("domain", ""), ("language", ""), ("acoustic_condition", "acoustic:")):
        for value in sorted({getattr(case, attr) for case in cases}):
            groups[prefix + value] = [case for case in cases if getattr(case, attr) == value]
    names = ["aggregate"]
    for attr, prefix in (("domain", ""), ("language", ""), ("acoustic_condition", "acoustic:")):
        names.extend(prefix + value for value in sorted({getattr(case, attr) for case in cases}))
    ordered = [groups[name] for name in names]
    return AsrMetricReport(len(cases), tuple(_slice(name, group) for name, group in zip(names, ordered)))
