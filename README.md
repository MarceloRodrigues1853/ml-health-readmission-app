# App de ML – Previsão de Readmissão Hospitalar (30 dias)

Template completo para um projeto de **ML em saúde** que prevê
readmissão em até 30 dias. Inclui **DVC**, **pipeline de treino**,
**API FastAPI**, **Docker**, **CI (GitHub Actions)** e documentação.

**Autor**: Marcelo Rodrigues — Gerado em 2025-09-23

> ⚠️ Aviso: dados reais de pacientes (PHI/LGPD) **não devem** ser
> colocados neste repositório. O pipeline usa **dados sintéticos**.

## ⚙️ Uso rápido

```bash
# 1) Ambiente
python -m venv .venv && source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) DVC
dvc init
git add .dvc .gitignore && git commit -m "chore: init dvc"

# 3) Pipeline (gera dados sintéticos, treina e avalia)
dvc repro  # ou: dvc repro --dry (simulação)

# 4) Subir API local
uvicorn src.service.app:app --reload
# Abra http://127.0.0.1:8000/docs
```

## 📁 Estrutura

```
.
├── .github/workflows/ci.yml
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── params.yaml
├── dvc.yaml
├── api/openapi.yaml
├── src/
│   ├── pipeline/prepare.py
│   ├── pipeline/train.py
│   ├── pipeline/evaluate.py
│   └── service/app.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── tests/
│   ├── test_pipeline.py
│   └── test_service_schema.py
└── docs/
    ├── STRATEGY.md
    ├── MODEL_CARD.md
    ├── MONITORING.md
    └── RISK_CHECKLIST.md
```

## 🔐 Conformidade e ética (resumo)

- **Sem PHI** no repo (nem em commits antigos).
- Variáveis sensíveis via `.env` / cofres (p.ex., Secrets Manager).
- Acompanhe métricas de **viés** e **desempenho** por subgrupos.
- Use **controle de acesso** no ambiente de produção.

Veja `docs/MODEL_CARD.md` e `docs/RISK_CHECKLIST.md`.

## 🧪 CI

Workflow em `.github/workflows/ci.yml`:
- Instala dependências, valida DVC (`--dry`), roda pytest.
- Lint com flake8 (não falha o build por padrão).

## 🚀 Docker

```bash
docker build -t readmission-api .
docker run -p 8000:8000 readmission-api
# acesse http://localhost:8000/docs
```

## 🔗 GitHub Pages (link público da estratégia)
- Coloque docs extras em `docs/`.
- Ative **Settings → Pages** (branch main, pasta `/docs`).
