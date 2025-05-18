class Settings():
    PROJECT_NAME: str = "{{ project_name }}"
    DEBUG: bool = True
    DATABASE_URL = "sqlite:///./test.db"

settings = Settings()
