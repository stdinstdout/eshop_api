from pydantic import BaseSettings    

import os

class Settings(BaseSettings):
	db_user: str = os.getenv("POSTGRES_USER", 'POSTGRES')
	db_pwd: str = os.getenv("POSTGRES_PASSWORD", 'POSTGRES')
	db_host: str = os.getenv("POSTGRES_HOST", 'POSTGRES')
	db_name: str = os.getenv("POSTGRES_DB", 'POSTGRES')


