# Citation Information

## Citing This Pipeline

If you use the TCASIA Alternative Splicing Analysis Pipeline in your research, please cite:

```bibtex
@article{TCASIA2026,
  title={TCASIA: An Integrative Atlas Linking Alternative Splicing Landscapes for Cancer Immunotherapy},
  author={Your Name and Collaborators},
  journal={Journal Name},
  year={2026},
  volume={XX},
  pages={XXX-XXX},
  doi={10.xxxx/xxxxx}
}
```

## Citing Individual Tools

This pipeline integrates multiple tools. Please also cite the original publications:

### Workflow Management

**Snakemake**
```bibtex
@article{Molder2021,
  title={Sustainable data analysis with Snakemake},
  author={M{\"o}lder, Felix and Jablonski, Kim Philipp and Letcher, Brice and Hall, Michael B and Tomkins-Tinch, Christopher H and Sochat, Vanessa and Forster, Jan and Lee, Soohyun and Twardziok, Sven O and Kanitz, Alexander and others},
  journal={F1000Research},
  volume={10},
  year={2021},
  publisher={Faculty of 1000 Ltd}
}
```

### Alignment

**STAR**
```bibtex
@article{Dobin2013,
  title={STAR: ultrafast universal RNA-seq aligner},
  author={Dobin, Alexander and Davis, Carrie A and Schlesinger, Felix and Drenkow, Jorg and Zaleski, Chris and Jha, Sonali and Batut, Philippe and Chaisson, Mark and Gingeras, Thomas R},
  journal={Bioinformatics},
  volume={29},
  number={1},
  pages={15--21},
  year={2013},
  publisher={Oxford University Press}
}
```

**featureCounts**
```bibtex
@article{Liao2014,
  title={featureCounts: an efficient general purpose program for assigning sequence reads to genomic features},
  author={Liao, Yang and Smyth, Gordon K and Shi, Wei},
  journal={Bioinformatics},
  volume={30},
  number={7},
  pages={923--930},
  year={2014},
  publisher={Oxford University Press}
}
```

### Alternative Splicing Detection

**rMATS**
```bibtex
@article{Shen2014,
  title={rMATS: robust and flexible detection of differential alternative splicing from replicate RNA-Seq data},
  author={Shen, Shihao and Park, Juw Won and Lu, Zhi-xiang and Lin, Lan and Henry, Michael D and Wu, Ying Nian and Zhou, Qing and Xing, Yi},
  journal={Proceedings of the National Academy of Sciences},
  volume={111},
  number={51},
  pages={E5593--E5601},
  year={2014},
  publisher={National Acad Sciences}
}
```

**MAJIQ**
```bibtex
@article{VaqueroGarcia2016,
  title={A new view of transcriptome complexity and regulation through the lens of local splicing variations},
  author={Vaquero-Garcia, Jorge and Barrera, Alejandro and Gazzara, Matthew R and Gonz{\'a}lez-Vallinas, Juan and Lahens, Nicholas F and Hogenesch, John B and Lynch, Kristen W and Barash, Yoseph},
  journal={eLife},
  volume={5},
  pages={e11752},
  year={2016},
  publisher={eLife Sciences Publications Limited}
}
```

**SUPPA2**
```bibtex
@article{Trincado2018,
  title={SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions},
  author={Trincado, Juan L and Entizne, Juan C and Hysenaj, Gerald and Singh, Babita and Skalic, Miha and Elliott, David J and Eyras, Eduardo},
  journal={Genome Biology},
  volume={19},
  number={1},
  pages={1--11},
  year={2018},
  publisher={BioMed Central}
}
```

**SplAdder**
```bibtex
@article{Kahles2016,
  title={SplAdder: identification, quantification and testing of alternative splicing events from RNA-Seq data},
  author={Kahles, Andr{\'e} and Ong, Cheng Soon and Zhong, Yi and R{\"a}tsch, Gunnar},
  journal={Bioinformatics},
  volume={32},
  number={12},
  pages={1840--1847},
  year={2016},
  publisher={Oxford University Press}
}
```

**Salmon** (used by SUPPA2)
```bibtex
@article{Patro2017,
  title={Salmon provides fast and bias-aware quantification of transcript expression},
  author={Patro, Rob and Duggal, Geet and Love, Michael I and Irizarry, Rafael A and Kingsford, Carl},
  journal={Nature Methods},
  volume={14},
  number={4},
  pages={417--419},
  year={2017},
  publisher={Nature Publishing Group}
}
```

### Reference Annotation

**GENCODE**
```bibtex
@article{Frankish2019,
  title={GENCODE reference annotation for the human and mouse genomes},
  author={Frankish, Adam and Diekhans, Mark and Ferreira, Anne-Maud and Johnson, Rory and Jungreis, Irwin and Loveland, Jane and Mudge, Jonathan M and Sisu, Cristina and Wright, James and Armstrong, Joel and others},
  journal={Nucleic Acids Research},
  volume={47},
  number={D1},
  pages={D766--D773},
  year={2019},
  publisher={Oxford University Press}
}
```

## Software Versions

The pipeline was developed and tested with:

| Software | Version | Citation Required |
|----------|---------|-------------------|
| Snakemake | ≥7.0.0 | Yes |
| STAR | 2.7.7a | Yes |
| rMATS | 4.3.0 | Yes |
| MAJIQ | 2.5.11 | Yes |
| SUPPA2 | 2.3 | Yes |
| SplAdder | 3.1.1 | Yes |
| Salmon | 1.10.3 | Yes |
| featureCounts | 2.0.1 | Yes |
| samtools | 1.15 | Optional |
| GENCODE | v34 | Yes |

## Acknowledgments

We thank the developers and maintainers of all the tools integrated in this pipeline for their excellent work and continued support of the bioinformatics community.

## License

This pipeline is released under the MIT License. See [LICENSE](../LICENSE) for details.

Individual tools may have different licenses:
- **rMATS**: Free for academic use
- **MAJIQ**: Academic license required
- **SUPPA2**: MIT License
- **SplAdder**: BSD 3-Clause License
- **STAR**: GPLv3
- **Salmon**: GPLv3

Please ensure compliance with individual tool licenses when using this pipeline.
