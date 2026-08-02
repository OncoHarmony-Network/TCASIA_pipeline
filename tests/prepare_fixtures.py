from pathlib import Path

root = Path(__file__).resolve().parent / "fixtures"
(root / "aligned" / "patient_01").mkdir(parents=True, exist_ok=True)
(root / "reference" / "star_index").mkdir(parents=True, exist_ok=True)
(root / "reference" / "salmon_index").mkdir(parents=True, exist_ok=True)

for relative_path in (
    "aligned/patient_01/patient_01_Aligned.sortedByCoord.out.bam",
    "reference/annotation.gtf.txt",
    "reference/annotation.gff3.txt",
    "reference/majiq.license.txt",
    "reference/events.ioe.txt",
):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
