python3.8 -m venv .python
source .python/bin/activate
pip install wheel neovim
pip install livemark PyGithub python-dotenv
cp -n .env.example .env
