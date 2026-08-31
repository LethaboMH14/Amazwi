# IDEAS BOARD — MoMo Mini App Hackathon 2026
**Updated:** 2026-08-15 · Wide-then-narrow pass · 33 concepts across 3 tracks

Read first: `../01_research/RESEARCH_BRIEF.md` (gaps §F1, rubric §F3) and `MOMO_API_AND_MINIAPP.md`.

---

## CHANGED ASSUMPTION — this reshapes everything

Original plan assumed a 24-hour build. **Actual plan: team of 4, building from registration through to 2 September (~2.5 weeks), with demo day reserved for polish, mentor feedback, UI and the pitch.**

Consequences:
- **The feasibility ceiling is now high.** Concepts that were impossible in 24 hours — real integrations, multi-sided flows, data pipelines, trained models — are all in range.
- **Therefore stop optimising for "buildable in a day."** Optimise for *"nobody else in the room can build this in a day, and we already have."* Depth becomes the differentiator.
- **The 24h teams will all ship the same thing**: a single-screen payment demo. Arriving with a working multi-sided product is how you win before the pitch starts.
- ⚠️ **Rules risk:** T&Cs say all work must be created during the hackathon; the registration form asks for a repo URL. Get written clarification from the organisers. See `../BUILD_LOG.md`.

## Rules of engagement

1. **One verb.** Every past winner was a single nameable action. Not a platform. Not a suite.
2. **Weekly-open test.** Can't say why a real person opens it every week? It's a VodaPay tile.
3. **Only-MTN test.** Strongest ideas need assets nobody else has: the SIM, 16 markets, the network graph, the USSD menu.
4. **No lending app.** There is no lending track. That is not an accident.
5. **Demo the moment, not the feature.** One scene the judges will still remember at lunch.

### Legend
🔒 **Only-MTN** — depends on an asset competitors can't replicate · ⚡ **Weekly-open** — creates a recurring reason to open MoMo · 💰 **MTN revenue** — money lands in MTN's pocket directly

---

# TRACK 1 — EVERYDAY ESSENTIALS
*Groceries · prepaid electricity & water · airtime & data · bills · school fees · health · household*

### 1.1 · UBUNTU — social underwriting 🔒⚡
**Verb:** *Vouch.*
Community as credit bureau, with skin in the game. I stake R50 of my balance against your R500. You repay → I earn yield. You default → I lose the stake. Vouching stops being a favour and becomes a priced investment.
**Insight:** every past SA winner (Zaka, Tata Imali, MoLo) tried to *be the lender*. That's the mistake. Be the trust layer.
**Under the hood:** MTN's network graph — who sends to whom, how often, how long — is the underwriting signal. MTN holds this and monetises none of it.
**APIs:** Pay, Get Paid, Get Consent (stake lock), Identify, Notify.
**Risk:** no lending track. Frame as *community savings & access*, never "a lending app."

### 1.2 · MoMo SHIELD — fraud defence only a telco can build 🔒
**Verb:** *Check before you send.*
Before any transfer to a new number: *"⚠️ This number was SIM-swapped 6 hours ago." / "New to network 2 days ago." / "✅ You've sent here 14 times since 2023."* Plus a 30-minute reversible send for first-time recipients.
**Insight:** SIM swap is **43% of all mobile money fraud**. MTN Nigeria lost **$53m in one year**. Fraud prevention is written into the Ant International deal. And Capitec, Shop2Shop, OPay *physically cannot build this* — they don't own the SIM.
**Bigger version:** offer it as a platform service to every other mini app — "Shield-verified." You didn't build an app, you built infrastructure.
**APIs:** Identify, Notify, Get Paid; MNO signals (position as required capability).
**Risk:** SIM-swap data access is the whole idea and may not be exposed. **Mitigate by shipping the full product against a simulated signal feed and pitching the data contract as the ask.** That framing is a strength, not a weakness — you're proposing a partnership.

### 1.3 · ISIKHWAMA (The Envelope) — budgeting inside the wallet ⚡
**Verb:** *Split it.*
Money arrives → auto-splits into labelled envelopes: rent, food, transport, school, black tax, self. Spend from an envelope, not from a number.
**Insight:** the single biggest reason people withdraw everything to cash is that **they cannot mentally partition one balance.** Cash in a tin is legible; a wallet balance is not. Envelopes make digital money as legible as cash — and money that stays in the wallet is money that isn't dormant.
**This is the purest attack on the 70% dormancy problem in the entire board.**
**APIs:** Manage, Pay, Get Consent (auto-split mandate), Notify.
**Risk:** looks simple. Win on execution and on the dormancy argument, not novelty.

### 1.4 · MoMo MANDATE — direct debit for the unbanked ⚡
**Verb:** *Set it once.*
*"Buy R100 electricity when my meter drops below 20 units, max twice a month." "Send gogo R200 airtime on the 1st."* Scoped, capped, revocable, PIN-signed.
**Insight:** MTN shipped a **Get Consent** API — PIN-authenticated consent over USSD — and nobody built on it. Get Consent + Invoice + Pay = standing authority over a wallet. Africa has no true direct debit for the unbanked.
**Stretch:** 2026's agentic payment protocols (AP2, x402) are all about scoped revocable mandates for AI agents. This makes MoMo the first African wallet with an agent-mandate layer.
**APIs:** Get Consent ⭐, Invoice, Pay, Notify.
**Risk:** abstract. Needs a concrete hero use case (electricity) to be felt.

### 1.5 · METER — stop losing money on prepaid electricity ⚡💰
**Verb:** *Buy smarter.*
Predicts when you'll run out; tells you the cheapest amount to buy; lets a household split the cost; warns before you fall into the "electricity advance" trap.
**Insight:** SA prepaid electricity uses **stepped block tariffs — buying R100 five times costs more per unit than R500 once.** Millions of households lose money to this every month and nobody has ever surfaced the arbitrage. That is a genuine, quantifiable, "I'm saving you money" demo.
**APIs:** Get Paid, Invoice, Mandate/Get Consent, Notify.
**Risk:** needs a token vendor integration. Mock it cleanly if unavailable.

### 1.6 · SOUND MONEY — payment with no data, screen or camera 🔒
**Verb:** *Pay by sound.*
Two phones transact over audio tones. Confirmation by SMS.
**Insight:** **Rova Pay won Nigeria** for removing the internet requirement; **EchoKash placed** for removing the screen. In access-constrained markets, the interface *is* the innovation. 600m sub-Saharan Africans lack reliable power. Every other mini app assumes a charged smartphone on LTE.
**APIs:** Get Paid, Notify, Interact (USSD fallback).
**Risk:** audio in a noisy demo hall. Test relentlessly; have a wired fallback.

### 1.7 · KASI OS — own the merchant with software, not a card reader ⚡
**Verb:** *Restock together.*
Photograph your shelf → stock read and tracked → reorder suggested → **group-buy with nearby shops via MoMo escrow** to reach wholesale price → margin tracked per line.
**Insight:** Shop2Shop proved software (not acceptance) owns the merchant — **R172bn** through its ecosystem. And there's a live 2026 cohort: **thousands of first-time local spaza owners** who took over shops this year with no buying networks, which is why bread went **R16 → R30** in some communities. Group buying is the **largest mini-program category in China** and has never been built for township retail.
**APIs:** Get Paid, Pay (escrow release), Invoice, Manage, Distribute.
**Risk:** two-sided and heavy. Strongest with the full 2.5 weeks.

### 1.8 · UMGALELO — the stokvel protocol ⚡
**Verb:** *Contribute.*
Rotating savings as a rail: programmable payout order, group wallet, automated collection, transparent ledger, defection rules, payout countdown. Generates a repayment record as a by-product.
**Insight:** stokvels are a **R50bn+ South African behaviour with no native digital rail.** Kabokisi won Uganda with a lighter version. This is not a new behaviour to teach — it's an existing one to instrument.
**APIs:** Get Consent (recurring contribution), Pay, Get Paid, Manage, Notify.
**Risk:** crowded idea space. Differentiate on the *defection/dispute* mechanics — that's the part everyone skips and the part that actually breaks stokvels.

### 1.9 · NKOSI — black tax, managed 🔒⚡
**Verb:** *Commit.*
Make family obligation a visible, budgeted, scheduled flow instead of ad-hoc WhatsApp requests. Set monthly commitments per recipient, auto-disburse, shared ledger, and out-of-plan requests get politely queued rather than refused.
**Insight:** deeply, specifically South African. Every young earner in that room knows exactly what this is — and nobody has built it. **It converts the most emotionally charged money flow in the country into recurring in-wallet transactions.** Judges will feel this one personally, which is worth more than a feature list.
**APIs:** Get Consent, Pay, Notify, Manage.
**Risk:** emotionally sensitive. Tone must be warm and dignified, never clinical.

### 1.10 · VOUCH — send groceries, not cash 💰
**Verb:** *Send food.*
Ring-fenced, merchant-restricted value: send your mother groceries or your child's school lunch, redeemable only at approved merchants.
**Insight:** MoMo SA already runs food vouchers — this extends an existing product. It gives people a reason to send money that **isn't a cash-out**, keeping value inside the ecosystem, and it kills a whole class of remittance misuse and scam.
**APIs:** Get Paid, Pay, Distribute, Notify, Identify.
**Risk:** merchant network required. Demo with 2–3 partner spazas.

### 1.11 · CLINIC — health money
**Verb:** *Save for medicine.*
Ring-fenced health savings, chronic medication top-ups, clinic queue booking, funeral-cover contributions.
**Insight:** Clinique Plus Pay placed third in Nigeria on a thinner version. SA angle: chronic medication collection and funeral cover are near-universal.
**APIs:** Get Paid, Invoice, Pay, Notify.
**Risk:** health data compliance. Keep it a *savings* product, not a health record.

### 1.12 · FEES — school payments
**Verb:** *Pay in instalments.*
Schools register; parents pay fees, uniforms, trips and matric dance in instalments with receipts; schools get reconciliation.
**Insight:** a school is an aggregator of thousands of low-income households. Sign one school, onboard 800 families. Pure distribution arbitrage.
**APIs:** Invoice ⭐, Get Consent, Get Paid, Manage, Notify.
**Risk:** B2B sales cycle. Great business, less spectacular demo.

---

# TRACK 2 — ENTERTAINMENT & LIFESTYLE
*Gaming · streaming · sport · events & ticketing · music · social · food · beauty · fitness*

> **This is the whitest space in the competition.** No MoMo hackathon winner has ever come from entertainment. It is also MoMo's weakest product area and — per the Ant International deal — explicitly where MTN wants to go ("commerce and lifestyle services"). Least competition, most novelty credit, highest strategic fit. **Recommend at least one primary candidate from here.**

### 2.1 · SHAYA — tip the artist 🔒⚡💰
**Verb:** *Tip.*
Scan and tip the DJ, dancer, taxi-rank performer, busker or streamer. Instant, R2 upward, no bank account needed on the receiving side. Leaderboards, shout-outs, and the artist's takings settle to MoMo live.
**Insight:** South Africa exports the most culturally dominant music scene on earth right now, and **the entire tipping economy around it runs on cash pushed into a hand.** Amapiano DJs, gqom dancers, church musicians, taxi-rank performers. There is no digital rail for appreciation.
**Why it wins the room:** you can demo it *on stage*. Put a performer in front of the judges and have the audience tip in real time. Nobody forgets that pitch.
**MTN angle:** micro-transactions at enormous volume, a youth-native reason to open MoMo weekly, and artists become MoMo merchants — merchant acquisition disguised as culture.
**APIs:** Get Paid, Pay (instant artist settlement), Identify, Notify, Collection Widget (QR).
**Risk:** ARPU per tip is tiny. Argue volume and engagement, not revenue per transaction.

### 2.2 · SOCIETY — the fun stokvel ⚡
**Verb:** *Chip in.*
Twelve friends, monthly contributions, one person's payout each month — for birthdays, December, a trip, a new phone. Countdown, group feed, automatic collection, public accountability.
**Insight:** "society" is real, widespread SA behaviour and it's the **joyful** cousin of the stokvel. Track 2 lets you build the same rail as Umgalelo but with all the social mechanics — which is what actually drives retention.
**APIs:** Get Consent (recurring), Pay, Get Paid, Notify.
**Risk:** overlaps 1.8. Pick one, don't run both.

### 2.3 · GIFT — send data with a message ⚡💰
**Verb:** *Gift data.*
Send someone airtime or a data bundle as a gift with a note, GIF or voice clip. Crowd-fund a friend's data for exam week. Data-gifting streaks between friends.
**Insight:** **data is the youth currency of South Africa.** "Ngicela i-data" is one of the most-sent messages in the country. There is no gifting layer, no social wrapper, no crowd-fund.
**Why judges say yes fast:** the money spent lands **directly in MTN's own revenue line**. This is the rare mini app where MTN is the merchant. That is an unusually easy internal business case, and it's viral by construction — every gift recruits a recipient into the app.
**APIs:** Get Paid, Distribute ⭐, Notify, Identify.
**Risk:** feels small. Sell it as a **viral acquisition and engagement loop**, not a product.

### 2.4 · LIGI — community sport, banked ⚡
**Verb:** *Pay subs.*
Amateur football league management: player subs, referee payment, fixture list, kit fundraising, log table, transparent team wallet.
**Insight:** every township in South Africa runs multiple amateur leagues **on cash in a plastic bag**, with constant disputes about who paid. It's a perfect aggregation unit — sign one league, onboard 300 players who now open MoMo every Saturday. Sport gives you weekly cadence for free.
**APIs:** Get Paid, Pay, Manage, Get Consent, Notify.
**Risk:** looks niche. It isn't — argue the aggregation and the weekly cadence.

### 2.5 · TICKET — group ticketing without the scalpers
**Verb:** *Split the ticket.*
Buy event tickets as a group with split payment, escrow until everyone pays, QR entry, and resale that routes value back to the organiser instead of the scalper.
**Insight:** **nobody attends an event alone**, and splitting the payment is the number-one friction in SA ticketing — one person fronts the money and chases everyone for weeks. Howler already proved cashless festival wallets work here; the *group* layer is missing.
**APIs:** Get Paid, Pay (escrow release + refunds), Invoice, Notify.
**Risk:** competitive category (Computicket, Quicket, Howler). Differentiate hard on group-split and escrow, not on ticketing.

### 2.6 · KASI KOS — order ahead, no delivery fleet ⚡
**Verb:** *Order ahead.*
Order and pay for your kota, shisanyama or vetkoek before you walk there. No delivery, no drivers, no fleet — just skip the queue and the cash.
**Insight:** township fast food is a **R90bn** market. Every delivery app has failed to serve it because delivery economics don't work at R35 a meal. **Remove delivery entirely** and the economics become trivial — you're selling queue-skipping and cashlessness, not logistics. This is exactly the mini app model: light, local, high-frequency.
**APIs:** Get Paid, Pay, Notify, Distribute.
**Risk:** merchant onboarding. Demo with 3 real spots; film them.

### 2.7 · ARENA — the informal gaming economy 💰
**Verb:** *Enter the tournament.*
Entry fees, brackets, and automated prize payout for the FIFA/CoD/Mortal Kombat tournaments that run in every township gaming shop and residence.
**Insight:** SA's gaming and esports market is on a path to **$12.9bn by 2032**, and the grassroots layer — entry fees collected in cash, prizes disputed, organisers accused of stealing the pot — has **no payment rail at all.** Escrowed prize pools solve a trust problem, not just a payment problem.
**APIs:** Get Paid, Pay (escrowed prize disbursement), Manage, Notify.
**Risk:** gambling-adjacent optics. Keep it skill-based tournaments with escrowed entry; never chance-based.

### 2.8 · SHARE — split the subscription ⚡
**Verb:** *Share the sub.*
Split Netflix, Showmax, DStv, Spotify or a data contract across friends or family, with automatic monthly collection and automatic removal of non-payers.
**Insight:** subscription sharing is universal and the *collection* is a permanent low-grade friction — one person pays, everyone forgets. The Get Consent mandate makes it automatic. Recurring by definition = the weekly-open test passes trivially.
**APIs:** Get Consent ⭐, Get Paid, Pay, Notify.
**Risk:** ToS grey area with some providers. Lead with data bundles and DStv, which are shareable by design.

### 2.9 · GLOW — bookings with deposits
**Verb:** *Book with a deposit.*
Hair, barber, nails, lashes: book a slot and pay a deposit that protects the stylist from no-shows.
**Insight:** the SA beauty economy is huge, informal and **destroyed by no-shows** — a stylist holding a two-hour slot for someone who doesn't arrive loses a day's income. The deposit is the product; the booking is the wrapper. Solves a business problem, not a convenience problem.
**APIs:** Get Paid, Pay (deposit release/refund), Identify, Notify.
**Risk:** two-sided marketplace. Narrow to one suburb for the demo.

### 2.10 · UMNIKELO — transparent community fundraising 🔒
**Verb:** *Give.*
Church offerings, funeral contributions, school fundraisers, "asambeni" collections — with a public, tamper-evident ledger showing every contribution and every disbursement.
**Insight:** community fundraising in SA is enormous, entirely cash, and **quietly poisoned by suspicion** about where the money went. The innovation is not the payment — it's the **auditability**. Trust is the product.
**Why MTN:** these are the highest-trust institutions in the community. Winning a church wins 400 families at once.
**APIs:** Get Paid, Pay, Manage, Notify, Identify.
**Risk:** sensitive context. Design must feel respectful and dignified, never startup-y.

### 2.11 · HUSTLE — get paid for your side gig ⚡
**Verb:** *Invoice.*
For SA's **1.8–2 million gig workers**: send a payment request, get paid, track income, and generate a provable earnings record.
**Insight:** the gig economy here is worth **$5.03bn**, 70% of participants use it to supplement other income — and almost none of them can **prove** what they earn, which is the wall between them and credit, housing or a bank account. **Proof of income is the gateway product to everything else.**
**APIs:** Invoice ⭐, Get Paid, Identify, Manage, Notify.
**Risk:** overlaps merchant tooling. Differentiate on the earnings-proof artefact.

---

# TRACK 3 — TRAVEL & MOBILITY
*Taxis · buses · e-hailing · fuel · tolls · parking · cross-border · delivery · logistics*

> **Hardest track, highest strategic value.** 15m daily cash taxi commuters, **80%+ of ride-hailing trips are cash**, and the taxi is the pump that keeps cash circulating in the whole township economy. But note: **at least 14 cashless taxi attempts have already failed** — teams better funded than us. Frontal assaults lose here. Every strong idea below is oblique.

### 3.1 · CHANGE — digitise the change, not the fare 🔒⚡
**Verb:** *Keep the change.*
You still pay cash. Instead of coins, the driver or shopkeeper flicks your change into your MoMo wallet in one second.
**Insight:** fourteen attempts failed trying to replace the fare. **Don't touch the fare.** Coins are the friction point in every township cash transaction — the driver has no change, the spaza rounds up, you lose R2–R5 a day and never think about it.
**Passenger:** zero behaviour change, change that doesn't vanish. **Driver:** never needs a coin float, keeps every note. **MTN:** a **cash-to-digital pump firing millions of times a day**, and every user gets a small credit *daily* — which is a daily reason to open MoMo. The dormancy problem solved as a side effect.
No taxi association negotiation. No R2,000/month terminal. No infrastructure.
**APIs:** Get Paid, Pay, Distribute, Notify, Interact (USSD for feature phones).
**Risk:** needs driver adoption. Counter: the driver benefit (no coin float) is immediate, selfish and requires no trust in the passenger.

### 3.2 · RANK — work with the marshals, not around them 🔒
**Verb:** *Pre-pay your route.*
Pay for your trip at the rank by QR or USSD, get a code, board. **Rank marshals — who already control the queues and already hold community authority — become the agents and earn commission.**
**Insight:** every failed taxi payment system tried to route around the industry's existing power structure. Anthony Stewart (Waxd) named the causes: political tension inside associations, systems that ignored operational reality, no education. **The winning move is to make the incumbent power structure the beneficiary.** Marshals aren't an obstacle; they're an untapped distribution network with existing trust.
**APIs:** Get Paid, Distribute ⭐ (marshal commission), Interact, Notify.
**Risk:** the hardest stakeholder problem in SA transport. But naming that in the pitch — and showing you designed *for* it — is exactly what separates you from the 14 who didn't.

### 3.3 · SETTLE — the e-hailing cash bridge 🔒⚡
**Verb:** *Pay the driver.*
**Over 80% of South African ride-hailing trips are paid in cash.** Drivers carry dangerous amounts of it, can't bank it easily, and get robbed for it. At the end of a cash trip the driver shows a QR; the passenger pays into MoMo; the driver cashes out at any of MTN's **1.4 million agents** when it suits them.
**Insight:** this is a *verified, enormous, documented* problem — Bolt published the number themselves — and everyone assumes e-hailing is already solved because the app has a card field. It isn't. Four out of five trips are cash.
**Bonus:** the driver's MoMo transaction history becomes a provable income record — the thing gig workers can't get.
**APIs:** Get Paid, Pay, Collection Widget (QR), Identify, Notify.
**Risk:** platform relationships (Uber/Bolt) not required for v1 — this works driver-to-passenger, outside the platform. That independence is a feature.

### 3.4 · TANK — the fuel wallet 🔒⚡
**Verb:** *Fill up.*
Ring-fenced fuel credit for taxi and e-hailing drivers: buy in advance, buy in bulk at a group discount, split fuel between owner and driver, price alerts before increases.
**Insight:** **one of the failed taxi payment systems died specifically because it couldn't pay for fuel.** Fuel is the largest and most volatile cost in a driver's week, and it's the missing half of every taxi solution ever attempted. Solve the *cost* side and drivers adopt willingly — no association politics required.
**APIs:** Get Paid, Pay, Get Consent (bulk buy mandate), Distribute, Notify.
**Risk:** fuel retailer integration. Mock with a partner forecourt; the argument stands regardless.

### 3.5 · PASSPORT — the roaming wallet 🔒
**Verb:** *Cross the border.*
Cross into another MTN market and your wallet re-denominates and becomes locally spendable: local data pre-loaded, cross-border bus ticket bookable, travel micro-insurance attached, settlement near interbank instead of **8.78%**.
**Insight:** MTN operates in **16 markets** and treats cross-border purely as *remittance* — a one-way diaspora pipe. It has never built anything for the people who physically move: cross-border traders (SA↔Zimbabwe↔Mozambique↔Zambia), students, seasonal workers.
**No competitor can copy this.** It requires MTN's actual physical footprint. The most unarguable strategic-fit idea on the board.
**APIs:** Remittances ⭐, Get Paid, Pay, Identify, Notify.
**Risk:** regulatory complexity across borders. Scope the demo to one corridor (SA→Zimbabwe) and be explicit about it.

### 3.6 · GOING HOME — intercity and cross-border bus
**Verb:** *Book your seat.*
Book and pay for long-distance bus and taxi travel in advance — with a guaranteed seat, especially for the December migration home.
**Insight:** millions of South Africans travel home each December and it is **cash at the rank, no booking, no seat guarantee, and price gouging at peak.** Seasonal, emotional, and utterly unserved by digital booking at the informal end of the market.
**APIs:** Get Paid, Invoice (layaway — pay for December travel across six months), Pay, Notify.
**Killer variant:** **December travel layaway.** Save for the trip home from July, seat locked. That's a mandate product wearing a mobility costume, and it runs all year.

### 3.7 · LIFT — formalise the lift club ⚡
**Verb:** *Join the lift.*
Recurring seat booking and automatic payment for the colleague-commute and student lift clubs that already run everywhere on cash and WhatsApp.
**Insight:** lift clubs are a huge, invisible, *already-recurring* behaviour. Recurring behaviour + Get Consent mandate = automatic weekly transactions with no new habit to teach.
**APIs:** Get Consent ⭐, Pay, Get Paid, Notify.
**Risk:** small groups, low value per transaction. Argue frequency and retention.

### 3.8 · BAKKIE — informal logistics with escrow
**Verb:** *Move it.*
Book a bakkie to move furniture, deliver stock to a spaza, or take goods to market. Payment held in escrow until proof of delivery.
**Insight:** informal logistics in SA is entirely cash, WhatsApp and trust — and the trust breaks constantly. Both sides are exposed: the driver fears non-payment, the customer fears non-delivery. **Escrow is the product.**
**APIs:** Get Paid, Pay (escrow release), Identify, Notify.
**Risk:** marketplace liquidity. Narrow to spaza restocking — a repeat, predictable route.

### 3.9 · COMMUTE — the transport envelope ⚡
**Verb:** *Ring-fence your fare.*
Pre-load and protect your transport money so you never reach month-end unable to get to work. Employers can pay a transport allowance directly into it.
**Insight:** **running out of taxi fare before payday is one of the most common and most damaging financial failures for low-income South African workers** — it costs people their jobs. Ring-fencing fare money is a small feature with a very large consequence, and the employer-disbursement angle gives you a B2B distribution channel.
**APIs:** Pay (employer disbursement), Get Consent, Manage, Notify.
**Risk:** overlaps Isikhwama (1.3). Run one or the other.

### 3.10 · BORDER — the Beitbridge problem 🔒
**Verb:** *Clear the border.*
Pre-pay customs and clearing fees, get forex at near-interbank, buy cross-border insurance, and hold your documents — before you reach the queue.
**Insight:** cross-border traders lose entire days at Beitbridge and Lebombo, get gouged on forex, and pay everything in cash to informal fixers. **MTN operates on both sides of these borders.** Extremely specific, extremely painful, and nobody serves it.
**APIs:** Remittances, Get Paid, Pay, Identify, Notify.
**Risk:** heavy regulatory surface. Position as a *payments and forex* layer, not a customs agent.

---

# SCORING

Scored 1–5 per criterion. Feasibility and Tech scored against the **real timeline** (team of 4, ~2.5 weeks + demo-day polish), not a 24-hour sprint. Max 40.

| # | Idea | Track | Innov | Relev | Feas | Tech | Pitch | Launch | Weekly | OnlyMTN | **TOT** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.3 | **SETTLE** — e-hailing cash bridge | 3 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | **38** |
| 3.1 | **CHANGE** — digitise the change | 3 | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 4 | **37** |
| 2.3 | **GIFT** — send data with a message | 2 | 4 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | **37** |
| 2.1 | **SHAYA** — tip the artist | 2 | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 3 | **36** |
| 1.2 | **MoMo SHIELD** — fraud defence | 1 | 5 | 5 | 3 | 4 | 5 | 5 | 3 | 5 | **35** |
| 1.9 | **NKOSI** — black tax, managed | 1 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 3 | **35** |
| 1.3 | **ISIKHWAMA** — envelopes | 1 | 3 | 5 | 5 | 5 | 4 | 5 | 5 | 2 | **34** |
| 1.4 | MANDATE | 1 | 5 | 5 | 4 | 4 | 3 | 4 | 4 | 4 | 33 |
| 1.1 | UBUNTU | 1 | 5 | 5 | 3 | 3 | 5 | 3 | 3 | 5 | 32 |
| 1.5 | METER | 1 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 2 | 32 |
| 2.6 | KASI KOS | 2 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 2 | 32 |
| 2.11 | HUSTLE | 2 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 3 | 32 |
| 2.10 | UMNIKELO | 2 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 3 | 32 |
| 2.8 | SHARE | 2 | 3 | 4 | 5 | 5 | 3 | 4 | 5 | 3 | 32 |
| 2.2 | SOCIETY | 2 | 3 | 4 | 5 | 5 | 4 | 4 | 5 | 2 | 32 |
| 3.9 | COMMUTE | 3 | 3 | 5 | 5 | 5 | 4 | 4 | 4 | 2 | 32 |
| 3.2 | RANK | 3 | 5 | 5 | 2 | 3 | 5 | 3 | 4 | 4 | 31 |
| 3.4 | TANK | 3 | 4 | 5 | 3 | 3 | 4 | 4 | 5 | 3 | 31 |
| 3.5 | PASSPORT | 3 | 5 | 4 | 3 | 3 | 5 | 4 | 2 | 5 | 31 |
| 3.6 | GOING HOME | 3 | 4 | 4 | 4 | 4 | 5 | 4 | 3 | 3 | 31 |
| 2.4 | LIGI | 2 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 2 | 31 |
| 1.7 | KASI OS | 1 | 4 | 5 | 3 | 3 | 4 | 4 | 5 | 2 | 30 |
| 3.7 | LIFT | 3 | 3 | 3 | 5 | 5 | 3 | 4 | 5 | 2 | 30 |
| 1.6 | SOUND MONEY | 1 | 5 | 4 | 3 | 3 | 5 | 3 | 3 | 3 | 29 |
| 1.8 | UMGALELO | 1 | 2 | 4 | 5 | 5 | 3 | 4 | 4 | 2 | 29 |
| 2.7 | ARENA | 2 | 4 | 3 | 4 | 4 | 4 | 3 | 4 | 2 | 28 |
| 1.10 | VOUCH | 1 | 3 | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 28 |
| 3.8 | BAKKIE | 3 | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 2 | 26 |
| 3.10 | BORDER | 3 | 4 | 4 | 2 | 3 | 4 | 3 | 2 | 4 | 26 |
| 2.5 | TICKET | 2 | 3 | 3 | 4 | 4 | 4 | 4 | 2 | 1 | 25 |
| 2.9 | GLOW | 2 | 3 | 3 | 4 | 4 | 3 | 4 | 3 | 1 | 25 |
| 1.11 | CLINIC | 1 | 3 | 4 | 4 | 4 | 3 | 3 | 2 | 2 | 25 |
| 1.12 | FEES | 1 | 2 | 4 | 4 | 4 | 3 | 4 | 2 | 2 | 25 |

---

# SYNTHESIS — the shortlist and the recommendation

## The pattern in the top five

Every idea above 35 does the same structural thing: **it converts an existing cash behaviour into a digital one without asking anyone to change their behaviour first.** Settle, Change, Gift, Shaya, Nkosi — none of them teach a new habit. They instrument one that already exists at scale.

That is also the single reason 14 taxi payment systems failed: they all required behaviour change before delivering value.

## The insight worth building the whole entry on

**SETTLE (3.3) and CHANGE (3.1) are the same idea at two points on the same curve.**

Both convert cash-in-hand into wallet balance **at the moment of a transport transaction** — the exact moment, millions of times a day, where South Africa's cash economy renews itself. Shop2Shop's CEO said it plainly: *"Once that layer is solved, cash will disappear."*

- **SETTLE** is the beachhead: **80%+ of ride-hailing trips are cash** (Bolt's own published figure), drivers are carrying dangerous amounts of it, and there are **no taxi associations to negotiate with.** Buildable now, demo-able now, verified problem.
- **CHANGE** is the vision: the same mechanic pushed into the minibus taxi and spaza economy, where the coin — not the fare — is the wedge.

Pitched together, you are not showing a feature. You are showing **a thesis about how cash actually dies in South Africa**, with a working product at the easy end of it and a credible path to the hard end. That is a launch-partner pitch, not a hackathon project.

Add the kicker: every cash trip settled through MoMo builds the driver a **provable income record** — the thing 2 million gig workers cannot get and the gateway to every financial product MTN wants to sell them.

## Recommended shortlist

| Slot | Pick | Why |
|---|---|---|
| 🥇 **Primary** | **SETTLE + CHANGE** as one Track 3 entry | Highest score, verified problem, unarguable strategic fit, a thesis rather than a feature, and demo-able end to end |
| 🥈 **Backup / if Track 3 feels crowded** | **GIFT** (2.3) | Track 2 is the whitest space in the competition's history; MTN is the merchant so the revenue case is instant; viral by construction |
| 🎭 **Highest-drama demo** | **SHAYA** (2.1) | You can put a live performer in front of the judges and have the room tip in real time. Nobody forgets that. |
| 🧠 **Most defensible moat** | **SHIELD** (1.2) | The only idea no competitor can physically copy — but depends on SIM-swap data access MTN may not expose |
| ❤️ **Most emotionally resonant** | **NKOSI** (1.9) | Every young earner in that room knows what black tax is. Nobody has built it. |

## Open decisions for the team

1. **One track only** — the form forces a choice. Recommendation: **Track 3**.
2. **Settle-only, or Settle-as-beachhead-with-Change-as-vision?** The second is a better pitch and barely more build.
3. **Do we need driver-side and passenger-side, or is one side enough for the demo?** (Recommend both — it's what proves it's real.)
4. **Team name.** Format is `South Africa-XXX`.
5. **250-character summary.** Hard limit. Draft once the concept is locked.

## Deliberately not chosen — and why

- **Lending in any form** (Ubuntu, Kasi OS credit, Hustle credit): there is no lending track in 2026. That is a signal, not an oversight.
- **Ticketing, beauty, generic marketplaces**: crowded, low only-MTN score, no structural advantage.
- **Rank (3.2)** despite a brilliant insight: the stakeholder problem is genuinely unsolvable in three weeks, and a demo that depends on taxi-association buy-in will be read as naïve by Johannesburg judges who have watched 14 attempts fail.

---

## NEXT SESSION
1. Lock the track and the concept
2. Write the user journeys (passenger side + driver side)
3. Map every screen to a specific MoMo API call
4. Draft the 250-character summary and the detailed description for registration
5. Set up the repo + get MoMo sandbox credentials
6. Get the organisers' written answer on pre-building
