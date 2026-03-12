# Steam API Scripts

Scripts to play with the Steam API.

## Set up environment

Install UV if not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

CD into cloned repository:

```bash
cd steam_api
```

Use UV Sync command (this will install the Python version specified in `.python-version`, creates the virtual environment, and installs all dependencies from `pyproject.toml`):
```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:
```
STEAM_API_KEY="your_api_key_here"
STEAM_USER_ID="your_steam_id_here"
```

- Get a Steam API key at https://steamcommunity.com/dev/apikey
- Find your Steam ID from your Steam profile URL or via https://steamid.io

## Usage

```bash
uv run main.py
```