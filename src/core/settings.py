from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Configurações da aplicação carregadas de variáveis de ambiente. """
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    DATABASE_URL_LOCAL: str


settings = Settings()
