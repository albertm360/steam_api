import logging
import httpx
from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict, SettingsError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    steam_api_key: str
    steam_user_id: str


class OwnedGame(BaseModel):
    appid: int
    name: str


class OwnedGamesResponse(BaseModel):
    game_count: int
    games: list[OwnedGame]


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("steam_api")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("owned_games.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def main() -> int:
    STEAM_OWNED_GAMES_URL: str = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    
    try:
        settings = Settings()
    except (ValidationError, SettingsError) as e:
        print("Missing or invalid configuration. Ensure .env has STEAM_API_KEY and STEAM_USER_ID.")
        raise SystemExit(1) from e
    
    logger = setup_logger()

    try:
        with httpx.Client() as client:
            response = client.get(STEAM_OWNED_GAMES_URL,
                params={
                    "key": settings.steam_api_key,
                    "steamid": settings.steam_user_id,
                    "format": "json",
                    "include_appinfo": 1,
                    "include_played_free_games": 1,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()["response"]
    except httpx.HTTPStatusError as e:
        logger.error("Steam API returned %d: %s", e.response.status_code, e.response.text)
        raise SystemExit(1) from e
    except (httpx.RequestError, KeyError) as e:
        logger.error("Failed to fetch owned games: %s", e)
        raise SystemExit(1) from e

    owned_games = OwnedGamesResponse.model_validate(data)

    logger.info("Total games owned: %d", owned_games.game_count)
    for game in owned_games.games:
        logger.info("[%d] %s", game.appid, game.name)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())