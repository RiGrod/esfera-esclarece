from dataclasses import dataclass
from typing import List

from .knowledge_base import Evidence
from .legislation import LegalDocument

@dataclass
class Response:
    answer: str
    documents: List[str]

def build_response(evidences: List[Evidence], legal_docs: List[LegalDocument]) -> Response:
    if not evidences:
        return Response("Não há evidência nos documentos consultados", [])

    answer_parts = []
    docs_list = []

    for ev in evidences:
        answer_parts.append(ev.snippet)
        docs_list.append(f"{ev.source} — local {ev.location} — {ev.snippet[:300]}")

    for doc in legal_docs:
        status = "vigente" if doc.active else "revogado"
        answer_parts.append(f"{doc.title} ({status})")
        docs_list.append(f"{doc.title} — {doc.url} — {doc.location} — {doc.snippet[:300]}")

    answer = " ".join(answer_parts)
    return Response(answer, docs_list)
