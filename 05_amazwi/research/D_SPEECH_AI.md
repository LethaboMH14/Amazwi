# D — SPEECH AI FEASIBILITY: AMAZWI

**Compiled:** 2026-08-31
**Scope:** ML feasibility for a South African voice-data game. Constraints: 2× Kaggle accounts (~30 GPU-h/week each, T4×2 or P100 16GB, 9–12h session cap), in-browser processing on mid-range Android, build window of 2 days + a 24h hackathon.

## Evidentiary conventions used in this document

- **[MEASURED]** — a number from a peer-reviewed or preprint paper, or a model card, with the source linked.
- **[VENDOR]** — a claim made by the party selling or promoting the thing. Not independently verified.
- **[ESTIMATE]** — a planning figure derived by me from stated reference points. **Not measured.** Must be calibrated by an actual timing run before it is used in a plan or quoted to anyone.
- **[NO PUBLISHED BENCHMARK]** — I looked and did not find one. This appears more often than is comfortable.

Every model named carries its licence. **CC-BY-NC and other non-commercial licences are flagged and excluded from the recommended stack**, per the commercial-pitch constraint.

---

# 1. SA LANGUAGE ASR — STATE OF THE ART, 2026

## 1.1 The headline: foundation models fail zero-shot on SA languages, and it isn't close

The single most important measured fact for this project:

| Model | Zero-shot WER, Southern Bantu | Source |
|---|---|---|
| Whisper large-v3-turbo | **146.30%** | [arXiv 2606.31642, Table 3](https://arxiv.org/abs/2606.31642) [MEASURED] |
| MMS-1B-all | **112.98%** | [arXiv 2606.31642, Table 3](https://arxiv.org/abs/2606.31642) [MEASURED] |
| Whisper large-v3-turbo, Setswana | **223.0%** | [Swivuriso, arXiv 2512.02201](https://arxiv.org/abs/2512.02201) [MEASURED] |
| Whisper large-v3-turbo, Xitsonga | **190.0%** | [Swivuriso, arXiv 2512.02201](https://arxiv.org/abs/2512.02201) [MEASURED] |

WER above 100% means the model emits more insertions+substitutions+deletions than there are reference words — it is hallucinating fluent text in the wrong language. **Off-the-shelf Whisper on isiZulu or Setswana is not "poor accuracy". It is non-functional.** Any product design that assumes a pretrained ASR baseline for these languages is built on nothing.

This is the finding that should shape the whole AMAZWI architecture: the product cannot lean on transcription quality on day one. It must be designed so that value accrues from *collection and validation*, not from transcription.

## 1.2 Post-fine-tuning WER (the achievable target)

**Swivuriso** — [arXiv 2512.02201](https://arxiv.org/abs/2512.02201), DSFSI / Marivate group, dataset **CC-BY-4.0**, [HF: dsfsi-anv/za-african-next-voices](https://huggingface.co/datasets/dsfsi-anv/za-african-next-voices).

Per-language dataset size [MEASURED, Table 2]:

| Language | Hours |
|---|---|
| isiXhosa | 504.28 |
| isiZulu | 502.85 |
| Sesotho | 503.58 |
| Setswana | 502.18 |
| Xitsonga | 500.15 |
| isiNdebele | 251.86 |
| Tshivenda | 250.89 |
| **Total** | **~3,000** |

Fine-tuned results [MEASURED]:

| Setting | WER |
|---|---|
| Setswana, Whisper-large-v3-turbo FT | **13.0%** (from 223.0% zero-shot) |
| Xitsonga, Whisper-large-v3-turbo FT | **12.0%** (from 190.0% zero-shot) |
| Multilingual baseline, Whisper-large-v3-turbo, 10k steps | **0.15 WER** |
| Multilingual baseline, W2v-BERT 2.0, 10k steps | **0.17 WER** |
| Multilingual baseline, MMS-1B-all, 10k steps | **0.32 WER** |

Reported FT config: effective batch size 32, bfloat16, LR 1e-4 (Whisper) / 5e-5 (W2v-BERT) / 3e-4 (MMS), 2,000–10,000 steps. **GPU type and wall-clock not stated in the paper.**

**Tone-Conditioned Curriculum Learning** — [arXiv 2606.31642](https://arxiv.org/abs/2606.31642), six Southern Bantu languages, evaluated on both Swivuriso and NCHLT [MEASURED]:

| Language | Best model | WER (Swivuriso) | WER (NCHLT) |
|---|---|---|---|
| isiZulu | W2V-BERT | **24.79%** | **34.63%** |
| isiZulu | Whisper | 28.12% | 39.48% |
| isiXhosa | W2V-BERT | **26.06%** | — |
| isiXhosa | Whisper | 30.73% | — |
| Sesotho | Whisper Multilingual | **23.30%** | — |
| Sesotho | W2V-BERT (best setting) | 24.53% | — |
| Setswana | Whisper Tone+Curriculum | **18.60%** | 27.54% |

Trained on **2× NVIDIA A100 80GB**. Note the Swivuriso dev+test split used here is only **26.7 hours**; per-language training sets ranged **1,192–4,939 utterances**.

**The architecture split is real and actionable:**
- **Nguni languages (isiZulu, isiXhosa, siSwati, isiNdebele): W2V-BERT 2.0 beats Whisper by 3–4 WER points.**
- **Sotho-Tswana languages (Sesotho, Setswana, Sepedi): Whisper beats W2V-BERT.**

No single model wins across all six. This is a genuine, citable, non-obvious finding and it is worth building into the product as a routing decision.

Note the tension between the two papers on Setswana: Swivuriso reports 13.0% FT, the curriculum paper reports 18.60% best. Different splits and setups. **Quote the range (13–19%), not a single number.**

## 1.3 Data-scaling curve on NCHLT (the most useful table for budgeting)

[arXiv 2512.10968, "Benchmarking ASR Models for African Languages"](https://arxiv.org/abs/2512.10968), Nahabwe et al. All **fine-tuned** on NCHLT read speech. Format below is WER/CER [MEASURED]:

| Language | Hours | XLS-R 300M | W2v-BERT 2.0 | Whisper-small | MMS-1B |
|---|---|---|---|---|---|
| Afrikaans | 1h | 38.62/8 | 22.70/3 | 26.38/4 | **22.23/3** |
| Afrikaans | 50h | 2.79/1 | 3.23/1 | **2.11/1** | 3.69/1 |
| isiXhosa | 1h | 54.70/10 | 27.83/5 | 33.56/7 | **27.54/4** |
| isiXhosa | 50h | 8.53/1 | **7.13/1** | 5.87/1 | 9.76/2 |
| isiZulu | 1h | 45.31/8 | 28.02/5 | 33.56/8 | **22.72/3** |
| isiZulu | 50h | 9.69/2 | **7.89/1** | 8.20/1 | 12.58/2 |

**This is the single most load-bearing table in the document for the 60-GPU-hour question.** It says: 1 hour of in-domain data takes isiZulu from ~113–146% WER to ~23–28% WER. 50 hours takes it to ~8%.

Two heavy caveats: NCHLT is **read speech** (prompted, clean, studio-ish), so these are an optimistic ceiling versus in-the-wild game audio; and this is a matched-domain train/test split. Real AMAZWI audio will be noisier and spontaneous, so expect materially worse.

## 1.4 Corpora

| Corpus | Size | Languages | Licence | Notes |
|---|---|---|---|---|
| [Swivuriso / ZA African Next Voices](https://arxiv.org/abs/2512.02201) | ~3,000h | 7 SA | **CC-BY-4.0** | The single best resource for this project. Agriculture/healthcare/general domains, scripted + unscripted. |
| [NCHLT](https://repo.sadilar.org) | 50–60h/lang core; auxiliary 20–170h/lang | **All 11 official SA** | **CC-BY 3.0 / CC-BY 2.5 ZA** | Read speech, ~200 speakers/language. Via SADiLaR. |
| [AfriSwitch](https://huggingface.co/datasets/intronhealth/AfriSwitch) | 61.36h | 16 African incl. Zulu, Tswana, Afrikaans | **CC-BY-4.0** | Code-switched, in-the-wild. See §2. |
| [WAXAL](https://huggingface.co/datasets/google/WaxalNLP) | see below | Sub-Saharan | **CC-BY-4.0** (some CC-BY-SA-4.0) | **Contains no SA languages — see §1.5.** |

## 1.5 WAXAL — resolving the conflict, and the finding that matters more

The user asked me to resolve "11,000h / 27 languages" versus "~1,846h ASR + 565h TTS" against a primary source. Here is what each primary source actually says:

| Source | ASR hours | TTS hours | Languages |
|---|---|---|---|
| [Google Research blog](https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/) [VENDOR] | "approximately 1,846 hours of transcribed natural speech" | "over 565 hours of high-fidelity recordings" | "27 Sub-Saharan African languages" |
| [arXiv 2602.02734](https://arxiv.org/abs/2602.02734) [MEASURED] | "~1,250 total hours, 224,767 instances", **14 languages** | "~186 total hours, 17,660 instances", **10 languages** | "21 Sub-Saharan African languages" |
| [HF dataset card](https://huggingface.co/datasets/google/WaxalNLP) [MEASURED — what is actually downloadable] | ~1,250h across **19 languages** | >180h across **17 languages** | — |

**Verdict on the numbers:** the "11,000 hours / 27 languages" figure is **not supported by any primary source I could find** and should not be repeated. The blog announcement (1,846h / 565h / 27 languages) is the *aspirational* framing; the paper and the actual released artefact are consistently **~1,250h ASR and ~186h TTS**. Cite ~1,250h ASR / ~186h TTS as the released figure, and note the announcement discrepancy if pressed.

**The finding that matters far more for AMAZWI:** the WAXAL language list is Acholi, Akan, Amharic, Baoule, Bambara, Dagaani, Dagbare, Ewe, Fula, Hausa, Igbo, Ikposo, Kamba, Kikuyu, Lingala, Luganda, Luo, Malagasy, Masaaba, Nigerian Pidgin, Nyankole, Oromo, Pular, Shona, Sidama, Soga, Swahili, Tigrinya, Twi, Wolaytta, Wolof, Yoruba.

**Not one South African official language is in it.** No isiZulu, no isiXhosa, no Sesotho, no Setswana, no Sepedi, no Tshivenda, no Xitsonga, no siSwati, no isiNdebele, no Afrikaans. WAXAL is a West/East African resource. **It is irrelevant to AMAZWI except as evidence that the SA language gap is real and unfilled by big tech.** That is actually a useful pitch point — Google poured resources into African speech in 2026 and skipped South Africa entirely.

## 1.6 Models not covered by published SA benchmarks

I found **[NO PUBLISHED BENCHMARK]** for the following on SA languages, and they should not be claimed:

- **Google Chirp / USM** — no per-language SA WER published in an independently verifiable form.
- **NVIDIA Parakeet / Canary** — English-centric; no SA-language WER found. Parakeet does not claim these languages.
- **SeamlessM4T** as an end-to-end ASR system on SA languages — the *encoder* (W2v-BERT 2.0) is benchmarked above, but Seamless as a whole is not.
- **siSwati, Sepedi, isiNdebele, Tshivenda individually** — thinly covered. Tshivenda and isiNdebele have only ~250h each in Swivuriso and appear in aggregate results only.

---

# 2. CODE-SWITCHED SA SPEECH

Code-switching is the norm, not the exception, in South African urban speech. Any product collecting "real" SA voice data will collect code-switched audio whether it plans to or not.

## 2.1 AfriSwitch (2026) — the current benchmark

[arXiv 2608.26434](https://arxiv.org/abs/2608.26434) · [HF: intronhealth/AfriSwitch](https://huggingface.co/datasets/intronhealth/AfriSwitch) · **CC-BY-4.0** · 61.36 hours, 16 African languages/varieties, human-transcribed, with switch-level English span tags, per-utterance Code-Mixing Index, and switch-point counts.

Zero-shot WER, five systems [MEASURED, Table 2]:

| Language | Sahara V2 | Sahara V2.5 | Omnilingual 7B | Gemini 3.6 | ElevenLabs |
|---|---|---|---|---|---|
| **Zulu** | 81.01 | 49.30 | **48.19** | 50.76 | 62.02 |
| **Tswana** | 43.18 | **28.33** | 36.79 | 64.42 | 66.39 |
| **Afrikaans** | 59.14 | 26.45 | 30.43 | 36.90 | **26.04** |
| **Average (12 langs)** | 59.90 | **35.93** | 51.46 | 55.05 | 56.48 |

Best system averages **35.93% WER**; **no system falls below 24% WER on any language**.

## 2.2 The code-switching penalty

The paper states plainly: *"Every system performs substantially worse than published figures for the same languages on monolingual benchmarks."*

Quantifying it against §1: fine-tuned monolingual isiZulu sits at **~8–25% WER**; code-switched in-the-wild isiZulu sits at **~48% WER** for the best system. **That is roughly a 2–6× degradation** depending on which monolingual figure you compare against. Setswana: ~13–19% monolingual FT versus 28.33% code-switched best.

Corpus-level CMI ranges **4.19 (Nigerian Pidgin) to 28.20 (Akan)**; average switch points range **1.46 (Pidgin) to 10.29 (Swahili)**. The paper's finding is that switch *frequency* and mixture *balance* are largely independent axes — no single scalar captures "how code-switched" a language is.

## 2.3 Earlier SA-specific code-switching work

- [Building a Unified Code-Switching ASR System for South African Languages, arXiv 1807.10949](https://arxiv.org/abs/1807.10949) — the foundational SA soap-opera corpus work (English–isiZulu, English–isiXhosa, English–Sesotho, English–Setswana).
- [Semi-supervised acoustic and language model training for English-isiZulu code-switched ASR, arXiv 2004.04054](https://arxiv.org/abs/2004.04054).
- [Multilingual self-supervised speech representations improve ASR of low-resource African languages with codeswitching, arXiv 2311.15077](https://arxiv.org/abs/2311.15077).
- [Semi-supervised Development of ASR Systems for Multilingual Code-switched Speech, arXiv 2003.03135](https://arxiv.org/abs/2003.03135).

**Product implication:** AMAZWI should *capture and tag* code-switching rather than treat it as noise. A code-switch-tagged SA corpus is a more differentiated and more valuable asset than another monolingual read-speech corpus, and AfriSwitch's tagging schema (English span tags + CMI + switch counts) is a ready-made, CC-BY-4.0 standard to copy. This is a strong, cheap differentiator.

---

# 3. FINE-TUNING FEASIBILITY ON KAGGLE T4×2 16GB

## 3.1 The platform, honestly

[Kaggle](https://www.kaggle.com/docs/efficient-gpu-usage) provides **30 GPU-hours/week** (a floating quota that can vary with demand), **12-hour session cap**, T4×2 or P100 16GB. Two accounts → **~60 GPU-hours/week**.

**Important accounting correction:** on the T4×2 option, Kaggle bills **wall-clock session time**, not per-GPU time. A 9-hour session using both T4s costs 9 hours of quota, not 18. So "60 GPU-hours" is really **~60 hours of wall-clock session time across two accounts**, with 2 GPUs available during each. That is more useful than it first sounds, *if* the training actually uses both GPUs — which for a T4×2 requires DDP or `accelerate`, and adds setup risk inside a 24-hour hackathon.

**Also note:** using two accounts to obtain additional free compute may conflict with Kaggle's terms of service. This is a business/compliance question, not a technical one, but it should not be described in a public pitch as a clever hack. Flagging it because it belongs in a risk register.

## 3.2 What fits in 16GB

| Model | Params | Full FT | LoRA (r=8–32) | Verdict on T4 16GB |
|---|---|---|---|---|
| Whisper-tiny | 39M | Yes | Yes | Trivial |
| Whisper-base | 74M | Yes | Yes | Trivial |
| Whisper-small | 244M | Yes, tight | Yes, comfortable | **Good hackathon target** |
| W2v-BERT 2.0 | 600M | Marginal | Yes | **Best Nguni target** |
| Whisper-medium | 769M | No | Yes | Feasible with care |
| Whisper-large-v3-turbo | **809M** | No | Yes | Feasible; 4 decoder layers helps a lot |
| Whisper-large-v3 | 1550M | No (needs ~24GB) | Yes with INT8 | Possible but slow; not advised |

The reference point: [PEFT + INT8 fine-tuning of Whisper-large-v2 (1.6B) runs in **under 8GB VRAM on a free T4**](https://github.com/openai/whisper/discussions/988), fitting ~5× the batch size of full FT. [Vaibhavs10/fast-whisper-finetuning](https://github.com/Vaibhavs10/fast-whisper-finetuning) is the canonical working recipe.

Full FT of large-v2 needs ~24GB and ~7GB per checkpoint — **out of reach**. LoRA is not a compromise here, it is the only option above ~300M params.

Supporting evidence that LoRA is sufficient: [LoRA-INT8 Whisper for Cantonese](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12431075/) fine-tuned Whisper-tiny with **rank 8, updating 1.6% of weights**, cutting CER from **49.5% → 11.1%**, "close to full fine-tuning performance", at roughly an order of magnitude less memory and compute. [MEASURED]

## 3.3 Concrete configs

**Config A — the safe hackathon run (recommended primary)**

```
base:            openai/whisper-small (244M, MIT)
method:          LoRA r=16, alpha=32, dropout=0.05
target_modules:  q_proj, v_proj
precision:       fp16 (T4 has no bf16; use fp16 + GradScaler)
per_device_bs:   8
grad_accum:      4          # effective batch 32, matching Swivuriso
lr:              1e-3       # LoRA tolerates higher LR than full FT
warmup:          50 steps
max_steps:       2000
gradient_checkpointing: True
eval_strategy:   steps, every 250
```

**Config B — the quality run (Nguni languages)**

```
base:            facebook/w2v-bert-2.0 (600M, MIT) + CTC head
method:          LoRA r=32 on attention, full FT on CTC head
precision:       fp16
per_device_bs:   4
grad_accum:      8          # effective batch 32
lr:              5e-5       # per Swivuriso
max_steps:       2000-10000
```

**Config C — the headline run (only if A and B land early)**

```
base:            openai/whisper-large-v3-turbo (809M, MIT)
method:          LoRA r=32 + INT8 (bitsandbytes)
precision:       fp16 compute, int8 base weights
per_device_bs:   2
grad_accum:      16
lr:              1e-4       # per Swivuriso
max_steps:       2000
```

Note fp16 not bf16: **T4 (Turing, sm_75) does not support bfloat16**. The Swivuriso paper used bf16 on presumably A100-class hardware. Copying their config verbatim onto a T4 will fail or silently fall back. This is the kind of detail that eats three hours of a 24-hour hackathon.

## 3.4 Hours per epoch — [ESTIMATE], and why you must measure it first

**I found [NO PUBLISHED BENCHMARK] giving hours-per-epoch for Whisper LoRA on a T4 for a specified quantity of audio.** Anyone quoting you one is extrapolating.

Planning estimates below are mine, derived from parameter counts and typical T4 throughput. **Treat as hypotheses to be falsified by a 15-minute timing run, not as facts.**

| Config | Audio | Est. wall-clock/epoch, 1× T4 |
|---|---|---|
| A: Whisper-small LoRA | 5h | **[ESTIMATE] 0.4–0.8h** |
| A: Whisper-small LoRA | 20h | **[ESTIMATE] 1.5–3h** |
| A: Whisper-small LoRA | 50h | **[ESTIMATE] 4–8h** |
| B: W2v-BERT 2.0 LoRA | 20h | **[ESTIMATE] 3–6h** |
| C: large-v3-turbo LoRA+INT8 | 20h | **[ESTIMATE] 6–12h** |

The spread is wide because it is dominated by things not yet known: audio length distribution, dataloader efficiency, whether features are precomputed, and whether INT8 kernels engage properly on Turing.

**Mandatory first job (Job 0 in the budget table): run 100 steps, time it, and derive the real rate.** Everything downstream is guesswork until that exists. This is doctrine rule 3 — build the measuring instrument before making the claim.

**Cost-saving trick worth its weight:** precompute log-Mel features once, cache to disk as a HF dataset, and never recompute. Feature extraction is CPU-bound and can dominate a T4 job. This alone can halve effective training time.

## 3.5 Realistic WER delta on 5–50 hours

Grounded in the NCHLT scaling table (§1.3) [MEASURED] and Swivuriso [MEASURED]:

| In-domain data | Expected isiZulu WER | Confidence |
|---|---|---|
| 0h (zero-shot) | 113–146% | High — measured |
| 1h | 23–28% | High — measured (read speech) |
| 5h | ~15–20% | Medium — interpolated |
| 20h | ~10–13% | Medium — interpolated |
| 50h | 8–13% | High — measured (read speech) |

**All of these are read-speech, matched-domain figures. Spontaneous in-the-wild game audio will be worse — plausibly 1.5–2× worse, and code-switched audio 2–6× worse (§2.2).**

## 3.6 What ~60 GPU-hours can and cannot produce — brutally

**CAN:**
- Fine-tune Whisper-small or W2v-BERT 2.0 with LoRA on 1–2 languages to a **demonstrable, honestly-measured WER improvement** over a zero-shot baseline. The improvement will be enormous (146% → ~25%) because the baseline is broken, not because the fine-tune is impressive. **Say it that way.**
- Train a **South African language ID classifier** from scratch on Swivuriso. This is cheap, fast, genuinely useful, and fills a real gap (§5.2). Highest value-per-GPU-hour job available.
- Build a full evaluation harness and produce a defensible baseline table across several models.
- Produce quantised ONNX exports for browser deployment.

**CANNOT:**
- Beat published SOTA on any SA language. The comparison points used 2× A100 80GB.
- Fine-tune on all 11 official languages. Realistically **two, maybe three**.
- Train anything from scratch on 3,000 hours of Swivuriso. Loading and feature-extracting 3,000 hours alone exceeds the budget.
- Produce a robust anti-spoofing model (§5.3).
- Produce statistically significant model-vs-model comparisons on small eval sets without the three-gate protocol — and small SA eval sets will frequently fail those gates. Expect and report null results.

**The honest framing for judges:** 60 GPU-hours does not buy a better model than the research community has. It buys a *working demonstration that the pipeline closes* — collect → validate → clean → fine-tune → measure — on real data, in two languages. That is the claim to make, and it is a strong one, because closing the loop is what nobody else has done for SA languages.

---

# 4. IN-BROWSER / ON-DEVICE, 2026

## 4.1 The design decision that saves the project

**Do not run Whisper in the browser for South African languages.** Sections 1.1 makes this unambiguous: even large-v3-turbo is at 146% WER zero-shot on these languages. A quantised whisper-tiny in the browser will be *worse than that*. It will produce confident, fluent, entirely wrong English text from isiZulu audio, which is the single worst possible failure mode for a data-collection product — it looks like it works.

**On-device should do gating, not transcription.** Gating = "is this audio worth uploading?" That question is answerable with pure DSP and a 2MB VAD, at near-zero cost, in any browser, offline.

## 4.2 Model sizes for the browser

[Xenova/whisper-tiny ONNX](https://huggingface.co/Xenova/whisper-tiny/tree/main/onnx) — **MIT**, exact file sizes [MEASURED]:

| Component | fp32 | fp16 | q4f16 | quantized (int8) |
|---|---|---|---|---|
| encoder_model | 32.9 MB | 16.5 MB | **6.3 MB** | 10.1 MB |
| decoder_model_merged | 119 MB | 59.6 MB | 46 MB | **30.7 MB** |
| **Practical total (merged decoder)** | ~152 MB | ~76 MB | **~52 MB** | **~41 MB** |

Whisper-base roughly doubles this. Whisper-small `decoder_model_merged_q4.onnx` alone is **233 MB** — far too large for a mid-range Android on mobile data.

**For a South African user on a metered prepaid data bundle, a 41 MB model download is a serious ask, and it buys transcription that does not work in their language. This is the whole argument for the DSP-first approach.**

Other on-device options:

| Model | Size | Licence | Verdict for AMAZWI |
|---|---|---|---|
| [Silero VAD](https://github.com/snakers4/silero-vad) | **~2 MB** (JIT; ONNX comparable) | **MIT** | **Recommended.** <1ms per 30ms chunk, single CPU thread. 8k/16k Hz. Trained on corpora spanning 6000+ languages [VENDOR]. |
| [Moonshine tiny](https://huggingface.co/UsefulSensors/moonshine) | 27M params, **26 MB ONNX** | **MIT** | **English-only.** Useless for SA languages. Possible as an "is this English?" signal only. |
| Moonshine base | 61M params, **57 MB ONNX** | **MIT** | Same limitation. |
| whisper.cpp / whisper-web | varies | MIT | Same language problem as above. |

## 4.3 WebGPU vs WASM

[WebGPU gives roughly 5–10× speedup over WASM for Whisper inference](https://www.sitepoint.com/webgpu-vs-webasm-transformers-js/), Chrome/Edge 113+. Embedding-model benchmarks have shown up to 64× [VENDOR — not Whisper, do not quote for ASR].

**Mid-range Android caveats that matter:**
- WebGPU support on mid-range Android Chrome is **inconsistent**. A WASM fallback is mandatory and must be automatic.
- On shared CPU/GPU memory (i.e. every phone), GPU allocation **directly reduces system RAM**. Devices with 4GB total RAM hit practical limits quickly with WebGPU and larger models.
- **[NO PUBLISHED BENCHMARK]** for transformers.js Whisper real-time factor on named mid-range Android devices in 2026. I looked. Do not quote a latency number for Android — measure it on the actual target device (e.g. a Samsung A-series) and report that measurement.

Silero VAD at ~2MB running in ONNX Runtime Web on WASM sidesteps every one of these problems.

## 4.4 Pure Web Audio API quality checks — NO model, NO download

This is the highest-leverage, lowest-risk component in the entire build. All of it runs in `AudioWorklet` / `AnalyserNode`, zero bytes downloaded, works offline, works on any Android browser, and costs nothing per user.

| Check | Method | Reject / flag threshold |
|---|---|---|
| **Duration** | buffer length ÷ sampleRate | <1.0s or >30s |
| **RMS level** | `sqrt(mean(x²))`, in dBFS | <−45 dBFS = too quiet / no speech |
| **Peak level** | `max(abs(x))` | >0.99 sustained = clipping |
| **Clipping rate** | fraction of samples with `abs(x) > 0.99` | >0.5% = reject |
| **Zero-crossing rate** | sign changes ÷ frame length | Very high + low RMS = fricative noise/wind, not voiced speech |
| **Spectral flatness** | geometric mean ÷ arithmetic mean of FFT magnitudes | →1.0 = white noise; →0 = tonal. Speech is mid-range. High flatness + high RMS = noise, not speech. |
| **Simple SNR** | ratio of energy in top-decile frames to bottom-decile frames | <10 dB = too noisy |
| **Silence ratio** | fraction of frames below noise floor + margin | >70% = mostly silence, reject |
| **Speech-band energy ratio** | energy 300–3400 Hz ÷ total energy | Low ratio = not speech |
| **DC offset** | mean(x) | Non-zero = hardware fault |
| **Spectral centroid / rolloff** | `AnalyserNode.getFloatFrequencyData()` | Sanity check on mic bandwidth |

**Recommended gate order (cheapest first, fail fast):** duration → RMS → clipping → silence ratio → speech-band ratio → spectral flatness → SNR → Silero VAD (only if all pass).

This catches: empty recordings, dead microphones, pocket recordings, wind, music, room noise, and clipped shouting — which will be the overwhelming majority of bad submissions in a game context. **No model needed. No download. This should ship on day one.**

---

# 5. VALIDATION AI

## (i) Is it speech?

| Option | Size | Licence | Note |
|---|---|---|---|
| **Web Audio DSP gate (§4.4)** | 0 MB | n/a | **First line. Free, offline, instant.** |
| **[Silero VAD v5](https://github.com/snakers4/silero-vad)** | ~2 MB | **MIT** | **Recommended.** <1ms/30ms chunk. 8k/16k Hz. Runs client or server. |
| WebRTC VAD | tiny | BSD | Older, faster, less accurate. Fallback only. |

## (ii) Is it the claimed language?

**This is the weakest link in the entire stack, and it is worth understanding precisely why.**

| Model | Licence | SA coverage | Verdict |
|---|---|---|---|
| **[MMS-LID (facebook/mms-lid-*)](https://huggingface.co/facebook/mms-1b-all)** | **CC-BY-NC-4.0** | 1,162 languages incl. zul, xho, sot, afr | **EXCLUDED — non-commercial licence.** Usable for internal research only, never in the commercial product. |
| **[speechbrain/lang-id-voxlingua107-ecapa](https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa)** | **Apache-2.0** | **Afrikaans ✓, Shona ✓. isiXhosa ✗, isiZulu ✗, Sesotho ✗, Setswana ✗** | Commercially usable but **misses almost every language AMAZWI needs**. 6.7% error rate on VoxLingua107 dev overall — that number does not apply to languages it cannot predict. |
| Whisper LID | MIT | 99 languages, SA coverage poor | Given 146% zero-shot WER, its LID posterior on these languages is not trustworthy. **[NO PUBLISHED BENCHMARK]** on SA-language LID accuracy. |

**Published difficulty warning [MEASURED]:** [Henselmans, van Leeuwen & Niesler](https://dsp.sun.ac.za/~trn/reports/henselmans+vanleeuwen+niesler_lid_prasa13.pdf) report *higher confusability among isiNdebele, Xitsonga, Tshivenda, isiXhosa and isiZulu*. These are closely-related languages; LID between them is genuinely hard, not just under-resourced.

**Therefore the recommendation: train your own SA LID classifier.** ECAPA-TDNN or a small W2v-BERT 2.0 classification head, trained on Swivuriso (CC-BY-4.0, 7 languages, ~3,000h — subsample heavily) plus NCHLT (CC-BY, all 11).

Why this is the right call:
- It is **cheap** — a 7-way utterance classifier converges in a few GPU-hours, far faster than any ASR fine-tune.
- It **fills a genuine gap**. There is no permissively-licensed SA LID model. That is a real contribution.
- It is **directly monetisable** as a validation product independent of ASR quality.
- It **de-risks the demo**: an LID model at 85% accuracy is a working demo; an ASR model at 25% WER is a hard sell to a non-technical judge.

**Do not report LID accuracy without a confusion matrix.** With Nguni languages this closely related, aggregate accuracy hides exactly the errors that matter.

## (iii) Is it human, or TTS/replay?

**Recommended: [AASIST](https://github.com/clovaai/aasist) — MIT licence.** Pretrained AASIST and AASIST-L checkpoints provided. AASIST-L is **85,306 parameters** — tiny. The repo also supports training RawNet2 and RawGAT-ST.

Reported in-domain performance [MEASURED]: **AASIST 0.83% EER, min t-DCF 0.0275 on ASVspoof 2019 LA**. AASIST-L: 0.99% EER, min t-DCF 0.0309.

**Now the part that must not be omitted from any pitch [MEASURED]:**

On [ASVspoof 5](https://arxiv.org/abs/2601.03944) (53 teams, crowdsourced non-studio speech, modern attacks), the same **AASIST scored 25.319% EER**, minDCF 0.662, actDCF 0.931, Cllr 2.486. RawNet2 and AASIST baselines both exceeded **29% EER** with minDCF above 0.7.

**AASIST goes from 0.83% EER in-domain to ~25% EER out-of-domain — a ~30× degradation.** The challenge organisers report solutions consistently struggling with generalisation, degrading further under adversarial attacks and neural codec compression. DNN-based Encodec and narrow-band codecs degrade detection most; FreqMask-style augmentation helps but is imperfect.

**Practical consequence for AMAZWI:** phone audio is narrow-band and codec-compressed — precisely the condition that degrades these detectors most. A 25% EER detector means roughly one in four spoofs pass and one in four genuine users are wrongly flagged. **It cannot be an automatic reject gate.** Use it as a *risk score* that routes to human review, and combine it with much stronger non-model signals: replay/near-duplicate detection (v), device and session metadata, timing patterns, and speaker-embedding clustering (vi). Fraud detection here should be **behavioural and statistical first, model-based second**.

## (iv) Quality scoring

| Model | Licence | Verdict |
|---|---|---|
| **[NISQA](https://github.com/gabrielmittag/NISQA)** | **Code MIT, but WEIGHTS are CC BY-NC-SA 4.0** | **EXCLUDED for commercial use.** This is an easy trap — the repo badge says MIT and the weights are not. Predicts Overall/Noisiness/Coloration/Discontinuity/Loudness. |
| **[DNSMOS / DNSMOS P.835](https://github.com/microsoft/DNS-Challenge)** | **Code MIT**, docs CC-BY-4.0 | **Recommended commercial option.** Verify the specific ONNX weight files carry MIT before shipping. |
| DNSMOS Pro (Cumlin et al. 2024) | Not confirmed | Lighter, probabilistic MOS. Verify licence. |
| [UTMOS / UTMOSv2](https://github.com/sarulab-speech/UTMOSv2) | **Licence not confirmed in this research** | UTMOS won 10/16 metrics at VoiceMOS 2022; UTMOSv2 1st in 7/16, 2nd in 9/16 at VoiceMOS 2024. Tuned for *synthesised* speech quality — arguably the wrong tool for scoring human recordings. **Verify licence before use.** |

**Honest note:** all of these are trained and validated on English and other high-resource languages. **[NO PUBLISHED BENCHMARK]** exists for MOS-prediction validity on isiZulu, isiXhosa or any SA language. Their correlation with human judgement on SA speech is **unknown**. Use them as relative ranking signals within your own corpus, never as absolute quality claims. The §4.4 DSP metrics are, ironically, more trustworthy here because they measure physical properties rather than learned perceptual proxies.

## (v) Near-duplicate detection

| Tool | Licence | Verdict |
|---|---|---|
| **[Chromaprint / AcoustID](https://github.com/acoustid/chromaprint)** | **LGPL-2.1+** | Explicitly designed for "duplicate audio file detection". LGPL is acceptable for server-side use; note the copyleft implications if linked into distributed binaries. |
| **[Dejavu](https://yunpengn.github.io/dejavu/)** | **MIT** | Python, requires MySQL. Shazam-style landmark fingerprinting. Simpler to embed. |

**For AMAZWI, roll a simple landmark fingerprint yourself.** The task is easier than music ID: you are detecting *exact or near-exact resubmission* of the same recording, not matching a noisy clip against a 10M-track catalogue. A spectral-peak-pair hash over the utterance, stored in a database index, catches replay attacks and lazy duplicate farming cheaply. This is a half-day of work and a genuinely strong anti-fraud signal — **much more reliable than AASIST at 25% EER.**

## (vi) Speaker embeddings for UNIQUENESS (not authentication)

**[speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) — Apache-2.0.** Reported **0.80% EER on VoxCeleb1-test (cleaned)** [MEASURED].

The framing here is correct and important. Used for **uniqueness**, this asks "how many distinct voices are in this corpus?" and "is one person submitting under 40 accounts?" — a clustering and diversity problem. Used for **authentication**, it would ask "is this person who they claim to be?" — which requires enrolment, liveness, spoof-resistance, and carries biometric-data legal obligations.

**POPIA implications (South Africa's Protection of Personal Information Act):** voice biometrics are likely special personal information. Storing speaker embeddings that can re-identify individuals is a data-protection question that needs a real answer before launch, not after. Storing *cluster IDs* and *diversity statistics* rather than raw retrievable embeddings is the safer architecture, and it is sufficient for the uniqueness use case. **Flag this to whoever owns compliance.**

Legitimate uses: corpus diversity metrics (how many unique speakers, gender/age balance proxies), duplicate-account detection, and per-speaker dataset splits so that train/test do not share speakers — **the last one is essential for honest WER reporting** and is routinely got wrong.

---

# 6. TWO-TRACK MODEL PLAN

## Track A — Day one, zero collected data

Everything here is permissively licensed, works immediately, and requires no training. **This is the entire hackathon demo if the GPU work fails.**

| Component | Model / method | Licence | Where it runs |
|---|---|---|---|
| Audio quality gate | Web Audio API DSP (§4.4) | n/a — your code | Browser, offline |
| Speech detection | Silero VAD v5 ONNX (~2MB) | **MIT** | Browser (ORT Web) or server |
| Duplicate detection | Landmark fingerprint (own) or Dejavu | **MIT** | Server |
| Spoof risk score | AASIST-L pretrained (85k params) | **MIT** | Server — **score only, never auto-reject** |
| Speaker uniqueness | ECAPA-TDNN VoxCeleb | **Apache-2.0** | Server |
| Quality MOS | DNSMOS P.835 | **MIT (verify weights)** | Server |
| Baseline ASR (Afrikaans only) | whisper-large-v3-turbo | **MIT** | Server |
| Baseline ASR (other 10 langs) | **None that works.** State this. | — | — |
| Language ID (Afrikaans vs other) | VoxLingua107 ECAPA | **Apache-2.0** | Server |

**Explicitly excluded from Track A on licence grounds:** MMS-1B-all and MMS-LID (**CC-BY-NC-4.0**), NISQA weights (**CC-BY-NC-SA-4.0**), SeamlessM4T (CC-BY-NC-4.0). All are fine for internal research; none may ship in a commercial product.

**The day-one honest claim:** "We validate that a submission is real, audible, unique, human-sounding speech of adequate quality — before a cent is paid for it. We do not yet claim to transcribe it, because no system on earth transcribes isiZulu reliably today. That is the gap we are collecting data to close."

That is a strong, true, defensible pitch. It is stronger than a fake transcription demo, and it will survive a technical judge.

## Track B — After data accumulates

**Loop:**

1. **Ingest** → Track A gates → accept/review/reject, with all metrics stored per utterance.
2. **Speaker-disjoint splits.** Cluster ECAPA embeddings; ensure no speaker appears in both train and test. Freeze the test set on day one and never touch it.
3. **Clean** → §8 pipeline.
4. **Seed** with Swivuriso (CC-BY-4.0) + NCHLT (CC-BY) so the first fine-tune has a real base, then blend in collected data at increasing ratios.
5. **Fine-tune** — Config A for Sotho-Tswana, Config B for Nguni (per §1.2's architecture split).
6. **Evaluate** on the frozen test set. Report WER **and** CER (CER is more informative for agglutinative Nguni languages, where a single morphological error costs a whole word).
7. **Three-gate before claiming any improvement**: Mann-Whitney p<0.05, bootstrap 95% CI excluding zero, Cliff's delta reported. If any gate fails → "no significant difference". Expect this often on small SA eval sets. **Report the null results; they are more credible than a wall of wins.**
8. **Feed back** — route low-confidence and high-disagreement utterances to prioritised re-collection (§7).

---

# 7. ACTIVE LEARNING FOR ASR — brief

**What the literature actually says [MEASURED]:** uncertainty-based selection **can underperform random sampling** for ASR. [Research](https://arxiv.org/pdf/2406.02566) finds methods like SMCA underperform random because their uncertainty measures correlate poorly with actual WER, and they select uncertain samples from small clusters, producing *less* diverse training sets. This is the opposite of the intuitive story.

**What works better:** hybrid uncertainty + diversity. [Two-stage pipelines combining x-vectors with Bayesian batch active learning](https://arxiv.org/pdf/2406.02566) explicitly add speaker/acoustic diversity to the uncertainty signal. [Bridging Diversity and Uncertainty with Self-Supervised Pre-Training, arXiv 2403.03728](https://arxiv.org/html/2403.03728v1) and [error-driven fixed-budget personalisation, arXiv 2103.03142](https://arxiv.org/pdf/2103.03142) point the same way.

**Is it honestly demonstrable in a hackathon? No.**

Demonstrating active learning requires showing that selection strategy X beats random selection at equal labelling budget. That needs: multiple training runs per strategy, multiple seeds, a held-out test set large enough for the three gates to have power, and enough unlabelled pool to select from. In 60 GPU-hours with a corpus collected over 24 hours, **you will not have the statistical power to distinguish X from random.** Attempting it and reporting a win would be a fabricated result.

**What you can honestly do:** build and demo the *mechanism* — the system scores every utterance by model confidence and acoustic novelty, and surfaces a prioritised re-collection queue. Show the queue working. Say: *"the selection policy is in place; whether it beats random selection is an open question we have not yet powered a study to answer."* That is honest, it shows engineering maturity, and it is more impressive to a good judge than an unfalsifiable claim.

---

# 8. AUDIO CLEANING PIPELINE — canonical steps

```
1. FORMAT NORMALISE   → 16 kHz mono PCM WAV, 16-bit. (Whisper and W2v-BERT both expect 16 kHz.)
                        Resample with a high-quality resampler (soxr / librosa 'kaiser_best').
2. DC OFFSET REMOVE   → subtract mean. Cheap, catches hardware faults.
3. CLIPPING DETECT    → flag if >0.5% samples |x|>0.99. Do NOT attempt declipping; reject or downweight.
4. SNR ESTIMATE       → top-decile vs bottom-decile frame energy. Reject <10 dB. Store the value.
5. VAD TRIM           → Silero VAD. Trim leading/trailing silence, keep ~200ms padding.
                        Do NOT strip internal pauses — they carry prosodic information and
                        removing them creates unnatural concatenation artefacts.
6. SEGMENT            → utterances of 3–30 s. Whisper's receptive field is 30 s; longer inputs
                        are truncated or padded, wasting compute either way.
7. LOUDNESS NORMALISE → EBU R128 / ITU-R BS.1770. Target -23 LUFS (broadcast standard) or
                        -20 dBFS RMS (common in speech pipelines). Apply AFTER trimming,
                        with true-peak limiting at -1 dBTP to avoid introducing clipping.
8. DENOISE            → *** USUALLY DO NOT. See below. ***
9. FORCED ALIGN       → MFA if a lexicon exists; WhisperX otherwise.
10. TRANSCRIPT NORM   → Unicode NFC; consistent orthography; expand or consistently render numerals;
                        decide and DOCUMENT the casing and punctuation policy; tag code-switch
                        spans (AfriSwitch schema: English span tags + CMI + switch counts).
11. PACKAGE           → HF datasets → Parquet; WebDataset (.tar shards) for streaming at scale.
```

## 8.1 When NOT to denoise — this is the important one

There is a strong and growing 2025–2026 literature that **denoising actively harms modern ASR** [MEASURED]:

- [When De-noising Hurts: A Systematic Study of Speech Enhancement Effects on Modern Medical ASR, arXiv 2512.17562](https://arxiv.org/abs/2512.17562) — enhancement preprocessing degrades ASR across noise conditions and models.
- [When Denoising Hinders: Revisiting Zero-Shot ASR with SAM-Audio and Whisper, arXiv 2603.04710](https://arxiv.org/pdf/2603.04710) — degradation is **more pronounced for larger models**, indicating interaction between enhancement artefacts and pretrained acoustic distributions.
- Documented as the *"noise reduction paradox"*: spectral subtraction can improve SNR by ~8 dB while driving **WER up 15%**, by stripping speech harmonics and formant transitions the recogniser depends on.

**Rule for AMAZWI: do not denoise by default.** Whisper and W2v-BERT were pretrained on vast noisy in-the-wild corpora and already encode substantial noise robustness. Denoising moves your audio *off* the distribution they were trained on.

**Denoise only if:** (a) you have measured that it improves WER on *your* held-out set with *your* model, and (b) you keep the un-denoised original. Store noise as metadata (the SNR value from step 4), and let the model handle it. If audio is too noisy to use, reject it — do not repair it.

**Corollary for training data:** noisy-but-real audio is *valuable* training data for a system that must work on real phones in real South African environments. Over-cleaning the corpus produces a model that fails in the field. Preserve the acoustic diversity.

## 8.2 Alignment

| Tool | Licence | Accuracy | Use when |
|---|---|---|---|
| **[MFA](https://arxiv.org/html/2606.18466v1)** | MIT (verify current) | **Better** — consistently outperforms WhisperX and MMS at all thresholds, especially ≤10ms and sub-20ms boundaries, due to explicit phoneme-state modelling | A pronunciation lexicon exists |
| **[WhisperX](https://github.com/m-bain/whisperX)** | **BSD-2-Clause** | Worse at tight boundaries; wav2vec2-based alignment | No lexicon — i.e. most SA languages |

[Multilingual MFA, arXiv 2504.07315](https://arxiv.org/html/2504.07315v1) shows transfer learning from a large English MFA model **halves boundary errors** versus training from scratch on low-resource field data — directly applicable here. WhisperX claims **70× realtime** with batched inference [VENDOR].

**Practical: start with WhisperX (no lexicon needed), move to MFA per-language once you have enough data to build a lexicon.** Word-level alignment is not needed for ASR fine-tuning at all — only for TTS, karaoke-style UI, and per-word quality scoring. Do not spend hackathon time on it unless the product needs it.

---

# 9. TTS FOR SA LANGUAGES, 2026 — brief

**State of play: thin, and mostly proprietary.**

- **[Swivuriso](https://arxiv.org/abs/2512.02201)** (CC-BY-4.0, ~3,000h, 7 SA languages) is the best available *training data* for SA TTS. It is a dataset, not a model.
- **[WAXAL](https://huggingface.co/datasets/google/WaxalNLP)** TTS split (~186h, CC-BY-4.0) contains **no SA languages** (§1.5).
- **[MzansiText / MzansiLM, arXiv 2603.20732](https://arxiv.org/abs/2603.20732)** (March 2026) — open corpus and decoder-only LM for SA languages. Text, not speech, but relevant for TTS front-end normalisation. Verify licence.
- **[Narakeet](https://www.narakeet.com/news/2026/03/09/new-sesotho-setswana-voices.html)** launched Sesotho and Setswana voices in March 2026 — **commercial, proprietary, paid**.
- **SpeechGen** and similar offer isiZulu TTS — **commercial, proprietary**.

**[NO PUBLISHED BENCHMARK]** for open-source TTS naturalness (MOS) on isiZulu, isiXhosa, Sesotho or Setswana that I could locate. There is no permissively-licensed, ready-to-use, high-quality SA-language TTS model.

**Implication for AMAZWI, and it cuts two ways:**
1. **Opportunity** — the Swivuriso TTS-suitable subset under CC-BY-4.0 means AMAZWI could train and *own* SA TTS voices. That is a second product line from the same corpus.
2. **Risk** — no good SA TTS also means **TTS-based spoofing of SA languages is currently hard**, which lowers near-term fraud risk. But it will not stay that way. As SA TTS improves (and Swivuriso will accelerate exactly that), the spoof-detection problem gets harder, while AASIST's 25% out-of-domain EER (§5.3) does not improve on its own. **Design the fraud system so it does not depend on TTS remaining bad.**

---

# RECOMMENDED MODEL STACK

| Task | Model | Size | Licence | Runs where | Why |
|---|---|---|---|---|---|
| **On-device gating** | **Web Audio API DSP (§4.4)** | **0 MB** | n/a (own code) | Browser, offline | Catches the majority of bad submissions. No download, no data cost, works on any Android, zero inference cost. Ships day one. |
| On-device speech detect | **Silero VAD v5 ONNX** | **~2 MB** | **MIT** | Browser (ORT Web/WASM) or server | <1ms per 30ms chunk. Trivial download. Language-agnostic. WASM avoids WebGPU fragmentation on mid-range Android. |
| **Server transcription (Nguni: isiZulu, isiXhosa, siSwati, isiNdebele)** | **facebook/w2v-bert-2.0 + CTC head, LoRA FT** | 600M | **MIT** | Kaggle T4 / server | Measured 3–4 WER points better than Whisper on Nguni ([arXiv 2606.31642](https://arxiv.org/abs/2606.31642)). MIT — commercially safe. |
| **Server transcription (Sotho-Tswana + Afrikaans)** | **openai/whisper-large-v3-turbo, LoRA FT** | 809M | **MIT** | Kaggle T4 / server | Measured better than W2v-BERT on Sotho-Tswana. Only 4 decoder layers → fits LoRA on T4. Swivuriso: 223%→13% Setswana. |
| Hackathon fallback ASR | openai/whisper-small, LoRA FT | 244M | **MIT** | Kaggle T4 | Trains fast enough to iterate inside a 24h window. |
| **Language ID** | **Own ECAPA-TDNN / W2v-BERT head trained on Swivuriso + NCHLT** | ~20M | **MIT/Apache code; CC-BY-4.0 data** | Server | **No permissively-licensed SA LID model exists.** MMS-LID is CC-BY-NC (excluded); VoxLingua107 lacks every Nguni/Sotho language. Cheap to train, fills a real gap, best value per GPU-hour. |
| LID stopgap (day one) | speechbrain/lang-id-voxlingua107-ecapa | ~20M | **Apache-2.0** | Server | Afrikaans + Shona only. Honest partial coverage until own model trains. |
| **Spoof detection** | **AASIST-L (pretrained)** | **85,306 params** | **MIT** | Server | Smallest credible option. **Risk score routing to human review — NEVER an auto-reject gate.** See caveat below. |
| Replay / duplicate detect | Own landmark fingerprint (or Dejavu) | tiny | **MIT** | Server | **More reliable than AASIST for this threat model.** Deterministic, no OOD degradation. |
| Speaker uniqueness | speechbrain/spkrec-ecapa-voxceleb | ~20M | **Apache-2.0** | Server | 0.80% EER VoxCeleb1. Corpus diversity + duplicate accounts + speaker-disjoint splits. Store cluster IDs, not raw embeddings (POPIA). |
| Quality MOS | DNSMOS P.835 | small | **MIT (verify weights)** | Server | Only permissively-licensed option. **NISQA weights are CC-BY-NC-SA — excluded.** |
| Forced alignment | WhisperX → MFA later | — | **BSD-2-Clause** / MIT | Server | WhisperX needs no lexicon. Not needed for ASR FT — defer. |
| Seed data | Swivuriso + NCHLT | 3,000h + 600h | **CC-BY-4.0 / CC-BY-3.0** | — | Both commercially usable with attribution. |
| Code-switch schema | AfriSwitch tagging | 61h | **CC-BY-4.0** | — | Ready-made standard; differentiator. |

**Explicitly excluded on licence grounds (commercial pitch):** MMS-1B-all and all MMS-LID variants (**CC-BY-NC-4.0**), SeamlessM4T (**CC-BY-NC-4.0**), NISQA pretrained weights (**CC-BY-NC-SA-4.0**). Research-only. Note that `facebook/w2v-bert-2.0` — the *encoder* that Seamless builds on — is **MIT** and is fine. That distinction is easy to get wrong and worth stating in any due-diligence conversation.

---

# 60 GPU-HOUR BUDGET PLAN

Assumes ~60h/week wall-clock across two Kaggle accounts, 9h sessions. **Ordered by value-per-hour and by de-risking: the cheap certain wins come first.**

| # | Job | Hours | Config | Expected output | Risk |
|---|---|---|---|---|---|
| **0** | **Timing calibration** | **1** | 100 steps of Config A, timed | **Measured steps/sec and hours/epoch. Every other row in this table is [ESTIMATE] until this exists.** Do this first, without exception. | None. Skipping it is the risk. |
| **1** | **Feature precompute + eval harness** | **3** | CPU-heavy; cache log-Mel to Parquet | Frozen speaker-disjoint test set; WER/CER scorer; three-gate stats script. Halves all later training time. | Low |
| **2** | **Zero-shot baseline sweep** | **3** | Inference only: whisper-turbo, whisper-small, w2v-bert on frozen test set | **The 100%+ WER baseline table.** This is the single most persuasive artefact for judges — it proves the problem is real. Cheap, certain, no training. | Very low |
| **3** | **SA Language ID model** | **6** | ECAPA-TDNN head on Swivuriso+NCHLT subsample, 7–11 classes | **Working SA LID + confusion matrix.** Highest value/hour in the plan. Fills a genuine gap. Demo-able. | Low |
| **4** | **Whisper-small LoRA, Setswana** | **8** | Config A, ~20h Swivuriso subsample | WER ~10–15% vs 223% zero-shot. **The headline number.** Sotho-Tswana → Whisper per §1.2. | Medium |
| **5** | **W2v-BERT 2.0 LoRA, isiZulu** | **10** | Config B, ~20h Swivuriso subsample | WER ~10–25%. Validates the Nguni/Sotho-Tswana architecture split on your own data. | Medium |
| **6** | **Data-scaling curve** | **8** | Config A, Setswana at 1h / 5h / 20h | **WER-vs-hours curve.** Directly answers "what is an hour of donated speech worth?" — the core business question. Underrated: this is the *investor* artefact. | Medium |
| **7** | **ONNX export + quantise** | **3** | Export VAD + LID to ONNX, q8/q4f16 | Browser-deployable artefacts with measured file sizes and on-device latency **measured on a real mid-range Android**. | Low |
| **8** | **Spoof + quality calibration** | **4** | Run AASIST-L, DNSMOS, ECAPA over collected corpus | Score distributions and **honest out-of-domain EER on your own data**. Expect it to be bad; report it anyway. | Low |
| **9** | **Fine-tune on collected data** | **8** | Best of jobs 4/5, seed corpus + collected audio | Does real collected data move WER? **May well be a null result — report it.** | High |
| **10** | **Contingency / reruns** | **6** | — | OOM recovery, fp16 instability, session timeouts, dataloader bugs. **You will use this.** | — |
| | **TOTAL** | **60** | | | |

**If time collapses, the minimum viable set is jobs 0, 1, 2, 3, 7 — 16 hours.** That yields the baseline table, a working SA LID model, and browser-deployable artefacts, which is a complete, honest, demonstrable story without any ASR fine-tuning at all. Everything above that is upside. **Plan to the 16-hour version and treat the rest as stretch.**

---

# WHAT WE CANNOT HONESTLY CLAIM

1. **We cannot claim working ASR for the 11 official languages.** We will fine-tune at most 2–3. Whisper large-v3-turbo scores **146.30% WER** zero-shot on Southern Bantu languages; it is non-functional, not merely weak.

2. **We cannot claim SOTA.** Published comparisons used **2× A100 80GB**. We have T4s. Our fine-tunes will underperform Swivuriso and the curriculum-learning results, and should be presented as *reproductions on constrained hardware*, not advances.

3. **We cannot claim in-browser transcription for SA languages.** Quantised whisper-tiny in a browser will produce confident, fluent, wrong English text from isiZulu input — the worst failure mode for a data-collection product, because it looks like success.

4. **We cannot claim reliable spoof/deepfake detection.** AASIST is **0.83% EER in-domain but 25.319% EER on ASVspoof 5**; RawNet2/AASIST baselines exceed **29% EER** with minDCF >0.7. Phone audio is codec-compressed and narrow-band — exactly the degrading condition. This is a **risk score**, not a gate. Anyone claiming "AI-verified human speech" from this is overclaiming by roughly 30×.

5. **We cannot claim validated language ID for Nguni languages.** No permissively-licensed model covers isiZulu, isiXhosa, siSwati or isiNdebele. MMS-LID does but is **CC-BY-NC-4.0** (commercially unusable). VoxLingua107 covers Afrikaans and Shona only. Published work reports **high confusability among isiNdebele, Xitsonga, Tshivenda, isiXhosa and isiZulu**. Our own LID must ship with a confusion matrix, not an aggregate accuracy.

6. **We cannot claim calibrated quality scoring for SA languages.** DNSMOS/NISQA/UTMOS have **[NO PUBLISHED BENCHMARK]** on any SA language. Their correlation with human judgement on isiZulu is unknown. Relative ranking only.

7. **We cannot claim active learning beats random selection.** The literature shows uncertainty sampling **sometimes underperforms random** in ASR. Demonstrating a win needs statistical power we will not have. We can show the *mechanism*, not a result.

8. **We cannot cite "11,000 hours / 27 languages" for WAXAL.** No primary source supports it. The paper and released dataset say **~1,250h ASR / ~186h TTS**; the blog says 1,846h/565h/27 languages. And **WAXAL contains no South African languages at all** — it is irrelevant to us except as evidence the gap exists.

9. **We cannot claim our WER numbers transfer to real-world use.** NCHLT figures are **read speech, matched domain**. Real game audio is spontaneous, noisy, and code-switched. AfriSwitch shows code-switched in-the-wild WER at **35.93% for the best system, never below 24% on any language** — a **2–6×** penalty versus monolingual figures.

10. **We cannot claim any improvement that has not passed three gates.** Mann-Whitney p<0.05, bootstrap 95% CI excluding zero, Cliff's delta reported. On small SA eval sets these will frequently fail. **Report the null results.** A pitch containing an honest null is more credible than one containing only wins.

11. **We cannot describe two-account Kaggle usage as a feature.** It may conflict with Kaggle's terms of service. This belongs in a risk register, not a pitch deck.

12. **We cannot store speaker embeddings casually.** Voice biometrics are likely special personal information under **POPIA**. Store cluster IDs and diversity statistics, not retrievable embeddings, and get a compliance answer before launch.

---

## Sources

- Swivuriso: https://arxiv.org/abs/2512.02201 · https://huggingface.co/datasets/dsfsi-anv/za-african-next-voices · https://www.dsfsi.co.za/za-african-next-voices/
- AfriSwitch: https://arxiv.org/abs/2608.26434 · https://huggingface.co/datasets/intronhealth/AfriSwitch
- Tone-Conditioned Curriculum Learning: https://arxiv.org/abs/2606.31642
- Benchmarking ASR for African Languages: https://arxiv.org/abs/2512.10968
- WAXAL: https://arxiv.org/abs/2602.02734 · https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/ · https://huggingface.co/datasets/google/WaxalNLP
- ASVspoof 5: https://arxiv.org/abs/2601.03944 · https://arxiv.org/pdf/2408.08739
- AASIST: https://github.com/clovaai/aasist
- Silero VAD: https://github.com/snakers4/silero-vad
- Moonshine: https://huggingface.co/UsefulSensors/moonshine · https://arxiv.org/html/2602.12241v1
- Whisper large-v3-turbo: https://huggingface.co/openai/whisper-large-v3-turbo
- W2v-BERT 2.0: https://huggingface.co/facebook/w2v-bert-2.0
- MMS: https://huggingface.co/facebook/mms-1b-all
- VoxLingua107 LID: https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa
- ECAPA-TDNN: https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb
- NISQA: https://github.com/gabrielmittag/NISQA
- DNSMOS: https://github.com/microsoft/DNS-Challenge
- UTMOS/UTMOSv2: https://github.com/sarulab-speech/UTMOSv2 · https://arxiv.org/abs/2204.02152
- WhisperX: https://github.com/m-bain/whisperX
- MFA: https://arxiv.org/html/2606.18466v1 · https://arxiv.org/html/2504.07315v1
- Denoising harms ASR: https://arxiv.org/abs/2512.17562 · https://arxiv.org/pdf/2603.04710
- Active learning for ASR: https://arxiv.org/pdf/2406.02566 · https://arxiv.org/html/2403.03728v1 · https://arxiv.org/pdf/2103.03142
- Whisper PEFT on T4: https://github.com/openai/whisper/discussions/988 · https://github.com/Vaibhavs10/fast-whisper-finetuning
- LoRA-INT8 Whisper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12431075/
- Xenova Whisper ONNX sizes: https://huggingface.co/Xenova/whisper-tiny/tree/main/onnx
- NCHLT: https://pmc.ncbi.nlm.nih.gov/articles/PMC8814303/ · https://repo.sadilar.org
- SA code-switching: https://arxiv.org/abs/1807.10949 · https://arxiv.org/abs/2004.04054 · https://arxiv.org/abs/2311.15077
- SA LID confusability: https://dsp.sun.ac.za/~trn/reports/henselmans+vanleeuwen+niesler_lid_prasa13.pdf
- Kaggle GPU quotas: https://www.kaggle.com/docs/efficient-gpu-usage
- MzansiText/MzansiLM: https://arxiv.org/abs/2603.20732
- Chromaprint: https://github.com/acoustid/chromaprint · Dejavu: https://yunpengn.github.io/dejavu/
- WebGPU vs WASM: https://www.sitepoint.com/webgpu-vs-webasm-transformers-js/
