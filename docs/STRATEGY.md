# Estratégia – Desenvolvimento de Aplicação de ML (Readmissão 30d)

Este documento resume o plano do projeto, cobrindo **coleta**, **preparo**,
**treino**, **validação**, **deploy** e **monitoramento**.

## 1) Problema & Objetivo
Prever se o paciente será **readmitido em 30 dias** pós-alta.
Objetivo: priorizar follow-up, reduzir custos e melhorar desfechos.

## 2) Dados
- Fonte: EHR/EMR, ADT, billing, laboratórios (em produção).
- Neste template: **dados sintéticos**.
- Esquema de features (exemplos):
  - `age`, `sex`, `length_of_stay`, `comorbidities`,
    `prior_readmissions`, `medication_count`, `lab_score`,
    `discharge_type`.
- Target: `readmitted_30d` (0/1).

## 3) Preparo
- Limpeza, imputação, normalização e codificação categórica.
- Split train/test estratificado.
- Versionamento de datasets com **DVC**.

## 4) Modelagem
- Pipeline com pré-processamento + **RandomForest**.
- Métricas: ROC-AUC, F1, precisão/recall, Brier (calibração).
- `params.yaml` guarda hiperparâmetros.

## 5) Validação
- Avaliar por subgrupos (ex.: faixas etárias).
- Curvas Precision-Recall; checar threshold por objetivo clínico.

## 6) Deploy da API
- **FastAPI** publica `/predict`.
- **Docker**: imagem única com modelo empacotado.
- Gateways/APIs e autenticação na borda (ex.: OAuth2/JWT).

## 7) Observabilidade
- Logs estruturados com latência, payload size (sem PII).
- Métricas de tráfego, erro e **drift** (distribuição de features).
- Rotina de re-treino baseada em janela temporal.

## 8) Segurança & Conformidade
- Sem PHI no repo. Use cofres de segredo.
- Controle de acesso e trilhas de auditoria.
- LGPD/HIPAA: mínimo necessário, finalidade e consentimento.

## 9) Operações
- CI valida pipeline (`dvc repro --dry`) e testa código.
- CD opcional: deploy por tag/release e rollback versionado.
