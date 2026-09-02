# Kaggle run records

This directory stores non-secret run records for Team Sonar A and Team Sonar B.

A run record moves to `COMPLETED` in `starter/ml/kaggle/budget.json` only after the
exact dataset revision, model revision, immutable manifest hash, config hash and
actual GPU-hours are pulled from the real run's output (`kaggle kernels output`)
and independently confirmed. Until that pull happens, this file may say a run was
**ATTEMPTED**, but `budget.json` correctly has no completed entry for it — those
two facts are not a contradiction, and this file exists so a reader sees both.

## Lethabo, Team Sonar A

- account alias: `team-sonar-a`
- candidate: `whisper-large-v3-turbo-peft` (LoRA fine-tune, 3 epochs, batch size 8)
- **status: `ATTEMPTED — completion unverified`** (see below; do not read this as `COMPLETED` or as `BLOCKED`)
- dataset revision: `3f988acc73676291de8a17a26abe2c716003233d` (Swivuriso `dsfsi-anv/za-african-next-voices-compressed`, isiZulu + Setswana **dev** splits only — not the full corpus or `train` split), preflight `APPROVED` by LethaboMH14 on 2026-09-01, `starter/ml/kaggle/preflight_swivuriso.json`
- model revision: not recorded in this repo — pending pull from the run's actual output
- manifest SHA-256 / config SHA-256: **not yet known here.** These are generated inside the Kaggle run against a staged copy of `budget.json`, not this repo's copy directly (see `KAGGLE_RUN.md`'s "Governance ledger reconciliation is provisional" note) — pulling them requires `kaggle kernels output lethabomh14/amazwi-overnight-asr`, which no session so far has run and pulled back into this repo
- reservation ID: **not present in `starter/ml/kaggle/budget.json`.** That file's schema (`amazwi_ml/budget.py`) requires real 64-hex-char manifest/config hashes to create a valid entry — inventing placeholder hashes to make the file "look reconciled" would be worse than the current gap, so it is left empty rather than falsified. A real hours figure is not fabricated here either: 10 GPU-hours were *requested* against the `ISIZULU_ADAPTATION` phase cap per `KAGGLE_RUN.md`, but a request is not evidence of consumption.
- output location: `https://www.kaggle.com/code/lethabomh14/amazwi-overnight-asr`
- **What actually happened, from this repo's own `BUILD_LOG.md`:** kernel pushed and reached `RUNNING` at least 9 times (v1–v9) across roughly 00:15–12:00 on 2 Sep. v3 was the only attempt that got deep into real training before failing on a data-quality edge case (since fixed). v6/v7/v8 failed with a byte-identical `ConnectionError` from Kaggle's own secrets service. v9 was pushed after Lethabo confirmed `HF_TOKEN` was genuinely attached and was confirmed `RUNNING` via `kaggle kernels status` — **no later entry in this repo confirms v9 completed, produced a checkpoint, or failed.** Priority shifted to the live golden-path demo at that point and nobody has checked back.
- **To actually close this out:** run `kaggle kernels status lethabomh14/amazwi-overnight-asr`. If `COMPLETED`, run `kaggle kernels output ... -p <dir>`, pull the real manifest/config/artefact hashes and actual GPU-hours from the output, and call `amazwi_ml.budget.reserve_gpu_run` then `complete_gpu_run` for real — that is what turns this from a claim into a verified ledger entry. If it failed or is still running, say which, here, honestly.

## Sbu, Team Sonar B

- account alias: `team-sonar-b`
- candidate: comparator adapter pending implementation
- status: `BLOCKED` — genuinely accurate, unlike Team Sonar A above. **No run has ever been attempted on this account.** Do not conflate this with Team Sonar A's status.
- dataset revision: pending gated preflight
- model revision: pending explicit approval
- manifest SHA-256: pending immutable manifest
- config SHA-256: pending run configuration
- reservation ID: pending budget reservation
- output location: pending Sbu Kaggle kernel

Do not place Kaggle credentials, access tokens, downloaded audio, checkpoints, or
unverified external revisions in this directory.
