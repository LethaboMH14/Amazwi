# REGISTRATION SUBMISSION PACK — all three entries
**Created:** 2026-08-15 · Session 3 · MoMo Mini App Hackathon 2026
**Everything below is copy-paste ready.** Each block is marked with the form question number.

---

## ⚠️ READ BEFORE ANYONE PASTES ANYTHING

**1. The multi-submission rule is still unconfirmed.** The T&Cs describe teams of ≤4 **or** individuals. Three people registering individually under one shared team name may or may not be permitted. **Get this answered in writing before submitting.** If it is disallowed, submit **Umoya only**.

**2. Tense matters — the T&Cs prohibit pre-existing projects.** Every description below is written in **planned/intended** tense ("will be built", "the architecture is designed as"). **Do not change this to past tense.** Do not claim anything is already built. If asked at check-in, the honest answer is: research, architecture and design were prepared in advance; all code is written at the event.

**3. Do not paste the section markers** (`--- Q8 ---` etc). Paste only the content beneath each one.

**4. Character counts are verified.** All three short summaries are under 250. Do not edit them without recounting — Microsoft Forms will silently truncate or reject.

**5. Team name** — use the identical string on all three forms: `South Africa-Umoya`

**6. GitHub URL** — all three repos must exist before submitting. Suggested: `github.com/<org>/umoya`, `/amazwi`, `/hamba`. Create them with a README only.

---
---

# ENTRY 1 · UMOYA — *Lethabo*

## --- Q8: Track ---

```
Track 1: Everyday Essentials
```

## --- Q9: Short summary (222 characters) ---

```
Umoya puts MoMo's intelligence in MTN's network instead of your phone. Speak isiZulu into a R149 Nokia. Transact with no data and no signal. Keep your money when the phone is taken at gunpoint. Banking that works, even if.
```

## --- Q10: Detailed description ---

```
UMOYA — "even if"
An AI money agent that lives in MTN's network, not on your phone.

=====================================================
1. PROBLEM STATEMENT
=====================================================

Every fintech product in South Africa is built for the smartphone. The smartphone is the least reliable object in a South African's life.

It gets stolen. 412,998 mobile phones were reported stolen between April 2017 and March 2023 — 189 a day, and that is a floor, because only 31% of victims report theft at all. Only 29% of stolen phones are ever blacklisted.

Theft is now a financial crime. SABRIC's 2025 Annual Banking Crime Statistics record R2.4 billion in digital banking crime losses, up 29.2% year on year. Banking app fraud alone accounts for 97,555 cases — 88.6% of all banking crime cases and 70.5% of claim value, averaging R17,400 per victim. In the same year, physical bank robberies yielded R630,000 across two incidents. The ratio is roughly 3,800 to 1. Criminals stopped robbing banks and started robbing phones.

It is now violent. Kidnapping in South Africa has risen 264% since 2014/15 to 17,061 incidents, running at approximately 53 per day. Of these, 44% are linked to hijackings and 22% to robberies; only 4% involve ransom. Nearly 80% of Gauteng kidnappings are tied to armed robbery. SABRIC describes the pattern directly: perpetrators detain victims "just long enough to coerce them into draining their accounts."

It runs out of data. A South African who can afford R89 upfront pays R17.80 per gigabyte. A South African who can only afford R249 for 4GB pays R62.25 per gigabyte. The poorest pay 3.5 times more per unit of data.

It is not universal. 16% of South African mobile connections are feature phones. MTN South Africa itself sold 29% 2G devices in 2023/24. Neither MTN nor Vodacom has committed to a 2G sunset date, and MTN has stated it will retain a 2G layer.

It cannot understand us. South Africa has 12 official languages. English is only the fifth most-spoken home language at 8.7%. Approximately 29 million South Africans are not proficient in English, and 3.8 million adults over 20 are classified as illiterate. Google Cloud Speech-to-Text has a 56.71% word error rate on isiXhosa in realistic conversational speech, against a 9.6% human baseline. Meta MMS scores 92.50%. Foundation ASR models score above 100% WER zero-shot on all six Southern Bantu languages — worse than producing no output at all.

The result is measurable. 84% of South African adults hold a bank account, but approximately 14 million practise what FinScope calls "mailbox banking" — the account exists only to receive money and immediately withdraw it. 76% of grant recipients withdraw their entire benefit on receipt. 71% of adults still use cash primarily for food and groceries. Across Africa, over 70% of registered mobile money accounts are dormant; only 25.7% are active in any given month.

South Africa's financial inclusion problem is not access. It is usage. And usage fails at exactly the points where the phone fails.

=====================================================
2. THE SOLUTION
=====================================================

Umoya inverts the assumption that the wallet lives on the handset.

Umoya is an AI money agent that runs in MTN's network. The user reaches the same agent, the same identity and the same balance through five surfaces:

  1. VOICE CALL — dial a number and speak. isiZulu, isiXhosa, Sesotho, Setswana, Afrikaans, English, or any mixture of them. No app. No data. No literacy required. Works on any handset that can make a call.
  2. USSD — a menu inside the channel users already open, delivered through MTN's Interact (Channel as a Service) API. Zero data.
  3. MINI APP (PWA) — the rich surface for smartphone users, built to the MoMo Mini App PWA specification.
  4. SMS — confirmations, alerts and receipts via the Notify API, reaching users with no data at all.
  5. OFFLINE NFC TAP — cryptographically signed value tokens transferred device-to-device with no network whatsoever, settling on reconnection.

The phone becomes a terminal, not the wallet.

Umoya delivers five capabilities:

SPEAK — Conversational money in South African languages, including code-switched speech ("ngicela i-data"), which is how South Africans actually talk and which no global vendor benchmark tests.

SURVIVE — Theft and duress defence. If the handset is lost or stolen, the user borrows any phone, calls, is verified, and freezes everything, because identity was never bound to the device. Critically, Umoya introduces a DURESS PIN: entering the real PIN transacts normally; entering the duress PIN displays a plausible reduced balance and executes a transfer that appears to complete successfully while moving nothing, while silently alerting MTN, the user's nominated contacts, and logging network location. The attacker receives nothing and does not know. High-value transfers to new recipients are time-locked and cancellable from any handset. Account recovery runs through the user's verified transaction graph rather than through the SIM, which structurally defeats SIM-swap fraud — currently 43% of all African mobile money fraud, with approximately 90% of SIM swaps occurring without the victim's awareness.

ACT — Programmable standing authority. MTN publishes a Get Consent API providing USSD-delivered, MoMo-PIN-authenticated consent. Combined with Invoice and Pay, this is a signed mandate primitive: effectively direct debit for the unbanked, which Africa structurally lacks. Umoya maps this onto the Intent Mandate / Cart Mandate structure defined by Google's Agent Payments Protocol (AP2), making MoMo the first African wallet with an agent-mandate layer. Mandates are scoped, capped, revocable and PIN-signed. Because Visa's own research finds 60% of consumers will not permit an AI to spend any amount without approval, every autonomous action is a proposal requiring explicit voice or USSD approval before execution.

FORESEE — Predictive protection. Peer-reviewed research (Björkegren & Grissen) shows mobile phone usage data predicts loan repayment at AUC 0.71–0.77, against 0.51–0.57 for a conventional credit bureau — barely better than chance for this population. The single strongest predictor is periodicity of usage, a proxy for income regularity. Umoya turns this signal inward: rather than selling a score to a lender, it warns the user. "Your income has been irregular for three weeks. At this rate you run out of transport money on the 23rd, four days before payday. Shall I ring-fence R180 now?" It also surfaces documented arbitrage the market hides — the 3.5x data poverty premium, and the electricity advance trap where a ~R5 fee on a R20–R50 advance compounds into hundreds of rands a year.

ENDURE — Offline value transfer. Android Host-based Card Emulation supports device-to-device NFC with no network and no secure element. Umoya implements Ed25519-signed value tokens carrying an ancestry chain, following the architecture published by the US Federal Reserve in December 2025 ("A Robust Risk Framework for Offline Payments"), with a stated risk budget modelled on production systems: R500 offline float ceiling, 24-hour token validity, approximately 10 hops before forced resynchronisation, and ancestry-chain replay detection at settlement.

=====================================================
3. WHY WE CHOSE THIS
=====================================================

Three reasons.

First, structural defensibility. MTN is simultaneously the mobile network operator and the wallet. Putting the money intelligence inside the network is something Capitec, TymeBank, Shop2Shop, Yoco, OPay and every neobank in Africa physically cannot replicate, because they do not own the SIM, the voice channel, the USSD menu or the network graph. This is not a feature advantage. It is a structural one.

Second, timing. In June 2026 MTN Group Fintech partnered with Ant International to build the next-generation MoMo super app and mini app platform, launching first in Nigeria in Q3 2026 — the same quarter as this hackathon. MTN has purchased the rails and has 69.5 million monthly active users. What it does not yet have is locally relevant supply. Separately, MTN removed Ayoba from the app stores on 20 March 2026 after it peaked at 35 million MAU and failed on retention. MTN has publicly committed to AI — a Huawei MoU including a Technology Innovation Lab in South Africa, AI data centres in South Africa and Nigeria — while shipping no consumer AI product. Umoya is the consumer AI product that only MTN can ship.

Third, the data barrier just fell. The Swivuriso corpus (South African Next Voices) released 3,016 hours of speech across seven South African languages, 483,191 clips from 2,440 speakers, under a CC BY 4.0 licence. Baseline results show fine-tuning takes Setswana from 223% WER to 13%, and Xitsonga from 190% to 12%. Meanwhile Google's February 2026 WAXAL release covered 11,000 hours across 27 Sub-Saharan languages and included zero South African official languages. The raw material to build South African voice AI became free and legally usable this year, and nobody has productised it.

=====================================================
4. HOW IT WORKS — USER JOURNEY
=====================================================

ONBOARDING: The user opens Umoya inside the MoMo super app, or dials the Umoya number from any handset. Identity is established through the MoMo Identify (KYC) API, so Umoya never collects or stores identity documents. The user records a short voice enrolment, sets a transaction PIN and a separate duress PIN, and nominates emergency contacts.

DAILY USE (SMARTPHONE): The user opens the mini app. A single-column dashboard shows balance, active mandates, upcoming predicted shortfalls and pending agent proposals. Speaking or typing an instruction in any supported language executes it after read-back confirmation.

DAILY USE (FEATURE PHONE): The user dials the Umoya number, hears a greeting in their registered language, and speaks. "Ngingakanani?" returns the balance. "Thumela u-two hundred rand ku-mama" initiates a transfer, reads the recipient and amount back for confirmation, and executes on PIN entry. Alternatively the user dials the USSD short code and navigates a menu.

SETTING A MANDATE: The user says "buy R100 of electricity whenever I drop below 20 units, twice a month maximum." Umoya constructs a scoped mandate, presents its exact terms for confirmation, and captures PIN-signed consent through the Get Consent API. The mandate is revocable at any time from any surface.

A PREDICTED SHORTFALL: Umoya's forecasting model detects irregular inflow and a projected transport-money shortfall. It calls or messages the user in their language, states the projection plainly, and proposes ring-fencing a specific amount. Nothing moves without approval.

PHONE STOLEN: The user borrows any handset, calls Umoya, and is verified through PIN plus behavioural and network signals. All outbound transactions are frozen instantly. Recovery proceeds through the verified transaction graph.

UNDER DURESS: The attacker demands the user transfer funds. The user enters the duress PIN. The interface displays a plausible reduced balance and completes a realistic-looking transfer. No value moves. MTN, nominated contacts and network location are alerted silently.

NO NETWORK: The user taps their handset against a merchant's, transferring a signed value token over NFC within the offline float ceiling. Both devices hold the token; it settles when either reconnects.

=====================================================
5. SYSTEM ARCHITECTURE
=====================================================

Umoya is a layered, event-driven system. Six layers:

LAYER 1 — CHANNEL LAYER (the five surfaces)
 - Voice gateway: SIP/PSTN termination, call session management, barge-in handling
 - USSD gateway: session state machine (state held server-side, since GSM 02.90 places no session state in the handset), 182-character response budget, menus capped at five levels
 - PWA client: service worker, offline shell, IndexedDB queue for deferred actions
 - SMS gateway: outbound transactional messaging
 - NFC/HCE client: Android HostApduService, APDU exchange budgeted at ~1KB within ~300ms

LAYER 2 — CONVERSATION LAYER
 - Cascaded speech pipeline: ASR → intent parsing → dialogue state → response generation → TTS. Deliberately CASCADED rather than speech-to-speech, because telephony audio is 8kHz narrowband and published benchmarks show speech-to-speech models lose their quality advantage over PSTN while retaining premium cost.
 - Language identification and code-switch handling
 - Read-back confirmation service: every value-bearing instruction is restated in the user's language before execution, with numeric amounts confirmed by keypad entry where ASR confidence is below threshold

LAYER 3 — AGENT & MANDATE LAYER
 - Intent router mapping utterances to a constrained set of typed financial actions (no free-form execution)
 - Mandate engine: creation, scoping, capping, expiry, revocation; AP2-aligned Intent/Cart mandate structures
 - Proposal queue: all autonomous actions enter as proposals requiring explicit approval
 - Policy engine enforcing per-transaction, daily and cumulative limits

LAYER 4 — INTELLIGENCE LAYER
 - Forecasting service: income regularity, balance runway, consumption prediction
 - Risk and anomaly engine: behavioural signals, device and SIM state, transaction graph features
 - Duress detection and silent alerting
 - Recovery graph service

LAYER 5 — LEDGER & SETTLEMENT LAYER
 - Transaction orchestrator with idempotency enforced on X-Reference-Id (UUID v4 per request)
 - Dual-mode outcome handling: webhook receiver AND status polling, because conference and field connectivity break webhooks
 - Offline token service: issuance, ancestry-chain validation, settlement reconciliation, double-spend detection
 - Escrow and time-lock state machines

LAYER 6 — INTEGRATION LAYER
 - MoMo API client with OAuth token lifecycle management (tokens expire in 3600 seconds; refresh is not optional)
 - Circuit breakers, exponential backoff, dead-letter queues
 - Simulation harness: a "simulate success" toggle and a synthetic network-signal feed, so the demo survives sandbox instability

CROSS-CUTTING: authentication and authorisation, secrets management, structured audit logging, distributed tracing, feature flags.

DATA FLOW (voice transaction): call arrives → voice gateway opens session → audio streamed to ASR → transcript to intent router → typed action constructed → policy engine validates against limits → read-back generated and spoken → user confirms → PIN captured → transaction orchestrator generates X-Reference-Id → MoMo Collections/Disbursements called → 202 accepted → webhook or poll resolves outcome → ledger updated → SMS confirmation dispatched via Notify → spoken confirmation delivered → call ends.

=====================================================
6. AI / ML ARCHITECTURE
=====================================================

SPEECH RECOGNITION
Base model: Whisper large-v3-turbo, fine-tuned on the Swivuriso corpus (CC BY 4.0, 3,016 hours, 7 South African languages) using parameter-efficient fine-tuning (LoRA). W2V-BERT evaluated as a comparator, since published results show it outperforms Whisper on Nguni languages while Whisper leads on Sotho-Tswana — so per-language model selection is a deliberate design decision, not an oversight. Inference served through CTranslate2/faster-whisper for latency. Telephony-band data augmentation (8kHz downsampling, AMR-NB codec simulation) applied during fine-tuning so the model is trained on the audio it will actually receive.

CODE-SWITCH HANDLING
Code-switching degrades monolingual ASR by 30–50% WER and is untested by every frontier vendor benchmark. Umoya applies a language-identification frontend with frame-level switching, plus targeted fine-tuning on code-switched utterances, drawing on the South African code-switched corpora developed at Stellenbosch University.

INTENT UNDERSTANDING
A constrained intent classifier over a closed action set, backed by a small commercially-licensed language model for slot filling and disambiguation. Note: InkubaLM, the leading African-language small model, is released under CC BY-NC and therefore cannot be used commercially; commercially-licensed alternatives in the same size class are used instead. The action set is closed by design — the model never generates free-form financial instructions.

SPEECH SYNTHESIS
Simba-TTS (CC-BY-4.0, covering Afrikaans, Southern Sotho, Tswana and Xhosa) and Meta MMS-TTS, with fallback to pre-recorded prompt concatenation for high-frequency confirmations, which guarantees intelligibility for the phrases that carry money.

FORECASTING
Gradient-boosted models (LightGBM) and classical time-series methods over transaction periodicity, inflow regularity, consumption slope and seasonality. Feature design follows the published finding that periodicity and slope of usage carry the predictive signal, not absolute amounts.

ANOMALY AND FRAUD DETECTION
Isolation forests and gradient-boosted classifiers over behavioural, device, SIM-state and velocity features. Graph features (transaction-network centrality, recipient tenure, relationship age) computed over the user's verified counterparty graph.

AUTHENTICATION — AN EXPLICIT DESIGN DECISION
Voice is the INTERFACE. Voice is NOT the lock.
Published peer-reviewed research demonstrates that open-source voice cloning trained on only 10–30 minutes of scraped audio bypasses speaker verification systems tuned to a 0.01% false-accept rate 82.7% of the time, and that anti-spoofing countermeasures degrade approximately 30-fold out of domain (0.83% to 24.84% EER). The New York Department of Financial Services advises combining cryptographic and biometric factors rather than relying on voice alone.
Umoya therefore authenticates on: PIN (Argon2id-hashed), behavioural signals, device and SIM state, network location consistency, and transaction-graph history. Voiceprint is used only as one low-weight signal in a risk score and never as a sole factor, with an anti-spoofing layer and explicit fallback to PIN. We state this openly because the alternative — pitching voice biometrics as authentication — is not defensible in 2026.

FAIRNESS
Documented risk exists that models trained on high-activity users (disproportionately urban and male) systematically undervalue rural usage patterns. Mitigations: the forecasting model serves the user and is never used to price them; stratified evaluation across language, province and urban/rural cohorts; reported openly rather than buried.

=====================================================
7. MOMO API INTEGRATION
=====================================================

  Get Paid (Collections)  — inbound payment requests, refunds, status, balance
  Pay (Disbursements)     — outbound transfers, payouts, escrow release
  Get Consent             — PIN-signed mandate capture; the core primitive for the ACT layer
  Identify (KYC)          — identity verification without collecting or storing identity
  Notify                  — transactional SMS to users with no data
  Invoice                 — deferred and staged payments underpinning mandates
  Interact (CaaS)         — insertion into the MoMo USSD and app menu; feature-phone reach
  Manage                  — reconciliation and transaction visibility
  Collection Widget       — QR-based collection

Auth: Ocp-Apim-Subscription-Key per product; API User ID and API Key per environment; Bearer access token via POST /{product}/token/ with Basic auth, refreshed on a 3600-second lifecycle. Every transactional call carries a fresh UUID v4 X-Reference-Id as the idempotency key, with X-Target-Environment set to the South Africa environment and X-Callback-Url configured. The asynchronous request-to-pay model is handled by implementing BOTH webhook receipt and status polling.

CAPABILITIES REQUIRING MTN PARTNERSHIP (stated openly, not hidden):
SIM-swap events, SIM tenure and network-location signals are not exposed through public MoMo APIs. Umoya will be built against a simulated signal feed with an identical interface contract, and the data-sharing agreement is presented as an explicit partnership proposal rather than an assumed capability. Similarly, Interact channel provisioning requires MTN action; the USSD surface will be demonstrated through an equivalent gateway until provisioned.

=====================================================
8. SDLC AND DELIVERY METHODOLOGY
=====================================================

METHODOLOGY: Trunk-based development with short-lived feature branches, continuous integration on every push, and time-boxed iterations. Given the compressed timeline, the team operates on a daily cadence: morning planning, midday integration checkpoint, end-of-day demo of working software.

PHASES
 Phase 0 — Discovery and architecture (completed prior to the event: research, sourcing, architectural design, API study, corpus identification. No application code.)
 Phase 1 — Foundation: repository, CI pipeline, MoMo sandbox connectivity, one successful end-to-end request-to-pay, deployment target live
 Phase 2 — Core: transaction orchestrator, ledger, PWA shell, PIN and duress logic
 Phase 3 — Intelligence: ASR fine-tuning, intent routing, TTS, forecasting models
 Phase 4 — Channels: voice gateway, USSD, SMS, NFC/HCE offline
 Phase 5 — Hardening: security review, failure-mode testing, demo rehearsal, fallback recording

RISK-FIRST SEQUENCING: The highest-uncertainty component is validated first. No published study evaluates an AI voice agent over a GSM/2G call; AMR-NB operates at 4.75–12.2 kbps against G.711's 64 kbps, and narrowband compression removes exactly the spectral cues that distinguish similar phonemes. This is prototype-tested within the first 72 hours. If it fails, the product stands on USSD, SMS, PWA and offline surfaces — but the team must know early, not late.

QUALITY ENGINEERING
 - Unit tests on all financial logic; property-based tests on ledger invariants
 - Integration tests against the MoMo sandbox with recorded fixtures for offline runs
 - End-to-end tests via Playwright on the PWA
 - Adversarial testing: duress flow, replay attacks, double-spend attempts on offline tokens, ASR misrecognition of amounts
 - Load testing on the voice gateway for concurrent session handling
 - Model evaluation: WER per language, stratified by cohort; forecasting evaluated on held-out time windows, never random splits

DEFINITION OF DONE: code reviewed, tests passing in CI, deployed to the demo environment, demonstrated working, and failure path verified.

DEMO-DAY RESILIENCE: a "simulate success" toggle for sandbox instability, a full recorded demo video as fallback, both webhook and polling paths implemented, and a tunnel (ngrok/Cloudflare) tested in advance for callbacks.

VERSION CONTROL AND PROVENANCE: honest commit history with meaningful messages and timestamps, and a README stating precisely what existed at registration (research and design documentation) versus what is built during the event (all application code).

=====================================================
9. SECURITY, PRIVACY AND COMPLIANCE
=====================================================

 - PINs hashed with Argon2id; never logged, never transmitted in plaintext
 - Data encrypted in transit (TLS 1.3) and at rest (AES-256-GCM)
 - Secrets in a managed vault; no credentials in source control; automated secret scanning in CI
 - Idempotency on every financial operation via X-Reference-Id
 - Webhook payloads signature-verified; replay windows enforced
 - Rate limiting and velocity checks per user, per device, per recipient
 - Least-privilege service accounts; production disbursement IP allow-listing documented for the go-live path
 - POPIA alignment: identity handled through the Identify API so identity documents are never collected or stored; voice audio processed transiently and not retained beyond the interaction unless the user explicitly opts in; explicit, purpose-limited, revocable consent captured through Get Consent for every mandate; data minimisation and defined retention periods; user-accessible audit trail of all agent actions
 - Mandates are PIN-signed, scoped, capped and revocable — auditable by construction
 - Full audit log of every proposal, approval, rejection and execution

=====================================================
10. ACCESSIBILITY AND INCLUSION
=====================================================

Inclusion is the architecture, not a feature.

 - LANGUAGE: South African languages first, English as one option among many. Approximately 29 million South Africans are not proficient in English.
 - LITERACY: voice requires no reading. 3.8 million South African adults over 20 are classified as illiterate.
 - DEVICE: full functionality on a feature phone via voice and USSD. 16% of South African connections are feature phones.
 - DATA: voice and USSD consume zero data. Where data is used, payloads are aggressively minimised because data cost is a real access barrier.
 - CONNECTIVITY: offline NFC value transfer for zero-signal conditions.
 - POWER: Eskom load shedding ended on 16 May 2025 (441 consecutive days clear as at 4 August 2026). However, LOAD REDUCTION continues — Eskom curtails specific overloaded township feeders in two daily windows, 05:00–09:00 and 17:00–22:00, unannounced and transformer-by-transformer. A voice call requires no charged smartphone and no home power; offline tokens survive an outage entirely.
 - VISUAL AND MOTOR: voice-first interaction, WCAG 2.2 AA targets on the PWA, high-contrast and large-text modes.
 - COST: the product actively reduces the user's costs — the data poverty premium and the electricity advance trap are both surfaced and countered.

=====================================================
11. INNOVATION — WHAT HAS NOT BEEN DONE BEFORE
=====================================================

 1. No African telecommunications operator or major bank has a verified production voice AI in an indigenous South African language. MTN's own flagship "AI for Mobile Money" is a text chatbot launched in Ivory Coast in May 2019.
 2. The duress PIN with decoy balance and silent alerting is not offered by any South African bank, despite express kidnapping rising 264% and specifically targeting banking app transfers.
 3. Get Consent has been published by MTN and remains essentially unused. Mapping it onto the AP2 mandate structure would make MoMo the first African wallet with an agent-mandate layer.
 4. Alternative-data prediction is universally deployed to price borrowers. Umoya inverts it to protect the person the data describes.
 5. Offline signed-token value transfer over Android HCE has no verified deployment in South Africa. Fewer than 13% of mobile money services worldwide offer NFC at all.
 6. Code-switched South African speech is untested by every frontier ASR benchmark published to date.
 7. Combining all five into one agent with a single identity across five channels is, to our knowledge, without precedent anywhere.

=====================================================
12. FEASIBILITY AND SCALABILITY
=====================================================

FEASIBILITY: Every component is either an API MTN already publishes, an openly licensed model or corpus, or a documented platform capability. Nothing depends on unreleased technology. Android HCE is a documented, stable API requiring no secure element. The Swivuriso corpus is CC BY 4.0 and downloadable today. The Federal Reserve's offline payment framework is published, and an open-source reference implementation exists. The MoMo Mini App programme is a PWA integration, so the client is a standard web application.

We are explicit about what is simulated: SIM-swap and network-location signals, and Interact channel provisioning. Both are presented as partnership asks with defined interface contracts, not as claimed capabilities.

SCALABILITY — TECHNICAL: Stateless services behind a load balancer; horizontally scalable ASR inference workers; queue-backed asynchronous processing; read replicas and time-partitioned transaction tables; CDN-delivered PWA assets; model serving decoupled from transaction serving so speech load cannot degrade payments.

SCALABILITY — GEOGRAPHIC: This is the decisive property. Expanding Umoya to another MTN market requires swapping the language model, not rebuilding the product. Nigeria (Hausa, Yoruba, Igbo), Uganda (Luganda, Acholi, Soga) and Ghana (Akan, Ewe, Dagbani) are all covered by Google's openly licensed WAXAL corpus, released under commercial-use terms in February 2026. MTN operates in 16 markets. The architecture is identical in every one.

SCALABILITY — ECONOMIC: Voice interaction costs are well understood, with published production benchmarks at approximately $0.07–0.21 per connected minute for cascaded pipelines, and interactions are short and transactional. USSD and SMS surfaces cost fractions of a cent. Cost per user falls as ASR inference is batched and quantised.

=====================================================
13. VALUE TO MTN
=====================================================

 - DORMANCY: Over 70% of African mobile money accounts are dormant. An agent that speaks the user's language, calls them before a shortfall, and works on the device they actually own creates recurring contact. MTN South Africa has explicitly deprioritised registration growth in favour of "quality, stickiness and profitability." Umoya is a stickiness product.
 - ADVANCED SERVICES REVENUE: MTN's advanced services grew 40.5% and now represent 34.1% of revenue excluding airtime, against 16% growth in basic services. A mini app is a unit of advanced service.
 - MINI APP SUPPLY: Safaricom's My OneApp hosts 221 mini apps. MTN's mini app programme is currently a documentation page, with the Ant International platform launching in Nigeria in Q3 2026. Umoya is supply for an empty shelf.
 - FRAUD: Fraud prevention is explicitly part of the Ant International partnership scope. Digital banking crime in South Africa reached R2.4 billion in 2025.
 - AI POSITIONING: MTN has committed publicly to AI without shipping a consumer AI product. Umoya is that product, and it is one no competitor can copy.
 - PLATFORM PRIMITIVE: The mandate layer, the duress primitive and the offline token rail can be exposed to every other mini app in the ecosystem. This is infrastructure, not an application.

=====================================================
14. RISKS AND MITIGATIONS
=====================================================

 RISK: AI voice agent viability over a 2G/GSM call is untested in published literature.
 MITIGATION: Prototype-tested in the first 72 hours. Cascaded pipeline chosen specifically because it outperforms speech-to-speech on narrowband telephony. Telephony-band augmentation during fine-tuning. Product remains viable on USSD, SMS, PWA and offline surfaces if voice underperforms.

 RISK: MTN may not expose SIM-swap or network-location signals.
 MITIGATION: Built against a simulated feed with an identical interface. Presented as a partnership proposal with a defined data contract.

 RISK: ASR misrecognises a monetary amount.
 MITIGATION: Mandatory read-back confirmation in the user's language; keypad confirmation of amounts below a confidence threshold; hard per-transaction caps.

 RISK: Voice cloning attack.
 MITIGATION: Voice is never an authentication factor. PIN plus behavioural, device and graph signals. Anti-spoofing layer. Documented openly.

 RISK: Offline double-spend.
 MITIGATION: This cannot be prevented in software; it can only be bounded and detected. We state this explicitly. R500 float ceiling, 24-hour validity, ~10-hop limit, ancestry-chain detection at settlement, and offline value convertible only while connected.

 RISK: Sandbox instability on demo day.
 MITIGATION: Simulate-success toggle, recorded demo video, both webhook and polling implemented, tunnel pre-tested.

 RISK: Scope. Five capabilities at 60% loses to two at 95%.
 MITIGATION: SPEAK and SURVIVE carry the demo. ACT, FORESEE and ENDURE are demonstrated in reduced form. A hard scope-review checkpoint is scheduled mid-build.

 RISK: Regulatory treatment of AI-initiated payments.
 MITIGATION: No autonomous spending. Every action is a proposal requiring explicit user approval, with a full audit trail.

=====================================================
15. SUCCESS METRICS
=====================================================

 PRODUCT: weekly active users; sessions per user per week; proportion of sessions on non-smartphone surfaces; mandates created and retained; balance retention (the inverse of "mailbox banking"); reduction in immediate full withdrawal.
 TECHNICAL: word error rate per language against the published Google Cloud isiXhosa baseline of 56.71%; end-to-end voice latency (target under 1,200ms, at which conversational rhythm breaks); transaction success rate; offline settlement reconciliation rate; false-alarm rate on duress and anomaly detection.
 IMPACT: users reachable who could not previously transact digitally; value protected in duress events; rand saved per user through data and electricity optimisation.
 BUSINESS: advanced-services revenue per user; cost per interaction by channel; agent cash-out volume displaced.

=====================================================
16. ROADMAP BEYOND THE HACKATHON
=====================================================

 0–3 months: Complete language coverage across all seven Swivuriso languages; formalise the network-signal data agreement with MTN; provision the Interact USSD channel; closed pilot in one metropolitan area.
 3–6 months: Public launch in South Africa within the MoMo super app; expose the mandate and duress primitives as platform services to other mini apps; independent security audit.
 6–12 months: Second market (Nigeria) using the WAXAL corpus; offline token rail at merchant scale; extend the forecasting layer to merchant cash-flow.
 12 months+: Full 16-market rollout; the language corpus and mandate layer become MTN Group infrastructure.

=====================================================
17. THE DEMONSTRATION
=====================================================

 1. A judge's smartphone is placed in a drawer.
 2. They are handed a R149 2G feature phone.
 3. They dial. They speak isiZulu. They check a balance, send money and set a mandate. It works.
 4. "You have just been hijacked. They have your phone and your PIN." The judge enters the duress PIN. A transfer completes convincingly on screen. Nothing moves. Behind them, the silent alert and network location appear on the operations display.
 5. All data and wifi are switched off. Two handsets are tapped together. The payment settles.

=====================================================

Umoya is not an app that uses MoMo. It is the intelligence layer MoMo has been missing, built out of the one asset MTN owns and nobody can copy: the network itself.
```

## --- Q11: Technologies ---

```
FRONTEND / MINI APP: React 18, TypeScript, Vite, Tailwind CSS, Progressive Web App (Service Worker, Workbox, Web App Manifest), IndexedDB for offline queueing, WCAG 2.2 AA. Built to the MTN MoMo Mini App PWA integration specification.

BACKEND: Python 3.12, FastAPI, Pydantic, Celery with Redis for asynchronous task processing, WebSockets/Server-Sent Events for real-time updates.

DATA: PostgreSQL 16 with TimescaleDB for time-series transaction and usage data, Redis for session state and access-token caching, S3-compatible object storage for audio artefacts.

SPEECH / ASR: OpenAI Whisper large-v3-turbo fine-tuned on the Swivuriso / South African Next Voices corpus (CC BY 4.0, 3,016 hours, 7 South African languages) using Hugging Face Transformers with PEFT/LoRA; Meta W2V-BERT 2.0 evaluated as a per-language comparator (published results favour W2V-BERT on Nguni languages and Whisper on Sotho-Tswana); CTranslate2 / faster-whisper for low-latency inference; torchaudio for telephony-band augmentation (8kHz downsampling and AMR-NB codec simulation); Silero VAD for voice activity detection; SpeechBrain for speaker embeddings.

TEXT-TO-SPEECH: Simba-TTS (UBC-NLP, CC-BY-4.0 — Afrikaans, Southern Sotho, Tswana, Xhosa), Meta MMS-TTS, with pre-recorded prompt concatenation as a guaranteed-intelligibility fallback for value-bearing confirmations.

NATURAL LANGUAGE UNDERSTANDING: constrained intent classification over a closed financial action set; a commercially-licensed small language model (Gemma 3 / Qwen 2.5 class, 0.5B–3B parameters, 4-bit quantised) for slot filling and disambiguation. Note: InkubaLM is CC BY-NC and therefore explicitly excluded from the production path.

MACHINE LEARNING: PyTorch, Hugging Face Transformers and Datasets, scikit-learn, LightGBM and XGBoost for forecasting and risk scoring, statsmodels for time-series, NetworkX and PyTorch Geometric for transaction-graph features, ONNX Runtime for optimised inference.

MLOPS: MLflow for experiment tracking and model registry, DVC for dataset versioning, Weights & Biases for training runs, stratified evaluation harness reporting WER and forecasting accuracy by language, province and urban/rural cohort.

TELEPHONY / CHANNELS: Africa's Talking Voice and USSD APIs for prototype channel delivery (SIP/PSTN termination, session management), with MTN Interact (Channel as a Service) as the production path; MTN Notify API for SMS.

OFFLINE PAYMENTS: Android (Kotlin) Host-based Card Emulation via HostApduService for device-to-device NFC with no network and no secure element; Ed25519 signatures via libsodium / Google Tink; token ancestry-chain validation and single-use key semantics following the US Federal Reserve "A Robust Risk Framework for Offline Payments" (December 2025); CBOR for compact token encoding within the ~1KB / ~300ms APDU budget.

MOMO APIS: Collections (Get Paid), Disbursements (Pay), Get Consent, Identify (KYC), Notify, Invoice, Manage, Interact (Channel as a Service), Collection Widget. OAuth bearer tokens on a 3600-second refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling outcome resolution.

AGENTIC STANDARDS: mandate structures aligned to Google's Agent Payments Protocol (AP2) Intent Mandate and Cart Mandate patterns, expressed as signed, scoped, revocable authorisations.

SECURITY: Argon2id password/PIN hashing, AES-256-GCM at rest, TLS 1.3 in transit, JWT with short-lived rotation, HMAC webhook signature verification, HashiCorp Vault or cloud KMS for secrets, OWASP ASVS as the control baseline, automated secret scanning and dependency auditing in CI.

INFRASTRUCTURE / DEVOPS: Docker and Docker Compose, GitHub Actions for CI/CD, Cloudflare Pages or Vercel for PWA delivery, containerised backend on Azure Container Apps or equivalent, Cloudflare Tunnel / ngrok for MoMo callback delivery during development, Terraform for infrastructure as code.

OBSERVABILITY: OpenTelemetry distributed tracing, Prometheus and Grafana metrics, Sentry error tracking, structured JSON audit logging.

TESTING / QA: pytest with Hypothesis for property-based testing of ledger invariants, Vitest for frontend units, Playwright for end-to-end PWA flows, Locust for voice-gateway load testing, adversarial test suites for duress flow, token replay and double-spend attempts.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, aggressive payload minimisation given South African data costs.
```

---
---

# ENTRY 2 · AMAZWI — *Teammate 2*

## --- Q8: Track ---

```
Track 2: Entertainment and Lifestyle
```

## --- Q9: Short summary (221 characters) ---

```
Amazwi is a game where speaking your language pays. Daily voice challenges in every South African language, instant MoMo payouts, cents at a time. It builds the African speech data the world skipped, and our youth own it.
```

## --- Q10: Detailed description ---

```
AMAZWI — "the voices"
The game where being South African pays.

=====================================================
1. PROBLEM STATEMENT
=====================================================

Two problems that have never been connected to each other.

THE FIRST: South Africa's young people have no income and no assets.
Official unemployment reached 32.7% in Q1 2026, with 8.1 million people unemployed. Youth unemployment (15–34) is 45.8% — 4.7 million young South Africans. Among those who do work, 33.5% of all employment is informal, rising to 50.5% of employed 15–24-year-olds. One in three working South Africans has no payslip, and half of employed young people have no formal contract at all.

THE SECOND: South Africa's languages are the most valuable untapped data asset on the continent, and they are being skipped.
Google Cloud Speech-to-Text has a 56.71% word error rate on isiXhosa in realistic conversational speech, against a 9.6% human baseline. Meta MMS scores 92.50%. Foundation ASR models score above 100% word error rate zero-shot on all six Southern Bantu languages — literally worse than producing no output.

This is not a model problem. It is a data problem, and the data gap is widening:
 - In February 2026 Google released WAXAL: 11,000+ hours across 27 Sub-Saharan African languages, openly licensed for commercial use. It contains ZERO South African official languages. The investment went to East and West Africa.
 - The only substantial South African corpus, Swivuriso (3,016 hours, 7 languages), excludes Afrikaans, Sepedi and siSwati entirely.
 - Code-switched South African speech — "ngicela i-data", which is how the country actually talks — barely exists as data. Code-switching degrades monolingual ASR by 30–50% word error rate, and a June 2026 benchmark of seven frontier ASR systems on code-switched speech tested Spanish, French and German pairs and zero African languages.

Meanwhile MTN Group has committed publicly to artificial intelligence — a Huawei memorandum of understanding including a Technology Innovation Lab in South Africa, AI data centres prioritised for South Africa and Nigeria — while shipping no consumer AI product and holding no proprietary African-language data asset. And MTN removed Ayoba from the app stores on 20 March 2026, leaving the group with no youth engagement product after it peaked at 35 million monthly active users and failed on retention.

The connection nobody has made: the demographic with no income owns the scarcest asset in African AI, and the operator that needs that asset has no way to buy it.

=====================================================
2. THE SOLUTION
=====================================================

Amazwi is a mobile game in which young South Africans are paid, in MoMo, cents at a time, for speaking their own language.

It is built as a game, not as a work platform, because that is what it is.

 - DAILY VOICE CHALLENGES. Read this sentence aloud. Describe this photograph. Say this the way you would say it to your friend, not the way you would write it. Argue with this statement for thirty seconds. Tell us what this word means in your area.
 - CODE-SWITCH CHALLENGES. Deliberately elicit the mixed-language speech that no dataset on earth contains and that every ASR system fails on.
 - PEER VALIDATION. Other speakers of the same language rate and correct submissions. Both the contributor and the validator earn. This is how quality is achieved without a laboratory.
 - STREAKS, LEVELS AND LEADERBOARDS. By language, and by place. Khayelitsha against Soweto. Thohoyandou against Giyani. Language as sport.
 - INSTANT PAYOUT TO MOMO. Cents per validated task, settled immediately. This is precisely what mobile money exists for and precisely what card rails cannot do economically.
 - SCARCITY PRICING. The rarer your language, the more you earn. Tshivenda (2.5% of home-language speakers) and isiNdebele (1.7%) pay the most. The smallest and most historically ignored language communities become the highest earners on the platform. This is economically correct — scarce data is worth more — and it is the moral core of the product.
 - CULTURAL OWNERSHIP. Contributors are credited as stakeholders in the resulting corpus, with published rates and revocable consent.

The output is a continuously growing, individually consented, ethically sourced South African speech corpus, plus the models trained on it.

=====================================================
3. WHY WE CHOSE THIS
=====================================================

Because it is a three-sided fit that does not come along often.

For young South Africans, it converts an asset they already own — fluency in a language global AI cannot handle — into income, on a device they already have, with no qualification, no interview and no CV.

For MTN, it is simultaneously the payer and the buyer. MTN funds the contributions and MTN needs the resulting data. It is the easiest internal business case imaginable, and it directly serves a publicly stated group AI strategy that currently has no consumer expression. It also replaces the youth engagement product MTN lost when Ayoba closed.

For the country, it addresses a genuine injustice. South African languages are being harvested for free by systems trained on scraped web text, and South Africans receive nothing. Amazwi makes the value flow the other way, with consent.

And it belongs in Entertainment and Lifestyle because it is a social game. The mechanics are streaks, rivalry, community pride and a leaderboard. Nobody opens it because it is worthy. They open it because their township is losing.

=====================================================
4. HOW IT WORKS — USER JOURNEY
=====================================================

ONBOARDING: The user opens Amazwi in the MoMo super app, or dials in from a feature phone. Identity is verified through the MoMo Identify (KYC) API, establishing that the contributor is a real, unique human without Amazwi collecting or storing any identity document. The user selects their home language and dialect region, and completes a short calibration recording.

CONSENT: Before any contribution, the user is presented with plain-language terms in their own language — what the recordings are used for, who may use them, how to withdraw. Consent is captured through the MoMo Get Consent API, PIN-authenticated, scoped and revocable at any time.

PLAYING: The user receives a set of daily challenges. Each takes seconds. Audio quality is validated on the device before upload, so nothing is wasted and no data is spent on a recording that will be rejected. Completed challenges enter a validation pool.

VALIDATING: The user is served other people's submissions in their language to rate and correct. Agreement with the consensus earns; systematic disagreement reduces the user's validation weight.

EARNING: Validated contributions pay out instantly to the user's MoMo wallet through the Disbursements API. The payout rate is displayed before the task, never after.

COMPETING: A live leaderboard ranks contributors by language and by area. Weekly community challenges pit regions against each other. Streaks unlock higher-value task types.

FEATURE PHONE PATH: A user with no smartphone dials the Amazwi number and completes voice challenges over a plain call, with no app and no data. This reaches rural, older and — linguistically — the most valuable speakers, who every other data collection effort systematically misses.

=====================================================
5. SYSTEM ARCHITECTURE
=====================================================

LAYER 1 — CLIENT
 - PWA with Web Audio API and MediaRecorder capture, Opus encoding
 - On-device quality gate running in the browser: signal-to-noise estimation, clipping detection, voice activity detection, duration and silence checks. Rejection happens BEFORE upload, so the user never spends data on a recording that will fail.
 - Offline capture queue in IndexedDB; contributions recorded without signal upload when connectivity returns
 - Voice-call client path via telephony gateway for feature phones

LAYER 2 — TASK ORCHESTRATION
 - Challenge generator and scheduler
 - Active-learning acquisition service: selects which prompts to serve based on model uncertainty, not at random
 - Per-user task assignment with anti-collusion routing (contributors never validate their own linguistic cluster's submissions exclusively)

LAYER 3 — QUALITY AND INTEGRITY
 - Peer validation pipeline with inter-annotator agreement scoring (Krippendorff's alpha, Fleiss' kappa)
 - Audio fingerprinting for duplicate and replay detection
 - Speaker embedding comparison for UNIQUENESS enforcement (one human, one account) — explicitly not used as an authentication factor
 - Device and SIM fingerprinting; velocity and behavioural anomaly detection
 - Payout gating: thresholds, holdbacks and statistical outlier review before settlement

LAYER 4 — DATA AND ML
 - Versioned corpus store with full provenance and consent lineage per clip
 - Fine-tuning pipeline: continuous retraining as new validated data arrives
 - Evaluation harness producing word error rate per language, stratified by dialect region, age band and gender
 - Model registry and rollback

LAYER 5 — GAME AND ECONOMY
 - Leaderboard service (Redis sorted sets) by language, region and time window
 - Streak, level and achievement engine
 - Dynamic pricing engine implementing scarcity-based rates by language and task type
 - Payout ledger with full audit trail

LAYER 6 — INTEGRATION
 - MoMo API client (Identify, Get Consent, Disbursements, Notify)
 - Batch disbursement with idempotency and reconciliation
 - Telephony gateway integration

DATA FLOW: challenge served → recorded on device → quality gate passes → uploaded with consent reference → enters validation pool → validated by N peers → agreement scored → integrity checks pass → contribution accepted into corpus with provenance → payout queued → MoMo disbursement executed → leaderboard updated → SMS confirmation dispatched.

=====================================================
6. AI / ML ARCHITECTURE
=====================================================

ACTIVE LEARNING — the core technical idea
Amazwi does not collect data randomly. An acquisition function ranks candidate prompts by expected model improvement, using uncertainty sampling (predictive entropy) and diversity-based selection over the embedding space. The system asks for what the model is least certain about. This is the difference between a survey and an acquisition engine, and it means the hundredth hour of data is worth more than the first.

CONTINUOUS FINE-TUNING
Whisper large-v3-turbo and W2V-BERT 2.0 fine-tuned with PEFT/LoRA on the accumulating corpus, seeded from the openly licensed Swivuriso corpus. Published baselines show fine-tuning moves Setswana from 223% to 13% word error rate and Xitsonga from 190% to 12% — so the improvement curve is real, measurable, and demonstrable live.

QUALITY MODELLING
Inter-annotator agreement statistics; a learned contributor-reliability score updated Bayesian-style from validation history; automatic escalation of low-agreement items to expert review.

INTEGRITY AND ANTI-FRAUD
This will be attacked. Assuming otherwise would be negligent. Defences: audio fingerprinting (chromaprint-style) against duplicate and re-uploaded content; speaker embedding clustering to detect one person operating many accounts; device and network fingerprinting; submission-velocity anomaly detection via isolation forests and gradient-boosted classifiers; payout thresholds and holdback windows; statistical review of outlier earners.

EVALUATION
Word error rate per language against published baselines, including the Google Cloud isiXhosa figure of 56.71%. Stratified evaluation across dialect region, age band and gender, published rather than buried — because a corpus that only represents urban young men reproduces exactly the bias documented in African mobile money AI, where models trained on high-activity users systematically undervalue rural patterns.

=====================================================
7. MOMO API INTEGRATION
=====================================================

  Identify (KYC)   — proves each contributor is a real, unique human without Amazwi storing any identity data. This solves the single hardest problem in crowdsourced data collection.
  Get Consent      — PIN-signed, scoped, revocable consent per contribution. This is what makes the resulting corpus ethically and legally defensible.
  Pay (Disbursements) — instant cent-scale payouts, batched with idempotency and reconciliation
  Notify           — SMS confirmation of earnings for users with no data
  Get Paid         — reserved for future enterprise licensing of corpus access
  Interact (CaaS)  — feature-phone entry point through the MoMo menu

=====================================================
8. SDLC AND DELIVERY METHODOLOGY
=====================================================

Trunk-based development, continuous integration on every push, daily working-software demos.

 Phase 0 — Discovery and architecture (completed before the event: research, corpus and licence review, architectural design. No application code.)
 Phase 1 — Foundation: repository, CI, MoMo sandbox connectivity, first successful disbursement end to end
 Phase 2 — Capture loop: recording client, on-device quality gate, upload pipeline, storage with provenance
 Phase 3 — Validation and integrity: peer review pipeline, agreement scoring, anti-fraud layer
 Phase 4 — Game and economy: leaderboards, streaks, scarcity pricing, payout ledger
 Phase 5 — ML: fine-tuning pipeline, active-learning acquisition, evaluation harness
 Phase 6 — Hardening: adversarial testing, security review, demo rehearsal, fallback recording

RISK-FIRST SEQUENCING: The highest-risk element is not technical, it is human — will real people contribute, and will they cheat? Both are tested first: a small cohort of genuine contributors is recruited early, and the team actively attempts to defraud its own platform before demo day.

QUALITY ENGINEERING: unit and integration tests across the capture and payout paths; property-based tests on the payout ledger; adversarial suites simulating duplicate submission, account farming and collusion; load testing on batch disbursement; model evaluation on held-out speakers, never held-out clips from the same speaker.

VERSION CONTROL AND PROVENANCE: honest commit history; README stating exactly what existed at registration (research and design) versus what is built during the event (all code).

=====================================================
9. SECURITY, PRIVACY, ETHICS AND COMPLIANCE
=====================================================

This product collects biometric data — voice — from a vulnerable population. The ethics are the architecture.

 - CONSENT: explicit, informed, in the contributor's own language, PIN-authenticated through Get Consent, scoped to defined uses, and revocable at any time. Revocation removes the contributor's data from future training runs and from redistributed corpus versions.
 - PROVENANCE: every clip carries its consent reference, contributor pseudonym, timestamp and licence terms. The corpus is auditable end to end.
 - MINIMISATION: no identity documents stored — Identify returns verification, not data. Contributors are pseudonymous in the corpus.
 - POPIA ALIGNMENT: lawful basis established through explicit consent; purpose limitation enforced technically; data subject access and deletion supported; voice treated as special-category personal information with correspondingly stricter controls.
 - TRANSPARENCY: payout rates published before the task, never adjusted retroactively.
 - NO VOICE AUTHENTICATION: speaker embeddings are used for uniqueness enforcement only. They are never used as an authentication factor, because published research shows open-source voice cloning bypasses speaker verification 82.7% of the time using 10–30 minutes of scraped audio.
 - TECHNICAL: TLS 1.3 in transit, AES-256-GCM at rest, Argon2id for credentials, signed upload URLs, rate limiting, OWASP ASVS baseline, secret scanning in CI.

ADDRESSING THE HARD QUESTION DIRECTLY: "Is this a digital sweatshop?" We raise it before anyone else does. Mitigations are structural, not cosmetic: published transparent rates; scarcity pricing that favours the most marginalised language communities; revocable consent; contributors credited as corpus stakeholders; and rates benchmarked openly against comparable data-work markets. A product that extracts from vulnerable people while calling itself inclusion is worse than no product.

=====================================================
10. ACCESSIBILITY AND INCLUSION
=====================================================

 - LANGUAGE: all 12 official languages are in scope, and the product is worth the most to the languages with the fewest speakers.
 - LITERACY: challenges can be delivered and answered entirely by voice. 3.8 million South African adults over 20 are classified as illiterate; they are not excluded — in this product they are among the most valuable participants.
 - DEVICE: feature-phone participation by voice call. 16% of South African mobile connections are feature phones.
 - DATA: on-device quality gating prevents wasted uploads; audio is Opus-compressed; MTN can zero-rate its own data-collection traffic at negligible marginal cost. This matters because the poorest South Africans pay R62.25 per gigabyte against R17.80 for those who can afford a large bundle.
 - GEOGRAPHY: dialect-region tagging deliberately values rural and non-metropolitan speech, correcting the documented urban bias in African language datasets.
 - INCOME: the product is itself an income intervention for a cohort with 45.8% unemployment.

=====================================================
11. INNOVATION — WHAT HAS NOT BEEN DONE BEFORE
=====================================================

 1. No consumer-scale data-work-for-mobile-money product exists in Africa. The economics only work where cent-scale payouts to tens of millions of wallets are possible, which requires mobile money, which requires MTN.
 2. No individually consented, revocable, ethically sourced African language corpus exists anywhere. Every major African speech dataset is institutionally collected. Amazwi's provenance model is the innovation as much as the data.
 3. Active learning has never been applied to African language data collection at consumer scale. Existing efforts collect broadly; Amazwi collects what the model actually needs.
 4. Scarcity pricing that pays the smallest language communities the most inverts every existing incentive in data collection.
 5. Code-switched South African speech is untested by every frontier ASR benchmark published to date, and no product deliberately elicits it.
 6. Using KYC infrastructure to solve unique-human verification in crowdsourced data is, to our knowledge, novel.

=====================================================
12. FEASIBILITY AND SCALABILITY
=====================================================

FEASIBILITY: Every component is standard, documented technology. Audio capture is a browser API. The quality gate runs in the browser. Fine-tuning uses published open-source models and an openly licensed seed corpus. The payout rail is an API MTN already publishes. There is no unreleased technology on the critical path.

The genuine risks are human, not technical, and are addressed above: contribution volume and fraud.

SCALABILITY — TECHNICAL: Stateless capture and validation services; object storage scales linearly; training is offline and batched, decoupled from the live product; leaderboards on Redis sorted sets handle millions of entries; payouts batch efficiently.

SCALABILITY — GEOGRAPHIC: This is the decisive property. Every MTN market has underserved languages — Nigeria alone has over 500. The architecture is identical everywhere; only the challenge set and the language list change. Amazwi becomes MTN Group's language data infrastructure across 16 markets, feeding every AI product the group builds.

SCALABILITY — ECONOMIC: Marginal cost per contribution is the payout plus storage plus a fraction of a cent in compute. Value per contribution rises as active learning targets acquisition. The corpus is an appreciating asset.

=====================================================
13. VALUE TO MTN
=====================================================

 - AI STRATEGY MADE REAL: MTN has committed publicly to AI with no consumer product. Amazwi produces a proprietary, ethically sourced, competitively unavailable African language data asset — the input to every AI product MTN could build.
 - YOUTH ENGAGEMENT: MTN lost its youth product when Ayoba closed in March 2026. Amazwi is youth-native by construction and has a daily reason to open.
 - DORMANCY: Over 70% of African mobile money accounts are dormant. An account that receives money daily is not dormant. Amazwi creates inbound wallet flow for the exact cohort most likely to be inactive.
 - MERCHANT AND WALLET ACTIVATION: contributors receive value into MoMo and spend it there.
 - ENTERPRISE REVENUE: licensed corpus and model access is a genuine B2B line, and one MTN would own outright.
 - STRATEGIC POSITIONING: it directly answers Google's decision to fund 27 African languages and skip South Africa entirely.

=====================================================
14. RISKS AND MITIGATIONS
=====================================================

 RISK: Track fit — a judge may see a work product rather than entertainment.
 MITIGATION: It is built and presented as a social game: rivalry, streaks, community pride, leaderboards. The earning is the reward mechanic, not the framing.

 RISK: Fraud and account farming.
 MITIGATION: Audio fingerprinting, speaker clustering for uniqueness, device and SIM checks, velocity anomaly detection, payout thresholds and holdbacks, statistical outlier review. Adversarial testing conducted by the team against its own platform before launch.

 RISK: Data quality.
 MITIGATION: On-device gating, peer validation with agreement scoring, contributor reliability weighting, expert escalation for contested items.

 RISK: Exploitation criticism.
 MITIGATION: Addressed openly and structurally — published rates, revocable consent, scarcity pricing favouring marginalised communities, contributor stakeholder status.

 RISK: Cold start — insufficient contributors for a meaningful demonstration.
 MITIGATION: Seed cohort recruited early through team networks; academic partnership sought (the DSFSI group at the University of Pretoria built the Swivuriso corpus and is the natural collaborator).

 RISK: Data cost deters contribution.
 MITIGATION: On-device rejection before upload, Opus compression, feature-phone voice path with zero data, and the option for MTN to zero-rate.

=====================================================
15. SUCCESS METRICS
=====================================================

 PRODUCT: daily and weekly active contributors; contributions per contributor per week; retention at day 7 and day 30; validation participation rate; leaderboard engagement.
 DATA: validated hours per language; dialect-region and demographic coverage; inter-annotator agreement; proportion of corpus that is code-switched.
 MODEL: word error rate per language over time, benchmarked against the published Google Cloud isiXhosa baseline of 56.71%; improvement per hundred hours acquired, comparing active-learning acquisition against random sampling.
 IMPACT: total rand paid to contributors; median monthly earnings; share of earnings flowing to the smallest language communities; share of contributors previously unemployed.
 INTEGRITY: fraud detection rate; payout reversal rate; false-positive rate on integrity checks.

=====================================================
16. ROADMAP BEYOND THE HACKATHON
=====================================================

 0–3 months: Expand to all 12 official languages including Afrikaans, Sepedi and siSwati, which the existing corpus omits. Formalise the academic partnership. Publish the first corpus release with full provenance.
 3–6 months: Text and translation task types alongside speech. Enterprise licensing pilot. Independent ethics and security review.
 6–12 months: Expansion into a second MTN market. The corpus begins powering MTN consumer products — including, directly, the voice layer of a South African language money agent.
 12 months+: MTN Group language data infrastructure across 16 markets.

=====================================================
17. THE DEMONSTRATION
=====================================================

 1. A judge speaks a sentence in their own language into a phone.
 2. Their contribution is validated live and appears on a national leaderboard. Their region's score moves.
 3. Cents settle into a MoMo wallet on screen, in real time.
 4. The closing slide: the model's isiXhosa word error rate falling live as contributions arrive, starting from Google's published 56.71%.

=====================================================

South Africa's culture is being harvested for free. Amazwi is the app where it pays you back.
```

## --- Q11: Technologies ---

```
FRONTEND: React 18, TypeScript, Vite, Tailwind CSS, Progressive Web App (Service Worker, Workbox), IndexedDB offline capture queue, built to the MTN MoMo Mini App PWA integration specification.

AUDIO CAPTURE AND ON-DEVICE PROCESSING: Web Audio API, MediaRecorder, Opus/WebM encoding, AudioWorklet for real-time analysis, Silero VAD compiled to ONNX and executed via ONNX Runtime Web for in-browser voice activity detection, in-browser signal-to-noise estimation and clipping detection so recordings are rejected before they cost the user any data.

BACKEND: Python 3.12, FastAPI, Pydantic, Celery with Redis for asynchronous validation and payout pipelines, WebSockets for live leaderboard updates.

DATA: PostgreSQL 16 for metadata, consent lineage and payout ledger; Redis sorted sets for leaderboards and streaks; S3-compatible object storage (Azure Blob / MinIO) for audio; Apache Parquet for corpus export.

MACHINE LEARNING: PyTorch, Hugging Face Transformers, Datasets and PEFT/LoRA; OpenAI Whisper large-v3-turbo and Meta W2V-BERT 2.0 fine-tuned on the accumulating corpus, seeded from the Swivuriso / South African Next Voices dataset (CC BY 4.0, 3,016 hours, 7 South African languages); jiwer for word error rate computation; scikit-learn and LightGBM for integrity and reliability modelling; isolation forests for submission anomaly detection.

ACTIVE LEARNING: uncertainty sampling by predictive entropy, diversity-based selection over speech embeddings, modAL-style acquisition orchestration, with A/B comparison against random sampling to prove the acquisition function earns its complexity.

SPEAKER AND AUDIO INTEGRITY: SpeechBrain and pyannote.audio ECAPA-TDNN speaker embeddings used strictly for uniqueness enforcement (one human, one account) and never as an authentication factor; chromaprint-style audio fingerprinting for duplicate and replay detection; librosa and torchaudio for feature extraction.

ANNOTATION QUALITY: Krippendorff's alpha and Fleiss' kappa for inter-annotator agreement; Bayesian contributor-reliability scoring; consensus routing with anti-collusion assignment.

MLOPS AND DATA GOVERNANCE: DVC for dataset versioning with consent lineage, MLflow for experiment tracking and model registry, Hugging Face Datasets for corpus packaging and release, Weights & Biases for training runs, stratified evaluation harness reporting word error rate by language, dialect region, age band and gender.

TELEPHONY: Africa's Talking Voice API for the feature-phone contribution path (SIP/PSTN, IVR challenge delivery and recording), with MTN Interact (Channel as a Service) as the production entry point; MTN Notify for SMS earnings confirmations.

MOMO APIS: Identify (KYC) for unique-human verification without storing identity, Get Consent for PIN-signed revocable contribution consent, Pay (Disbursements) for batched cent-scale instant payouts with idempotency and reconciliation, Notify for SMS, Interact for feature-phone reach. OAuth bearer tokens on a 3600-second refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling outcome resolution.

SECURITY: TLS 1.3, AES-256-GCM at rest, Argon2id credential hashing, signed pre-authenticated upload URLs, per-user and per-device rate limiting, HMAC webhook verification, HashiCorp Vault or cloud KMS, OWASP ASVS baseline, automated secret scanning and dependency auditing in CI.

INFRASTRUCTURE / DEVOPS: Docker and Docker Compose, GitHub Actions CI/CD, Cloudflare Pages or Vercel for the PWA, containerised backend on Azure Container Apps or equivalent, Terraform for infrastructure as code, Cloudflare Tunnel for MoMo callbacks in development.

OBSERVABILITY: OpenTelemetry, Prometheus and Grafana, Sentry, structured JSON audit logging with full consent and payout traceability.

TESTING / QA: pytest with Hypothesis for property-based testing of the payout ledger, Vitest, Playwright for end-to-end capture flows, Locust for batch disbursement load testing, and a dedicated adversarial suite simulating duplicate submission, account farming, collusion rings and replay attacks.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, game UI patterns (progress, streaks, tiers), aggressive payload minimisation given South African data costs.
```

---
---

# ENTRY 3 · HAMBA — *Teammate 3*

## --- Q8: Track ---

```
Track 3: Travel and Mobility
```

## --- Q9: Short summary (224 characters) ---

```
Hamba turns a taxi fare into a safety contract. Pay by USSD, funds sit in escrow, and MTN's network watches the journey by cell tower. No app, no GPS, no data. Arrive, the driver is paid. Deviate, and your people are called.
```

## --- Q10: Detailed description ---

```
HAMBA — "go", from "hamba kahle", go well
The journey someone is watching.

=====================================================
1. PROBLEM STATEMENT
=====================================================

South African transport has two problems, and every previous attempt has tried to solve only one of them.

THE PAYMENT PROBLEM
15 million South Africans commute by minibus taxi every day, and all of them pay cash. Over 80% of South African ride-hailing trips are paid in cash — a figure published by Bolt itself — against more than 85% cashless in Nigeria. At least 14 prior cashless taxi initiatives have failed in South Africa. Documented causes include political tension inside taxi associations, systems that ignored operational reality (one failed specifically because it could not pay for fuel), and no education across drivers, owners and passengers. Current tap-and-go terminal approaches cost roughly R2,000 per taxi per month.

THE SAFETY PROBLEM
Kidnapping in South Africa has risen 264% since 2014/15, reaching 17,061 incidents and running at approximately 53 per day. Of 2023/24 kidnappings, 44% were linked to hijackings and 22% to robberies; only 4% involved a ransom demand. Nearly 80% of Gauteng kidnappings are tied to armed robbery. These are acquisitive crimes, and transport is where they happen. SABRIC documents the pattern of perpetrators detaining victims "just long enough to coerce them into draining their accounts," including a case of an e-hailing driver robbed at gunpoint for a forced R6,000 transfer.

THE CONNECTION NOBODY HAS MADE
These are the same problem. The reason the driver insists on cash is the reason the driver gets robbed. The reason the passenger carries cash is the reason the passenger is a target. Every one of the 14 failed attempts tried to remove the cash without giving anyone a reason to want it removed, and required the taxi industry's permission to do so.

THE COMPOUND COST
South Africa's gig economy comprises 1.8 to 2 million participants and is valued at approximately $5.03 billion, with ride-hailing representing 29% of it. Almost none of these workers can prove what they earn, which is the wall between them and credit, housing, or a bank account. Meanwhile 33.5% of all South African employment is informal, rising to 50.5% among employed 15–24-year-olds.

AND THE PHONE CANNOT BE ASSUMED
16% of South African mobile connections are feature phones; MTN South Africa itself sold 29% 2G devices in 2023/24, and has stated it will retain a 2G layer with no committed sunset date. Any solution that requires a smartphone app with GPS and a live data connection excludes the majority of the people who need it most.

=====================================================
2. THE SOLUTION
=====================================================

Hamba turns a journey into a payment contract that the network itself supervises.

  1. START THE JOURNEY. The passenger initiates by USSD, by voice, or by scanning a code at the rank. Origin and destination are declared. No application is required on either handset.
  2. FUNDS ENTER ESCROW. The fare is committed but not released. The driver sees confirmed funds. This is the trust unlock — and it is the moment the cash leaves the vehicle.
  3. THE NETWORK WATCHES. The journey is monitored through cell-tower handover sequences. No GPS. No application. No data consumption. No battery drain. Expected route corridor and duration are learned from aggregate journeys on the same route.
  4. ARRIVAL RELEASES PAYMENT. Reaching the declared destination within the learned envelope releases escrow automatically. No confirmation ritual, no dispute.
  5. DEVIATION ESCALATES. A sustained departure from the corridor, a stop where journeys do not stop, or a duration far outside the learned envelope triggers a tiered escalation: a silent check-in request first, then nominated contacts, then a response partner.

WHAT EACH SIDE GETS
 - The driver: no cash in the vehicle, guaranteed payment on arrival, and a verifiable income record built automatically from settled journeys — the exact artefact two million gig workers cannot obtain.
 - The passenger: a journey somebody is watching, and no cash on their person.
 - MTN: cash-to-digital conversion at the single highest-frequency transaction point in the South African informal economy, and a live view of the country's informal transport network.

WHY THIS SUCCEEDS WHERE 14 ATTEMPTS FAILED
Every previous system tried to REPLACE the fare, and therefore needed the taxi industry's permission, a terminal in every vehicle, and simultaneous behaviour change from three parties. Hamba replaces nothing. It ADDS safety and guaranteed payment to a journey that happens anyway, and it works driver-to-passenger with no association agreement, no terminal and no platform. The driver's incentive — no cash in the car, in a country where drivers are killed for cash — is immediate, selfish, and requires no trust in the passenger whatsoever.

=====================================================
3. WHY WE CHOSE THIS
=====================================================

Because it is the single most defensible idea available on this platform.

Cell-tower handover data belongs to the mobile network operator and to nobody else. Uber does not have it. Bolt does not have it. Shop2Shop, Capitec, TymeBank, Yoco and every fintech in South Africa do not have it. A journey-supervision product that requires no application, no GPS and no data is not merely difficult for a competitor to build — it is structurally impossible without owning the radio network. MTN is the only organisation in South Africa that can ship this.

Because the problem is enormous, verified and unsolved. 15 million daily cash commuters. Over 80% of ride-hailing paid in cash, published by an operator. Kidnapping up 264%. These are not estimates.

Because it is the correct strategic entry point. As long as commuters must hold cash for transport, they withdraw cash; and once they hold cash, they spend it at the spaza. The taxi is the pump that keeps cash circulating in the township economy. Every digital payment product in South Africa is fighting the taxi, directly or indirectly.

And because MTN needs Track 3 supply. No MoMo hackathon winner has ever come from mobility, and MTN's Ant International partnership explicitly targets commerce and lifestyle services beyond basic transfers.

=====================================================
4. HOW IT WORKS — USER JOURNEY
=====================================================

DRIVER ONBOARDING: The driver registers through the MoMo Identify (KYC) API — no documents collected or stored by Hamba. They nominate their MoMo wallet for settlement and are issued a static QR and a driver short code.

PASSENGER ONBOARDING: The passenger registers nominated emergency contacts and grants journey-scoped monitoring consent through the Get Consent API, PIN-authenticated and revocable at any time.

STARTING A TRIP (FEATURE PHONE): The passenger dials the Hamba USSD code, selects or enters a destination, confirms the fare, and enters their MoMo PIN. Funds move to escrow. The driver receives an SMS confirming committed funds. Monitoring begins.

STARTING A TRIP (SMARTPHONE): The same flow inside the mini app, with an optional GPS layer for higher precision and a live trip view for nominated contacts.

DURING THE TRIP: Cell-tower handovers are evaluated against the learned corridor model for that origin-destination pair. Nothing is displayed to the driver. The passenger sees a simple "trip active" state. Battery and data consumption are effectively zero.

NORMAL ARRIVAL: The handover sequence resolves to the destination cell cluster within the expected envelope. Escrow releases to the driver's wallet. Both parties receive SMS confirmation. The journey is appended to the driver's income record.

ANOMALY: A sustained corridor departure or duration overrun triggers a silent check-in — a USSD push or app prompt requiring a simple acknowledgement. No response, or an explicit distress response, escalates to nominated contacts with the last known cell location, then to a response partner. Escrow is held pending resolution.

DISPUTE: Because the corridor and duration record exists independently of both parties, disputes resolve against network evidence rather than against one person's word.

=====================================================
5. SYSTEM ARCHITECTURE
=====================================================

LAYER 1 — CHANNEL
 - USSD gateway with server-side session state machine, 182-character response budget, menus capped at five levels (GSM 02.90 places no session state in the handset, so all state is held in the gateway)
 - Voice IVR path for low-literacy users
 - PWA for smartphone users with optional GPS augmentation
 - SMS via Notify for all confirmations and alerts
 - QR presentment for rank-side trip initiation

LAYER 2 — JOURNEY ORCHESTRATION
 - Trip lifecycle state machine: INITIATED → FUNDED → ACTIVE → ARRIVED → SETTLED, with ANOMALY and DISPUTED branches
 - Escrow service with time-bounded holds and defined release, refund and split conditions
 - Idempotent transitions with full event sourcing, so every state change is auditable

LAYER 3 — NETWORK TELEMETRY
 - Handover ingestion pipeline consuming cell-transition events
 - Spatial indexing of cells using H3 hexagonal binning
 - Corridor model store: learned cell-sequence signatures per origin-destination pair
 - Missing-observation handling: coverage gaps are treated as missing data, never as anomalies

LAYER 4 — INTELLIGENCE
 - Corridor learning: sequence models over aggregate historical handover traces
 - Duration distribution modelling per route, per time-of-day band, per day-of-week
 - Anomaly detection: sequence deviation scoring plus duration outlier detection, with per-corridor adaptive thresholds
 - Risk scoring by route, corridor, time of day and historical incident density
 - Transit network inference: continuous aggregation of settled journeys into a live view of the informal network

LAYER 5 — ESCALATION
 - Tiered escalation engine: silent check-in → nominated contacts → response partner
 - Configurable per-user thresholds and quiet-hours logic
 - Full escalation audit log

LAYER 6 — INTEGRATION
 - MoMo API client (Get Paid, Pay, Get Consent, Identify, Notify, Interact)
 - Dual webhook and polling outcome resolution
 - Operations dashboard over WebSockets for live monitoring during demonstration and pilot

DATA FLOW: trip initiated by USSD → fare quoted → PIN captured → Collections request creates escrow hold → driver notified by SMS → journey marked ACTIVE → handover events stream into the telemetry pipeline → corridor model scores each transition → normal arrival detected → Disbursements releases escrow to the driver → both parties notified → journey appended to the driver's income record and to the aggregate network model.

=====================================================
6. AI / ML ARCHITECTURE
=====================================================

CORRIDOR LEARNING
Cell-tower handover sequences are treated as symbolic sequences over a spatially indexed cell vocabulary. Corridor signatures for each origin-destination pair are learned from aggregate historical traces using sequence models (GRU/LSTM encoders, with hidden Markov models as an interpretable baseline). No map data and no GPS are required — the network already generates the signal.

DURATION MODELLING
Per-route, per-time-band duration distributions modelled with quantile regression and gradient-boosted models, capturing peak-hour and day-of-week variation. Escalation thresholds are set on distribution quantiles, not on fixed timeouts, so a slow Friday evening does not trigger alarms.

ANOMALY DETECTION
Sequence deviation scored against the learned corridor; duration outliers scored against the learned distribution; combined into a single risk score with hysteresis so a momentary handover to an adjacent cell cannot trigger escalation. Autoencoder reconstruction error over trajectory embeddings serves as a complementary unsupervised signal.

AN EXPLICIT AND HONEST LIMITATION
Cell-tower positioning is coarse. Resolution ranges from hundreds of metres in dense urban areas to several kilometres in rural coverage. This is sufficient for CORRIDOR and DURATION anomaly detection. It is NOT turn-by-turn tracking, and we do not claim that it is. Escalation thresholds, hysteresis and the design of the silent check-in all follow from this constraint rather than ignoring it. Smartphone users may optionally add GPS for higher precision; the product is designed to work correctly without it.

INCOME RECORD GENERATION
Settled journeys aggregate into a verifiable earnings record. Feature design follows published research showing that periodicity and regularity of activity carry predictive signal for financial behaviour (mobile usage data predicts loan repayment at AUC 0.71–0.77, against 0.51–0.57 for conventional credit bureaux in comparable populations). The record is owned by the driver and disclosed only with their explicit consent.

TRANSIT NETWORK INFERENCE — AN HONEST CLAIM
South Africa's minibus network has been mapped before: WhereIsMyTransport conducted large-scale survey mapping, and open-data and consumer projects such as TeksiMap exist. What has never existed is a LIVE feed. Every prior mapping effort is a snapshot that decays from the day it is published. Hamba produces a continuously updating view of routes, frequencies and travel times as a by-product of settled payments, at zero marginal cost. That is the accurate and still-significant claim.

=====================================================
7. MOMO API INTEGRATION
=====================================================

  Get Paid (Collections) — fare collection into escrow
  Pay (Disbursements)    — escrow release to the driver, refunds, partial settlements
  Get Consent            — PIN-signed, journey-scoped, revocable monitoring consent. This is the legal and ethical foundation of the entire product.
  Identify (KYC)         — driver and passenger verification without Hamba collecting or storing identity
  Notify                 — SMS trip confirmation, arrival, escalation. Reaches users with no data.
  Interact (CaaS)        — USSD menu placement inside MoMo for feature-phone reach
  Manage                 — reconciliation of escrow positions
  Collection Widget      — QR presentment at ranks

CAPABILITY REQUIRING MTN PARTNERSHIP (stated openly): cell-handover telemetry is not exposed through public MoMo APIs. Hamba will be built against a synthetic handover feed with an identical interface contract, generated from realistic route geometries, and the data-sharing agreement is presented as an explicit partnership proposal. This is the product's central ask and we present it as such rather than assuming access.

=====================================================
8. SDLC AND DELIVERY METHODOLOGY
=====================================================

Trunk-based development, continuous integration on every push, daily working-software demonstrations.

 Phase 0 — Discovery and architecture (completed before the event: research, route and crime data analysis, architectural design. No application code.)
 Phase 1 — Foundation: repository, CI, MoMo sandbox connectivity, first end-to-end collection and disbursement
 Phase 2 — Escrow: trip state machine, event sourcing, hold and release logic, refund paths
 Phase 3 — Channels: USSD flow, SMS notification, PWA, QR initiation
 Phase 4 — Telemetry and intelligence: handover simulator, corridor learning, duration modelling, anomaly scoring
 Phase 5 — Escalation: tiered engine, contact management, operations dashboard
 Phase 6 — Hardening: adversarial testing, false-positive tuning, security review, demo rehearsal

RISK-FIRST SEQUENCING: The highest-uncertainty item is whether MTN exposes any handover signal, even in simulated form. This is raised with the MoMo developer community on day one. In parallel, a synthetic handover generator with a production-identical interface is built first, so the entire product can be developed and demonstrated regardless of the answer, and switched to live telemetry by configuration.

FALSE-POSITIVE DISCIPLINE: A safety product that cries wolf is worse than no product at all. Threshold tuning is treated as a first-class engineering task with an explicit target false-alarm budget, measured against simulated journeys before any escalation path is enabled.

QUALITY ENGINEERING: unit and integration tests across the escrow state machine; property-based tests asserting that funds are never lost, double-released or stranded; simulated journey corpora covering normal, delayed, rerouted and distress scenarios; adversarial tests for collusion between driver and passenger, false distress claims and escrow gaming; load testing on concurrent active journeys.

VERSION CONTROL AND PROVENANCE: honest commit history; README stating exactly what existed at registration (research and design) versus what is built during the event (all code).

=====================================================
9. SECURITY, PRIVACY AND COMPLIANCE
=====================================================

This product processes location data. The privacy design is the product design, and it must be stated before anyone asks.

 - MONITORING IS STRICTLY JOURNEY-SCOPED. Telemetry is consumed only while a trip is in the ACTIVE state. There is no background tracking, no monitoring between journeys, and no capability to query a user's location outside an active, consented trip. This constraint is enforced technically, not by policy.
 - CONSENT: journey-scoped, PIN-authenticated through Get Consent, revocable at any time, with plain-language terms in the user's own language.
 - RETENTION: raw handover traces are retained only for the journey window plus a short dispute period, then reduced to aggregate, de-identified route statistics. Individual traces are not retained for network mapping — only aggregates are.
 - MINIMISATION: identity handled through the Identify API; Hamba stores no identity documents. Emergency contacts are stored encrypted and are accessible only during an active escalation.
 - POPIA ALIGNMENT: lawful basis through explicit consent; purpose limitation enforced in code; location treated as sensitive personal information; data subject access and deletion supported; a documented data protection impact assessment for the monitoring function.
 - FINANCIAL CONTROLS: escrow held in a segregated position with full reconciliation; idempotency on every transition via X-Reference-Id; property-tested invariants asserting conservation of funds; defined timeout behaviour so no journey can strand money indefinitely.
 - TECHNICAL: TLS 1.3, AES-256-GCM at rest, Argon2id for credentials, HMAC webhook verification, secrets in a managed vault, OWASP ASVS baseline, automated secret scanning in CI, least-privilege access to telemetry with full access auditing.

=====================================================
10. ACCESSIBILITY AND INCLUSION
=====================================================

 - DEVICE: complete functionality on a feature phone through USSD and SMS. No application, no GPS, no smartphone. 16% of South African connections are feature phones and MTN sold 29% 2G devices in 2023/24.
 - DATA: zero data consumed on the USSD and SMS path.
 - BATTERY: no GPS polling and no background application means effectively no battery cost — which matters because a dead phone mid-journey is exactly the failure this product must survive.
 - LANGUAGE: USSD menus and SMS in the user's registered language; voice IVR path for low-literacy users. Approximately 29 million South Africans are not proficient in English and 3.8 million adults over 20 are classified as illiterate.
 - COST: no terminal, no hardware, no subscription. Previous taxi payment systems required roughly R2,000 per vehicle per month.
 - COVERAGE: South Africa has 99.85% 3G and 99.5% 4G population coverage, so the underlying signal exists essentially everywhere people travel.

=====================================================
11. INNOVATION — WHAT HAS NOT BEEN DONE BEFORE
=====================================================

 1. No product anywhere uses cell-handover telemetry as a safety supervision layer bound to a payment escrow. The payment is the safety instrument.
 2. Journey supervision with no application, no GPS and no data consumption has no precedent in South African transport.
 3. Every prior cashless taxi attempt tried to replace the fare and required industry permission. Hamba adds value without replacing anything and requires no association agreement.
 4. A continuously updating live view of the informal transit network, produced as a by-product of payments rather than as a survey exercise, has never existed.
 5. Automatic generation of a verifiable income record for gig workers as settlement exhaust, rather than as a separate product they must adopt.
 6. It is structurally impossible for any non-operator to build. This is not a moat; it is a physical constraint.

=====================================================
12. FEASIBILITY AND SCALABILITY
=====================================================

FEASIBILITY: USSD, SMS, QR and PWA are all standard, documented channels. Escrow is a state machine over MoMo Collections and Disbursements, both published APIs. Sequence anomaly detection over symbolic sequences is a well-posed, well-understood machine learning problem, not a research gamble. The only external dependency is handover telemetry, and the product is deliberately built against a synthetic feed with an identical interface so that development, demonstration and evaluation are unaffected by whether that access is granted during the event.

SCALABILITY — TECHNICAL: Stateless services; event-sourced trip state partitioned by trip identifier; telemetry ingestion designed as a streaming pipeline; corridor models trained offline and served from a registry; H3 spatial indexing scales to national coverage; escrow reconciliation batched.

SCALABILITY — GEOGRAPHIC: Every MTN market has an informal transport economy and a personal safety problem. The architecture is identical in every market; only the corridor models retrain on local data, and they retrain automatically from usage. MTN operates in 16 markets.

SCALABILITY — ECONOMIC: No hardware. No terminal. No per-vehicle cost. Marginal cost per journey is a USSD session, two SMS messages and a fraction of a cent of compute. This is the reason the R2,000-per-month terminal model failed and this one does not have to.

=====================================================
13. VALUE TO MTN
=====================================================

 - CASH-TO-DIGITAL CONVERSION at the highest-frequency transaction point in the informal economy. 15 million daily commuters, and over 80% of ride-hailing paid in cash.
 - MERCHANT ACQUISITION: every participating driver becomes an active MoMo merchant, with settlement into the wallet and cash-out across MTN's agent network.
 - DORMANCY: drivers receive settlement daily; passengers transact daily. Neither account is dormant.
 - THE ONLY-MTN ASSET MONETISED: network telemetry becomes a consumer product rather than an operational cost centre. This is the clearest example in the MoMo ecosystem of converting telco legacy into fintech advantage.
 - DATA ASSET: a live view of the informal transport network has direct value to government, urban planners, insurers and MTN's own network planning.
 - CREDIT PIPELINE: verified driver income records are the input to every financial product MTN would want to sell that cohort.
 - TRACK RECORD: no MoMo hackathon winner has come from mobility, and it is the hardest and most strategically valuable category in South Africa.

=====================================================
14. RISKS AND MITIGATIONS
=====================================================

 RISK: MTN may not expose handover telemetry.
 MITIGATION: Built against a synthetic feed with a production-identical interface contract; switchable by configuration. The data agreement is presented explicitly as the partnership ask.

 RISK: Cell positioning is too coarse for meaningful supervision.
 MITIGATION: Stated openly and first. The design targets corridor and duration anomaly, not turn-by-turn tracking. Thresholds, hysteresis and the silent check-in mechanism are all consequences of this constraint. Optional GPS augmentation for smartphone users.

 RISK: False alarms destroy trust.
 MITIGATION: Tiered escalation beginning with a silent check-in, never an alarm. Per-corridor adaptive thresholds on distribution quantiles. An explicit false-alarm budget measured before escalation paths are enabled.

 RISK: Privacy objection to journey monitoring.
 MITIGATION: Monitoring is technically constrained to active, consented journeys. No background tracking capability exists. Raw traces are retained only for the journey window. Stated on a slide before it is asked.

 RISK: Drivers refuse escrow.
 MITIGATION: They are paid instantly on arrival and carry no cash in a country where drivers are killed for cash. The incentive is immediate and selfish. Tested with real drivers early rather than assumed.

 RISK: Taxi association resistance.
 MITIGATION: Not required for version one. The product works for e-hailing, private hire and lift clubs, driver-to-passenger, with no association agreement, no terminal and no route concession. The minibus industry is phase two, entered with proof rather than promises.

 RISK: Collusion or false distress claims.
 MITIGATION: Independent network evidence for both parties; adversarial test suite; reputation weighting; escrow held rather than reversed pending resolution.

 RISK: Coverage gaps produce spurious anomalies.
 MITIGATION: Gaps are modelled as missing observations. Escalation requires sustained anomaly, never a single missing transition.

=====================================================
15. SUCCESS METRICS
=====================================================

 PRODUCT: journeys initiated per week; completion rate; driver retention; passenger repeat rate; proportion of journeys initiated from feature phones.
 SAFETY: escalation precision and recall on labelled journeys; false-alarm rate per thousand journeys; median time to first escalation; check-in response rate.
 TECHNICAL: corridor model accuracy; duration prediction error; escrow settlement latency; reconciliation accuracy; zero fund-conservation violations.
 IMPACT: cash removed from vehicles (rand value per driver per week); drivers with a verifiable income record; incidents detected.
 BUSINESS: MoMo transaction volume and value; new active merchants; agent cash-out volume; wallet balance retention among drivers.

=====================================================
16. ROADMAP BEYOND THE HACKATHON
=====================================================

 0–3 months: Formalise the telemetry data agreement with MTN; provision the Interact USSD channel; closed pilot with an e-hailing driver cohort in one metropolitan corridor; response-partner integration.
 3–6 months: Public launch for e-hailing and private hire; driver income record released as a shareable, driver-owned credential; insurance partnership on trip-linked micro-cover.
 6–12 months: First minibus taxi association pilot, entered with demonstrated results; live transit network view released to municipal planning partners.
 12 months+: Second MTN market; the journey supervision layer offered as a platform primitive to other mini apps.

=====================================================
17. THE DEMONSTRATION
=====================================================

 1. Two handsets. One of them a R149 2G feature phone. No application installed on either.
 2. A journey is initiated by USSD. Funds move visibly into escrow.
 3. The presenter walks out of the room. On the operations display, the journey tracks cell by cell.
 4. The presenter deviates — takes a wrong turn, or stops and stands still. The silent check-in fires. Unanswered, the escalation reaches a nominated contact's handset live on stage.
 5. The presenter returns to the destination. Escrow releases. The driver is paid. The journey appends to the driver's income record.

=====================================================

Fourteen systems tried to take the cash out of South African transport and failed, because they asked people to change first. Hamba gives the driver a reason to want the cash gone — and gives the passenger someone watching. The payment is the safety instrument.
```

## --- Q11: Technologies ---

```
FRONTEND: React 18, TypeScript, Vite, Tailwind CSS, Progressive Web App (Service Worker, Workbox), built to the MTN MoMo Mini App PWA integration specification, with optional Geolocation API augmentation for smartphone users.

CHANNELS: Africa's Talking USSD and Voice APIs for prototype channel delivery, with MTN Interact (Channel as a Service) as the production path; server-side USSD session state machine respecting the 182-character response limit and a five-level menu depth ceiling; MTN Notify for SMS; QR presentment via the MoMo Collection Widget.

BACKEND: Python 3.12, FastAPI, Pydantic; event-sourced trip state machine; Celery with Redis for asynchronous escalation and settlement workflows; WebSockets and Server-Sent Events for the live operations dashboard.

DATA: PostgreSQL 16 with PostGIS for spatial data and TimescaleDB for handover time-series; Uber H3 hexagonal spatial indexing for cell and corridor binning; Redis for active-journey state and session caching; Apache Kafka or Redis Streams for the telemetry ingestion pipeline.

MACHINE LEARNING: PyTorch for sequence models (GRU/LSTM encoders over symbolic cell-handover sequences) with hmmlearn hidden Markov models as an interpretable baseline; LightGBM and quantile regression for per-route, per-time-band duration distributions; scikit-learn isolation forests and autoencoder reconstruction error for unsupervised trajectory anomaly detection; NetworkX for transit graph inference; scikit-mobility and MOVINGPANDAS for trajectory processing.

TELEMETRY SIMULATION: a purpose-built synthetic cell-handover generator producing realistic handover sequences from route geometries, cell tower placement models and configurable coverage gaps, exposing a production-identical interface so the system can be switched from synthetic to live telemetry by configuration alone.

GEOSPATIAL VISUALISATION: deck.gl and MapLibre GL JS for the live network view and operations dashboard; GeoJSON and vector tiles for corridor rendering.

MLOPS: MLflow for experiment tracking and model registry, DVC for dataset versioning, Weights & Biases for training runs; an evaluation harness reporting escalation precision, recall and false-alarm rate against a labelled corpus of simulated normal, delayed, rerouted and distress journeys.

MOMO APIS: Get Paid (Collections) for escrow funding, Pay (Disbursements) for escrow release and refunds, Get Consent for PIN-signed journey-scoped revocable monitoring consent, Identify (KYC) for driver and passenger verification without storing identity, Notify for SMS, Interact (Channel as a Service) for USSD placement, Manage for escrow reconciliation, Collection Widget for QR. OAuth bearer tokens on a 3600-second refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling outcome resolution.

SECURITY: TLS 1.3, AES-256-GCM at rest, Argon2id credential hashing, encrypted emergency contact storage with access gated on active escalation, HMAC webhook signature verification, HashiCorp Vault or cloud KMS, least-privilege telemetry access with full access auditing, OWASP ASVS baseline, automated secret scanning and dependency auditing in CI.

INFRASTRUCTURE / DEVOPS: Docker and Docker Compose, GitHub Actions CI/CD, Cloudflare Pages or Vercel for the PWA, containerised backend on Azure Container Apps or equivalent, Terraform for infrastructure as code, Cloudflare Tunnel for MoMo callbacks in development.

OBSERVABILITY: OpenTelemetry distributed tracing across the trip lifecycle, Prometheus and Grafana, Sentry, structured JSON audit logging of every state transition and escalation event.

TESTING / QA: pytest with Hypothesis for property-based testing asserting fund-conservation invariants across the escrow state machine (funds are never lost, double-released or stranded); simulated journey corpora covering normal, delayed, rerouted, coverage-gap and distress scenarios; adversarial suites for driver-passenger collusion, false distress claims and escrow gaming; Playwright for end-to-end PWA flows; Locust for concurrent active-journey load testing.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, USSD flow design constrained to five steps to confirmation, aggressive payload minimisation given South African data costs.
```

---
---

# APPENDIX — THE ORGANISER EMAIL

Send this before submitting. All three questions in one message.

```
Subject: MoMo Mini App Hackathon 2026 — three clarification questions before registration

Good day,

We are a South African team preparing to register for the MoMo Mini App
Hackathon 2026 on 2-3 September. Three questions we would like to resolve
before we submit, so that our entries comply exactly with your intent.

1. TEAM SUBMISSIONS ACROSS TRACKS
   May individual members of the same team each submit one entry in a
   different track under a shared team name, or is the rule one submission
   per team? We would rather ask than assume.

2. JUDGING STRUCTURE
   Are prizes awarded per track, or overall across all three tracks?

3. PRE-EVENT PREPARATION
   The Terms and Conditions state that all work must be created during the
   hackathon and that pre-existing projects are prohibited unless approved
   by the organiser. The registration form, however, asks for a GitHub
   repository URL and a detailed project description in advance.

   Could you confirm what preparation is permitted before the event? Our
   intention is to arrive with research, architecture and design
   documentation prepared, and to write all application code during the
   event, with an honest commit history and a README stating clearly what
   existed at registration versus what was built on the day. Please let us
   know if that is acceptable or if you would prefer a different approach.

We would also appreciate confirmation of which MoMo APIs will be enabled
in the South African sandbox for the event, and whether day-of credentials
will be provided or whether we should pre-register developer accounts.

Thank you for your time.

Kind regards,
[Name]
[Team name]
[Contact]
```

---

# APPENDIX — PRE-SUBMISSION CHECKLIST

- [ ] Organiser reply received on the multi-submission rule
- [ ] Three GitHub repositories created (README only, no code)
- [ ] Identical team name string on all three forms: `South Africa-Umoya`
- [ ] Short summaries pasted without edit (222 / 221 / 224 characters — recount if changed)
- [ ] All descriptions checked: no past-tense claims that anything is already built
- [ ] Sesotho and Setswana speakers have signed off the "moya" claim
- [ ] MoMo developer accounts registered; sandbox subscription keys obtained
- [ ] Gated Mini App PWA integration spec and design standards downloaded
- [ ] Each teammate has read their own entry end to end and can defend every number in it
