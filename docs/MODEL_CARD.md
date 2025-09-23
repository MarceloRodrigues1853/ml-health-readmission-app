# Model Card – Readmission 30d

**Tarefa**: classificação binária (readmissão em 30 dias).  
**Dados**: sintéticos para este template (não representam pacientes reais).  
**Intended Use**: apoio a priorização de follow-up. Não substituir julgamento
clínico. Decisão final é do médico/equipe.

## Métricas
- ROC-AUC, F1, precisão, recall, Brier.

## Limitações
- Dados sintéticos não refletem viés real.
- Drift de dados pode degradar desempenho.
- Não adequado para diagnósticos.

## Considerações Éticas
- Minimizar viés por idade/sexo/raça (avaliar por subgrupos).
- Transparência e explicabilidade (SHAP/LIME, se necessário).
- Logs e auditoria de decisões automatizadas.
