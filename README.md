# TikTokBackend

## What is this all about?
Israeli advocacy videos are often blocked on Tiktok (and other social medias), due to a violation of community
guidelines. This project aims to provide a backend service that will allow users to upload their videos to the
service, and get a full report of violations in the video which should be fixed before uploading to Tiktok.

At this stage, the service is built of 4 separate categories -
1. In-Video text analysis - Detecting text in the video, and checking for violations in the text
2. Audio analysis - Detecting audio in the video, and checking for violations in the audio
3. Video analysis - Detecting video-content, and checking for violations in the video
4. Static/Quality analysis - Evaluating the quality of the video to make sure it is good enough for social media

## Setting up python environment
1. Install pyenv-win in PowerShell.

```pwsh
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

2. Open CMD
3. Run `pyenv --version` to check if the installation was successful.
4. Run `pyenv install 3.10.11` to install our version
5. Run `pyenv global 3.10.11` to set a Python version as the global version
6. Run `python3 -m pip install pip --upgrade` to upgrade pip
7. Run `python3 -m pip install virtualenv` to install virtualenv
8. Run `python3 -m virtualenv .venv` to initiate venv
9. Run `./.venv/Scripts/activate.bat` to activate the venv


## Install requirements
1. Run `pip install -r requirement.txt`

## A quick look into the Architecture & Relationships

### Architecture
![image](https://github.com/tovatovatova/TikTokBackend/assets/6629650/6ceb8f72-3176-431c-975b-031f785ebd83)

### Relationships
![image](https://github.com/tovatovatova/TikTokBackend/assets/6629650/3e4a06ff-1b46-40fe-b682-82bbb31a3714)

## Working w/ static checkers

### Whats included
1. **pre-commit hooks** - built-in hooks (https://pre-commit.com/hooks.html)
   * trailing-whitespace
   * end-of-file-fixer
2. **isort** - import sorter (https://pycqa.github.io/isort/)
3. **mypy** - type checker (https://mypy-lang.org/)

### Setting up
1. Install dev-packages - `pip install -r dev-requirements.txt`
2. Install pre-commit hook - `pre-commit install`

### Running the pre-commit hooks
* **Automatic Runs -**<br />
If you installed the hooks (as described above), they will run automatically (on the staged files)
on every commit. Fixes will be made but will not be staged automatically (allowing to review them)
* **Manual Runs -**<br />
  1. Use `pre-commit run` to run the hooks on the staged files only
  2. Use `pre-commit run --all-files` to run the hooks on all the files
