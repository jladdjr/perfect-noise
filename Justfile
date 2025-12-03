venv:
        #!/usr/bin/env bash
        set -x
        venv_parent_folder="$HOME/venvs"
        mkdir -p $venv_parent_folder
        rm -r ${venv_parent_folder}/perfect-noise
        python3 -m venv ${venv_parent_folder}/perfect-noise
        ${venv_parent_folder}/perfect-noise/bin/pip3 install -r requirements-dev.txt
        ${venv_parent_folder}/perfect-noise/bin/pip3 install -e .

test_with_pdb:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/perfect-noise/bin/pytest --pdb --cov=perfect-noise --cov-fail-under=70

test:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/perfect-noise/bin/pytest --cov=perfect-noise --cov-fail-under=50

lint:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/perfect-noise/bin/black .