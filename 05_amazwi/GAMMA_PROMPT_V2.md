# AMAZWI - Gamma Generation Prompt v2 (paste into a Gamma account with credits)

This is a single, self-contained prompt. Paste the whole block below (everything between the `=== START ===` and `=== END ===` markers) into Gamma's "Generate" text box on an account that still has credits. It keeps every fix from the earlier rounds (calibration, sandbox labelling, Proven/Pilot/Not Built, banned-phrase list, no em dashes, empty logo band, WAXAL-refined problem, sourced Mupita quote) and adds four new cards: tech architecture, unemployment/skills-gap, cost breakdown, and scale-up.

**Important framing note before you paste this:** this produces a ~13-card *reference* deck, not the ~9-card timed pitch deck. The six spoken beats in `PITCH_SCRIPT.md` still only need cards 1, 2, 3, 5, 6, 7, 8, 12, 13 in the timed run. Cards 4 (architecture), 9 (jobs), 10 (cost), and 11 (scaling) are there for the judges' packet, Round 2, and Q&A depth, not to be spoken through in the 2:30 Round 1 slot. Say this explicitly if anyone asks why the deck has more cards than the timed script uses.

The cost figures on card 10 are labelled illustrative planning estimates throughout, not vendor-quoted or audited numbers; this is deliberate and must not be edited out. Real vendor quotes replace them before any commitment is made.

---

=== START ===

Generate a 16:9 presentation deck. Theme: dark background, black/gray/yellow accent (Bonan Hale style), Instrument Sans headings, Open Sans body. Title: "AMAZWI: MTN MoMo Mini App Hackathon 2026". Absolutely no em dashes anywhere in any card, use commas, periods, or colons instead. Do not invent, add, or extrapolate any statistic, currency amount, or projection beyond what is written below; every number here is either sourced or explicitly labelled as an illustrative estimate, and that labelling must stay visible on the card. No stock photos of people holding phones, no fabricated app UI mockups; imagery should stay abstract, technical, or human-voice themed.

Card 1, title:
AMAZWI. Izwi lakho linenani, your voice has value. MTN MoMo Mini App Hackathon 2026, Track 2: Entertainment and Lifestyle. Team Sonar: Sibusiso Khumalo and Lethabo M. Reserve a clean empty horizontal band here captioned "LOGO ZONE: paste the official MTN and MTN MoMo logos here before presenting." Do not generate or approximate any MTN or MoMo logo.

---

Card 2, the problem, labelled "The Problem":
Google Research's WAXAL programme is real and substantial: 27 African languages, over 100 million speakers, thousands of hours of natural speech, built with African academic and community partners over multiple years. It is exactly the kind of investment this problem needs, and we say so plainly rather than pretend it doesn't exist.

Its current challenge targets Lingala, Shona and Luganda. Not one South African official language is among them.

Here is the real hook: when a person cannot be understood by voice AI, they are locked out of the digital future MTN and everyone else is building. And right now, almost nobody is paying South Africans to fix that gap themselves. Foundation ASR models exceed 100% word-error-rate zero-shot on Southern Bantu languages; in practice these languages are unusable with today's voice AI.

MTN already owns the daily-use surface this data needs to come from: MoMo. A funded, verified mini-app mission gives MTN a governed, consented source of local-language voice-intent data tailored to MoMo use cases, and gives ordinary South Africans a fair, transparent way to be paid for closing that gap themselves.

---

Card 3, how it works, labelled "How AMAZWI Works", render as a clean 3-step horizontal connected-circles diagram:
One person speaks. Two approved peers independently verify the meaning. Agreement credits the AMAZWI ledger once; disagreement pays nothing and records why.
Step 1, Record: speaker records a short phrase in-app, in their own language.
Step 2, Verify: two independent human peers check the meaning; AI advises only and can never overrule them.
Step 3, Resolve: the resolver applies one fixed rule to their verdicts, every time, no exceptions.

---

Card 4, technical architecture, labelled "System Architecture", render as a clean layered technical-architecture diagram with four horizontal layers plus one dotted side-box, top to bottom:
Layer 1, Client: MoMo Mini App, React and TypeScript, three screens: Record, Verify, Wallet and Receipt.
Layer 2, API: FastAPI backend. Consent and identity middleware. Assignment service. Resolver. Ledger.
Layer 3, Data: PostgreSQL. Consent grants. Contributions and verifications. Ledger entries. Transactional outbox for reliable event handling.
Layer 4, External: MTN MoMo Collections API, sandbox environment, OAuth token, requesttopay, status polling.
Side box, dotted border, connected to the API layer with a labelled arrow reading "advisory only, never authoritative": AI Council, an advisory layer that can suggest but never decide; peer verification is the only authority that credits the ledger.
Caption below the diagram: Every layer is real and running today, except the MoMo integration, which is sandbox, and a production MoMo Disbursement leg for speaker cash-out, which is designed but not yet built.

---

Card 5, live demo agreement path, labelled "Live Demo", near-empty huge-type holding slide:
Agreement.
Real device. A peer verifier confirms it matches. The AMAZWI ledger is credited once.

---

Card 6, live demo disagreement path, labelled "Live Demo", near-empty huge-type holding slide:
Disagreement.
Same flow, different verdict: two verifiers disagree. The resolver pays nothing, and the receipt records why. Refusal is a first-class result here, not a hidden failure.

---

Card 7, MoMo evidence, labelled "SANDBOX ONLY" with a warning icon:
Sandbox Collections funding request.
Warning callout: SANDBOX environment only. No speaker was paid. Speaker cash-out is a separate, not-yet-built settlement leg.
Three-item smart layout: OAuth token issued, authentication confirmed in MTN sandbox. Requesttopay, status 202, funding call accepted by MTN sandbox. Status confirmed, status 200: a 202 and a 200 confirm the call reached MTN sandbox and this funds the mission via the AMAZWI ledger, they do not mean a speaker was paid.

---

Card 8, honest status, labelled "Honest Status", render as three clearly distinct columns with strong labels PROVEN, PILOT, NOT BUILT, not a bullet dump:
Column PROVEN, "Running today, tested": consent-gated recording, two-verifier peer decision, idempotent reward ledger, sandbox MoMo Collections funding request for a mission, 264 backend tests passing, CI green.
Column PILOT, "Designed, not yet run with real users": funded missions at scale, multi-language rollout beyond the pilot language, measuring real acceptance and repeat participation.
Column NOT BUILT, "Named honestly, not hidden": speaker cash-out and payout settlement leg, automatic answer-correctness scoring, any margin or cost-saving claim, unmeasured, so not claimed.

---

Card 9, combating unemployment and the skills gap, labelled "Beyond the Corpus":
AMAZWI does not claim to solve unemployment. It offers two specific, honest things instead.

First, a fair alternative to exploitative data-labelling work. Global data-annotation platforms have a documented record of underpaying African workers for exactly this kind of task; independent audits have scored some of them as low as 1 out of 10 on fair pay, and some have shut down entirely. AMAZWI's per-contribution reward is transparent, published, and paid through an auditable ledger, not a black-box piece rate.

Second, a low-barrier on-ramp into real digital skills. Verifying spoken meaning is structured judgment work: listening, comparing, deciding, and it builds exactly the digital literacy and quality-assessment skills the global AI data economy and South Africa's own business-process-outsourcing sector already hire for. That sector alone employs roughly 150,000 people, generates about R53 billion in revenue, and adds around 400 jobs a week, according to BPESA and the dtic. AMAZWI is not that sector. It is a small, honest step toward the same kind of work, done fairly, for people who currently have no paid way into it at all.

---

Card 10, estimated cost, labelled "Illustrative Cost Estimate, Pilot Scope", subtitle in small text: "Planning-level estimate, not vendor-quoted or audited. Confirmed figures required before any commitment."
Two-column layout, "Build" and "Run".
Build column, one-time, pilot-hardening only, the core platform is already built: production hardening, authentication, rate limits, PII-safe logging, and a MoMo Disbursement integration, estimated three to four weeks for one to two engineers. Pilot-language content and native-speaker quality review, estimated one to two weeks plus a small honorarium budget.
Run column, monthly, illustrative, at a pilot scale of roughly 1,000 verified contributions a month: cloud hosting for the API, database, and private audio storage, estimated three thousand to six thousand Rand a month on a small managed tier. Verifier and speaker reward pool, 1,000 contributions at an illustrative two Rand each equals two thousand Rand a month, and this scales linearly with participation; it is the funded-missions budget itself and is typically sponsor-funded, not a hidden cost. MoMo Collections and Disbursement transaction fees, not yet known, to be confirmed directly with MTN as part of this partnership. Moderation and operations support, estimated part-time, small honorarium.
Closing line, bold: Total illustrative monthly run cost for the pilot, excluding MoMo fees which are still to be confirmed, is roughly five thousand to ten thousand Rand a month. It is intentionally small because this is a contained, one-language pilot, not a launch.

---

Card 11, how this scales, labelled "Scaling Path":
Technical scaling: a new language is a governed content pack and a verifier cohort, not new code; the backend is language-parameterised by design. The API is stateless and scales horizontally behind a load balancer. The transactional outbox pattern already in production supports background workers and queues as volume grows. PostgreSQL scales with read replicas and partitioning as contribution volume increases.
Operational scaling, in order: one MTN-supported pilot language first. Then the remaining South African official languages. Then MTN's other African markets, where the same funded-mission model applies to different language gaps. Then deeper MoMo use cases, agent and merchant voice banking, USSD-alternative voice interfaces, as data quality and volume mature enough to support them.
Closing line: Every stage before disbursement and multi-language rollout is a decision to spend more, not a technical rewrite. That is deliberate.

---

Card 12, what the pilot measures, labelled "Pilot Design":
None of these numbers exist yet. Each is a commitment to measure and report back, not a claim.
Six-item vertical smart layout with icons: repeat MoMo opens. Funded mission participation. Cost per eligible contribution. Verifier liquidity. Settlement feasibility. Usefulness of intent-labelled speech for MTN's own voice products.

---

Card 13, the ask, labelled "The Ask":
One MTN-supported language pilot, plus a MoMo partnership to test funded missions and provider settlement.
Two-column layout. Left column, "What we are not claiming": we are not claiming revenue before measuring it. The pilot tests whether funded mini-app missions increase repeat MoMo use and produce useful, consented voice-intent data, at a cost MTN can support.
Right column, "What MTN gets": a daily-use engagement engine. A dormant-wallet reactivation path. A start on an African-language dataset built with real, revocable consent. A direct input to MTN's own disclosed AI infrastructure investment, the 150MW AI data centre programme named in MTN's H1 2026 results, with South Africa and Nigeria as priority markets. As MTN's own Group President Ralph Mupita has said: "I think the next frontier is how do we develop the digital services ourselves that we can have our customers consume."
Closing quote block, bold: Speak. Be understood. Earn.

=== END ===

---

## Banned phrases, do a final search across every generated card and remove any hit before presenting
- "your MoMo wallet is credited"
- "cash-out is live"
- "money crossed MoMo twice"
- "k-anonymised" or "k-anonymity"
- "the dataset nobody else has built"
- any percentage or number attached to MTN revenue, savings, or margin
- "only" or "first" used as a competitive superlative
- any em dash

## Sources for every sourced claim above, for your own records
- Google Research WAXAL challenge scope (27 languages, 100m+ speakers, thousands of hours, Lingala/Shona/Luganda target languages): the WAXAL challenge brief the user supplied directly.
- Foundation ASR 100%+ WER zero-shot on Southern Bantu languages: Marivate et al., arXiv.
- Whisper large-v3-turbo 146.30% WER / 223% Setswana: arXiv 2606.31642 (named benchmark, do not universalise).
- Data-annotation platform fair-pay record: Remotasks Kenya shutdown March 2024, Fairwork score 1/10; Sama/OpenAI Kenya worker pay $1.32-2/hr vs $12.50/hr billing rate, TIME investigation. Both in `05_amazwi/plan/07_TRUTH.md`.
- South African BPO sector: ~150,000 employed, ~R53bn revenue (2024), ~400 jobs/week, BPESA/dtic. In `07_TRUTH.md`.
- MTN 150MW AI data centre plan, H1 2026 results, SA/Nigeria priority markets: ITWeb; MTN H1 2026. In `07_TRUTH.md`.
- Ralph Mupita quote, verbatim: Joyce Onyeagoro, "Ralph Mupita on MTN's New Frontier: Connectivity, Content, and African AI," TechAfrica News, 9 Apr 2026.
- 264 backend tests, CI green, sandbox MoMo Collections evidence: this repository's own verified build (`BUILD_LOG.md`).

The cost figures on card 10 are the one part of this deck that is not independently sourced; they are a planning-level illustrative estimate built from generic small-scale cloud hosting costs and the project's own existing illustrative R2.00 per-contribution reward rate (already used elsewhere in `03_BUSINESS.md`/`17_BUSINESS_CASE.md`). Say so if asked, and get real vendor quotes before any commitment.
