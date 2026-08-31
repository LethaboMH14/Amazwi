# VERIFICATION STATUS — what is solid, what is shaky, what must NOT be said
**Created:** 2026-08-15 · Session 3 · Compiled from four parallel research sweeps

> **Read this before the pitch.** `INFO_LOG.md` gives you the facts and their sources. This file gives you the *confidence level*, and — more importantly — the claims that will get you publicly corrected if you make them.
>
> The single fastest way to lose a room of Johannesburg fintech judges is to state something they know is out of date. Three of the items in §1 are exactly that.

---

# 1. ⛔ DO NOT SAY THESE — you will be corrected on stage

### 1.1 "Load shedding is a problem South Africans face"
**Load shedding ENDED on 16 May 2025.** As at 4 August 2026 South Africa had gone **441 consecutive days without it**. FY2025/26 saw 26 hours of load shedding in the entire financial year. Peak daily EAF hit 82.04% in July 2026, the highest since 2017, with zero diesel burned for two consecutive weeks.

**✅ Say this instead:** *load reduction.* It has **not** ended. Eskom still curtails specific overloaded township transformers and feeders in two daily windows — **05:00–09:00 and 17:00–22:00** — unannounced, transformer by transformer. 651,828 customers were removed from load reduction schedules by late June 2026; the remaining number is unpublished. Nationwide eradication is targeted for 2027.
*Source: [TechFinancials, 4 Aug 2026](https://techfinancials.co.za/2026/08/04/eskom-reports-441-days-without-load-shedding/) · [EnergyBee, 29 Jun 2026](https://energybee.co.za/news/load-reduction-schedule-south-africa-2026)*

### 1.2 "MTN and Vodacom have announced 2G/3G sunset dates"
**They have not.** Only the government's DCDT gazette exists, targeting total shutdown by **31 December 2027**, and ICASA is already hedging on it.
- **MTN SA:** no fixed national date. Phased, area-by-area. Explicitly plans to **retain a limited 2G layer** for legacy devices.
- **Vodacom:** has not commenced 3G sunsetting and has published no timeline. Will decommission **3G before 2G**.

**✅ The defensible position:** *2G will outlast 3G in South Africa, and 2G is not going away in practice by 2027.*
⚠️ DataCenterDynamics ran a headline "MTN to retire 3G in South Africa by end of 2026." **This is contradicted by MTN's own June 2026 statement. Do not cite it.**
*Source: [MyBroadband, 13 Jun 2026](https://mybroadband.co.za/news/cellular/653722-mtn-switching-off-3g-in-parts-of-south-africa.html) · [TechCentral, 4 May 2026](https://techcentral.co.za/why-2g-will-outlast-3g-in-south-africa/280940/)*

### 1.3 "MTN has never done AI for Mobile Money"
MTN launched what it called **Africa's first AI service for Mobile Money in May 2019** — a text chatbot, in Ivory Coast, on WhatsApp/Messenger/SMS.

**✅ Say this instead:** *MTN's flagship AI-for-payments product is a seven-year-old English/French **text** chatbot, and its 2026 AI announcements are infrastructure and a Microsoft 365 Copilot licensing deal. There is no shipped consumer AI product, and nothing in any indigenous South African language.* That framing is accurate, checkable, and much stronger.
*Source: [MTN Group, May 2019](https://www.mtn.com/mtn-group-launches-africas-first-artificial-intelligence-service-for-mobile-money/)*

### 1.4 "South Africa's minibus taxi network has never been mapped"
It has. **WhereIsMyTransport** ran large-scale survey mapping, and open-data projects and consumer apps like **TeksiMap** exist.

**✅ Say this instead:** *every mapping effort to date is a **snapshot that decays**. What has never existed is a **live** feed — and payments produce one continuously, at zero marginal cost, as exhaust.* Still remarkable, and now unassailable.
*Source: [Bizcommunity](https://www.bizcommunity.com/Article/196/709/168626.html) · [TeksiMap](https://www.teksimap.co.za/)*

### 1.5 "USSD works offline"
It does not. USSD is **session-oriented and requires a live radio link.** GSM 02.90 places no session state in the handset — all state lives in your gateway.
**✅ Say:** *USSD needs no **data**.* That is the accurate and still-powerful claim.

### 1.6 "Our offline payments prevent double-spending"
They cannot. **Offline double-spend cannot be prevented in software — only bounded and detected later.** The US Federal Reserve's own framework is explicit that the secure element is the entire trust anchor, and Android provides no API to reach one.
**✅ Say:** *here is our risk budget — R500 float, 24h validity, ~10 hops, ancestry-chain detection at settlement* — and note that e-CNY, UPI Lite X and the digital euro all do exactly this. Being the team that says it out loud is a strength.

### 1.7 "Voice biometrics secures the wallet"
Do not build or claim this. Open-source cloning on **10–30 minutes of scraped audio bypasses speaker verification 82.7% of the time** against a system tuned to 0.01% FAR, and anti-spoofing degrades **~30× out of domain** (0.83% → 24.84% EER). NY DFS advises combining cryptographic *and* biometric factors.
**✅ Say:** *voice is the interface, never the lock.*

---

# 2. ⚠️ UNVERIFIED — do not put these on a slide without checking

| Claim | Status |
|---|---|
| **Lelapa AI funding beyond $2.5M** | Crunchbase, PitchBook, Tracxn and CB Insights all blocked automated access. No Series A confirmed. Treat $2.5M as a floor. |
| **Any Vulavula WER/CER figure** | Lelapa publishes **none**. The "94.7% / 92.1% confidence" figures on their homepage are **UI mockups**, not benchmarks. Do not cite as accuracy. |
| **A Lelapa–Microsoft partnership** | One outlet claims March 2025; Microsoft's own blog features Lelapa as a case study and states no partnership. **Do not claim it.** |
| **Simba-TTS quality (MOS)** | No MOS or intelligibility scores published. Run your own listening test. |
| **On-device LLM performance on low-end Android** | Every published figure is for flagship hardware. Assume server-side inference; treat on-device as aspirational. |
| **AI voice agent over 2G/GSM** | **No published study exists.** AMR-NB runs 4.75–12.2 kbps vs G.711's 64 kbps and strips the cues distinguishing similar phonemes. This is a genuine engineering risk — prototype-test it, do not assume it. |
| **On-device meter/receipt OCR accuracy** | No benchmark published anywhere. Measure it yourself if you need it. |
| **AP2 mandate revocation semantics** | Published material covers issuance and signing only. Read the spec at ap2-protocol.org directly before claiming revocation. |
| **"All ACP checkout deployments stopped in March 2026"** | Single non-authoritative source making a strong negative claim. High-impact if true — verify before using. |
| **HSBC Voice ID current figures** | Sources conflict (£981m vs ~£400m) and both appear pre-2026. |
| **Voice biometrics at any named African bank** | Found none. Absence of evidence, not evidence of absence. |
| **Eskom 2026/27 Homelight inclining-block thresholds** | Could not obtain. The FY2026 restructuring may have flattened the classic residential IBT. Verify against Eskom's Schedule of Standard Prices before building any tariff model. |
| **SA prepaid-meter household share** | No authoritative national figure found. Closest proxy: 90.6% of households connected to mains (GHS 2025), which does **not** break out prepaid. Do not invent a share. |
| **SA-specific coverage/usage gap** | Only regional (SSA) data verified. The ~20pp SA gap is arithmetic across two sources, not a published figure — label it an estimate. |
| **"SA telecom fraud = $320.5m/yr, 60% SIM swap"** | From a **radio interview** with a former Vodacom CRO, not an official statistic. Do not cite. |
| **Cignifi and Juvo current operating status** | Only company-database entries found. Do not name them as current players. |
| **Indigenius performance claims** | "Sub-200ms latency", "60–75% call deflection", "NPS +28", "68% prefer mother tongue" — all vendor marketing, no independent source. |
| **34 million SA feature-phone users** | This is **arithmetic** (117.3m subs − 83.04m smartphones), and ICASA counts SIMs not people. SA has 196% mobile penetration. **Do not present it as 34 million people.** Use the GSMA figure: 16% of connections. |
| **Q4 2025/26 SAPS robbery line items** | SAPS PDF blocked by an invalid TLS certificate. Get directly from SAPS if needed. |

---

# 3. ✅ ROCK SOLID — lead with these

These are primary-source, current, and checkable. They are the spine of all three pitches.

| Claim | Source quality |
|---|---|
| **Google Cloud Speech-to-Text: 56.71% WER on isiXhosa** conversational speech; Meta MMS 92.50%; human 9.6% | Peer-reviewed, NAACL CL4Health 2025 |
| **Foundation ASR models exceed 100% WER zero-shot** on all six Southern Bantu languages | arXiv, Marivate et al. |
| **Swivuriso: 3,016 hours, 7 SA languages, CC BY 4.0**, Setswana 223%→13% WER on fine-tuning | arXiv + Zenodo + DSFSI, downloadable today |
| **Google WAXAL (Feb 2026): 27 African languages, zero South African** | TechCabal, with the language list published |
| **Code-switching costs monolingual ASR 30–50% WER**; June 2026 frontier benchmark tested zero African languages | arXiv survey + ServiceNow AI benchmark |
| **SABRIC 2025: R2.4bn digital banking crime (+29.2%), 97,555 banking-app fraud cases = 88.6%, avg R17,400; 2 bank robberies yielding R630,000** | SABRIC / BASA, published Aug 2026 |
| **Kidnapping +264% since 2014/15 to 17,061; ~53/day; 44% hijacking-linked, 4% ransom; ~80% of Gauteng kidnappings tied to armed robbery** | ISS via Daily Maverick + Parliament research |
| **Voice cloning bypasses speaker verification 82.7%** on 10–30 min of audio; anti-spoofing degrades 30× out of domain | arXiv, peer-reviewed |
| **Ayoba removed from app stores 20 March 2026**, peaked 35m MAU | TechCabal + Techpoint |
| **MTN + Ant International, June 2026** — super app and mini app platform, Nigeria Q3 2026 | MTN Group press release |
| **Android HCE works with no network and no secure element**; ~1KB in ~300ms; no SE API on stock Android | Android developer documentation |
| **US Federal Reserve offline payments framework (Dec 2025)** — SignOnce keys + ancestry chains | Federal Reserve FEDS paper |
| **e-CNY ~24h validity, ~10 offline hops; RBI ₹1,000/₹5,000; UPI Lite X 4-day settlement** | Regulator and operator sources |
| **VeryPay NFC offline — MTN Uganda launched Q4 2024**; 81% of mobile money services offer USSD, <13% offer NFC | GSMA Mobile for Development |
| **Phone-usage data predicts repayment at AUC 0.71–0.77 vs 0.51–0.57 for a credit bureau**; periodicity is the top predictor | Björkegren & Grissen, peer-reviewed |
| **Visa: 60% of consumers would not allow AI to spend any amount without approval** | Visa research via TechInformed |
| **Google AP2 (16 Sep 2025): Intent Mandate + Cart Mandate as signed Verifiable Credentials**, 60+ partners | Google Cloud + ap2-protocol.org |
| **QLFS Q1 2026: unemployment 32.7%, youth 45.8% (4.7m); informal employment 33.5%, 50.5% of employed 15–24s** | StatsSA |
| **12 official languages; English 5th at 8.7%; ~29m adults not proficient; 9.7% adult illiteracy (3.8m)** | StatsSA Census 2022 + DHET + Eighty20/MAPS |
| **~14m adults practise "mailbox banking"; 76% of grant recipients withdraw everything on receipt; 71% use cash for groceries; 84% banked** | FinScope 2023 via CFI + FSCA |
| **16% of SA connections are feature phones; MTN SA sold 29% 2G devices in 2023/24; cheapest smartphone R399** | GSMA + TechCentral + ICASA |
| **Data poverty premium: R17.80/GB at 5GB (R89 upfront) vs R62.25/GB at 4GB** | MyBroadband, July 2026 retail pricing |
| **SIM swap = 43% of African mobile money fraud; ~90% occur without victim awareness** | Technext24 + Efani |

---

# 4. 🔴 STILL OPEN — chase these this week

1. **May three members of one team each submit in a different track under a shared team name?** Everything about the three-entry strategy depends on this. Ask in writing.
2. **Is judging per-track or overall?** Never asked. Changes track strategy entirely.
3. **Pre-building clarification** — open since Session 1. The T&Cs prohibit pre-existing projects; the form asks for a repo URL.
4. **Which MoMo APIs are enabled in the SA sandbox for the event**, and whether day-of credentials are provided.
5. **Will MTN expose any SIM-swap, tower or network-graph signal — even simulated?** Umoya and Hamba both depend on the answer. Ask the MoMo developer community now.
6. **Native-speaker sign-off on the *moya* claim.** Nguni forms are secure; the Sotho-Tswana forms (Sesotho, Setswana, Sepedi *moya/mowa*) are confident but not confirmed from a primary lexicographic source. Get a Sesotho and a Setswana speaker to confirm before it goes on a slide.
7. **Does an AI voice agent actually work over a GSM/2G call?** No published study. Prototype-test by day three.
8. **Retrieve WER figures from "Code-switched ASR in five South African languages"** (*Speech Communication*, 2021) — paywalled, and the most on-point SA result in existence.
9. **Confirm Eskom's 2026/27 Homelight inclining-block thresholds** from the Schedule of Standard Prices.
10. **IP clause** — the T&C text contains both "royalty free, sub-licensable" and "exclusive". Clarify on the day.

---

# 5. HOW TO HANDLE A CHALLENGE ON STAGE

If a judge disputes a number:

- **Name the source and the date.** "SABRIC's 2025 Annual Banking Crime Statistics, published August 2026." Not "we read that somewhere."
- **If it's in §2 above, concede immediately and cleanly.** "That one we couldn't verify — we flagged it internally as unconfirmed." That answer *builds* credibility. Bluffing destroys it.
- **If it's in §1, you already said the right thing** — because you used the corrected version.
- **Never argue a number you can't source.** Move to one you can.

Every figure in all three entries traces to `INFO_LOG.md`. Each teammate should be able to name the source for every number in their own submission before demo day. If they can't, cut the number.
