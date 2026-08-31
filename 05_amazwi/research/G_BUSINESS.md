# AMAZWI Commercial Evidence Base — Who Pays, How Much, How MTN Makes Money

Compiled 2026-08-31 for the AMAZWI business case (MTN MoMo Mini App — paid, validated African-language voice contributions → consented speech corpus + derived models/APIs).

Legend: every claim carries a source URL and date. Where a number could not be found, this is stated explicitly as **NO PUBLISHED FIGURE FOUND**. Explicit estimates built from labelled assumptions are marked **ESTIMATE** with the arithmetic shown in full — never silently blended with sourced figures. FX used throughout: **USD/ZAR ≈ 16.15** (28 Aug 2026), tradingeconomics.com / exchangerates.org.uk, https://www.exchangerates.org.uk/news/46955/2026-08-21-south-african-rand-outlook-the-usd-zar-levels-traders-are-watching-next.html (accessed 2026-08-31).

---

## 1. SPEECH DATA PRICING — what transcribed/labelled speech actually sells for

| Vendor / catalogue | Price point | Source | Date |
|---|---|---|---|
| **Defined.ai** Data Access Plan (DAP) | Premium: 625 hrs for €100,000; Ultimate: 1,565 hrs for €250,000; Elite: 3,125 hrs for €500,000 — all three tiers work out to **≈€160/hour** (~$175/hr at typical EUR/USD) | https://defined.ai/press-room/defined-ai-launches-data-access-plan-dap-allowing-access-to-speech-datasets-at-affordable-prices | accessed 2026-08-31 |
| **Shaip** | Speech data with transcription typically **$5–30 per audio hour** (general guide, not African-language-specific) | https://www.shaip.com/blog/ai-data-collection-buyers-guide/ | accessed 2026-08-31 |
| **Speechocean** | No public price list; speechocean762 corpus free for academic use, "charged for commercial use" (amount undisclosed); ~500 commercial + ~250 research corpora across 110+ languages/dialects | https://www.openslr.org/101/ ; http://en.speechocean.com/datacenter/details/1337.html | accessed 2026-08-31 |
| **ELRA/ELDA catalogue** | Per-corpus "Unit Price" fields exist in the online catalogue but actual prices are not rendered in public search/browse pages — **NO PUBLISHED FIGURE FOUND** for a general per-hour rate; must query catalogue.elra.info per corpus | https://catalogue.elra.info/en-us/ | accessed 2026-08-31 |
| **LDC (Linguistic Data Consortium)** | Fees are corpus-specific ("nonmember license fee" varies by corpus); no flat per-hour figure published; members get free annual releases + discounts | https://www.ldc.upenn.edu/language-resources/data/obtaining | accessed 2026-08-31 |
| **Summa Linguae** | Custom quote only, 60+ languages, no public pricing | https://datarade.ai/data-providers/summa-linguae-technologies/profile | accessed 2026-08-31 |
| **Appen** | Pricing "opaque and project-specific," no public rate card; SaaS + bespoke managed-services split; 20–40% surcharge reported for specialised (medical/legal) annotation; 165,000+ hours of audio in inventory across languages | https://www.futurebeeai.com/knowledge-hub/ai-data-provider-pricing-comparison ; https://www.appen.com/speech-and-audio-training-data | accessed 2026-08-31 |

### The scarcity premium on low-resource / African-language speech
- **Conventional (human) data collection for as-yet-unsupported languages costs "more than US$100 to 150 per hour, even in the best case"** — explicit quote, source: "Synthetic Voice Data for Automatic Speech Recognition in African Languages," https://arxiv.org/html/2507.17578 (accessed 2026-08-31). Same paper: synthetic voice data was produced "at below 1% of the cost of real data" for 2,500+ hours — i.e. real African-language speech data is treated in the literature as the expensive, scarce input synthetic data is built to avoid.
- **A $345.42/hour figure for Hausa surfaced in aggregated search summaries but could NOT be traced to a primary, quotable source** on a second verification pass (checked arxiv 2507.17578 and 2510.12781 directly — neither contains it). **Treat this figure as UNVERIFIED — do not cite it as fact.**
- **Human correction labour for predominantly-oral languages: 30 hours of human labour per hour of audio under laboratory conditions, 36 hours under field conditions** (Bambara case study) — "Cost Analysis of Human-corrected Transcription for Predominately Oral Languages," https://arxiv.org/html/2510.12781 (accessed 2026-08-31). Same paper cites US English professional transcription as a baseline: **$1.50–$3.00/audio minute = $90–$180/audio hour**, a 3–6x labour ratio versus 30-36x for a low-literacy oral language — i.e. **the "low-resource penalty" is roughly 5–10x the labour intensity of a high-resource language.**
- **African crowdsourcing platform annotator pay: $10–50/hour**, reported as "above local market rates" — search-aggregated from academic sources on African data-collection projects (accessed 2026-08-31). Individual project data point: Hausa and Yoruba annotators paid **$80 flat per completed task** in one speech-evaluation project (task duration not disclosed — cannot be converted to an hourly rate; flagged as such).
- **Professional Nigerian-language transcription (Hausa/Yoruba/Igbo/Pidgin): ~$1.50–2.00/audio minute ≈ $90–120/audio hour** — https://dyplus.com.ng/audio-transcription/ (accessed 2026-08-31).
- **Kenyan-language transcription: Ksh 5,000 (≈USD 38) per hour** paid to transcribers — search-aggregated academic source (accessed 2026-08-31), specific paper not independently re-verified; treat as **lower-confidence**.
- **African Next Voices (ANV) — the single best "real-world, ethically-compensated, at-scale" comparable**: $2.2 million Gates Foundation grant funded ~9,000 hours of speech across 18 languages in Kenya, Nigeria and South Africa over two years. **$2.2M ÷ 9,000 hrs = ≈$244/hour, all-in program cost** (this includes research overhead, fieldwork, university partners — not just contributor pay). Source: Gates Foundation Africa, https://x.com/GatesAfrica/status/1994768311985336582 (accessed 2026-08-31); corroborated by iAfrica.com and the Swivuriso paper, https://arxiv.org/html/2512.02201v1 (South African subset: 3,000 hours, 7 languages, 2,353 speakers — remuneration "stratified by language" but the exact rate is **NOT disclosed** in the paper).

**Bottom line for AMAZWI:** the market floor for low-resource speech data is **$100–150/hour** even under conventional (non-African-specific) collection; ethically-compensated African-language collection at ANV's scale runs **≈$244/hour all-in**; commercial marketplace pricing (Defined.ai) for general speech is **≈$175/hour**. Any AMAZWI cost structure that lands meaningfully below $150/hour has a real, sourced margin story.

---

## 2. AI DATA LICENSING DEALS — disclosed values and the 2025–2026 trend

| Deal | Value | Source | Date |
|---|---|---|---|
| **Reddit ↔ Google** | ~$60 million/year (Feb 2024) | CBS News, https://www.cbsnews.com/news/google-reddit-60-million-deal-ai-training/ | reported Feb 2024, accessed 2026-08-31 |
| **Reddit ↔ OpenAI** | ~$70 million/year (estimated by press, not officially disclosed by either party) | Search Engine Land, https://searchengineland.com/openai-may-pay-reddit-70m-for-licensing-deal-451882 | accessed 2026-08-31 |
| **Reddit total data-licensing revenue** | Grew 24% YoY to **$43 million** (Q2 2026); described as only ~5% of Reddit's total revenue despite the headline Google/OpenAI deal sizes | The Motley Fool, https://www.fool.com/investing/2026/08/17/reddits-data-revenue-openai-google-buyers/ | 17 Aug 2026 |
| **News Corp ↔ OpenAI** | Up to **$250 million over 5 years** (~$50M/year) — largest single publisher AI licensing deal on record; covers WSJ, Barron's, MarketWatch, NY Post + global titles | Variety, https://variety.com/2024/digital/news/news-corp-openai-licensing-deal-1236013734/ | May 2024 |
| **Shutterstock ↔ OpenAI/Meta/Google/Amazon/Apple** | Individual deal values undisclosed; CFO stated **initial Big Tech deals ranged $25–50 million each**; total AI-licensing revenue across all partners was **$104 million in 2023** | Yahoo Finance, https://finance.yahoo.com/news/shutterstock-ai-licensing-business-generated-120000890.html | accessed 2026-08-31 |
| **Stack Overflow ↔ Google** | Undisclosed (Feb 2024) | https://itmagazine.com/2024/03/01/unpacking-googles-latest-deal-with-stack-overflow-a-testament-to-ai-giants-investing-in-data/ | accessed 2026-08-31 |
| **Suno ↔ BMG** | Undisclosed sum, announced 12 Aug 2026 | Forbes, https://www.forbes.com/sites/cathyolson/2026/08/12/ai-music-generator-suno-inks-latest-music-label-licensing-deal/ | 12 Aug 2026 |
| **Suno/Udio ↔ Warner Music** | Undisclosed value; global deal + settled all past copyright litigation, Nov 2025 | Chartlex, https://www.chartlex.com/blog/business/ai-music-licensing-deals-tracker-2026 | accessed 2026-08-31 |
| **Stability AI ↔ AudioSparx** | Exclusive license, 800,000+ audio files, value undisclosed | Chartlex (as above) | accessed 2026-08-31 |

**No audio/speech-specific deal with a disclosed dollar value was found** — every named speech/audio deal (Suno-BMG, Suno-Warner, Stability-AudioSparx) has an **undisclosed value**. This is itself a data point: speech/voice/music licensing deal *terms* are systematically more opaque than text/publisher deals.

### The 2025–2026 trend
- **AI training dataset market ≈ $4 billion in 2026** — Troveo, https://www.troveo.ai/resources/ai-training-data-statistics (accessed 2026-08-31).
- **Epoch AI projection: the stock of high-quality public text data could be effectively exhausted for training between 2026 and 2032**, pushing labs toward licensing non-public data — cited via Pebblous/Troveo analysis, https://blog.pebblous.ai/report/ai-data-licensing-realtime-shift-2026/en/ (accessed 2026-08-31).
- **Structural shift in what's being bought**: in early deals (2023–24) nearly all licensing agreements included training rights; **by 2026 only about 4 in 10 deals include training rights** — the market has shifted from one-time data dumps to continuously-refreshed/real-time feeds ("renting" data rather than buying it once) — https://mediaandthemachine.substack.com/p/ai-content-licensing-fewer-deals-include-training (accessed 2026-08-31).

**Relevance to AMAZWI:** the deals with disclosed dollar values are all **text/publisher** deals ($43M–$250M scale); every **audio-specific** deal found has an undisclosed value, meaning AMAZWI cannot point to a comparable "X million dollars for speech data" precedent — this is a real gap in the evidence base, not a gap in this research (see "Numbers I could not verify").

---

## 3. THE SOUTH AFRICAN BUYER SIDE

### 3a. BPO / Global Business Services (GBS) sector — likely the largest buyer, sized

- **Headcount and revenue growth**: GBS sector headcount grew from **65,000 (2019) to an estimated 150,000 (2024)**; market revenue grew from **USD 1.04 billion (2019) to an estimated USD 2.91 billion (2024, ≈R53 billion)** — Outsource Accelerator / BPESA reporting, https://news.outsourceaccelerator.com/bpesa-500k-south-africa-gbs/ (accessed 2026-08-31).
- **Recent quarterly pace**: April–June 2025 alone added **8,180 net new international jobs** and **R2.3 billion (≈US$131 million) in export revenue** for that quarter — https://www.bpesa.org.za/news/667-bpesa%E2%80%99s-new-value-proposition-aims-for-500k-jobs-and-global-bpo-expansion.html (accessed 2026-08-31). Full 2024: **20,518 net new international jobs**, "nearly 400 new roles every week."
- **Forward projection**: SA BPO market projected to reach **USD 3.60 billion by 2030**, growing at **10.1% CAGR (2025–2030)** — roughly 2x the global BPO growth rate — https://afrishorebpo.com/south-africa-bpo-statistics/ (accessed 2026-08-31).
- **Government GBS incentive scheme (the dtic's Business Process Services Incentive)**: **over R808 million disbursed to qualifying firms in 2024/25**; cumulatively (2010–March 2025) the industry created **~174,000 new jobs and generated over US$2.7 billion in export revenue**; **more than 50 global companies** have set up GBS operations in SA since the incentive launched, generating **≈R40 billion in export revenue**; the Masterplan (2022) targets **500,000 cumulative jobs by 2030**; government is exploring converting the incentive from cash-based to a tax-based model (11th Schedule of the Income Tax Act) — https://www.bpesa.org.za/news/698-the-dtic-plans-to-bolster-gbs-sector-incentives-to-create-500-000-jobs-by-2030.html (accessed 2026-08-31).
- **The single most important sourced fact for AMAZWI's pitch to this sector**: **"Up to 70% of call centre conversations happen in languages other than English"** in South Africa, yet "most automated quality assurance tools can only process English calls" — TechCabal reporting on Botlhale AI, https://techcabal.com/2025/06/04/botlhale-ai-south-africa-multilingual-call-centres/ (4 June 2025). This is the direct commercial case for a validated multi-language speech corpus/API: the BPO sector is scaling toward 500,000 jobs on a 70%-non-English-conversation base with, per Botlhale's own market pitch, inadequate tooling.

### 3b. Banks / insurers

- **Absa**: ~**5,000 contact-centre reps**; deploying Salesforce Agentforce to "double the impact" of that team via automated inquiry response; in collections specifically, self-paying customers rose from **23% to 43%** with a **three-month ROI of 29:1** — Salesforce customer story, https://www.salesforce.com/customer-stories/absa-group/ (accessed 2026-08-31).
- **Standard Bank**: uses AWS Bedrock as its AI platform; reports a "20% productivity boost from AI coding tools" (an internal engineering metric, not a call-centre volume/automation-spend figure) — CNBC Africa, https://www.cnbcafrica.com/media/7774350918549/-agentic-artificial-intelligence-transforms-sa-banking (accessed 2026-08-31).
- **Total SA banking-sector call-centre volume and total customer-service automation spend: NO PUBLISHED FIGURE FOUND.** No sector-wide aggregate was located.

### 3c. Government — Use of Official Languages Act 2012, and call volumes

- **Use of Official Languages Act 12 of 2012** obliges every **national department, national public entity and national public enterprise** to: (i) adopt a language policy on the use of official languages within **18 months**; (ii) establish a **language unit**; (iii) have that unit advise the accounting officer, monitor compliance, and report annually to the Minister and to the Pan South African Language Board (PanSALB) — https://www.saflii.org/za/legis/consol_act/uoola12o2012232/ ; https://www.gov.za/documents/use-official-languages-act (accessed 2026-08-31). This is a **standing statutory obligation**, not a discretionary CX nicety — a validated indigenous-language ASR/API layer is a compliance tool, not just a convenience feature, for every national department.
- **Home Affairs contact centre**: each operator handles **~120 calls/day**; **112 operators recruited, target of 120** → implies daily volume in the range of **~13,440–14,400 calls/day** (arithmetic from the two disclosed figures; **ESTIMATE**, not a directly published daily total) — Daily Maverick, https://www.dailymaverick.co.za/article/2023-05-01-south-africa-government-customer-service-hotlines-contact-details/ (accessed 2026-08-31).
- **SASSA and SARS annual/monthly call volumes: NO PUBLISHED FIGURE FOUND.** SARS confirms it experiences "high call volumes" seasonally but publishes no number; SASSA publishes no call-centre volume statistics that this research could locate.

### 3d. Global tech companies — what SA languages they support, and the gap

- **Google**: has added **isiZulu and Sesotho** (among other African languages) to its AI search tools — ITWeb, https://www.itweb.co.za/article/google-adds-african-languages-to-ai-search-tools/WnpNgq21na9MVrGd (accessed 2026-08-31). Exact product scope (Search AI Overviews vs. full Assistant voice support) not fully disaggregated in the source.
- **Amazon Alexa**: supports **9 languages natively + 7 English-paired multilingual modes** in 2026; **isiZulu, isiXhosa and Sesotho are not among them** — https://flauntaudio.com/does-alexa-understand-other-languages/ (accessed 2026-08-31).
- **OpenAI Whisper**: the standard release has **Afrikaans and Swahili at "the lower end of the performance spectrum"**; **isiZulu and isiXhosa are not dedicated/supported languages** in the standard model — https://medium.com/@izwe.ai/speech-to-text-platforms-facing-a-new-competitor-in-open-ais-whisper-the-battle-for-accuracy-6b738005ca43 (accessed 2026-08-31). A community fine-tune, "Whisper 51 African Languages" (Sunbird AI's SALT project), exists as a third-party adaptation, not an OpenAI product — https://salt.sunbird.ai/models/asr-whisper-51-african-languages/ (accessed 2026-08-31).
- **Meta / Microsoft specific SA-language voice support: NO PUBLISHED FIGURE/STATEMENT FOUND** in this research pass.
- **Google's own WAXAL dataset** (see Section 8) is Google's direct acknowledgement of this gap: a 3-year, Google + Gates Foundation-funded, 11,000+ hour, 21-language open African speech corpus built specifically because the gap existed — https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/ (accessed 2026-08-31). **This means the single most credible global-tech buyer signal is that Google is already paying (via grant funding, amount undisclosed) to close this exact gap** — evidence of willingness-to-pay, not yet evidence of a commercial licence AMAZWI could sell into.

---

## 4. MTN'S OWN ECONOMICS

### MTN Group FY2025 (year ended 31 December 2025)
- **Group service revenue: R218.5 billion**, +22.9% reported — Engineering News, https://www.engineeringnews.co.za/article/mtn-delivers-robust-fy2025-unveils-ambition-2030-2026-03-16 (16 Mar 2026).
- **EBITDA: R98.5 billion**, +36.8% reported, margin expanded 5.4pp to **44.5%**.
- **Data revenue: R101.5 billion**, +37.7% reported.
- **Fintech revenue: +30.0% reported / +23.2% constant currency.**
- **Fintech transaction value: $500.3 billion**, +37.6% for FY2025; **transaction volumes: 23.3 billion**, +14.9%.
- **MoMo active users: 69.5 million**, +10% YoY; active agents +16.3%; active merchants +8.2%.
- **Total customers: 307.2 million** across 16 markets, +5.6% YoY.
Source for the fintech/MoMo figures: Ecofin Agency, https://www.ecofinagency.com/news-digital/1711-50564-mtn-group-claims-301m-customers-with-fintech-transactions-soaring-38-to-342b (accessed 2026-08-31); Group revenue/EBITDA figures cross-checked against mtn-investor.com results overview, https://mtn-investor.com/reporting/annuals-2025/results-overview.php (accessed 2026-08-31).

### MTN South Africa specifically (the relevant P&L for a South Africa-first mini app)
- **MTN South Africa service revenue: +2.0%** in what MTN itself describes as "a mature and competitive market."
- **MTN South Africa fintech revenue actually DECLINED 8.4% year-on-year**, "largely reflecting a slowdown in XtraTime activity" (airtime advance product), **partially offset by growth within the MoMo portfolio, supported by continued momentum in InsurTech-related services.** Source: search-aggregated from CNBC Africa reporting on the FY2025 results, https://www.cnbcafrica.com/2026/mtn-reports-strong-2025-earnings-as-data-and-fintech-drive-growth (accessed 2026-08-31). **This is an important, sobering fact**: MTN SA's fintech line is currently shrinking, not growing — the MoMo/InsurTech pocket of growth inside that decline is the specific pocket AMAZWI would need to plug into.
- **Absolute MTN South Africa revenue in Rand (not just % growth): NO PUBLISHED FIGURE FOUND** in this research pass (only the percentage growth figure was located; the segment's absolute Rand revenue was not isolated from Group totals in the sources found — the MTN Group FY25 SENS PDF at https://www.mtn.com/wp-content/uploads/2026/03/MTN-Group-FY-25-results-JSE-SENS.pdf would carry this but was not opened in full in this pass).

### What MTN spends on customer care / call centres
**NO PUBLISHED FIGURE FOUND.** No disclosed MTN Group or MTN South Africa customer-care/call-centre cost line was located. MTN outsources call-centre work to BPO partners (e.g., WNS Global Services is reported to be one such partner, 4,000+ staff across 8 SA delivery centres) but no MTN-specific spend figure, contract value, or per-call cost was found — https://za.indeed.com/q-call-centre,-mtn-jobs.html and related listings (accessed 2026-08-31, job-board sources, not financial disclosure).

### What a 1% call deflection would be worth — ESTIMATE (explicit, labelled)
This cannot be answered from disclosed figures because MTN's call-centre cost base is not published. Below is a fully labelled estimate, not a sourced fact:
- **A1 (assumption):** MTN South Africa customer base ≈ 30 million subscribers (order-of-magnitude, not sourced in this pass — MTN Group total is 307.2M across 16 markets; SA is one of MTN's larger markets but an exact SA subscriber count was not retrieved here — **flag as unverified input**).
- **A2 (assumption):** average 2 inbound service calls per subscriber per year (generic telco benchmark assumption, not MTN-specific).
- **A3 (assumption):** average fully-loaded cost per handled call ≈ R25 (blended BPO seat-cost assumption for SA contact centres — not an MTN-disclosed figure).
- Arithmetic: 30,000,000 × 2 calls = 60,000,000 calls/year. 1% deflection = 600,000 calls. 600,000 × R25 = **R15 million/year** in avoided handling cost.
- **This is a bottom-of-the-range, deliberately conservative arithmetic exercise built entirely on unverified assumptions (A1–A3) — it must be presented to any reader as an ESTIMATE with these three inputs shown, never as an MTN-disclosed number.**

### How mini-app / super-app platforms monetise
- **Apple's Mini Apps Partner Program**: Apple takes a **15% commission** on WeChat-style mini-app transactions it processes payment for — half its standard 30% App Store cut — https://www.ctol.digital/news/apple-lowers-app-store-commission-15-percent-mini-apps-wechat-deal/ (accessed 2026-08-31).
- **WeChat/Alipay mini-programs**: monetise via **commerce, payments, membership and order commissions** rather than classic in-app-purchase — https://mighil.com/app-monetization-in-china (accessed 2026-08-31).
- **General super-app take-rate benchmarks**: ride commissions **10–20%**, food delivery **15–25%**, marketplace transactions similar; the "real economics" layer above take-rate is **advertising, financial services (lending/insurance), and platform fees charged to third-party developers** — https://digitalinasia.com/how-super-apps-work-in-asia/ (accessed 2026-08-31).
- **MTN's own Ayoba** (its prior super-app attempt): peaked at **35–36 million monthly active users (2023–2024)**; monetisation plan was explicitly **premium content + advertising** (revenue-share basis for third-party advertisers), with **payment transactions largely commission-free during the growth phase** — https://techfinancials.co.za/2024/08/19/mtns-ayoba-super-app-grows-user-base-by-28-6-to-36-million-monthly-active-users/ ; https://techfocus24.com/mtn-integrating-ads-payment-systems-into-ayoba-super-app/ (accessed 2026-08-31). **This is directly relevant precedent**: MTN's own super-app playbook keeps transaction fees at or near zero to drive adoption and monetises via ads/premium content layered on top — the same logic would argue AMAZWI should not try to make its unit economics work off MoMo transaction fees, but off the data/API licensing layer sitting on top.

---

## 5. COST OF PAID CROWDSOURCED SPEECH

- **Mozilla Common Voice**: entirely **volunteer/unpaid** — 33,150 hours of speech collected, 22,108 hours validated, at essentially **zero direct cost-per-hour to contributors** (foundation absorbs only platform/hosting cost, which is not separately disclosed) — https://www.mozillafoundation.org/en/blog/common-voice-20-is-now-available/ (accessed 2026-08-31). **This is the "free" end of the spectrum AMAZWI is deliberately not choosing** — Common Voice's African-language coverage remains thin precisely because unpaid volunteer collection does not reliably reach under-resourced languages/populations at scale.
- **Karya (India)**: pays workers **$5/hour — reported as "nearly 20 times the Indian minimum wage"** — https://time.com/6297403/the-workers-behind-ai-rarely-see-its-rewards-this-indian-startup-wants-to-fix-that/ (accessed 2026-08-31). Scale: **50,000 low-income workers, 42+ million paid digital tasks, deployed across all 28 Indian states**; clients include **Google and Microsoft**; workers additionally **earn ongoing royalties whenever their data is resold** — a data point directly relevant to AMAZWI's own consent/benefit-sharing design question. Source: Forbes India, https://www.forbesindia.com/article/ai-special-2025/why-karyas-manu-chopra-safiya-husain-pay-people-handsomely-to-speak-local-languages/96181/1 (accessed 2026-08-31).
- **African Next Voices**: see Section 1 — **≈$244/hour all-in program cost** ($2.2M / 9,000 hours), the best available real-world, ethically-compensated, African-language-specific comparable at meaningful scale.
- **Fairwork ratings (labour-standards context)**: In Kenya, Fairwork found "insufficient evidence that workers for any of the nine [gig] platforms evaluated earned the minimum wage of KES 15,201 (~$122) after costs" — https://fair.work (Fairwork Kenya round, accessed 2026-08-31). This is the reputational bar AMAZWI must clear: Karya's $5/hour (≈20x local minimum wage) sets the "gold standard" precedent; underpaying relative to local minimum wage is the single most damaging comparison a critic could draw (see also the Sama/OpenAI Kenya $1.32–2/hr-vs-$12.50/hr-billed scandal noted in prior AMAZWI competitive research, C_COMPETITIVE.md).

---

## 6. CALIBRATING THE REWARD FOR SOUTH AFRICA

| Benchmark | Value | Source | Date |
|---|---|---|---|
| SRD grant | **R370/month** (frozen since April 2024; extended to 31 March 2027, then converts to the "Livelihoods Support Grant") | https://gauteng.news/2026/03/03/sassa-srd-grant-increase-to-r370-from-r350-2026/ ; Budget 2026 confirmation via multiple SASSA-tracking sites | accessed 2026-08-31 |
| National minimum wage | **R30.23/hour**, effective 1 March 2026 (up from R28.79) | Dept. of Employment and Labour, https://www.labour.gov.za/minister-of-employment-and-labour-meth-increases-the-statutory-national-minimum-wage-to-r30-23-per-hour | accessed 2026-08-31 |
| EPWP minimum wage | R16.62/hour | same source | accessed 2026-08-31 |
| 1GB mobile data | **MTN: R85/1GB** (also a promotional R50/1GB monthly TikTok-specific bundle); **Vodacom: R89/1.2GB** | https://businesstech.co.za/news/telecommunications/778546/data-price-comparison-vodacom-vs-mtn-vs-telkom-and-more/ | accessed 2026-08-31 |
| Minibus taxi fare | **R15–R35** for a short-to-medium local metro route; fares rose ~11.5% May–June 2026 on fuel costs (petrol +31.7% YoY, diesel +50.8% YoY) | https://allafrica.com/stories/202607230336.html | accessed 2026-08-31 |
| Standard loaf of bread | **R19.61** (StatsSA, May 2026, urban comparable price, up from R18.93 in May 2025) | Statistics South Africa via businesstech.co.za summary | accessed 2026-08-31 |

**Calibration reasoning:** a per-contribution reward of **R2–R5** sits at 10–26% of a loaf of bread, 2–6% of a 1GB data bundle, and roughly a tenth to a sixth of a single minibus taxi fare — small enough to pay millions of times over, yet large enough that a short multi-clip session (10–20 contributions in under 10 minutes) can plausibly clear **R20–R100**, which is meaningful against a **R370/month (≈R12.33/day) SRD grant** or against the **R30.23/hour minimum wage** if the "labour" involved (reading a prompt, recording ~15–20 seconds, reviewing the take) takes well under a minute per contribution. This is the basis for the reward figure used in the Unit Economics section below. **This is a calibration argument, not a sourced "correct" reward figure** — no published study benchmarks an optimal African-language micro-task reward for South Africa specifically.

---

## 7. MOMO FEES

- **MTN MoMo South Africa standard transaction fee: 2% per transaction** — https://www.mtnmomo.co.za/ (pricing page, accessed 2026-08-31).
- **Zero fees** on: electricity purchases, bill payments, Lotto, airtime, vouchers, and betting.
- **No monthly service fee** — "you only pay for certain transactions."
- **A minimum flat fee (in Rand) for very small transactions, and the specific cost structure for bulk/business B2C disbursement (as opposed to consumer P2P transfers), was NOT found and is NOT the same thing as the 2% consumer-facing rate above. NO PUBLISHED FIGURE FOUND for AMAZWI's actual disbursement cost as a business paying out thousands of small (e.g. R2–R5) rewards.** This is a material open question: if MoMo's bulk-disbursement API charges a flat minimum fee per payout (common in mobile-money bulk-disbursement products elsewhere in Africa, e.g. M-Pesa Bulk), a R3 reward could be mostly or entirely consumed by the transaction fee unless AMAZWI **batches earnings into periodic (e.g. weekly) payouts** rather than paying out after every single contribution. **This should be treated as an unresolved, must-verify-with-MTN-directly item before finalising the reward/payout design**, not an estimate this research can safely produce.

---

## 8. AFRICAN LANGUAGE AI MARKET

| Company/entity | Funding / deal | Source | Date |
|---|---|---|---|
| **Lelapa AI** (South Africa) | **$2.5 million seed** (17 Feb 2023); no confirmed subsequent round found despite a stated intent to raise again in 2025 | https://www.technologyreview.com/2023/11/17/1083637/lelapa-ai-african-languages-vulavula/ ; Tracxn | accessed 2026-08-31 |
| **Intron Health** (Nigeria) | **$1.6 million pre-seed** (announced mid-2024), led by Microtraction, w/ Plug and Play Ventures, Jaza Rift Ventures, Octopus Ventures. Trained on 3.5M audio clips from 18,000+ contributors across 29 countries/288 accents; reports 92% accuracy on medical terminology; used by clinicians in Nigeria, Ghana, Kenya, **South Africa** and Uganda | https://techcrunch.com/2024/07/25/intron-health-raises-1-6m-pre-seed ; https://afrotech.com/intron-health-raises-1-6m | accessed 2026-08-31 |
| **Awarri** (Nigeria) | Built Nigeria's first government-backed multilingual LLM ("N-ATLAS," unveiled Sept 2025) with NITDA/NCAIR and DataDotOrg; trained initially on Yoruba, Hausa, Igbo, Ibibio, Pidgin + accented English; used **500 fellows from the federal government's 3 Million Technical Talent (3MTT) programme** as data collectors. **The specific deal/grant value in USD or NGN was NOT found — NO PUBLISHED FIGURE FOUND** despite multiple targeted searches | https://restofworld.org/2024/nigeria-awarri-ai-startup-llm/ ; https://techcabal.com/2025/09/25/nigerian-government-awarri-launch-n-atlas/ | accessed 2026-08-31 |
| **Botlhale AI** (South Africa) | Founded 2019, Cape Town; currently **raising $2 million**; supports **11 South African languages**, expanding to Ghana, Kenya, Nigeria; core stat used in its own market pitch: **"up to 70% of SA call-centre conversations happen in non-English languages"** | https://techcabal.com/2025/06/04/botlhale-ai-south-africa-multilingual-call-centres/ | 4 June 2025 |
| **WAXAL** (Google + Gates Foundation) | 3-year effort, **11,000+ hours of speech from ~2 million recordings, 21 Sub-Saharan African languages**; funding amount from Google/Google.org **NOT disclosed** — **NO PUBLISHED FIGURE FOUND** | https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/ | accessed 2026-08-31 |

### Market sizing
- **Africa-wide AI market: $4.51 billion (2025) → $16.53 billion (2030), 27.42% CAGR** — Mastercard/Ecofin Agency reporting, https://www.ecofinagency.com/news-digital/1308-48038-africa-s-ai-market-poised-to-reach-16-5-billion-by-2030-mastercard-reports (accessed 2026-08-31).
- **South Africa Conversational AI market specifically: $159.6 million (2025) → $549.8 million (2030), 22.9% CAGR** — MarketsandMarkets, https://www.marketsandmarkets.com/Market-Reports/geography/conversational-ai-market/South-Africa (accessed 2026-08-31).
- **A market-size figure for "African-language AI" as its own distinct segment (as opposed to general AI or general conversational AI) does NOT exist in any source found — NO PUBLISHED FIGURE FOUND.** Every market-sizing report found sizes either continent-wide AI or SA conversational AI broadly, not the specific low-resource-language subsegment AMAZWI would occupy.

---

## THE PRICE LIST — what AMAZWI could charge, per product, with the comparable that justifies it

| Product | Suggested price point | Comparable that justifies it |
|---|---|---|
| **Dataset access (bulk, licensed hours of validated speech)** | **$100–150/hour**, undercutting Defined.ai's ≈$175/hour blended DAP rate and roughly matching (not exceeding) the literature's own "conventional cost floor" for low-resource collection | Defined.ai DAP ≈€160/hr (https://defined.ai/press-room/defined-ai-launches-data-access-plan-dap-allowing-access-to-speech-datasets-at-affordable-prices); "Synthetic Voice Data..." $100–150/hr floor (https://arxiv.org/html/2507.17578) |
| **Model/ASR API access (per-minute transcription/inference, not raw data)** | Anchor near **izwe.ai's own published SA-language rates: R0.25/min (community) to R0.35/min (private tier)** — i.e. ≈R15–21/hour of audio processed, since this is the only South African-language-specific published API price point found | izwe.ai pricing (search-aggregated, accessed 2026-08-31) |
| **Campaign sponsorship (brand/government pays to fund a themed data-collection drive, e.g. "SARS tax-season isiZulu campaign")** | Priced as a **CPM-style sponsorship against Ayoba's own precedent** — Ayoba sold advertising/content-marketing placements to brands (Cadbury, Chappies) on a revenue-share/campaign basis at 35M+ MAU scale; AMAZWI's initial scale would justify a proportionally smaller flat sponsorship fee, not a rate card this research can size without AMAZWI's own traffic data | MTN Ayoba brand campaign precedent, https://www.mtn.com/african-messaging-app-ayoba-launches-continent-wide-atl-campaign-with-partner-mtnlife-inside-ayoba/ |
| **Learner subscription (language-learning layer on top of the corpus)** | **NO DIRECT COMPARABLE FOUND** for a South African indigenous-language learning subscription price (Angula's pricing was not disclosed in prior AMAZWI research either) — cannot responsibly price this without primary research into Angula/Duolingo-style SA-market willingness-to-pay | See C_COMPETITIVE.md — Angula noted but pricing undisclosed |
| **Proficiency certification (e.g. "verified isiZulu speaker" credential for BPO hiring pipelines)** | Priced against the **BPESA hiring pipeline's own economics**: BPO employers are adding ~400 jobs/week and the government pays an operational-expenditure grant per SA employee under the GBS incentive — a certification that speeds hiring/reduces mis-hire risk could plausibly be priced as a **small fraction of one month's per-employee GBS grant value**, but the per-employee grant amount itself was **NOT found (NO PUBLISHED FIGURE FOUND)**, so this price point cannot be arithmetically anchored — it is a plausible product, not a priced one | BPESA jobs pace: https://www.bpesa.org.za/news/667-... |

---

## UNIT ECONOMICS — full cost-per-validated-minute build-up (ESTIMATE, every input labelled)

**This entire section is a labelled estimate. No published source states AMAZWI's actual future cost structure — it does not exist yet.**

Inputs and why each was chosen:
- **[A] Average clip length ≈ 15 seconds (0.25 min).** Anchored near WAXAL's own empirical average: 11,000+ hours ÷ ~2,000,000 recordings ≈ **19.8 seconds/recording** (https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/). 15 sec is a rounded, slightly-conservative assumption, not WAXAL's exact figure.
- **[B] Reward per validated (accepted) clip = R3.** Calibrated in Section 6 against SRD (R370/mo), minimum wage (R30.23/hr), bread (R19.61), and data (R85/GB) — an assumption, not a sourced rate.
- **[C] Validation = 2 independent peer listens per submitted clip (accepted or rejected), each peer paid R0.50/vote.** Assumption modelled on generic crowdsource QA design (Common Voice-style community validation), not a sourced AMAZWI or comparable-project rate.
- **[D] Acceptance rate = 70%** (30% of submitted clips rejected for noise/misread prompt/etc). Generic crowdsource-QA assumption, **not South Africa- or AMAZWI-specific** — no source found for an expected SA voice-app rejection rate.
- **[E] MoMo disbursement fee = 2%**, per Section 7's sourced consumer rate — flagged there as possibly not representative of actual bulk B2C disbursement cost (unresolved, see Section 7).
- **[F] Platform overhead = 40% of direct contributor-facing cash cost**, covering engineering, hosting, moderation, fraud review, customer support, compliance. Generic assumption for an early-stage consumer data platform, not sourced to any disclosed AMAZWI, Karya, or Common Voice cost breakdown (none of those breakdowns are public).

**Arithmetic, to produce 1 validated minute of audio (4 accepted 15-second clips):**

1. Submitted clips needed: 4 accepted ÷ 70% acceptance = **5.71 submitted clips**.
2. Reward cost (only accepted clips paid): 4 × R3 = **R12.00**
3. Validation cost (all submitted clips validated, 2 votes × R0.50): 5.71 × 2 × R0.50 = **R5.71**
4. MoMo fee on rewards (2% × R12.00) = **R0.24**
5. MoMo fee on validator payouts (2% × R5.71) = **R0.11**
6. **Direct cash cost = R12.00 + R5.71 + R0.24 + R0.11 = R18.06**
7. Platform overhead (40% × R18.06) = **R7.22**
8. **Total fully-loaded cost per validated minute ≈ R25.28**
9. **Per validated hour ≈ R25.28 × 60 = R1,517** ≈ **US$94** at USD/ZAR 16.15

**Margin check against sourced comparables:**
- Against the literature's own **$100–150/hour "conventional cost floor"** for low-resource collection (https://arxiv.org/html/2507.17578): AMAZWI's modelled **$94/hour all-in cost sits at or slightly below that floor** — i.e., even before selling anything, the model is cost-competitive with the cheapest documented conventional approach.
- Sold at $100/hour (floor): margin = (100−94)/100 = **~6%**.
- Sold at $150/hour (top of conventional range): margin = (150−94)/150 = **~37%**.
- Sold at Defined.ai's ≈$175/hour blended rate: margin = (175−94)/175 = **~46%**.
- Against African Next Voices' **≈$244/hour all-in program cost**: AMAZWI's modelled cost is **~61% cheaper**, which — if the underlying assumptions [A]–[F] hold up in reality — is the single strongest efficiency argument for a gamified, mobile-money-native, telco-distributed model over a grant-funded academic fieldwork model.

**Every one of these margin figures inherits the uncertainty of assumptions [A]–[F] above, most importantly [D] (acceptance rate) and [E] (whether 2% really is the applicable bulk-disbursement fee). This is a plausibility model, not a forecast.**

---

## THE FIVE BUYERS — ranked and named, with each one's specific pain

1. **BPO / Global Business Services sector (BPESA members)** — **Pain:** scaling toward 500,000 jobs by 2030 on a base where "up to 70% of call centre conversations happen in languages other than English" (Botlhale AI's own stated market problem), with call-centre QA/analytics tooling that "can only process English calls." **Why ranked #1:** it is the only buyer segment in this research with (a) a hard, sourced pain statement, (b) fast headcount growth (≈400 jobs/week), (c) government subsidy already flowing (R808M+ disbursed in 2024/25) that could co-fund tooling spend, and (d) a direct competitor (Botlhale AI) already selling into it and raising capital to do so, proving the willingness-to-pay exists.
2. **Global tech platforms (Google, OpenAI, Meta, Microsoft, Amazon)** — **Pain:** demonstrable, sourced gaps in isiZulu/isiXhosa/Sesotho support across Alexa and Whisper; Google is already funding WAXAL (undisclosed amount) specifically to close this class of gap. **Why ranked #2:** highest willingness-to-pay per data-hour if precedent (Defined.ai ≈$175/hr, News Corp $50M/yr-scale deals) holds, but the audio-specific deals found in this research are uniformly **undisclosed in value**, and no South African-language-specific deal with any of these five companies was found — this is a real, not just hypothetical, buyer, but an unproven one at AMAZWI's likely deal size.
3. **South African government departments** — **Pain:** a *statutory* obligation (Use of Official Languages Act 12 of 2012) to have a language policy and language unit, not a discretionary CX choice; Home Affairs alone estimated at ~13,000+ calls/day. **Why ranked #3, not higher:** government procurement cycles are slow, SASSA/SARS/Home Affairs call-volume figures are largely undisclosed (weakening the ability to size the deal), and no evidence was found of any department currently procuring a commercial speech-AI product for indigenous-language service delivery.
4. **Banks and insurers** — **Pain:** Absa's 5,000-seat contact centre and its own stated ambition to "double impact" via automation; proven ROI logic exists (29:1 three-month ROI in one internal collections automation case). **Why ranked #4:** the sourced automation activity (Absa/Agentforce, Standard Bank/Bedrock) is with global enterprise AI vendors already, not with an African-language-data specialist — no sourced evidence any SA bank is short on English-language automation tooling; the specific unmet need is language coverage, which is asserted by inference (multilingual customer base) rather than directly evidenced in the banking sources found.
5. **Direct-to-developer / API buyers of a South African-language ASR product** — **Pain:** izwe.ai already exists and prices its API (R0.25–0.35/min), proving there is a live, paying market at small scale; Botlhale AI, Lelapa AI and Intron Health all monetise API/product access to African-language speech technology. **Why ranked #5 (last):** this is the smallest, most crowded, most price-competitive segment — AMAZWI would be a data supplier to these companies more plausibly than a direct API competitor against them, given izwe.ai, Botlhale and Lelapa are all already operating exactly here.

---

## HOW MTN MAKES MONEY — five revenue lines ranked by credibility

1. **Sponsorship/campaign revenue on the mini app itself, Ayoba-style (advertising + premium content, revenue-share with brands/government)** — **Most credible**, because it is MTN's own already-executed playbook: Ayoba monetised via "premium paid content and advertising," kept payment transactions "commission-free during the growth phase," and signed real brand campaigns (Cadbury, Chappies) at scale (35M+ MAU) — https://techfinancials.co.za/2024/08/19/mtns-ayoba-super-app-grows-user-base-by-28-6-to-36-million-monthly-active-users/. This requires no new deal-making muscle from MTN — it is a repeat of a model MTN has already run.
2. **Data/dataset and API licensing to third parties (BPO, global tech, government)** — **Second most credible**, because comparable markets and price points are real and sourced (Section 1, Section 3a/3d), but **no comparable telco-run version of this exact model exists anywhere in the world** (per prior AMAZWI competitive research, C_COMPETITIVE.md) — the revenue mechanics are proven in adjacent markets (Defined.ai, izwe.ai) but unproven specifically for a telco-operated consumer app.
3. **MoMo transaction float/fee economics indirectly boosted by increased MoMo wallet activity** — **Third, moderate credibility.** MTN's SA fintech revenue is *currently declining* (−8.4% YoY, driven by XtraTime softness), with MoMo/InsurTech cited as the only growing pocket inside that decline. AMAZWI would inject a large number of small, regular inbound MoMo credits (contributor rewards), which increases wallet float and transaction volume/frequency — a real mechanism, but MTN's own 2% standard fee structure and its "commission-free during growth phase" precedent on Ayoba suggest MTN is unlikely to charge AMAZWI's own reward payouts at the full 2% rate, capping how much direct fee revenue this line could realistically generate.
4. **Government GBS-incentive-adjacent revenue (MTN positions AMAZWI as national-language-compliance infrastructure and captures a services/licensing fee from the state or from GBS-incentive-recipient BPOs)** — **Fourth, lower credibility currently**, because it depends on two unproven links: (a) government departments actually procuring a commercial tool to meet Official Languages Act obligations (no evidence found that any department currently does this), and (b) GBS-incentive-recipient BPOs directing incentive-linked budget toward a specific vendor like AMAZWI (mechanism plausible, not evidenced).
5. **Direct advertising/data-broker sale of anonymised linguistic insights (market research on language/dialect usage patterns) to non-AI buyers (e.g. market researchers, media planners)** — **Least credible / most speculative.** No comparable precedent, dollar figure, or named buyer was found anywhere in this research for this specific use case; included only because it is a theoretically available revenue line, not because any evidence supports it.

---

## NUMBERS I COULD NOT VERIFY

- **The $345.42/hour Hausa speech-data cost figure** — appeared in an AI-search-engine synthesis but could not be traced to a primary source on direct verification of the two most likely candidate papers (arxiv 2507.17578, arxiv 2510.12781). **Do not cite.**
- **MTN South Africa's absolute Rand revenue figure** (as opposed to its % growth rate) — not isolated from Group totals in sources reviewed; would require opening the full FY25 SENS PDF (https://www.mtn.com/wp-content/uploads/2026/03/MTN-Group-FY-25-results-JSE-SENS.pdf), which was not fully parsed in this pass.
- **MTN's disclosed customer-care/call-centre spend, in South Africa or Group-wide** — NO PUBLISHED FIGURE FOUND anywhere in this research.
- **SASSA and SARS annual/monthly call-centre volumes** — NO PUBLISHED FIGURE FOUND; only Home Affairs yielded an arithmetic-derivable estimate (~13,000+ calls/day), and even that is a calculation from two secondary figures, not a directly published total.
- **The dtic's GBS incentive per-employee grant amount** — the scheme's total disbursement (R808M in 2024/25) is known; the per-employee/per-role grant rate is not, which blocks any arithmetic pricing of a "certification" product against it.
- **Any audio/speech-specific AI licensing deal with a disclosed dollar value** — every named example (Suno-BMG, Suno-Warner, Stability-AudioSparx) has an undisclosed value; text/publisher deals are the only disclosed-value comparables available.
- **The Awarri-Nigerian-government deal's monetary value** — extensively searched, genuinely not published in any source found.
- **Google.org's/Google's funding amount for WAXAL** — confirmed as Google + Gates Foundation funded, amount not disclosed.
- **izwe.ai's, Botlhale AI's, and Lelapa AI's actual revenue or customer counts** — only funding-round or unit-price figures were found, not revenue.
- **A market-size figure specifically for "African-language AI"** as a distinct category (as opposed to general AI or conversational AI) — does not appear to exist in published market research.
- **MTN MoMo South Africa's bulk/business B2C disbursement fee structure** (as distinct from the 2% consumer P2P/merchant rate) — this is the single most consequential unresolved number for AMAZWI's actual unit economics, and it is not publishable from open search; it requires a direct conversation with MTN MoMo's business/API team.
- **Angula's (SA indigenous-language learning app) subscription pricing** — referenced in prior AMAZWI competitive research as funded and MTN-award-winning, but no price point was found in either that research or this one.
