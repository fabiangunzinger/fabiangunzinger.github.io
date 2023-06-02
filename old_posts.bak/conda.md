---
title: "Conda"
subtitle: "Notes on stuff I tend to forget"
tags: [python]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

## Installing Conda

- [Docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent)

- Download miniconda installer:
    - `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh` (Mac)
    - `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh ~/miniconda.sh` (ARN-based linux)

- Execute installer: `bash ~/miniconda.sh -b -p $HOME/miniconda`

## Sharing environment

- To share environments across platforms, only create an environment with
  explicityly required specs rather than a complete set of dependencies and
  versions. You can do this using `conda env export --from-history >
  requirements.yml`. In case this doesn't work, the issue might be that you're
  run `--update-deps` in the past, in which ase all dependencies are added as
  explicit specs (from [here](https://stackoverflow.com/a/58015738/13666841)).
  In this case, it might be best to recreate the environment.

- To create an `environment.txt` that can be used by pip, install pip into
  conda environment (`conda install pip`), then run `pip list --format=freeze
  environment.txt` ([source](https://stackoverflow.com/a/57845418/13666841)).
