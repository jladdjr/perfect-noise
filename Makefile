venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements-dev.txt
	.venv/bin/pip3 install -e .

test_with_pdb:
	.venv/bin/pytest --pdb --cov=perfect_noise --cov-fail-under=70

test:
	.venv/bin/pytest --cov=perfect_noise --cov-fail-under=50

lint:
	.venv/bin/black .
