import re
from dataclasses import dataclass
from typing import Optional

import requests

@dataclass
class LegalDocument:
    title: str
    url: str
    location: str
    snippet: str
    active: bool

REVOGADO_PATTERN = re.compile(r"revogad[ao]", re.IGNORECASE)

class LegislationClient:
    """Fetches legislation texts and checks if they are active."""

    def fetch(self, url: str) -> Optional[str]:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception:
            return None
        return None

    def check_active(self, text: str) -> bool:
        return not bool(REVOGADO_PATTERN.search(text))

    def extract_snippet(self, text: str, query: str) -> str:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        m = pattern.search(text)
        if not m:
            return text[:300].replace('\n', ' ')
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 200)
        return text[start:end].replace('\n', ' ')

    def get_document(self, title: str, url: str, query: str = "") -> Optional[LegalDocument]:
        text = self.fetch(url)
        if text is None:
            return None
        active = self.check_active(text)
        snippet = self.extract_snippet(text, query)
        return LegalDocument(title=title, url=url, location=query, snippet=snippet, active=active)
