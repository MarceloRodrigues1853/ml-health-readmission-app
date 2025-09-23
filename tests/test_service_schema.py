from pydantic import ValidationError
from src.service.app import PatientFeatures

def test_patient_schema_ok():
    PatientFeatures(
        age=45, sex=1, length_of_stay=3.5, comorbidities=2,
        prior_readmissions=1, medication_count=5, lab_score=0.2,
        discharge_type=0
    )

def test_patient_schema_invalid():
    try:
        PatientFeatures(
            age=-1, sex=2, length_of_stay=-1, comorbidities=-3,
            prior_readmissions=-1, medication_count=-1, lab_score=0.2,
            discharge_type=3
        )
        assert False, 'deveria falhar'
    except ValidationError:
        assert True
