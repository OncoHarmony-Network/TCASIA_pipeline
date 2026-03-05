# TCASIA Alternative Splicing Analysis Pipeline

[![Snakemake](https://img.shields.io/badge/snakemake-≥7.0.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A reproducible computational pipeline for detecting alternative splicing events from RNA-seq data, integrating four state-of-the-art algorithms: rMATS, MAJIQ, SUPPA2, and SplAdder.

## Overview

This pipeline implements the alternative splicing detection workflow described in the TCASIA (The Cancer Alternative Splicing and Immunotherapy Atlas) project. It provides a standardized, reproducible framework for:

- **RNA-seq alignment** using STAR (2-pass mode)
- **Multi-algorithm AS detection** with rMATS, MAJIQ, SUPPA2, and SplAdder
- **Automated workflow management** via Snakemake
- **Conda-based environment isolation** for reproducibility

## Features

- ✅ **Multi-algorithm integration**: Combines 4 complementary AS detection tools
- ✅ **Reproducible workflows**: Snakemake-based automation with version control
- ✅ **Conda environments**: Isolated dependencies for each tool
- ✅ **Scalable**: Parallel processing support for large cohorts
- ✅ **Publication-ready**: Parameters optimized for GRCh38/GENCODE v34

## Quick Start

### Prerequisites

- Linux/Unix system
- [Conda](https://docs.conda.io/en/latest/), [Mamba](https://mamba.readthedocs.io/), or [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
- ≥16 GB RAM (32 GB recommended)
- Disk space: ~30-50 GB per sample + 30 GB for references (e.g., 10-sample cohort ≈ 300-500 GB)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline.git
cd TCASIA_AS_Pipeline

# Create Snakemake environment (using micromamba)
micromamba create -c conda-forge -c bioconda -n snakemake snakemake
micromamba activate snakemake

# Or using conda/mamba
# conda create -c conda-forge -c bioconda -n snakemake snakemake
# conda activate snakemake
```

### Basic Usage

#### 1. RNA-seq Alignment

```bash
cd workflows/01_alignment

# Edit configuration
cp config/config.yml config/my_config.yml
# Modify paths in my_config.yml

# Run alignment
snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 10 --use-conda
```

#### 2. AS Event Detection

```bash
cd workflows/02_as_calling

# Edit configuration
cp config/config.yml config/my_config.yml
# Modify paths in my_config.yml

# Run AS calling
snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 40 --use-conda
```

## Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Usage Tutorial](docs/usage.md) - Step-by-step workflow execution
- [Parameter Reference](docs/parameters.md) - Complete parameter documentation
- [Output Format](docs/output_format.md) - Description of output files
- [Method Verification](METHOD_VERIFICATION.md) - Code-method consistency report

## Workflow Architecture

```
Input: FASTQ files
    ↓
[01_alignment]
    ├── Quality control (fastp)
    ├── STAR alignment (2-pass)
    ├── BAM sorting & indexing
    └── Gene counting (featureCounts)
    ↓
[02_as_calling]
    ├── rMATS (BAM mode, --cstat 0.0001)
    ├── MAJIQ (--minreads 10)
    ├── SUPPA2 (Salmon + psiPerEvent)
    └── SplAdder (default confidence)
    ↓
Output: AS events (PSI/ΔPSI values)
```

## Key Parameters

| Tool | Version | Key Parameters |
|------|---------|----------------|
| Snakemake | ≥7.0.0 | Workflow management |
| STAR | 2.7.7a | `--twopassMode Basic` |
| rMATS | 4.3.0 | `--cstat 0.0001`, `--variable-read-length` |
| MAJIQ | 2.5.11 | `--minreads 10` |
| SUPPA2 | 2.3 | Salmon `--gcBias`, `-f 1` |
| SplAdder | 3.1.1 | Default confidence |

**Reference**: GRCh38 + GENCODE v34

## Citation

If you use this pipeline in your research, please cite:

```bibtex
@article{TCASIA2026,
  title={TCASIA: The Cancer Alternative Splicing and Immunotherapy Atlas},
  author={Your Name et al.},
  journal={Journal Name},
  year={2026},
  doi={10.xxxx/xxxxx}
}
```

Please also cite the individual tools:
- **rMATS**: Shen et al., PNAS 2014
- **MAJIQ**: Vaquero-Garcia et al., eLife 2016
- **SUPPA2**: Trincado et al., Genome Biology 2018
- **SplAdder**: Kahles et al., Genome Biology 2016

See [CITATION.md](CITATION.md) for complete citation information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline/issues)
- **Documentation**: [Full Documentation](docs/)
- **Contact**: jianguo.zhou@zmu.edu.cn

## Acknowledgments

This pipeline was developed as part of the TCASIA project. We thank the developers of rMATS, MAJIQ, SUPPA2, and SplAdder for their excellent tools.

---

**Note**: This pipeline implements the alignment and AS calling steps described in the TCASIA manuscript. Downstream analyses (quality filtering, consensus calling, integration) are performed separately.
