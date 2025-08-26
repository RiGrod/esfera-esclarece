# Aplicativo de Consulta de Legislação do Setor Elétrico

Este protótipo carrega arquivos Markdown como base de conhecimento e consulta documentos oficiais da legislação brasileira para complementar as respostas.

## Uso

1. Crie um diretório `knowledge_base` e coloque arquivos `.md` com o conteúdo desejado.
2. Execute:

```bash
python main.py "sua pergunta" --kb knowledge_base
```

Os arquivos Markdown podem incluir referências a leis no formato:

```
Lei 9.427/1996 | https://www.planalto.gov.br/ccivil_03/leis/l9427.htm
```

O aplicativo verificará se o texto da lei contém indicações de revogação antes de citá-la.

## Requisitos

- Python 3.11
- `requests` (ver `requirements.txt`)
