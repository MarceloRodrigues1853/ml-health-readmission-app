"""Gera dados sintéticos e processados para o problema
de readmissão em 30 dias. Não usa dados reais (sem PHI).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import yaml


def main() -> None:
    with open('params.yaml', 'r', encoding='utf-8') as f:
        params = yaml.safe_load(f)

    seed = params['seed']
    n_rows = params['prepare']['n_rows']
    rng = np.random.default_rng(seed)

    # Dados sintéticos (mini exemplo)
    age = rng.integers(18, 90, size=n_rows)
    sex = rng.integers(0, 2, size=n_rows)  # 0=f, 1=m (exemplo simples)
    los = rng.normal(4, 2, size=n_rows).clip(0, None)  # length of stay
    comorb = rng.integers(0, 6, size=n_rows)  # nº comorbidades
    prior = rng.integers(0, 5, size=n_rows)  # readmissões passadas
    meds = rng.integers(0, 20, size=n_rows)
    labs = rng.normal(0.0, 1.0, size=n_rows)  # escore genérico
    discharge = rng.integers(0, 3, size=n_rows)  # 0=home,1=clinic,2=other

    # Probabilidade base (logit) – apenas p/ demo
    logit = (
        -3.0 + 0.02 * (age - 50) + 0.25 * comorb + 0.35 * prior
        + 0.15 * (los > 5).astype(int) + 0.05 * meds + 0.2 * (discharge == 1)
    )
    prob = 1 / (1 + np.exp(-logit))
    y = (rng.random(n_rows) < prob).astype(int)

    df = pd.DataFrame(
        {
            'age': age,
            'sex': sex,
            'length_of_stay': los.round(2),
            'comorbidities': comorb,
            'prior_readmissions': prior,
            'medication_count': meds,
            'lab_score': labs.round(3),
            'discharge_type': discharge,
            'readmitted_30d': y,
        }
    )

    # Em um caso real: split, imputação, encoding etc.
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    df.to_csv('data/processed/dataset.csv', index=False)


if __name__ == '__main__':
    main()
