from sqlalchemy import func, select
from app.models import Card, Campaign, CampaignRewardRule, ConsentGrant, User, VerifierQualification
from app import seed_demo
def test_seed_demo_is_idempotent(db_engine, monkeypatch):
    monkeypatch.setenv("AMAZWI_DATABASE_URL", str(db_engine.url))
    seed_demo.get_engine.cache_clear()
    seed_demo.seed(); seed_demo.seed()
    from app.db import get_engine
    with get_engine().connect() as conn:
        assert conn.execute(select(func.count()).select_from(Card)).scalar_one()==16
        assert conn.execute(select(func.count()).select_from(Campaign)).scalar_one()==2
        assert conn.execute(select(func.count()).select_from(CampaignRewardRule)).scalar_one()==2
        demo_user_ids = [seed_demo._id(key) for key in (
            "speaker:zu", "verifier:zu:1", "verifier:zu:2",
            "speaker:tn", "verifier:tn:1", "verifier:tn:2",
        )]
        assert conn.execute(select(func.count()).select_from(User).where(User.id.in_(demo_user_ids))).scalar_one()==6
        assert conn.execute(select(func.count()).select_from(VerifierQualification)).scalar_one()==4
        assert conn.execute(select(func.count()).select_from(ConsentGrant).where(ConsentGrant.user_id.in_(demo_user_ids))).scalar_one()==8
        bad=conn.execute(select(func.count()).select_from(Card).where((func.cardinality(Card.blocked_words)!=4) | (func.cardinality(Card.accepted_answers)<2) | (func.cardinality(Card.distractors)!=3))).scalar_one()
        assert bad==0
