import pandas as pd
from dataclasses import asdict
from typing import List
from pathlib import Path
from models import JobListing

FILEPATH = "output/vagas.xlsx"

COLUMNS = ["title", "company", "location", "salary", "source", "url", "description"]


def export_to_excel(jobs: List[JobListing], filepath: str = FILEPATH) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = [asdict(job) for job in jobs]
    df = pd.DataFrame(rows, columns=COLUMNS)

    df.to_excel(filepath, index=False)
    print(f"✅ {len(df)} vagas exportadas para {filepath}")