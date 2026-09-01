from app.models import AudioObject, AudioObjectState, CampaignRewardRule, ConsentScope, VerifierQualification


def test_governance_audio_records_are_defined():
    assert ConsentScope.RECORD_PROCESS_ROUND.value == "RECORD_PROCESS_ROUND"
    assert AudioObjectState.AVAILABLE.value == "AVAILABLE"
    assert AudioObject.__tablename__ == "audio_objects"
    assert VerifierQualification.__tablename__ == "verifier_qualifications"
    assert CampaignRewardRule.__tablename__ == "campaign_reward_rules"
