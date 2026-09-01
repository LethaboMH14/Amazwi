# Kaggle overnight ASR run — how it's actually deployed

**Kernel:** https://www.kaggle.com/code/lethabomh14/amazwi-overnight-asr
**Support-files dataset:** https://www.kaggle.com/datasets/lethabomh14/amazwi-ml-support-files

## Why a dataset upload, not `git clone`

The GitHub repo is private, so Kaggle's kernel environment has no credentials to clone it (`git clone` fails with "could not read Username"). Rather than making the repo public or embedding a token in the kernel (a real credential-handling line not worth crossing for this), the actual code this pipeline depends on (`amazwi_ml/`, `reserve_run.py`, `train_asr.py`, `budget.json`, `preflight_swivuriso.json`, both requirements files) is uploaded as a **private Kaggle Dataset** and mounted read-only at `/kaggle/input/amazwi-ml-support-files/` inside the kernel. `kernel_entrypoint.py` copies that into a writable `/kaggle/working/ml/` first (since `reserve_run.py` needs to write `budget.json`, and `/kaggle/input/` is read-only), extracts `amazwi_ml.zip` if needed (Kaggle doesn't always auto-extract), then runs the same gated `reserve_run.py`/`train_asr.py` this repo already tests — nothing here reimplements or bypasses those gates.

## To re-stage and re-push after a code change

```bash
cd starter/ml
rm -rf kaggle/dataset_push_tmp && mkdir -p kaggle/dataset_push_tmp
cp -r amazwi_ml kaggle/dataset_push_tmp/amazwi_ml
cp kaggle/reserve_run.py kaggle/train_asr.py kaggle/budget.json kaggle/preflight_swivuriso.json requirements-kaggle.txt requirements.txt kaggle/dataset_push_tmp/
cp kaggle/dataset_push/dataset-metadata.json kaggle/dataset_push_tmp/
cd kaggle/dataset_push_tmp && python -m kaggle datasets version -p . -m "update" --dir-mode zip
cd ../.. && rm -rf kaggle/dataset_push_tmp

cp kaggle/kernel_entrypoint.py kaggle/kernel_push/amazwi-overnight-asr.py
cd kaggle/kernel_push && python -m kaggle kernels push -p .
```

## Monitoring

```bash
python -m kaggle kernels status lethabomh14/amazwi-overnight-asr
python -m kaggle kernels output lethabomh14/amazwi-overnight-asr -p <local dir>   # pulls the log + any output files
```

## Scope of this run, stated plainly

- **isiZulu ("zul") + Setswana ("tsn") DEV splits only** of Swivuriso (`dsfsi-anv/za-african-next-voices-compressed`) — ~683MB, ~8,000 clips combined. **Not** the full ~3,000-hour, 7-language corpus, and **not** the (much larger) `train` split — a deliberately bounded, overnight-sized scope, not a production training run.
- Candidate: `whisper-large-v3-turbo-peft` (LoRA fine-tune via PEFT), 3 epochs, batch size 8.
- Budget reservation: 10 GPU-hours requested against the `ISIZULU_ADAPTATION` phase cap (16h) — filed under one phase bucket even though both languages train together in this run; a simplification for one overnight pass, not a claim that Setswana adaptation is separately tracked here.
- **Governance ledger reconciliation is provisional.** The reservation happens inside the Kaggle run against its own copy of `budget.json` (staged from the dataset, not this git repo directly) — the canonical `starter/ml/kaggle/budget.json` in this repo needs to be updated by hand from the run's actual output once it completes, not assumed to already reflect it.
