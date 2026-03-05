# Contributing to TCASIA AS Pipeline

Thank you for your interest in contributing to the TCASIA Alternative Splicing Analysis Pipeline! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Reporting Issues](#reporting-issues)
- [Submitting Changes](#submitting-changes)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Documentation](#documentation)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Reports**: Report issues with the pipeline
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit bug fixes or new features
4. **Documentation**: Improve or expand documentation
5. **Testing**: Add test cases or improve test coverage
6. **Examples**: Provide example datasets or use cases

## Reporting Issues

### Before Submitting an Issue

1. **Search existing issues**: Check if the issue has already been reported
2. **Check documentation**: Review the [documentation](docs/) for solutions
3. **Test with latest version**: Ensure you're using the latest release

### Creating a Good Issue Report

Include the following information:

**For Bug Reports:**
```markdown
**Description**: Brief description of the bug

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. ...

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: [e.g., Ubuntu 20.04]
- Snakemake version: [e.g., 7.32.4]
- Tool versions: [e.g., STAR 2.7.7a, rMATS 4.3.0]
- Configuration: [attach config.yml if relevant]

**Logs**: Attach relevant log files or error messages

**Additional Context**: Any other relevant information
```

**For Feature Requests:**
```markdown
**Feature Description**: Clear description of the proposed feature

**Use Case**: Why is this feature needed?

**Proposed Solution**: How should it work?

**Alternatives Considered**: Other approaches you've considered

**Additional Context**: Any other relevant information
```

## Submitting Changes

### Workflow

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline.git
   cd TCASIA_AS_Pipeline
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Write clear, concise code
   - Follow style guidelines (see below)
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Test alignment workflow
   cd workflows/01_alignment
   snakemake -s Snakefile --configfile config/test_config.yml --dry-run

   # Test AS calling workflow
   cd workflows/02_as_calling
   snakemake -s Snakefile --configfile config/test_config.yml --dry-run
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature X"
   # or
   git commit -m "fix: resolve issue with Y"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### Pull Request Guidelines

**PR Title Format:**
```
<type>: <short description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Maintenance tasks
```

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes Made
- Change 1
- Change 2
- ...

## Testing
How were these changes tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

## Development Setup

### Prerequisites

- Linux/Unix system
- Conda/Mamba/Micromamba
- Git
- Python ≥3.8
- Snakemake ≥7.0.0

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline.git
cd TCASIA_AS_Pipeline

# Create development environment
micromamba create -n tcasia-dev -c conda-forge -c bioconda \
  snakemake python=3.10 pytest black flake8

# Activate environment
micromamba activate tcasia-dev

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Directory Structure for Development

```
TCASIA_AS_Pipeline/
├── workflows/
│   ├── 01_alignment/
│   │   ├── Snakefile
│   │   ├── config/
│   │   └── envs/
│   └── 02_as_calling/
│       ├── Snakefile
│       ├── config/
│       ├── envs/
│       └── rules/
├── docs/
├── tests/
├── scripts/
└── examples/
```

## Testing

### Running Tests

```bash
# Syntax check
snakemake -s workflows/01_alignment/Snakefile --dry-run
snakemake -s workflows/02_as_calling/Snakefile --dry-run

# Lint Snakefiles
snakemake --lint

# Test with example data (if available)
cd tests
bash run_tests.sh
```

### Adding Tests

When adding new features:

1. **Add test data**: Place in `tests/data/`
2. **Add test config**: Create `tests/config/test_feature.yml`
3. **Add test script**: Create `tests/test_feature.sh`
4. **Document test**: Update `tests/README.md`

## Documentation

### Documentation Structure

```
docs/
├── installation.md      # Installation guide
├── usage.md            # Usage tutorial
├── parameters.md       # Parameter reference
├── output_format.md    # Output description
└── troubleshooting.md  # Common issues
```

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add screenshots/diagrams where helpful
- Keep formatting consistent
- Test all commands and examples

### Documentation Style

- **Headers**: Use sentence case
- **Code blocks**: Specify language for syntax highlighting
- **Links**: Use descriptive text, not "click here"
- **Examples**: Provide realistic, working examples

## Style Guidelines

### Snakemake Style

```python
# Rule naming: lowercase with underscores
rule align_reads:
    input:
        r1="data/{sample}_R1.fastq.gz",
        r2="data/{sample}_R2.fastq.gz"
    output:
        bam="aligned/{sample}.bam"
    params:
        index=config["star_index"]
    threads: 16
    conda:
        "envs/star.yaml"
    shell:
        """
        STAR --runThreadN {threads} \
             --genomeDir {params.index} \
             --readFilesIn {input.r1} {input.r2} \
             --outFileNamePrefix {wildcards.sample}
        """
```

### YAML Style

```yaml
# Use 2-space indentation
# Add comments for clarity
# Group related parameters

# Project information
cohort: PRJNA498500

# Directory paths
root_DIR: /data/IO_RNA
raw_DIR: /data/IO_RNA/fastq

# Reference files
ref: /data/reference/gencode.v34.annotation.gtf
ref_fa: /data/reference/GRCh38.primary_assembly.genome.fa
```

### Shell Script Style

```bash
#!/bin/bash
# Script description
# Usage: script.sh <input> <output>

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly INPUT="${1:-}"
readonly OUTPUT="${2:-}"

# Functions
function main() {
    # Main logic here
    echo "Processing ${INPUT}..."
}

# Execute
main "$@"
```

### Python Style

Follow PEP 8:
- 4-space indentation
- Max line length: 88 characters (Black formatter)
- Use type hints where appropriate
- Docstrings for functions and classes

```python
def calculate_psi(inclusion_counts: list[int],
                  skipping_counts: list[int]) -> float:
    """
    Calculate PSI (Percent Spliced In) value.

    Args:
        inclusion_counts: Junction counts supporting inclusion
        skipping_counts: Junction counts supporting skipping

    Returns:
        PSI value between 0 and 1
    """
    total_inclusion = sum(inclusion_counts)
    total_skipping = sum(skipping_counts)

    if total_inclusion + total_skipping == 0:
        return 0.0

    return total_inclusion / (total_inclusion + total_skipping)
```

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```
feat(rmats): add support for variable read length

- Add --variable-read-length flag to rMATS rule
- Update documentation with new parameter
- Add test case for mixed read lengths

Closes #45
```

```
fix(majiq): correct license path in config

The MAJIQ license path was incorrectly specified in the
configuration template, causing build failures.

Fixes #67
```

## Review Process

### What to Expect

1. **Initial Review**: Maintainers will review within 1-2 weeks
2. **Feedback**: You may receive requests for changes
3. **Iteration**: Make requested changes and push updates
4. **Approval**: Once approved, PR will be merged
5. **Release**: Changes included in next release

### Review Criteria

- Code quality and style
- Test coverage
- Documentation completeness
- Backward compatibility
- Performance impact

## Getting Help

### Resources

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline/discussions)

### Contact

- **Email**: jianguo.zhou@zmu.edu.cn
- **GitHub**: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

## Recognition

Contributors will be acknowledged in:
- `CONTRIBUTORS.md` file
- Release notes
- Project documentation

Thank you for contributing to TCASIA AS Pipeline! 🎉
