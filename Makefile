install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api:
	uvicorn src.service.app:app --reload

repro:
	dvc repro

test:
	pytest -q
