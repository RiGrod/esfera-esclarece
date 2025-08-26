import argparse
import re
from typing import List

from esfera.knowledge_base import KnowledgeBase
from esfera.legislation import LegislationClient, LegalDocument
from esfera.response_builder import build_response

REGEX_REFERENCE = re.compile(r"(Lei|Decreto|Portaria|Resolu[cç][aã]o)[^\d]*(\d+[\.\/]?\d*)[\/\.](\d{4})")


def extract_references(text: str) -> List[str]:
    return [" ".join(m.groups()) for m in REGEX_REFERENCE.finditer(text)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Busca evidências em base markdown e legislação brasileira")
    parser.add_argument("question", help="Pergunta a ser respondida")
    parser.add_argument("--kb", default="knowledge_base", help="Diretório com arquivos MD")
    args = parser.parse_args()

    kb = KnowledgeBase(args.kb)
    evidences = kb.search(args.question)

    references = []
    for ev in evidences:
        references.extend(extract_references(ev.snippet))

    client = LegislationClient()
    legal_docs: List[LegalDocument] = []
    for ref in references:
        # Expect user to provide URL via pattern "Nome | URL" inside snippet
        parts = [p.strip() for p in ref.split("|")]
        title = parts[0]
        url = parts[1] if len(parts) > 1 else ""
        if url:
            doc = client.get_document(title, url)
            if doc:
                legal_docs.append(doc)

    response = build_response(evidences, legal_docs)

    print("(A) Resposta:\n" + response.answer + "\n")
    print("(B) Documentos consultados:")
    for doc in response.documents:
        print("- " + doc)


if __name__ == "__main__":
    main()
