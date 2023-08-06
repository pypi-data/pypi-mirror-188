![Build Status](https://drone.mcos.nc/api/badges/scrippy/scrippy-git/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, mon ami le scrangourou](./scrippy-git.png "Scrippy, mon ami le scrangourou")

# `scrippy_git`

Client _Git_ pour le cadriciel [`Scrippy`](https://codeberg.org/scrippy).

## Prérequis

### Modules Python

#### Liste des modules nécessaires

Les modules listés ci-dessous seront automatiquement installés.

- GitPython

## Installation

### Manuelle

```bash
git clone https://codeberg.org/scrippy/scrippy-git.git
cd scrippy-git.git
sudo python3 -m pip install -r requirements.txt
make install
```

### Avec `pip`

```bash
pip3 install scrippy-git
```

### Utilisation

Le module `scrippy_git.git` fournit l'objet `Repo` facilitant la manipulation d'un dépôt _Git_.

```python
import os
from scrippy_git import git

username = "git"
host = "gitlab.monty.py"
port = 2242
reponame = "luiggi.vercotti/monty_python.git"
branch = "master"

repo = git.Repo(username, host, port, reponame)
local_path = os.path.join(workspace_path, "monty_python")
repo.clone(branch=branch, path=local_path)

test_fname = os.path.join(local_path, "dead_parrot.txt")
with open(test_fname, mode="w") as test_file:
  test_file.write("Nobody expects the Spanish inquisition !")
  commit_message = "Inquisition shall not be expected"
  repo.commit_push(commit_message)
```
