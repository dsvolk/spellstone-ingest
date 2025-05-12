# 💎 Spellstone-ingest
Spellstone is a collection of tools for ingesting, processing, and interacting with your personal knowledge base. It is a modular system that can be run in the cloud or locally. It uses Obsidian vault as a storage backend.

Spellstone-ingest is the ingestion part of the system, responsible for fetching data from various sources and storing it in the Obsidian vault. It can be both triggered manually and run on a schedule.

Feel free to modify the flows, add your own flows, and send me a pull request if you think it would be useful for others.

## Installation
This is a modular system, so depending on what you want to run, you need to install different parts of it.

### Cloud installation
For most clouds, it should be sufficient to just push the git repo and let them build everything for you. This, for example, works for [Railway](https://railway.app/), [Heroku](https://www.heroku.com/), and others. The repo already has the Dockerfile and Makefile provided.

So all you need is to set up the API keys as described above.

### Local installation
#### Install external libraries
- ffmpeg (Debian: `sudo apt install ffmpeg`)

#### Set up Poetry
```console
curl -sSL https://install.python-poetry.org | python3 -
poetry --version
poetry config virtualenvs.in-project true
```

#### Set up Python environment
(in the project folder)
```console
poetry install --with=bot,dev,test,dashboard,etl,tools --no-root
poetry run pre-commit install
```
OR
```console
make env
```

#### Debugging in VSCode
When debugging, select "Python: Module" configuration.

### AI module

#### Get OpenAI API key
Set up your own OpenAI account. Visit [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) in your OpenAI account to create a new API key.

#### Set up API keys for the bot
The bot requires some API keys to run. There are two ways of providing them:
- environment variables. Provide the env variables listed in `template.env`. This option is more convenient for a cloud installation.
- `.env` file in the project root. You should manually create it. I do not provide my own `.env` file because of security reasons, but I put `template.env` as a template for the keys required. This option is better suited for a local installation.

## Disclaimers

1. **As-Is Provision**: This software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the author or contributors be held liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

2. **Usage Rights**: The software is free for both private and commercial use.

3. **Liability Disclaimer**: The author does not take any responsibility for any damage that may result from using this software. Users are solely responsible for determining the appropriateness of using the software and assume any risks associated with its use.

4. **Modification and Licensing**: You are allowed to modify the software under the terms of the MIT License. Contributions are welcome, and pull requests are highly encouraged.

5. **Errors and Glitches**: The software is likely to contain some glitches and errors. Users are encouraged to report any issues and are very welcome to submit pull requests to fix them.

6. **Enjoyment Clause**: We hope you enjoy using the software and find it useful!
