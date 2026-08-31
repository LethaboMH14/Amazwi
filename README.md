# AMAZWI

**The describe-it game — in your language, and it pays.**

Team Sonar's entry for the **MTN MoMo Mini App Hackathon 2026** · Track 2, Entertainment & Lifestyle
Wednesday 2 September 09:30 → Thursday 3 September 12:00 · The Forum, Bryanston

---

## What it is

A speaker gets a word in their own South African language and 30 seconds to describe it — without saying any of four banned words. Two randomly-assigned strangers hear the clip and guess what it was.

**Agreement between independent strangers is the validation.** Nobody reviews anything. There is no approve button. If people understand you, MoMo pays you.

Language learners play the guessing side for free, because guessing what a native speaker just described *is* how you learn a language. Two populations, opposite motivations, one loop — and what comes out is the South African conversational speech data that does not currently exist.

---

## Why it matters

- **There is no working speech recognition for ten of South Africa's eleven spoken official languages.** Whisper scores 146% word error rate on Southern Bantu languages, 223% on Setswana. Above 100% means it invents more words than it gets right.
- **Google's WAXAL dataset contains zero South African languages.** East and West Africa were funded. We were skipped.
- **One hour of in-domain data takes isiZulu from ~146% to about 25% WER.** When the baseline is broken, the first hour is worth more than the next thousand — which is the whole argument for paying people to produce it.

---

## Repository

| Path | Contents |
|---|---|
| **[`05_amazwi/`](05_amazwi/)** | **The current plan.** Start at [`README.md`](05_amazwi/README.md), then [`plan/00_MASTER_PLAN.md`](05_amazwi/plan/00_MASTER_PLAN.md) |
| [`05_amazwi/plan/`](05_amazwi/plan/) | Eleven documents — product, architecture, business case, design system, build plan, pitch, claims register, adversarial review, mockup library |
| [`05_amazwi/research/`](05_amazwi/research/) | Six evidence files — MTN corporate, MoMo API, competitive landscape, speech AI, SA language & culture, market economics |
| [`HANDOVER_SBU.md`](HANDOVER_SBU.md) | Handover brief |
| `01_research/` · `02_ideas/` · `03_build/` | Earlier research and the three-track exploration this entry came out of |

---

## How this was built

The plan was written, then **attacked**. A red-team review produced 23 findings — including a hole that would have killed the core mechanic: nothing checked whether the speaker simply said the banned word, and nothing *could*, because catching it needs exactly the speech recognition the product exists to create. All 23 are recorded in [`08_REDTEAM.md`](05_amazwi/plan/08_REDTEAM.md) and folded into the plan.

Every claim carries a source and a date. Claims that could not be verified are listed as unverified in [`07_TRUTH.md`](05_amazwi/plan/07_TRUTH.md), alongside the things we have decided not to say.

---

*Built in Johannesburg.*
