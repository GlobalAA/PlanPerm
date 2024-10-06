from os import path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	BOT_TOKEN: SecretStr
	PERMISSION_MESSAGE: str

	model_config = SettingsConfigDict(env_file=path.join(path.dirname(path.abspath(__file__)), '.env'))

config = Config()