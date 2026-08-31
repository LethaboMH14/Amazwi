# AMAZWI — THE PITCH
### Stage choreography · slides · demo script · judge Q&A · fallbacks

**Parent:** `00_MASTER_PLAN.md` · **Written:** 2026-08-30

---

## 1. WHAT THE JUDGES ACTUALLY WANT

Three of the five official criteria are non-code — Innovation, Relevance, Presentation. At a 24-hour event with a dozen demos, **the room's memory is the scoring mechanism.** Judges deliberate on what they can repeat to each other, not on your architecture.

They will have watched eleven other people say *"let me show you our app."* By the time you present, the room is saturated. The entry that wins is the one that **changes what is happening in the room**, not the one with the best slides.

And behind the rubric sits one unstated question:

> *Could this be app #1 on the MoMo shelf in Johannesburg in six months?*

MTN bought the shelf from Ant International in June 2026. The shelf is empty. **They are recruiting supply.** So do not present as a science project. Present as a launch partner who has already thought about their business.

---

## 2. THE STRUCTURE — five minutes

> **The governing decision: do not demo the app. Make the room use it.**
>
> Everyone present scans a QR code and plays. Ninety seconds later the room has generated real speech, a real leaderboard has formed on the big screen, and a sandbox disbursement has resolved end to end on a judge's screen. Nobody else in that building will do anything remotely like this — and it is the summit's own theme, *"As One,"* made literal instead of quoted.
>
> 🔴 **Never say "real money moved."** MTN's own sandbox documentation states it *"will not process real money,"* and you will be saying this to the engineers who built it. Overselling to the people who own the rail is the fastest credibility loss available in that room. The honest version scores higher — see §3 at 2:30.

| Time | Beat | Who |
|---|---|---|
| 0:00–0:20 | **The sound** — the problem, heard not stated | Lethabo |
| 0:20–0:50 | **The turn** — one sentence, the whole product | Lethabo |
| 0:50–2:30 | **The room plays** — live, everyone, a payout resolving on screen | Both |
| 2:30–3:30 | **The proof** — receipt, wallet, console | Sbu |
| 3:30–4:30 | **The business** — who pays, and why MTN wins | Sbu |
| 4:30–5:00 | **The close** — the archive fills; the ask | Lethabo |

---

## 3. THE SCRIPT

### 0:00 — OPEN WITH SOUND, NOT STATISTICS

Do not open with unemployment figures. Every social-impact pitch opens with a statistic and the room has stopped hearing them.

**Play a ten-second clip** of a South African speaking isiXhosa naturally — conversational, code-switched, the way people actually talk. Then:

> *"Hands up — who understood that?"*

Hands go up across the room. Wait for it. Let them look at each other.

> *"Now here's what the world's best speech recognition heard."*

Cut to the transcript. It is garbage. Let it sit for two full seconds.

> *"Every person in this room understood her. The machine didn't come close. That's a 56.71% word error rate on isiXhosa. A human listener gets 9.6%."*

You have now made the problem physical, made the room participants rather than audience, and earned the right to one statistic — which lands because they felt it first.

---

### 0:20 — THE TURN

> *"And it's worse than it looks. Whisper — the model most of the world runs on — scores a hundred and forty-six percent word error rate on Southern Bantu languages. Two hundred and twenty-three percent on Setswana. Those aren't bad scores. Above a hundred percent means it invents more words than it gets right. For ten of our eleven spoken official languages, there is no working speech recognition at all."*
>
> *"That's not a modelling problem — Google has better models than anyone. Earlier this year Google released WAXAL, a major African speech dataset. It covers no South African language. Not one. They funded East and West Africa and skipped us."*
>
> *"There is almost nothing to learn from, and no reason for a South African to give their voice away for free."*
>
> *"So we built the reason."*
>
> **"AMAZWI is the describe-it-without-saying-the-word game — you know the one — in your own language, against the whole country. Speaking pays you. Listening teaches you. And what comes out is the speech data this country has never had."**

⚠️ ***"You know the one"* is the whole trick.** Every South African in that room fills the blank themselves, so you get the instant recognition without ever saying a registered trade mark aloud in a recorded commercial pitch. If someone says the name back to you in Q&A, that is them, not you.

Stop. Do not explain further. If the sentence needs explaining, it is the wrong sentence — and this one does not.

---

### 0:50 — THE ROOM PLAYS

**QR code, full screen.**

> *"Everyone — cameras out. You've got sixty seconds, and I need a judge up here."*

> 🔴 **The QR must open a GUEST PATH, not the onboarding.** One screen, one consent line — *"you're guessing only, we record nothing"* — no age gate, no MoMo link, no language multi-select, no five consent toggles. Guessing collects no personal information, so the consent burden genuinely is near-zero, **and saying that out loud is a stronger ethics beat than the toggles are.** Without this, most of the room is still on the consent screen when your timer ends and the counter reads 7, not 52. `05_BUILD.md` G2.

**The sequence — note step 3, which is the fix that matters:**
1. The judge's phone shows a card — a word in the language *they* chose, with four banned words.
2. They get 30 seconds and describe it. **Into the phone, not the room.**
3. 🔴 **The room plays the recording on their own phones and guesses.** *(There will be laughter. That laughter is your Innovation score.)*
4. Results resolve: *"41 of 52 people understood you."*

> **Why step 3 is not optional.** In the obvious version the room simply hears the judge speaking aloud and guesses from that — which demonstrates a party game, not your product. **The product is a stranger, later, somewhere else, playing back a clip.** Making the room listen to the *recording* shows the actual thing, is more impressive, and pre-empts the sharp judge who notices that you never demonstrated asynchronous matching.
5. **The reward moves.** Pending → available → disbursement submitted → resolved, with the provider reference visible.
6. The judge's ward or the room's team climbs the league.

**Then, while it is still on screen — and say it exactly this way:**
> *"That's a sandbox disbursement. The sandbox doesn't move real rands and we're not going to tell you it did. What's real is the state machine: the reference is persisted before the call, a 202 means submitted and not paid, and if you fire it twice no extra money exists. Point it at production and nothing changes but a header."*
>
> *"And what's completely real is the rest of it — the recording, the peer validation, the consent record. Fifty-two people just produced South African speech that did not exist ninety seconds ago."*

---

### 2:30 — THE PROOF *(Sbu)*

Three screens, thirty seconds each. Speak to the engineering, not the vision.

**① The Voice Value Receipt.** Contribution ID, clarity score, coverage contribution, reward and its published basis, consent version, MoMo reference, archive number.
> *"One screen that proves four things at once: what was said, what it was worth, who agreed to it, and where the money went."*

**② The wallet.** Pending, available, paid — three distinct states.
> *"We never show 'paid' until the provider says paid. A request accepted is not money moved. Our ledger is append-only, in integer cents, and idempotent — repeat the approval or the payout call and no extra money exists. We tested that adversarially."*

**③ The Impact Console.** Coverage by language, validated minutes, acceptance rate, active-consent corpus, cost per validated minute, and the next language the budget should fund.
> *"This is the buyer's view. It prices a data gap and tells you where the next rand should go."*

**The honesty beat — deliver it deliberately. This is the paragraph that wins Technical Execution.**
> *"Here's what our AI does and doesn't do. It checks that a submission is real, audible, unique, human-sounding speech of adequate quality — before a cent is paid for it. It does **not** transcribe it, because no system on earth transcribes isiZulu reliably today. That's the gap we're collecting the data to close."*
>
> *"And we have not improved anyone's word error rate today. You can't do that in twenty-six hours, and anyone who tells you otherwise is showing you a slide, not a training run."*

**Then the number that pays it all off:**
> *"But here is what an hour of speech is worth. On the published benchmarks, isiZulu goes from a hundred and forty-six percent word error rate to about twenty-five — **on one hour of real in-domain data.** Fifty hours gets you to eight. When the baseline is broken, the first hour is worth more than the next thousand. That's the whole argument for paying people to produce it."*

Judges are used to being oversold. Precision disarms them, and the honest version of this story is stronger than the exaggerated one.

---

### 3:30 — THE BUSINESS *(Sbu)*

**The two-sided market — one diagram, ten seconds:**
```
LEARNERS & SPONSORS  ──pay──▶  MoMo  ──earn──▶  SPEAKERS
                                 │
                                 └──▶ consented corpus ──▶ MTN
```

### 7a · 🔴 THE INBOUND LEG — build it, or change the sentence

*"Money crosses MoMo twice"* is the central strategic claim of this entire entry. It carries the Track 2 defence, the sweatshop defence, the Duolingo defence and the fintech-relevance argument — **four separate answers resting on one flow.**

**And the build has seventeen items, not one of which collects money from anyone.** A judge who asks *"show me someone paying"* ends four arguments with one question.

**Build it — one screen, ~90 minutes, and it is worth displacing the story chain for.**
> **"Sponsor a language — R20 funds 10 clips of Tshivenda."**

Use MoMo **Collections** `requesttopay`, which is one of the few confirmed-live sandbox products and is better documented than Disbursement. One payment in, credited to a named campaign, spending down live on the Impact Console while the room watches. Then the line becomes true, and it is the best line in the pitch:

> *"Money crossed MoMo twice just now — in from a sponsor, out to a speaker. We settled both legs. That's not a payment button bolted onto an app; that's a rail with a spread on it."*

**If it does not fit, change the sentence** — do not keep it and hope. The honest version still scores:
> *"Today the outbound leg is real and the inbound leg is designed. Learners are free while we learn what they'd pay for — and we'd rather tell you that than invent a subscription price we can't defend."*

**Then the four reasons MTN wins.** Delivered fast, in this order — the fourth is the one that lands.

1. **A daily-open lifestyle loop**, which is exactly what an empty mini app shelf is short of.
2. **MoMo is structurally necessary.** Cent-scale two-sided settlement is impossible on card rails — the interchange exceeds the payment. Remove MoMo and there is no product.
3. **It builds the asset MTN's own CEO has said Africa cannot do without.** Ralph Mupita, at MWC this April, on getting Africa's 2,000-plus languages into large language models: Africa *"cannot afford to be left out of the AI era."* MTN has said that. MTN does not own a language asset.
4. **MTN is its own first customer.** Every other data play has to go and find a buyer. This one starts inside the building — MTN South Africa runs customer service in a country where English is the fifth home language.

**And the number that should close it:**
> *"MoMo South Africa has thirteen million registered users. In the 2020 relaunch, about eight percent of registered users were active. Your problem in this market isn't sign-ups — it's daily reasons to open the wallet. We are a daily reason."*

That reframes AMAZWI from a cost centre to a **MoMo SA activation product**, which is a live commercial problem the people in the room actually own.

---

### 4:30 — THE CLOSE *(Lethabo)*

Bring the **Archive** up on screen. The map of South Africa, filling with the points this room just created.

> *"In the last four minutes, this room created [N] seconds of South African speech that did not exist when we walked in. It's in the archive. Every one of you is credited. You can withdraw it tonight if you want to — that's built."*

Beat.

> *"South Africa has twelve official languages. One of them has a single fluent speaker left. When she stops speaking, it stops existing. We are not going to pretend an app fixes that."*
>
> *"But it does force the question underneath it: **what is a language worth, and who gets paid for it?**"*

> ⚠️ **Do not add her name, her age, or anything about her finances.** There is exactly one such person and every South African in that room knows who she is — not naming her is not anonymising her. Asserting an identifiable, elderly, non-consenting person's financial circumstances in a commercial pitch, for a prize, on video, is precisely the extraction this product claims to oppose, and a cultural-sector judge will feel it instantly. The version above carries the same force with zero exposure, and every word of it is verified. This also contradicts your own instruction in `01_PRODUCT.md` §2 Mode 6 — that instruction was right.

Final line — deliver it slowly:

> *"MTN is building a hundred and fifty megawatts of AI data centres in South Africa. We think that's the right bet. But a data centre is a room full of machines waiting to be taught something."*
>
> **"AMAZWI is how you teach them to understand the people outside the building."**

**Then stop talking.** Do not add a thank-you slide. Do not summarise. Let it land.

---

## 4. THE SLIDES

Ten slides maximum. The app is on screen for most of the five minutes; slides are punctuation.

| # | Slide | On screen |
|---|---|---|
| 1 | **The clip** | Waveform, then the mangled transcript |
| 2 | **The sentence** | One line of type on black |
| 3 | *(live app — no slide)* | The game |
| 4 | **Receipt** | Real screenshot |
| 5 | **Wallet states** | Real screenshot |
| 6 | **Impact Console** | Real screenshot |
| 7 | **The loop** | The two-sided diagram |
| 8 | **Why MTN** | Four lines, no paragraphs |
| 9 | **What we did not build** | The honest scope list |
| 10 | **The Archive** | The map, live, on screen through the close |

**Slide 9 is not a weakness.** Volunteering your limits before you are asked is the highest-trust move available and it inoculates you against the whole Q&A. Three bullets: *no model retrained today · two languages quality-assured, not twelve · sandbox disbursement, labelled.*

---

## 5. SPEAKING OWNERSHIP

| | **Lethabo** | **Sbu** |
|---|---|---|
| Owns | Story, opening, live game, close | Proof, engineering, business, architecture |
| Answers | Product, design, ethics, culture | Money, ledger, MoMo, data, security |

**Both must be able to run the entire demo alone.** One of you will be holding a phone, resetting a device, or fixing the projector at the moment the other needs to be talking. Rehearse the whole thing solo, twice, each.

---

## 6. FAILURE PLAN — rehearse these, do not improvise them

| What breaks | The move |
|---|---|
| **Venue wifi dies** | ⚠️ **A phone hotspot is NOT a fallback for the room** — iPhone carries ~5 clients, Android ~10. It is a fallback for the judge-only demo and nothing else. Drop to the judge-only path immediately, then **seeded mode** — simulated listeners fill the guess slots so the loop completes visibly. Say it: *"we're on simulated listeners, the wifi is gone."* |
| **Only part of the room gets in** | **The most likely failure, and the one that needs a rehearsed line.** *"Half the room got in — that's a hackathon wifi problem, not a product problem. Here's what the eleven who did just produced."* Then keep moving. **The unrehearsed recovery is the failure; the failure itself is survivable.** |
| **Nobody in the room scans** | Sbu and two pre-briefed friends are already in and playing **before the QR goes up**, so the counter is never zero. |
| **iOS Safari plays no audio** | Safari needs a user gesture per audio context and blocks autoplay. The guest screen's first tap must arm the audio context. Test on a real iPhone Monday — a chunk of the room hearing nothing and saying so out loud is a public failure. |
| **MoMo sandbox is down** | The provider adapter's demo implementation, **clearly labelled on screen**. Say it: *"sandbox is down, this is our demo provider, the state machine is identical."* Do not pretend. |
| **Sandbox quota exhausted** *(higher probability than "down", and the cooldown is ~2 days)* | Same move, said out loud. This is why the reserve API user exists and why the 30-call budget is on the wall. `05_BUILD.md` §2.2 |
| **Recording fails on the judge's phone** | Record on your own device and continue. Never make a judge feel they broke it. |
| **The judge is shy** | Ask for a volunteer from the room first; a judge who has watched someone else enjoy it will step up. |
| **Overrunning** | The compressible sections are the business (3:30) and the proof (2:30). The open, the live game and the close are never cut. |
| **Total technical failure** | A 90-second screen recording of the full loop, on the local drive, on both laptops, plus a phone. Rehearse the sentence: *"the network's gone — here's the same flow recorded twenty minutes ago"*, and keep going without apologising. |

**Rehearse the whole run four times minimum**, at least once with something deliberately broken.

---

## 7. JUDGE QUESTIONS

### "Isn't this just paid data labelling with a leaderboard?"
No — and the difference is structural, not cosmetic. Nobody in AMAZWI reviews anything. There is no approve button. Quality comes from strangers *guessing*, and a guess is only correct if the speech was genuinely intelligible. That is the ESP Game mechanic applied to speech. And the other half of our players are language learners who earn nothing — they play because guessing what a native speaker just described is how you learn a language. A labelling platform cannot have that population.

> 🔴 **Say "learners are free today," not "learners pay to be there" — unless you have actually built the inbound leg.** See §7a. Claiming a paying population that does not exist, at a price you have correctly declined to invent, is the one place in this pitch where you would be inventing a fact.

### "Common Voice and Swivuriso already exist. Why do you?"
They are valuable and we seed from them. They are also static, read-aloud and thin on exactly what is missing: conversational, code-switched, regional, current speech. Read-aloud corpora are easy to collect; that is why they exist. AMAZWI is a *continuous acquisition layer* with per-contributor consent lineage — which no existing corpus has, and which is what makes it licensable rather than merely academic.

### "Duolingo already tried South African languages. It didn't work."
True, and it is the sharpest version of this question. Duolingo launched isiZulu in 2022 with Nal'ibali and Vodacom, **dropped isiXhosa in 2023 for low engagement**, and has never shipped Afrikaans. But look at *why*: Duolingo's model is solo drilling against content a small team has to author, for a language where they had no content pipeline and no native-speaker supply. Ours inverts that. **The content is generated by the speakers, and they get paid to make it.** You are not practising against a course someone wrote in Pittsburgh — you are trying to understand a real person in Khayelitsha, right now, who earns when you understand them. That is a supply model Duolingo does not have, and it is exactly why they retreated.

### "How is this Entertainment and Lifestyle?"
It is a party game. You just watched the room laugh. The earning is a feature; the category is the game. And a language product is a lifestyle product in a country with twelve official languages where most people are multilingual.

### "You said nothing transcribes isiZulu. So how do you know the speaker didn't just say the word?"
**This is the question that kills the mechanic if you have not prepared it. Answer it before it is asked.**
> *"We can't transcribe it — so we don't try. The room referees. After the answer is revealed, every listener gets one tap: did they say it? Both listeners agreeing that you cheated voids the round — no reward, and your clarity score takes the hit. That's the same agreement primitive that validates the clip, pointed at the rule instead. And we keep them honest with gold cards: one in eight clips is a seeded one that does say the word, and if you wave it through, your rewards stop."*
>
> *"It's peer-reported, not machine-verified. We'd rather build the verifier — but building it needs the data, and getting the data is what this is."*

### "Will people game it?"
They will try. The mechanic makes it expensive: a speaker earns only when randomly-assigned strangers understand them, and listeners are paid **for judging, not for being right** — so there is nothing to converge on and no shared answer to collude toward. To farm the speaker side you would have to collude with people you cannot choose. On top: gold honeypots, no self-review, a hard R11/day cash ceiling per account, device and account rate limits, duplicate-audio hashing, one account per verified MoMo identity, and an append-only ledger. **We do not claim it is unbreakable — we claim breaking it costs more than it pays, and a stolen account is worth eleven rand a day.**

### "Isn't this a digital sweatshop?"
Raise this yourself before they do. Rates are published before the task and never cut retroactively. Consent is versioned and revocable. Contributors are credited by name in a public archive. Adults only. And critically, we designed the game to be fun with the money switched off — because if payment is the only reason to play, quality follows the money down. The literature on motivation crowding-out is clear about that and we built against it.

### "Can someone withdraw consent after being paid?"
Yes. Money already earned stays theirs. New contributions are blocked, and the recording is excluded from future exports and training runs. We will not claim we can un-train a model that has already seen it — that is not how models work, and anyone promising it is misleading you. We handle it with a declared retirement and retraining policy.

### "Is this actually a Mini App? Because that looks like a website."
**Say it before they do — the room just played a PWA outside the MoMo shell, and the whole "app #1 on the shelf" argument is otherwise being made from a website.**
> *"What the room just played is the PWA build — same bundle, same API. The Mini App shell is the authentication wrapper: you arrive already logged in via `START_JOURNEY`, which hands us the MSISDN and a session token, and we keep it alive with the heartbeat. We've built to the integration spec — it's open on the second laptop. What you're looking at is what would sit on the shelf."*

### "How do you decide an isiZulu free-text guess is correct?"
> *"Per card, not per language. Each card carries an accepted-answers array built with a first-language speaker — the target, its morphological variants, the noun-class forms, and the code-switched English equivalent. We normalise, strip a whitelisted set of prefixes, and allow an edit distance of two for typos. For today's demo the listener input is multiple choice, which is deterministic — free text is the advanced mode, and it's the only mode that validates the corpus."*

That answer shows you know why the question is hard. *(`02_TECH.md` §3.4.)*

### "Is your challenge targeting active learning? Does it beat random selection?"
**This is one of the strongest answers in the plan and it currently lives buried in a tech document. Get it into the room.**
> *"The selection policy is in place — we score every utterance by model confidence and acoustic novelty and surface a prioritised re-collection queue. Whether it beats random selection is an open question we have not powered a study to answer. The literature is genuinely mixed: uncertainty sampling can underperform random for ASR because uncertainty correlates poorly with word error rate. We'd need multiple runs, multiple seeds and a test set with real power. So we built the mechanism and we're not claiming the result."*

### "How does MTN actually make money?"
Five lines, ranked by how soon they are real: MoMo SA activation and daily wallet engagement; learner subscriptions and corporate language packages; sponsored acquisition campaigns; governed model and API access; and internal value — MTN's own call-centre deflection and a MoMo voice interface that works in isiXhosa. Full pricing in `03_BUSINESS.md`.

### "Did the model improve?"
No, and we are not going to say it did. In twenty-six hours we can honestly show acquisition, validation, coverage and consent. Word error rate moves after a real training run against a fixed test set with a named model version. We would rather show you a real coverage curve than a fake WER curve.

### "It's Tuesday in Thohoyandou. I record a Tshivenda clip. How long until anyone hears it?"
**The cold start is the real hard problem and the demo hides it completely — 52 people in one room is the most favourable matching condition that will ever exist. Say it first.**
> *"That's the hard problem, and it isn't the game — it's liquidity. A clip needs listeners who speak that language. Two things follow. One: we launch two languages, not twelve, and the first cohort is a place, not a country. Two: if a clip doesn't get two listeners in 48 hours we pay you anyway, at half, and we tell you why — 'not enough Tshivenda listeners yet, we're going to go and find them.' We'd rather carry that as an acquisition cost than leave a promise unpaid on someone's screen."*

### "How does this scale to other MTN markets?"
The loop is constant; language packs, consent text, reward configuration, regulatory rules and card content change per market. Nigeria has over 500 languages and is where the Ant International mini app platform launches first. Expansion is configuration plus local governance — not a claim that South Africa copies over unchanged.

### "What did you build today versus before?"
Answer this one plainly and without defensiveness. Have the exact answer agreed and identical from both of you before you walk in — see `05_BUILD.md` §1.

---

## 8. THE ASK

Do not end on "thank you." End on a specific, small, credible request. It signals you have thought past the prize.

> *"Three things. Put us in front of the MoMo South Africa activation team — we think we're an answer to the registered-versus-active gap. Give us a zero-rating conversation, because an income product that costs data to use isn't one. And tell us what language MTN's own call centre needs first — we'll go and get it."*

That is what a launch partner sounds like.
