venv:
	uv venv

test_with_pdb:
	uv run pytest --pdb --cov=perfect_pad --cov-fail-under=70

test:
	uv run pytest --cov=perfect_pad --cov-fail-under=100

coverage:
	uv run coverage html

lint:
	uv run ruff format
