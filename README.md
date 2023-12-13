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

## Working w/ static checkers

### Whats included
1. **pre-commit hooks** - built-in hooks (https://pre-commit.com/hooks.html)
   * trailing-whitespace
   * end-of-file-fixer
2. **isort** - import sorter (https://pycqa.github.io/isort/)
3. **mypy** - type checker (https://mypy-lang.org/)

### Setting up
1. Install dev-packages - `pip install -r dev_requirements.txt`
2. Install pre-commit hook - `pre-commit install`

### Running the pre-commit hooks
* **Automatic Runs -**<br />
If you installed the hooks (as described above), they will run automatically (on the staged files)
on every commit. Fixes will be made but will not be staged automatically (allowing to review them)
* **Manual Runs -**<br />
  1. Use `pre-commit run` to run the hooks on the staged files only
  2. Use `pre-commit run --all-files` to run the hooks on all the files
