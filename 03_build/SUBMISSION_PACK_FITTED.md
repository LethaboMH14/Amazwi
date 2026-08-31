# SUBMISSION PACK v2 — FITTED TO THE 4000-CHARACTER LIMIT
**Verified 2026-08-15.** The form caps Q10 (detailed description) and Q11 (technologies) at **4000 characters** each. Q9 (short summary) is capped at 250. Every block below is measured and under limit with headroom.

## READ BEFORE PASTING
1. **Paste only what is inside the fences.** Not the fence marks, not the headings above them.
2. **Do not edit and re-paste without recounting.** Paste into a character counter first if you change a word.
3. **Tense is deliberate.** Everything is written as planned work. The T&Cs prohibit pre-existing projects — do not switch anything to past tense.
4. **Multi-submission rule still unconfirmed.** Send the organiser email (in SUBMISSION_PACK.md) before anyone submits. If three entries under one team name are disallowed, submit Umoya only.
5. **Team name, identical on all three:** `South Africa-Umoya`
6. **Three GitHub repos must exist before submitting** — README only, no code.
7. What was cut to fit: success metrics, roadmap, full user journeys and the risk register. Those live in `02_ideas/MOONSHOTS.md` and `THE_THREE_ENTRIES.md` and belong in the pitch deck, not the form.


---

# UMOYA — Lethabo

## Q8 — Track
```
Track 1: Everyday Essentials
```

## Q9 — Short summary (222 characters, limit 250)
```
Umoya puts MoMo's intelligence in MTN's network instead of your phone. Speak isiZulu into a R149 Nokia. Transact with no data and no signal. Keep your money when the phone is taken at gunpoint. Banking that works, even if.
```

## Q10 — Detailed description (3915 characters, limit 4000)
```
UMOYA — "even if". An AI money agent that lives in MTN's network, not on your phone. Only an operator can build it: no bank can reach the voice channel of a R149 Nokia.

PROBLEM. SA fintech is built for the smartphone — the least reliable object in a South African's life. SABRIC 2025 logs R2.4bn in digital banking crime, 88.6% of it banking-app fraud, against R630,000 from physical bank robberies. Kidnapping is up 264% to ~53/day, victims coerced into "draining their accounts". English is SA's 5th home language at 8.7%, and Google Cloud scores 56.71% WER on isiXhosa against 9.6% for a human. ~14m banked South Africans only receive and immediately withdraw; 70%+ of African wallets are dormant. Not access — usage, failing where the phone fails.

SOLUTION. One agent, one identity, one balance, five surfaces: VOICE CALL (any SA language or a mix; no app, no data, no literacy), USSD via Interact/Channel as a Service, MINI APP to the MoMo PWA spec, SMS via Notify, OFFLINE NFC TAP. The phone is a terminal, not the wallet.
SPEAK — code-switched SA speech ("ngicela i-data"), costing monolingual ASR 30-50% WER and tested by no global benchmark.
SURVIVE — a DURESS PIN shows a reduced balance and completes a convincing transfer that moves nothing, silently alerting MTN, your contacts and network location. Phone stolen: call from any handset and freeze; recovery runs on your transaction graph, not the SIM.
ACT — Get Consent is a PIN-signed mandate primitive MTN publishes and nobody uses. Mapped onto Google AP2 mandates it gives MoMo the first African agent-mandate layer: scoped, capped, revocable.
FORESEE — usage periodicity predicts repayment at AUC 0.71-0.77 versus 0.51-0.57 for a credit bureau; lenders price people with it, we warn the person.
ENDURE — Ed25519 tokens with ancestry chains over Android HCE per the US Federal Reserve offline framework: R500 float, 24h, ~10 hops.

WHY NOW. MTN signed Ant International in June 2026: rails bought, supply missing. MTN still ships no consumer AI product. Swivuriso released 3,016 hours across 7 SA languages under CC BY 4.0 this year; Google's WAXAL covered 27 African languages and none of ours.

ARCHITECTURE. Six event-driven layers: channels (voice gateway, server-side USSD state machine, PWA, SMS, NFC HostApduService); conversation (cascaded ASR-intent-TTS, not speech-to-speech, since 8kHz telephony erases the S2S advantage; read-back before value moves); agent; intelligence; ledger (UUID v4 idempotency, dual webhook and polling).
AUTHENTICATION: voice is the interface, never the lock — cloning on 10-30 minutes of audio bypasses speaker verification 82.7% of the time, so we authenticate on PIN, behaviour, device and SIM state, and graph.

MOMO APIS. Get Paid, Pay, Get Consent, Identify, Notify, Invoice, Manage, Interact, Collection Widget. Stated openly: SIM-swap and network-location signals are not publicly exposed, so we build against a simulated feed with an identical interface and present the data agreement as a partnership ask.

SDLC. Trunk-based, CI on every push, daily demos. Phase 0 discovery and architecture preceded the event — research and design only, no code. Risk-first: an AI voice agent over a GSM call is untested in the literature, so it is prototyped inside 72 hours.

SECURITY AND SCALE. AES-256-GCM, TLS 1.3, HMAC webhook verification, OWASP ASVS; identity via Identify so no documents are stored; mandates revocable under POPIA. Scaling swaps the language model, not the product — Nigeria, Uganda and Ghana are covered by the open WAXAL corpus.

DEMO. A judge's smartphone goes in a drawer; they get a R149 2G feature phone. They dial, speak isiZulu, send money, set a mandate. Then: "you have been hijacked and they have your PIN." They enter the duress PIN, a transfer completes convincingly, nothing moves, and the silent alert appears behind them. Data off, two handsets tapped, the payment settles.
```

## Q11 — Technologies (3795 characters, limit 4000)
```
FRONTEND: React 18, TypeScript, Vite, Tailwind, PWA (Workbox service worker, Web App Manifest), IndexedDB offline queue, WCAG 2.2 AA, built to the MTN MoMo Mini App PWA integration specification.

BACKEND: Python 3.12, FastAPI, Pydantic, Celery + Redis for async work, WebSockets/SSE for real-time updates.

DATA: PostgreSQL 16 + TimescaleDB for transaction and usage time-series, Redis for session and access-token caching, S3-compatible object storage for audio.

SPEECH/ASR: OpenAI Whisper large-v3-turbo fine-tuned on the Swivuriso / South African Next Voices corpus (CC BY 4.0, 3,016 hours, 7 SA languages) with Hugging Face Transformers and PEFT/LoRA; Meta W2V-BERT 2.0 as a per-language comparator, since published results favour W2V-BERT on Nguni and Whisper on Sotho-Tswana; CTranslate2/faster-whisper for low-latency inference; torchaudio telephony-band augmentation (8kHz downsampling, AMR-NB codec simulation) so the model trains on the audio it will actually receive; Silero VAD; SpeechBrain speaker embeddings.

TTS: Simba-TTS (UBC-NLP, CC-BY-4.0: Afrikaans, S. Sotho, Tswana, Xhosa), Meta MMS-TTS, with pre-recorded prompt concatenation as a guaranteed-intelligibility fallback for value-bearing confirmations.

NLU: constrained intent classification over a closed financial action set, plus a commercially-licensed small model (Gemma 3 / Qwen 2.5 class, 0.5-3B, 4-bit quantised) for slot filling. InkubaLM is CC BY-NC and is explicitly excluded from the production path.

ML: PyTorch, Hugging Face Transformers/Datasets, scikit-learn, LightGBM and XGBoost for forecasting and risk scoring, statsmodels, NetworkX and PyTorch Geometric for transaction-graph features, ONNX Runtime for optimised inference.

MLOPS: MLflow model registry, DVC dataset versioning, Weights & Biases, and a stratified evaluation harness reporting WER and forecast accuracy by language, province and urban/rural cohort.

TELEPHONY/CHANNELS: Africa's Talking Voice and USSD APIs for prototype delivery (SIP/PSTN termination, session management) with MTN Interact (Channel as a Service) as the production path; MTN Notify for SMS.

OFFLINE: Android/Kotlin Host-based Card Emulation via HostApduService for device-to-device NFC with no network and no secure element; Ed25519 via libsodium/Google Tink; token ancestry chains and single-use key semantics per the US Federal Reserve "A Robust Risk Framework for Offline Payments" (Dec 2025); CBOR encoding inside the ~1KB / ~300ms APDU budget.

MOMO APIS: Collections (Get Paid), Disbursements (Pay), Get Consent, Identify (KYC), Notify, Invoice, Manage, Interact, Collection Widget. OAuth bearer tokens on a 3600s refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling outcome resolution.

AGENTIC STANDARDS: mandate structures aligned to Google's Agent Payments Protocol (AP2) Intent Mandate and Cart Mandate patterns as signed, scoped, revocable authorisations.

SECURITY: Argon2id PIN hashing, AES-256-GCM at rest, TLS 1.3, short-lived rotating JWTs, HMAC webhook signature verification, HashiCorp Vault or cloud KMS, OWASP ASVS baseline, secret scanning and dependency auditing in CI.

DEVOPS: Docker, GitHub Actions CI/CD, Cloudflare Pages or Vercel for the PWA, containerised backend on Azure Container Apps, Cloudflare Tunnel/ngrok for MoMo callbacks in development, Terraform.

OBSERVABILITY: OpenTelemetry tracing, Prometheus and Grafana, Sentry, structured JSON audit logging.

TESTING: pytest with Hypothesis for property-based tests of ledger invariants, Vitest, Playwright end-to-end, Locust load testing, and adversarial suites for the duress flow, token replay and double-spend.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, aggressive payload minimisation given SA data costs.
```


---

# AMAZWI — Teammate 2

## Q8 — Track
```
Track 2: Entertainment and Lifestyle
```

## Q9 — Short summary (221 characters, limit 250)
```
Amazwi is a game where speaking your language pays. Daily voice challenges in every South African language, instant MoMo payouts, cents at a time. It builds the African speech data the world skipped, and our youth own it.
```

## Q10 — Detailed description (3958 characters, limit 4000)
```
AMAZWI — "the voices". A game where speaking your language pays. Young South Africans earn MoMo, cents at a time, for the one asset global AI cannot buy: their language.

PROBLEM. Two problems nobody has connected. Youth unemployment is 45.8% — 4.7 million people — and 50.5% of employed 15-24s work informally. Meanwhile SA languages are the continent's most valuable untapped data asset and are being skipped. Google Cloud scores 56.71% WER on isiXhosa against 9.6% for a human; foundation models exceed 100% WER zero-shot on all six Southern Bantu languages. Google's Feb 2026 WAXAL release covered 11,000 hours across 27 African languages and zero South African ones. Code-switched SA speech barely exists as data, costs monolingual ASR 30-50% WER, and the June 2026 frontier benchmark tested zero African languages. MTN has committed publicly to AI with no consumer AI product, no African-language data asset, and no youth product since Ayoba closed in March 2026.

SOLUTION. Daily voice challenges: read this, describe this photo, say it the way you'd say it to a friend, argue with this. Code-switch challenges deliberately elicit the speech no dataset on earth contains. Peers validate and correct each other; both sides earn. Streaks, levels and leaderboards by language and by place — Khayelitsha against Soweto. Instant MoMo payout per validated task. SCARCITY PRICING: the rarer your language the more you earn, so Tshivenda (2.5%) and isiNdebele (1.7%) speakers earn most — economically correct, and the moral core of the product. Output: a continuously growing, individually consented SA speech corpus.

WHY MTN. MTN is simultaneously payer and buyer — it funds the contributions and needs the data. Cent-scale payouts to 69.5m wallets are impossible on card rails. Identify solves the hardest problem in crowdsourced data, proving each contributor is a real unique human, without storing any identity.

ARCHITECTURE AND AI. Capture client with on-device quality gating (SNR, clipping, VAD) so nothing is uploaded that will be rejected and no data is wasted; task orchestration; validation and integrity; corpus and ML; game economy; MoMo integration. ACTIVE LEARNING is the core idea: an acquisition function ranks prompts by expected model improvement using uncertainty sampling and embedding diversity, so the system asks for what the model is least certain about — the difference between a survey and an acquisition engine. Continuous PEFT/LoRA fine-tuning of Whisper and W2V-BERT on the accumulating corpus, seeded from Swivuriso, where published baselines take Setswana from 223% to 13% WER.

MOMO APIS. Identify for unique-human verification, Get Consent for PIN-signed revocable contribution consent, Pay for batched cent-scale instant payouts, Notify for SMS earnings confirmation, Interact for feature-phone entry.

SDLC. Trunk-based, CI on every push, daily demos. Phase 0 discovery and architecture preceded the event — research and design only, no code — then capture loop, validation and integrity, game economy, ML pipeline, hardening. Risk-first: the real risks are human, so a live contributor cohort is recruited early and the team attacks its own platform for fraud before demo day.

ETHICS AND COMPLIANCE. This collects biometric data from a vulnerable population, so the ethics are the architecture. Consent is explicit, in the contributor's language, PIN-authenticated and revocable, and revocation removes data from future training. POPIA lawful basis by consent, purpose limitation enforced in code. Rates published before the task, never adjusted after. We raise the sweatshop question ourselves and answer it structurally.

SCALE. Every MTN market has underserved languages; Nigeria alone has 500+.

DEMO. A judge speaks one sentence in their language. It validates live, their region climbs the leaderboard, cents land in a MoMo wallet on screen — and the model's isiXhosa WER falls in real time from Google's 56.71%.
```

## Q11 — Technologies (3949 characters, limit 4000)
```
FRONTEND: React 18, TypeScript, Vite, Tailwind, PWA (Workbox service worker), IndexedDB offline capture queue, built to the MTN MoMo Mini App PWA integration specification.

AUDIO CAPTURE AND ON-DEVICE PROCESSING: Web Audio API, MediaRecorder, Opus/WebM encoding, AudioWorklet for real-time analysis, Silero VAD compiled to ONNX and run via ONNX Runtime Web for in-browser voice activity detection, plus in-browser SNR estimation and clipping detection so a recording is rejected before it costs the contributor any data.

BACKEND: Python 3.12, FastAPI, Pydantic, Celery + Redis for the validation and payout pipelines, WebSockets for live leaderboards.

DATA: PostgreSQL 16 for metadata, consent lineage and the payout ledger; Redis sorted sets for leaderboards and streaks; S3-compatible object storage (Azure Blob / MinIO) for audio; Apache Parquet for corpus export.

ML: PyTorch, Hugging Face Transformers/Datasets/PEFT; OpenAI Whisper large-v3-turbo and Meta W2V-BERT 2.0 fine-tuned with LoRA on the accumulating corpus, seeded from Swivuriso / South African Next Voices (CC BY 4.0, 3,016 hours, 7 SA languages); jiwer for WER; scikit-learn and LightGBM for reliability and integrity modelling; isolation forests for submission anomaly detection.

ACTIVE LEARNING: uncertainty sampling by predictive entropy, diversity-based selection over speech embeddings, modAL-style acquisition orchestration.

AUDIO AND SPEAKER INTEGRITY: SpeechBrain and pyannote.audio ECAPA-TDNN speaker embeddings used strictly for uniqueness enforcement (one human, one account) and never as an authentication factor, since cloning bypasses speaker verification 82.7% of the time; chromaprint-style audio fingerprinting for duplicate and replay detection; librosa and torchaudio for feature extraction.

ANNOTATION QUALITY: Krippendorff's alpha for inter-annotator agreement, Bayesian contributor-reliability scoring, consensus routing with anti-collusion assignment.

MLOPS AND DATA GOVERNANCE: DVC for dataset versioning with consent lineage, MLflow for experiment tracking and model registry, Hugging Face Datasets for corpus packaging and release, Weights & Biases for training runs, and a stratified evaluation harness reporting WER by language, dialect region.

TELEPHONY: Africa's Talking Voice API for the feature-phone contribution path (SIP/PSTN, IVR challenge delivery and recording), with MTN Interact (Channel as a Service) as the production entry point; MTN Notify for SMS earnings confirmations.

MOMO APIS: Identify (KYC) for unique-human verification without storing identity, Get Consent for PIN-signed revocable contribution consent, Pay (Disbursements) for batched cent-scale instant payouts with idempotency and reconciliation, Notify for SMS, Interact for feature-phone reach. OAuth bearer tokens on a 3600s refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling resolution.

SECURITY: TLS 1.3, AES-256-GCM at rest, Argon2id credential hashing, signed pre-authenticated upload URLs, per-user and per-device rate limiting, HMAC webhook verification, HashiCorp Vault or cloud KMS, OWASP ASVS baseline, secret scanning in CI.

DEVOPS: Docker, GitHub Actions CI/CD, Cloudflare Pages or Vercel for the PWA, containerised backend on Azure Container Apps, Terraform, Cloudflare Tunnel for MoMo callbacks in development.

OBSERVABILITY: OpenTelemetry, Prometheus and Grafana, Sentry, structured JSON audit logging with full consent and payout traceability.

TESTING: pytest with Hypothesis for property-based tests of the payout ledger, Vitest, Playwright end-to-end capture flows, Locust for batch disbursement load, and a dedicated adversarial suite simulating duplicate submission, account farming, collusion rings and replay attacks.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, game UI patterns for progress, streaks and tiers, aggressive payload minimisation given SA data costs.
```


---

# HAMBA — Teammate 3

## Q8 — Track
```
Track 3: Travel and Mobility
```

## Q9 — Short summary (224 characters, limit 250)
```
Hamba turns a taxi fare into a safety contract. Pay by USSD, funds sit in escrow, and MTN's network watches the journey by cell tower. No app, no GPS, no data. Arrive, the driver is paid. Deviate, and your people are called.
```

## Q10 — Detailed description (3950 characters, limit 4000)
```
HAMBA — "go", from hamba kahle, go well. Pay for your journey and MTN's network watches you take it. No app, no GPS, no data.

PROBLEM. SA transport has two problems and every attempt has solved only one. PAYMENT: 15 million daily minibus commuters pay cash, over 80% of ride-hailing trips are cash on Bolt's own figure,. SAFETY: kidnapping is up 264% to ~53/day; 44% are tied to hijackings and 22% to robberies, only 4% to ransom, and nearly 80% of Gauteng kidnappings involve armed robbery. These are the same problem: the reason the driver wants cash is the reason the driver gets robbed.

SOLUTION. Start a journey by USSD, voice or a QR at the rank — origin and destination declared, no app on either handset. The fare enters ESCROW: the driver sees committed funds and the cash leaves the vehicle. The network then watches by CELL-TOWER HANDOVER — no GPS, no app, no data, no battery drain — with route corridor and duration learned from aggregate journeys. Arrival within the learned envelope releases escrow automatically. Sustained corridor departure, a stop where journeys don't stop, or a duration far outside the envelope triggers tiered escalation: silent check-in, then nominated contacts, then a response partner. The driver gets no cash in the car, guaranteed payment and an automatic verifiable income record. The passenger gets a journey someone is watching, and no cash on them.

WHY IT BEATS 14 FAILURES, AND WHY ONLY MTN. Every previous system tried to REPLACE the fare, so it needed industry permission, a terminal per vehicle. Hamba replaces nothing — it adds safety and guaranteed payment to a journey that happens anyway, driver-to-passenger, with no association agreement and no hardware. And cell-handover data belongs to the operator alone: Uber, Bolt, Shop2Shop, Capitec and Yoco do not have it. Journey supervision with no app, no GPS and no data is not merely hard for a competitor — it is structurally impossible without owning the radio network.

ARCHITECTURE AND AI. Channels (USSD state machine, voice IVR, PWA, SMS, QR); journey orchestration (INITIATED-FUNDED-ACTIVE-ARRIVED-SETTLED, event-sourced, with escrow holds and release); telemetry (handover ingestion, H3 spatial indexing, corridor model store, missing-observation handling); intelligence; escalation; MoMo integration.
STATED PLAINLY: cell positioning is coarse, hundreds of metres to kilometres. That is enough for CORRIDOR and DURATION anomaly. It is not turn-by-turn tracking and we do not claim it is.

MOMO APIS. Get Paid for escrow funding, Pay for release and refunds, Get Consent for journey-scoped revocable monitoring consent, Identify for verification without storing identity, Notify for SMS, Interact for USSD placement, Manage for reconciliation, Collection Widget for QR. Handover telemetry is not publicly exposed, so we build against a synthetic feed with a production-identical interface and present the data agreement as the partnership ask.

SDLC. Trunk-based, CI on every push, daily demos. Phase 0 discovery and architecture preceded the event — research and design only, no code. Risk-first: the synthetic handover generator is built first so everything is demonstrable regardless of data access, switchable by configuration. False-positive tuning is a first-class task with an explicit alarm budget, because a safety product that cries wolf is worse than none.

PRIVACY AND SCALE. Monitoring is technically scoped to ACTIVE journeys — no background tracking capability exists. Journey-scoped PIN-signed consent, revocable; POPIA lawful basis by consent with a documented impact assessment.

DEMO. Two handsets, one a R149 2G feature phone, no app on either. A journey starts by USSD and funds visibly enter escrow. The presenter walks out; the journey tracks cell by cell on screen. They deviate — the silent check-in fires, then a nominated contact's phone rings live on stage. They return, escrow releases, the driver is paid.
```

## Q11 — Technologies (3957 characters, limit 4000)
```
FRONTEND: React 18, TypeScript, Vite, Tailwind, PWA (Workbox service worker), built to the MTN MoMo Mini App PWA integration specification, with optional Geolocation API augmentation for smartphone users.

CHANNELS: Africa's Talking USSD and Voice APIs for prototype channel delivery, with MTN Interact (Channel as a Service) as the production path; a server-side USSD session state machine respecting the 182-character response limit and a five-level menu-depth ceiling; MTN Notify for SMS; QR presentment via the MoMo Collection Widget.

BACKEND: Python 3.12, FastAPI, Pydantic; an event-sourced trip state machine; Celery + Redis for asynchronous escalation and settlement workflows; WebSockets and Server-Sent Events for the live operations dashboard.

DATA: PostgreSQL 16 with PostGIS for spatial data and TimescaleDB for handover time-series; Uber H3 hexagonal spatial indexing for cell and corridor binning; Redis for active-journey state; Apache Kafka or Redis Streams for the telemetry ingestion pipeline.

ML: PyTorch for sequence models (GRU/LSTM encoders over symbolic cell-handover sequences) with hmmlearn hidden Markov models as an interpretable baseline; LightGBM and quantile regression for per-route, per-time-band duration distributions; scikit-learn isolation forests and autoencoder reconstruction error for unsupervised trajectory anomaly detection; NetworkX for transit graph inference; scikit-mobility.

TELEMETRY SIMULATION: a purpose-built synthetic cell-handover generator producing realistic sequences from route geometries, tower placement models, exposing a production-identical interface so the system switches from synthetic to live telemetry by configuration alone.

GEOSPATIAL VISUALISATION: deck.gl and MapLibre GL JS for the live network view and operations dashboard; GeoJSON and vector tiles for corridor rendering.

MLOPS: MLflow for experiment tracking and model registry, DVC for dataset versioning, Weights & Biases for training runs, and an evaluation harness reporting escalation precision, recall and false-alarm rate against a labelled corpus of simulated normal, delayed, rerouted.

MOMO APIS: Get Paid (Collections) for escrow funding, Pay (Disbursements) for escrow release and refunds, Get Consent for PIN-signed journey-scoped revocable monitoring consent, Identify (KYC) for driver and passenger verification without storing identity, Notify for SMS, Interact (Channel as a Service) for USSD placement, Manage for escrow reconciliation, Collection Widget for QR. OAuth bearer tokens on a 3600s refresh cycle, UUID v4 X-Reference-Id idempotency keys, dual webhook-and-polling outcome resolution.

SECURITY: TLS 1.3, AES-256-GCM at rest, Argon2id credential hashing, encrypted emergency-contact storage gated on active escalation, HMAC webhook signature verification, HashiCorp Vault or cloud KMS, least-privilege telemetry access with full access auditing, OWASP ASVS baseline, secret scanning in CI.

DEVOPS: Docker, GitHub Actions CI/CD, Cloudflare Pages or Vercel for the PWA, containerised backend on Azure Container Apps, Terraform, Cloudflare Tunnel for MoMo callbacks in development.

OBSERVABILITY: OpenTelemetry distributed tracing across the trip lifecycle, Prometheus and Grafana, Sentry, structured JSON audit logging of every state transition and escalation event.

TESTING: pytest with Hypothesis for property-based tests asserting fund-conservation invariants across the escrow state machine (funds never lost, double-released or stranded); simulated journey corpora covering normal, delayed, rerouted, coverage-gap and distress scenarios; adversarial suites for driver-passenger collusion, false distress claims and escrow gaming; Playwright end-to-end; Locust for concurrent active-journey load.

DESIGN: Figma, mobile-first single-column layouts per MoMo Mini App design standards, USSD flows constrained to five steps to confirmation, aggressive payload minimisation given SA data costs.
```
