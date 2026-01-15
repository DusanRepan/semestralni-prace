from dataclasses import dataclass
from typing import Optional

@dataclass
class Zver:
    druh: str
    vek: int
    pohlavi: str
    datum_pozorovani: str
    datum_uloveni: Optional[str] = None
