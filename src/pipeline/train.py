"""Treina um modelo simples para readmissão (exemplo).
Salva models/model.pkl e models/metrics.json.
"""
import json
from pathlib import Path
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


def main() -> None:
    with open('params.yaml', 'r', encoding='utf-8') as f:
        params = yaml.safe_load(f)

    df = pd.read_csv('data/processed/dataset.csv')
    y = df['readmitted_30d']
    X = df.drop(columns=['readmitted_30d'])

    cat = ['sex', 'discharge_type']
    num = [
        'age', 'length_of_stay', 'comorbidities',
        'prior_readmissions', 'medication_count', 'lab_score'
    ]

    pre = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=params['train']['n_estimators'],
        max_depth=params['train']['max_depth'],
        random_state=params['prepare']['random_state'],
        n_jobs=-1,
    )

    clf = Pipeline(steps=[('pre', pre), ('rf', model)])

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y,
        test_size=params['prepare']['test_size'],
        random_state=params['prepare']['random_state'],
        stratify=y
    )

    clf.fit(X_tr, y_tr)
    proba = clf.predict_proba(X_te)[:, 1]
    pred = (proba >= params['evaluate']['threshold']).astype(int)
    roc = roc_auc_score(y_te, proba)
    f1 = f1_score(y_te, pred)

    Path('models').mkdir(exist_ok=True)
    dump(clf, 'models/model.pkl')

    metrics = {'roc_auc': float(roc), 'f1': float(f1)}
    with open('models/metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)


if __name__ == '__main__':
    main()
