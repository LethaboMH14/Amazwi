# AMAZWI — MODEL ROUTING
### When Lethabo switches Claude · when Sbu switches Codex · and why the boundary is the same for both

**Written:** 2026-08-31 · **Applies from:** now through demo day

> ⚠️ **On the Codex tiers.** Sol / Terra / Luna and their capability ordering are Sbu's setup as described to me — **I have not verified what those models are or how they compare.** The routing below is built on **task type**, which is the part that actually determines the answer. Slot your models into the tiers; if the mapping is wrong, fix the mapping, not the tiers.

---

## 1. THE ONE PRINCIPLE

Everything below follows from this. If you remember nothing else, remember this:

> ### Route by **how expensive it is to be wrong**, and **whether a machine can tell you that you are wrong.**

| | Can a machine check it? | Cost of being wrong | Tier |
|---|---|---|---|
| Tests pass · typecheck · lint · a hash matches | **Yes, instantly** | Near zero — you find out in seconds | **BUILD** |
| Code against a written spec | Mostly — the spec says what right looks like | Low — caught at integration | **BUILD** |
| Wiring two components together | Partly | Medium — surfaces at the seam | **MID** |
| Architecture · data model · state machines | **No** | High — you find out at 03:00 Thursday | **TOP** |
| A number, a claim, a legal position, anything on a slide | **No** | **Highest — you find out on stage** | **TOP** |

**The trap to avoid:** routing by how *important the project feels*. Everything about AMAZWI feels important. A determinism check is still a BUILD task, and a pricing claim is still TOP even though it's one sentence.

---

## 2. THE TIERS

| Tier | Lethabo (Claude) | Sbu (Codex) | Effort | Use for |
|---|---|---|---|---|
| **TOP** | **Opus** | **Sol** | high → ultra | Judgement work. Wrong is expensive and invisible until later |
| **MID** | **Opus low** or **Sonnet high** | **Terra** | medium → high | Integration, review, anything with a seam |
| **BUILD** | **Sonnet** | **Luna** | light → medium | Verifiable work against a settled spec |

### Effort inside a tier
Effort is the **bigger lever than model choice** and the one usually left at default. Move it before you move tiers.

| Effort | When |
|---|---|
| **light** | Mechanical and checkable — rename, format, move a file, write a test for behaviour that already exists |
| **low** | Single-file changes against a clear spec |
| **medium** | **The default for building.** Multi-file, spec exists, integration is straightforward |
| **high** | **The default for judgement.** Architecture, review, anything adversarial |
| **ultra** | Reserve it. A genuine dead end, a contradiction you cannot resolve, or the pitch's load-bearing argument |

> **Do not run ultra by default because the project matters.** Ultra on a task a machine could verify is waste, and it slows the loop that catches your actual mistakes.

---

## 3. AMAZWI, PRIORITY GATE BY PRIORITY GATE

`05_BUILD.md` deliberately uses priority gates rather than a timed schedule. **Both of us switch at the same boundaries** — that is the point.

| Gate | Work | Tier | Effort |
|---|---|---|---|
| **Pre-build** | Theme choice, content design and any business-claim review | **TOP** | high |
| **A** | Running shell, deploy, health check and host/browser-mode label | **BUILD** | light |
| **B** | Seeded endpoints, screens wired and deterministic reset | **BUILD** | medium |
| **C** | Consent enforcement logic | **MID** | high |
| **C** | Consent screens against the settled spec | **BUILD** | medium |
| **D** | Recorder, quality gates and upload | **BUILD** | medium |
| **E** | `is_correct`, two-verifier resolution, referee, `EXPIRED` | **TOP** | high |
| **E** | Verifier UI once resolution is settled | **BUILD** | medium |
| **F** | Ledger, idempotency, reward credit and provider state | **TOP** | high |
| **F** | Wallet and receipt UI against existing endpoints | **BUILD** | medium |
| **G** | Collections proof or labelled funded seed | **MID** | high |
| **H** | Rate limits, consent-export check, rehearsal, screenshots and deck claims | **TOP** *(for claims)* | high |

### The two gates that are TOP no matter how late it is
**E** (the resolution logic is the product), **F** (money, and wrong is invisible until someone is paid twice), and **anything that becomes a claim on a slide.** If you are tempted to drop these to BUILD because you are tired, that is exactly when the tier exists.

---

## 4. THE FOUR TRIGGERS TO GO BACK UP MID-BUILD

You will be on BUILD for most of the event. Come back up when:

1. **The spec turns out to be wrong or ambiguous.** That is a decision, not a bug. Do not let a build-tier model guess at a decision.
2. **A design or UI direction is genuinely open.**
3. **Something is about to be claimed** — a number, a benchmark, a sentence on a slide.
4. **You have been stuck on the same failure for 20 minutes.** Being stuck usually means the model is solving the wrong problem, and that is a judgement failure, not an effort failure. **Go up a tier before you go up an effort level.**

**Say it out loud in the log** when you switch, both directions. `↑TOP` and `↓BUILD` in the entry.

---

## 5. WHAT NEITHER TIER DECIDES

Some things are not a model's call at all, whatever tier:

- **Money, legal and consent decisions** — Sbu breaks ties, per the role split
- **Product and experience ties** — Lethabo breaks ties
- **Anything that goes on a slide** — verified against `07_TRUTH.md` first, by a human
- **Whether to install a tool during the competition** — read it first, both agree

---

## 6. THE HANDOFF SENTENCE

When one of us hands work to the other, or to a lower tier, the handoff carries three things or it is not a handoff:

```
WHAT   the thing to build, in one sentence
SPEC   where the spec lives (file + section) — if there isn't one, this is a TOP task, not a handoff
DONE   how we will know it worked (a test, a screen, a state transition)
```

If you cannot write `SPEC`, you are not ready to hand off. **Go up a tier and write the spec first.**
