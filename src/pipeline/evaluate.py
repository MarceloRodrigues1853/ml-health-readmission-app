"""Etapa de avaliação (pós-treino).
Aqui poderíamos calcular matriz de confusão, calibração e etc.
"""
import json
from pathlib import Path
import pandas as pd
import yaml
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, brier_score_loss
)


def main() -> None:
    with open('params.yaml', 'r', encoding='utf-8') as f:
        params = yaml.safe_load(f)

    df = pd.read_csv('data/processed/dataset.csv')
    y = df['readmitted_30d']
    X = df.drop(columns=['readmitted_30d'])

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y,
        test_size=params['prepare']['test_size'],
        random_state=params['prepare']['random_state'],
        stratify=y
    )

    clf = load('models/model.pkl')
    proba = clf.predict_proba(X_te)[:, 1]
    pred = (proba >= params['evaluate']['threshold']).astype(int)

    acc = accuracy_score(y_te, pred)
    prec = precision_score(y_te, pred, zero_division=0)
    rec = recall_score(y_te, pred, zero_division=0)
    brier = brier_score_loss(y_te, proba)

    metrics_path = Path('models/metrics.json')
    if metrics_path.exists():
        with open(metrics_path, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
    else:
        metrics = {}

    metrics.update(
        {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'brier': float(brier),
        }
    )

    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)


if __name__ == '__main__':
    main()
