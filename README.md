## Projeto de Agentes de IA

Estrutura pensada para desenvolvimento local (Cursor/VSCode) seguindo boas práticas mínimas.

### Estrutura de pastas

```
IA/
  ├─ src/
  │   ├─ agents/          # Agentes e orquestração
  │   ├─ tools/           # Ferramentas (busca, RAG, ações externas)
  │   ├─ chains/          # Cadeias/pipelines de prompts
  │   └─ config/          # Configurações e carregamento de env
  ├─ data/
  │   ├─ raw/             # Dados brutos
  │   └─ processed/       # Dados tratados
  ├─ notebooks/           # Experimentos Jupyter/Colab (opcional)
  ├─ scripts/             # Scripts utilitários (ETL, indexação, etc.)
  ├─ tests/               # Testes unitários
  ├─ logs/                # Logs de execução
  ├─ requirements.txt
  ├─ .env.example
  └─ README.md
```

### Setup

1. Crie seu `.env` na pasta `IA/` baseado no `.env.example`:

```
GOOGLE_API_KEY=coloque_sua_chave
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
```

2. Crie e ative um venv (recomendado):

```
py -m venv .venv
.\.venv\Scripts\activate
```

3. Instale dependências:

```
pip install -r IA/requirements.txt
```

### Rodando o exemplo

```bash
python -m src.main
```

Se tudo estiver correto, você verá o sistema de triagem processando casos de teste.

### Próximos passos

Ir no arquivo COMO_USAR.md para ter um tutorial de como rodar o projeto.
