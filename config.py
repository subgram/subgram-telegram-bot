from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    TELEGRAM_TOKEN: str  # get yours from @botfather
    SUBGRAM_TOKEN: str   # get your from
    SUBGRAM_PRODUCT_ID: int  # product id which you are selling


settings = Config()