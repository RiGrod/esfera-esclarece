import os
import re
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Evidence:
    source: str
    location: str
    snippet: str

class KnowledgeBase:
    """Simple loader and searcher for markdown knowledge base."""

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.documents = []
        self._load_documents()

    def _load_documents(self) -> None:
        for root, _, files in os.walk(self.base_path):
            for fname in files:
                if fname.lower().endswith('.md'):
                    path = os.path.join(root, fname)
                    with open(path, 'r', encoding='utf-8') as fh:
                        text = fh.read()
                    self.documents.append((path, text))

    def search(self, query: str, max_results: int = 5) -> List[Evidence]:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        evidences: List[Evidence] = []
        for path, text in self.documents:
            for m in pattern.finditer(text):
                start = max(0, m.start() - 200)
                end = min(len(text), m.end() + 200)
                snippet = text[start:end].replace('\n', ' ')
                evidences.append(Evidence(path, f"{start}-{end}", snippet))
                if len(evidences) >= max_results:
                    return evidences
        return evidences
