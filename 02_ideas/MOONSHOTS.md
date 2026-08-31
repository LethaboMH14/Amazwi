# MOONSHOTS — the out-of-this-world tier
**Created:** 2026-08-15 · Session 3 · Owner: Lethabo
**Status:** wide ideation at maximum ambition. Supersedes nothing — sits *above* `IDEAS_BOARD.md`.

> **Why this file exists.** The 33 concepts in `IDEAS_BOARD.md` are competent fintech products. Not one of them would make a judge lean back and ask *"how did you do that?"* They are all, structurally, *a screen that moves money*. Every one of them dies when the phone is stolen, the data runs out, the network drops, or the user doesn't read English.
>
> This file is the answer to that. Everything here is grounded in research done 15 Aug 2026 — sources in `../INFO_LOG.md` under Session 3.

---

# PART 1 — THE SEVEN FACTS THAT CHANGE THE BRIEF

These were not known when the 33 were written. Each one is load-bearing.

### FACT 1 · The language barrier just became crossable — and the window is open *now*

- South Africa has **12 official languages**. English is the **5th** most-spoken home language at **8.7%**. Roughly **29 million South Africans are not proficient in English.**
- **Google Cloud Speech-to-Text gets isiXhosa wrong 56.71% of the time** on realistic conversational speech. Meta MMS gets it wrong **92.50%**. A human transcriber: 9.6%.
- Foundation ASR models score **above 100% WER zero-shot** on all six Southern Bantu languages — worse than outputting nothing.
- **But in the last twelve months the data barrier collapsed.** The **Swivuriso** corpus (South African Next Voices) released **3,016 hours across 7 SA languages, 483,191 clips, 2,440 speakers, CC BY 4.0 — free and commercially usable.** Fine-tuning on it took Setswana from **223% WER → 13%** and Xitsonga from **190% → 12%**.
- **Google's WAXAL push (Feb 2026, 11,000 hours, 27 African languages) contains zero South African official languages.** Google is investing in East and West Africa.
- **Code-switching** — how South Africans actually speak ("ngicela i-data") — costs monolingual ASR **30–50% WER**, and the June 2026 frontier code-switching benchmark tested **zero African languages**.
- Lelapa AI's Vulavula is the only commercial contender: **isiZulu and Sesotho only** for transcription, **no isiXhosa transcription, TTS not shipped, and no published accuracy figures anywhere.**
- **No African telco or bank has a verified production voice AI in an indigenous South African language.** MTN's flagship "AI for Mobile Money" is a **text chatbot from May 2019, in Ivory Coast.**

> **The read:** the raw material to build South African voice AI became free and legal to use *this year*, and nobody has shipped it. That is a window, and windows close.

### FACT 2 · The phone is the least reliable object in a South African's life

- **16% of SA mobile connections are feature phones.** ~**10% of connections are still 2G/3G.**
- **MTN South Africa: 29% of the devices it sold in 2023/24 were 2G feature phones.** Pepkor moves ~**5 million 2G devices a year**, and 7 in 10 phones sold in SA go through Pepkor.
- **2G will outlast 3G.** Vodacom will decommission 3G *first* and has published no timeline; MTN has **no fixed national shutdown date** and explicitly plans to **retain a 2G layer**. *(Correction to earlier notes: neither operator has announced a sunset date. Only the government's 31 Dec 2027 target exists, and ICASA is already hedging.)*
- **South Africans buy cheap feature phones specifically as anti-theft secondary devices.** Crime is shaping the device market.
- 85.6% of households have internet access; only **17.4% have it fixed at home.** Mobile-only country.
- **The data poverty premium, quantified:** R17.80/GB if you can pay R89 for 5GB up front — **R62.25/GB if you can only afford 4GB.** The poor pay **3.5× more per gigabyte.**

### FACT 3 · Theft is now a *financial* crime, and it is vertical

This is the emotional core, and every person in that room has lived it or watched a family member live it.

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| **Digital banking crime losses** | R1.09bn | R1.86bn | **R2.4bn (+29.2%)** |

- **Banking app fraud is 97,555 cases — 88.6% of all banking crime cases** and 70.5% of claim value. Average loss per case: **R17,400.**
- Physical bank robberies in 2025: **2 incidents, R630,000 total.** Digital: **R2.4 billion.** A ratio of roughly **3,800 : 1.** *Criminals stopped robbing banks and started robbing phones.*
- **Express kidnapping — abduct someone just long enough to force transfers — is up 264% since 2014/15**, to 17,061 incidents; roughly **53 per day**. **Nearly 80% of Gauteng kidnappings are linked to armed robberies.** SABRIC: *"detaining individuals just long enough to coerce them into draining their accounts."*
- **189 phones reported stolen per day** (a floor — only ~31% of victims report, and only 29% of stolen phones are blacklisted).
- **SIM swap is 43% of all African mobile money fraud**, and **~90% of SIM swaps happen without the victim's awareness.**

> **The read:** the single most painful, fastest-growing, most universally-felt money problem in South Africa is *"they took my phone and emptied my account."* Nobody has built the defence.

### FACT 4 · Voice biometrics is a trap — and knowing that is worth points

- Speaker verification tuned to a 0.01% false-accept rate was **bypassed 82.7% of the time** by open-source voice cloning trained on **10–30 minutes of scraped audio.**
- Anti-spoofing detectors degrade **30×** out of domain (0.83% → 24.84% EER). They memorise synthesis artefacts, not invariant features.
- Peer-reviewed conclusion: **"voiceprint authentication alone is unlikely to provide reliable protection."** NY DFS (2024) tells banks to combine cryptographic *and* biometric factors.

> **The read:** several teams will pitch "log in with your voice" and be destroyed by one informed question. Naming this problem and designing around it is free credibility. **Voice is the interface. It is not the lock.**

### FACT 5 · Offline payments are buildable — and honesty about their limits is the differentiator

- **Android HCE gives device-to-device NFC with no network and no secure element.** Budget ~1 KB in ~300 ms. (Screen-off restriction on Android 9 and below.)
- The **US Federal Reserve published the canonical design in December 2025**: single-use signing keys deleted at the moment of use ("SignOnce"), plus **token ancestry chains** checked at reconciliation. There is a **working open-source Kotlin prototype** of the offline-euro equivalent.
- Every real deployment bounds the risk rather than eliminating it: **e-CNY ≈24h validity and ~10 offline hops before forced resync**; RBI **₹1,000 per transaction / ₹5,000 cumulative**; UPI Lite X **4-day merchant settlement deadline**.
- **Offline double-spend cannot be prevented in software. It can only be bounded and detected later.** Saying that out loud, with a stated risk budget, is what separates an engineer from a hackathon demo.
- **MTN is already doing a hardware version of this**: VeryPay NFC offline wearables and cards linked to mobile money — **MTN Uganda launched Q4 2024**, alongside Orange Senegal and Zamtel. Scale is pilot-tiny (6,000 students in Uganda). **81% of mobile money services offer USSD for merchant payments; fewer than 13% offer NFC.**
- **USSD is not offline.** It is session-based and needs a live radio link. 182 characters, no session state in the handset.

### FACT 6 · MTN just watched its own super app die

- **Ayoba was pulled from the app stores on 20 March 2026.** It peaked at 35 million MAU and lost on retention against WhatsApp; growth had been bought with free-data incentives that never converted to engagement.
- MTN is consolidating into a single "unified digital platform." Digital Services grew 15% in 2025; **fintech grew 24.9% on $500bn of transaction value.** That is where the money and the attention are going.
- MTN's 2026 AI posture is **infrastructure and partnerships — Huawei MoU, a Technology Innovation Lab in South Africa, AI data centres, a Microsoft 365 Copilot licensing deal. No shipped consumer AI product.**

> **The read:** the judges have *just lived through* a failure caused by the absence of a real reason to open an app. They will be hypersensitive to "why would anyone use this weekly" — and unusually receptive to anything that visibly proves engagement. Also: MTN has publicly committed to AI and has nothing consumer-facing to show. You can hand them that.

### FACT 7 · South Africa's problem is usage, not access — and the maths to fix it exists

- **84% of SA adults hold a bank account.** Only 2% are fully financially excluded.
- **~14 million adults practise "mailbox banking"** — the account exists only to receive money and immediately withdraw it. **76% of grant recipients withdraw their entire benefit on receipt. 71% of adults primarily use cash for food and groceries.**
- **26.5 million SASSA grant beneficiaries**, R292.8bn a year.
- Unemployment **32.7%**, youth **45.8%**. **33.5% of all employment is informal — and 50.5% of employed 15–24-year-olds.** One in three workers has no payslip.
- **Phone-usage data predicts loan repayment better than credit bureaux do** (AUC 0.71–0.77 vs 0.51–0.57 — the bureau is barely better than a coin flip for this population). The top predictor is **periodicity of usage** — the *regularity* of spend, a proxy for income regularity. Then the *slope*.
- **There is no peer-reviewed evidence on AI credit scoring in African mobile money contexts.** And a documented fairness risk: models trained on high-activity users (urban, male) systematically undervalue rural patterns.

---

# PART 2 — THE CORE INVERSION

Every fintech in Africa builds **for the phone.**

In South Africa the phone is the weakest link in the chain. It gets stolen — and now you get kidnapped so they can make you unlock it. It runs out of data, and if you're poor you pay 3.5× per gigabyte. One in six connections can't run an app at all. And it cannot understand 29 million people when they speak.

> **Put the money intelligence in the NETWORK, not in the phone. Then the phone becomes optional.**

**MTN is the only organisation in South Africa that can do this.** You have to *own the network* to live inside it. Capitec cannot put an agent on the GSM voice channel of a R149 Nokia. Shop2Shop cannot. OPay, TymeBank, Yoco cannot. This is not a feature advantage — it is a structural one, and it is exactly the "Only-MTN" test at maximum strength.

---

# PART 3 — THE FLAGSHIP

## 🚀 UMOYA — *the money that answers when you call*

> **isiZulu / isiXhosa:** breath · air · wind · spirit. It is the voice. It is also, literally, the thing in the air — the network.
> **Alternative name:** **NOMA** — isiZulu for *"even if."* Even if your phone is gone. Even if there's no data. Even if there's no network. Even if you don't read. *(Naming is the team's call — see Open Decisions.)*

### The one sentence

**An AI money agent that lives on MTN's network instead of on your phone — so it works on a R149 Nokia, in isiZulu, with no data, with no network, and it survives your phone being stolen at gunpoint.**

### Five faces, one agent, one identity

The mini app is *one surface*, not the product. The product is the agent behind all of them.

| Surface | Reaches | Built on |
|---|---|---|
| **Voice call** | Anyone with any phone. No app, no data, no literacy. Speak any SA language, or mix them. | GSM voice → ASR fine-tuned on Swivuriso → intent → TTS |
| **USSD** | Feature phones, zero data, inside the menu people already open | **Interact / Channel as a Service** — the most powerful API MTN ships and nobody uses |
| **Mini app (PWA)** | Smartphone users — the rich surface, and the hackathon deliverable | MoMo Mini App PWA spec |
| **SMS** | Anyone, for confirmations and alerts | **Notify** |
| **Offline NFC tap** | No network at all | Android HCE + signed value tokens |

Same agent. Same money. Same identity. **The phone is a terminal, not the wallet.**

---

### The five capabilities

#### ① SPEAK — the language moat

Fine-tune ASR on **Swivuriso** (free, CC BY 4.0, 3,016 hours, 7 SA languages) and handle **code-switching**, which is how South Africans actually talk and which no frontier vendor benchmarks.

**The demo moment:** a judge says *"Ngicela ukuthumela u-two hundred rand ku-mama"* into a feature phone. It works. Then you show Google Cloud getting isiXhosa wrong **56.71%** of the time on the same class of input, on a slide, with the citation.

**Why this cannot be copied quickly:** the corpus exists, but nobody has productised it, and Google's 2026 African-language investment skipped South Africa entirely.

#### ② SURVIVE — theft and duress defence

This is the emotional heart and, I think, the single strongest idea in the whole project.

- **Phone stolen?** Borrow any phone. Call. You are recognised. Everything freezes. Your identity was never the device.
- **The duress PIN.** Express kidnapping is up **264%** and running at **~53 a day**; the entire crime is *forcing you to transfer*. So: enter your real PIN and you transact normally. **Enter your duress PIN and the interface shows a plausible reduced balance, executes a transfer that looks completely real and completes — and moves nothing.** Silently: MTN is alerted, trusted contacts are alerted, tower location is logged. **The attacker gets nothing and never knows.** No South African bank does this.
- **Time-locked high-value transfers** to new recipients, cancellable from any phone.
- **Social recovery**: your account is recoverable through the people you have actually transacted with over years — a graph MTN already holds and monetises not at all. This is what kills SIM swap structurally, because the SIM stops being the identity.
- **Security design, stated honestly:** voice is the *interface*, never the *lock*. Auth is PIN + behavioural signals + device/SIM/tower state + graph, with voice as one weak signal in a risk engine and an explicit anti-spoofing layer. **We will say in the pitch that voice cloning bypasses speaker verification 82.7% of the time and that anyone pitching voiceprint-as-login is wrong.**

#### ③ ACT — the mandate layer

MTN shipped the **Get Consent** API — PIN-authenticated consent over USSD — and nobody built on it. That is a **signed mandate primitive**, which is precisely what 2026's agentic payment protocols are built around.

Map Get Consent onto **AP2's Intent Mandate / Cart Mandate** structure and MoMo becomes **the first African wallet with an agent-mandate layer** — built on rails MTN already owns.

- *"Gcina imali yebhasi"* — ring-fence my taxi fare for the month.
- *"Buy R100 of electricity when I drop below 20 units, twice a month maximum."*
- *"Send gogo R200 on the 1st."*

**Trust design, grounded in evidence:** Visa's own research says **60% of consumers will not let an AI spend *any* amount without approval.** So every autonomous action is a *proposal* until you approve it — by voice, in your language, in one word. Scoped, capped, revocable, PIN-signed.

#### ④ FORESEE — prediction, pointed at the user instead of at a lender

Phone-usage **periodicity** predicts repayment better than a credit bureau does (**AUC 0.71–0.77 vs 0.51–0.57**). Every lender in this market wants that signal to *price* you.

**Turn it around and give it to the person.**

> *"Your income has been irregular for three weeks. At this rate you run out of taxi fare on the 23rd — four days before payday. Shall I ring-fence R180 now?"*

Plus the arbitrages nobody surfaces: the **data poverty premium** (R62.25/GB vs R17.80/GB — buy the bigger bundle, or group-buy it), the **electricity advance trap** (~R5 fee on a R20–50 advance, compounding to R250–350 a year), and prepaid electricity purchase timing.

**Why this framing is strategically correct:** there is no lending track in 2026. This is the credit-scoring maths handed to the customer as protection rather than sold to a lender as pricing. It is also, straightforwardly, the right thing to do — and it answers the documented fairness problem, since the model serves the person it scores.

#### ⑤ ENDURE — offline

Android HCE + Ed25519-signed value tokens with **ancestry chains**, following the Federal Reserve's December 2025 framework, with a stated risk budget copied from what actually works in production: **~R500 offline float, 24-hour validity, ~10 hops before forced resync.**

And the line that wins engineering respect: **"Offline double-spend cannot be prevented in software. It can only be bounded and detected. Here is our risk budget and here is why it's the right one."**

*(Context: MTN already ships hardware NFC offline via VeryPay in Uganda. You would be showing them the software version, with no wearable to distribute.)*

---

### Scale — "flexible depending on market"

The architecture does not change. **You swap the language model.**

| Market | Languages | Corpus available |
|---|---|---|
| South Africa | isiZulu, isiXhosa, Sesotho, Setswana, Xitsonga, isiNdebele, Tshivenda | **Swivuriso** — 3,016 hrs, CC BY 4.0 |
| Nigeria | Hausa, Yoruba, Igbo | WAXAL — open, commercial licence |
| Uganda | Luganda, Acholi, Soga | WAXAL |
| Ghana | Akan, Ewe, Dagbani, Fante | WAXAL |

16 markets, one architecture. **That is the scalability story, and it is the only idea in the project where scaling is a configuration change rather than a rebuild.**

---

### Who it serves — the "macro and multiversed" test

| Person | What they get | Surface |
|---|---|---|
| Gogo, 71, rural KZN, Nokia, isiZulu, doesn't read | Speaks to her money. Grant arrives, she ring-fences it, she is warned before it runs out. | Voice call |
| Student, Braamfontein, smartphone, code-switches constantly | Full agent, data-cost optimisation, group-buys bundles with friends | Mini app |
| Taxi driver, carries cash, gets robbed | Duress PIN, instant freeze from any phone, provable income record | Voice + USSD |
| Spaza owner, 2G phone, no data budget | Offline tap payments, stock float forecasting | USSD + NFC |
| Domestic worker paid irregularly | Income-volatility warning before the shortfall, not after | Voice + SMS |
| Anyone, anywhere, phone just stolen | Borrow a stranger's phone. Call. Freeze. | Voice call |

**Every demographic. Every device. Every language. Every connectivity state.**

---

### The demo — the thing they still remember at lunch

1. Take a judge's smartphone. **Put it in a drawer.**
2. Hand them a **R149 Nokia 2G feature phone.**
3. They dial. They speak **isiZulu**. Balance, transfer, set a rule. It works.
4. *"Now you've just been hijacked. They have your phone and they have your PIN."* They enter the **duress PIN**. On screen, a transfer completes — realistically, convincingly. **Nothing moved.** Behind you, on the big screen, the silent alert and the tower location.
5. **Turn off the wifi. Turn off the data.** Tap two phones together. The payment settles.

Nobody in that room can follow that.

---

# PART 4 — BULLETPROOFING: every scenario has an answer

| Scenario | Answer |
|---|---|
| **Phone lost or stolen** | Identity lives on the network. Call from any phone, be recognised, freeze in seconds. Recovery via transaction graph, not via SIM. |
| **Forced to transfer at gunpoint** | Duress PIN → decoy balance, convincing fake completion, silent alert + tower log. Attacker leaves with nothing. |
| **No smartphone** | Voice call and USSD are first-class surfaces, not fallbacks. 16% of connections are feature phones; MTN sold 29% 2G in 2023/24. |
| **No data** | Voice and USSD consume zero data. |
| **No network at all** | Offline NFC signed tokens, capped and time-boxed, settling on reconnection. |
| **Load shedding** | *Correction: load shedding ended 16 May 2025 — 441 days clear as of 4 Aug 2026.* **Load reduction has not ended** — Eskom still cuts specific overloaded township feeders, 05:00–09:00 and 17:00–22:00, unannounced, transformer by transformer. Design answer: a voice call needs no charged smartphone and no home power, and offline tokens survive an outage entirely. **Do not claim load shedding as the problem — you will be corrected on stage. Claim load reduction, and cite it.** |
| **Doesn't speak English** | 12 official languages; English is 5th at 8.7%. Fine-tuned on Swivuriso, code-switching handled. |
| **Cannot read** | 3.8 million adults aged 20+ are classified as illiterate. Voice requires no reading. |
| **Voice cloning / deepfake attack** | Voice is never the lock. PIN + behavioural + device/tower + graph. We name the 82.7% bypass figure ourselves. |
| **SIM swap** | The SIM stops being the identity. Graph-based recovery + network-side SIM-swap signal. |
| **Offline double-spend** | Cannot be prevented, only bounded: R500 float, 24h validity, ~10 hops, ancestry-chain detection at settlement. Stated as a risk budget, not a claim of security. |
| **AI gets it wrong / hallucinates** | No autonomous spend. Every action is a proposal requiring explicit approval. 60% of consumers demand exactly this. |
| **ASR mis-hears an amount** | Read-back confirmation in the user's language before execution; amounts confirmed by digit entry on USSD where ambiguity is detected. |
| **2G voice quality degrades ASR** | **Honest risk.** AMR-NB runs 4.75–12.2 kbps and no published study tests an AI voice agent over GSM. **Prototype-test this in week one.** Cascaded STT→LLM→TTS beats speech-to-speech on narrowband telephony — build cascaded. |
| **Sandbox fails on demo day** | Simulate-success toggle, recorded video backup, both webhook and polling implemented. |
| **"Isn't this just a chatbot?"** | A chatbot needs an app, data and English. This is on the voice channel of a 2G phone in isiZulu, with a mandate layer and an offline rail. |
| **"Can MTN actually ship this?"** | Every piece is an API MTN already publishes (Interact, Get Consent, Identify, Notify, Pay, Get Paid) plus an open corpus and open models. Nothing here requires a partnership MTN doesn't have. |
| **Regulatory / POPIA** | Identify API means you never store identity. Voice is processed, not retained. Mandates are PIN-signed and revocable — auditable by construction. |
| **Fairness / bias** | Documented risk that models trained on urban, male, high-activity users undervalue rural patterns. Mitigation: the model serves the user, never prices them; stratified evaluation reported openly. |

---

# PART 5 — THE ALTERNATIVE MOONSHOTS

Same ambition tier. Real choice, not consolation prizes.

### 🅑 ISIBANI — *the account that cannot be robbed*
**The narrow, sharpest version of Umoya's best idea.** Coerced-transfer defence as **infrastructure**, offered to every other mini app and every bank as a service. Duress PIN, decoy balance, time-locked transfers, silent alerting, graph recovery, SIM-swap signal.
**Numbers:** R2.4bn digital banking crime vs R630k physical bank robbery. 88.6% of all cases are app fraud. Express kidnapping +264%.
**Only-MTN:** ★★★★★ — needs SIM state and tower data. No bank can build it.
**Weakness:** narrower story; less "wow" and more "obviously necessary." Which may be exactly right.

### 🅒 ISISEKELO — *the income truth engine*
**5.7 million informally employed South Africans; 50.5% of employed 15–24-year-olds. None can prove what they earn** — and the credit bureau is barely better than a coin flip for them (AUC 0.51–0.57) while their phone data hits 0.71–0.77.
Build a **portable, verifiable earnings credential the worker owns and grants access to** — not a score sold to lenders. Graph ML + Identify API.
**Only-MTN:** ★★★★☆ · **Weakness:** the artefact is a PDF-shaped thing; harder to demo viscerally.

### 🅓 THE POVERTY PREMIUM KILLER
Pure data science on documented arbitrage. **Poor people pay 3.5× per GB** (R62.25 vs R17.80) because they can't front R89. Electricity advances cost ~R5 on R20–50 and compound to R250–350/yr. Prepaid tariff blocks punish small purchases.
**Forecast consumption, group-buy bundles, time every micro-purchase optimally.** "We put R400 a year back in your pocket" is the least arguable demo there is — and MTN is the merchant on the data half.
**Only-MTN:** ★★★☆☆ · **Weakness:** feels like a feature, not a company. Strongest as a *module of Umoya*.

### 🅔 THE MESH — *money that moves with no network at all*
Go all-in on resilience. Signed value notes hopping phone-to-phone over NFC and BLE, settling whenever any holder next touches a tower. Fed-framework ancestry chains, capped float.
**Most technically impressive thing on this board.** Fewer than 13% of mobile money services offer NFC at all.
**Only-MTN:** ★★☆☆☆ · **Weakness:** hardest to make anyone *feel*. Best as Umoya's fifth surface rather than a standalone entry.

### 🅕 THE GRANT RAIL
**26.5 million SASSA beneficiaries. R292.8bn a year. 76% withdraw the entire grant the moment it lands.** That is the largest single cash-conversion event in the South African economy and it happens monthly, on a schedule, to a known list of people.
Make the balance *stay*: legible, spendable, ring-fenced, warned.
**Only-MTN:** ★★☆☆☆ · **Weakness:** government dependency, and grant distribution is politically contested ground.

---

# PART 6 — SCORING AT THE MOONSHOT TIER

Rated against the official five criteria plus the project's own three. Max 40.

| Concept | Innov | Relev | Feas | Tech | Pitch | Launch | Weekly | OnlyMTN | **TOT** |
|---|---|---|---|---|---|---|---|---|---|
| **UMOYA** | 5 | 5 | 3 | 5 | 5 | 5 | 5 | **5** | **38** |
| **ISIBANI** | 5 | 5 | 4 | 4 | 5 | 5 | 3 | **5** | **36** |
| **ISISEKELO** | 4 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | **32** |
| **POVERTY PREMIUM** | 4 | 4 | 5 | 4 | 5 | 4 | 4 | 3 | **33** |
| **THE MESH** | 5 | 4 | 3 | 5 | 3 | 3 | 2 | 2 | **27** |
| **GRANT RAIL** | 3 | 5 | 3 | 3 | 4 | 4 | 3 | 2 | **27** |
| *SETTLE (previous pick)* | *3* | *5* | *5* | *3* | *4* | *5* | *4* | *3* | *32* |

**Umoya's only weak score is feasibility — and that is the honest one.** It is the most ambitious thing in the project. Mitigation is in Part 7.

---

# PART 7 — IS UMOYA ACTUALLY BUILDABLE IN 2.5 WEEKS?

Honest answer: **not all of it. And it doesn't need to be.**

**Build for real (the spine):**
- The mini app PWA — full agent, all five capabilities visible
- Voice pipeline: cascaded ASR → intent → TTS, fine-tuned on Swivuriso for **two languages** (isiZulu + one more). Not seven.
- Duress PIN and decoy balance — pure application logic, high drama, near-zero technical risk
- Get Consent mandate flow against the sandbox
- Offline NFC tap between two Android phones via HCE
- The forecasting model on synthetic + sandbox transaction data

**Simulate honestly, and say so on the slide:**
- SIM-swap and tower signals — MTN doesn't expose them. **Pitch the data contract as the ask.** That reframes a gap as a partnership proposal, which is the launch-partner posture.
- USSD via Interact — mock the menu unless MTN provisions it on the day
- Full 7-language coverage — show two working, show the corpus, show the fine-tuning curve

**Highest technical risk, test in week one:** the voice agent over an actual GSM call. No published study covers it. AMR-NB at 4.75–12.2 kbps will hurt ASR. **If it fails, the product still stands on USSD + SMS + PWA + offline — but you need to know by day three, not day fifteen.**

---

# PART 8 — OPEN DECISIONS

1. **Track.** Umoya spans all three. **Everyday Essentials** is the honest home — but see the open question below.
2. **Prize structure — ask the organisers this week.** Is judging *per track* or *overall*? If per track, the emptiest track is straightforward arbitrage and this decision changes completely. Nobody has asked.
3. **The pre-building question** — still unanswered since Session 1. Now urgent.
4. **Name.** UMOYA (breath/spirit/the thing in the air) vs NOMA ("even if") vs something else. Team name still needs the `South Africa-XXX` format.
5. **Scope discipline.** Umoya's failure mode is doing all five capabilities at 60%. Which two carry the demo? *(Recommendation: SPEAK and SURVIVE. Foresee and Endure are the third act.)*
6. **Is the duress PIN the whole entry?** ISIBANI alone is more focused, more feasible, and possibly a better hackathon project. Umoya is the better *company*.

---

# PART 9 — WHAT MAKES THIS DIFFERENT FROM THE 33

| The 33 | The moonshots |
|---|---|
| A screen that moves money | An agent that lives in the network |
| Assumes a smartphone | Works on a R149 Nokia |
| Assumes data | Zero-data surfaces are first-class |
| Assumes a network | Offline signed value |
| Assumes English | Assumes isiZulu, and code-switching |
| Dies when the phone is stolen | Designed for the moment the phone is stolen |
| Uses Get Paid and stops | Uses Interact, Get Consent and Identify — the three sleepers |
| A product | A primitive other mini apps build on |
| Ships in South Africa | Ships in 16 markets by swapping a model |
| Competes with Shop2Shop | Cannot be built by anyone who doesn't own the SIM |

---

*Sources for every figure in this document: `../INFO_LOG.md`, Session 3.*
