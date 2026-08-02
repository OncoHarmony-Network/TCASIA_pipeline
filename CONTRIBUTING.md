# Contributing

Keep changes focused and consistent with the existing Snakemake structure.

## Setup

```bash
git clone https://github.com/OncoHarmony-Network/TCASIA_pipeline.git
cd TCASIA_pipeline
micromamba create -f environment.yml
micromamba activate tcasia-workflow
```

## Rules

- Put shared parsing in `workflows/lib/`.
- Put caller-specific logic in `workflows/02_as_calling/rules/`.
- Declare inputs, outputs, logs, threads, and Conda environments.
- Quote shell paths with Snakemake's `:q` formatter.
- Update configuration templates and tests with behavior changes.
- Do not include credentials, MAJIQ licenses, controlled data, or private paths.

## Test

```bash
bash tests/run_tests.sh
git diff --check
```

Open issues and pull requests at:

https://github.com/OncoHarmony-Network/TCASIA_pipeline
