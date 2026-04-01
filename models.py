from dataclasses import dataclass
from typing import Optional


@dataclass
class JobListing:
    title: str
    company: str
    location: str
    url: str
    source: str                  # "linkedin", "catho" etc.
    salary: Optional[str] = None
    description: Optional[str] = None
