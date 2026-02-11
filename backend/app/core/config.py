from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    ENV:str = 'dev'
    OPENAI_API_KEY:str |None = None
    PINECONE_API_KEY:str |None =None
    PINECONE_ENV: str | None = None
    PINECONE_INDEX: str | None = None

    model_config = SettingsConfigDict(
        env_file = '.env'
    )

settings = Settings()
# ---------------------------------------------------------------------------
# 📘 CONFIG MODULE DOCUMENTATION
# ---------------------------------------------------------------------------
#
# Purpose:
# --------
# This file defines the single source of truth for all runtime configuration
# in the backend service.
#
# Instead of calling os.getenv() in random places, every part of the app
# should import:
#
#     from app.core.config import settings
#
# and read values from that object.
#
#
# Why BaseSettings?
# -----------------
# BaseSettings is a special Pydantic class that:
# - Loads values from OS environment variables
# - Loads values from the `.env` file
# - Validates types at startup
#
# This allows the app to fail fast if required config is missing or invalid.
#
#
# Field Meanings:
# ---------------
# ENV
#   - Controls runtime mode (dev / staging / prod)
#   - Defaults to "dev" for local development
#
# OPENAI_API_KEY
#   - API key for OpenAI models
#   - Optional for now during scaffolding
#   - Should be required in production
#
# PINECONE_API_KEY / ENV / INDEX
#   - Credentials and configuration for Pinecone
#
#
# model_config:
# -------------
# env_file=".env"
#   - Tells Pydantic to load variables from backend/.env automatically
#
# extra="ignore"
#   - If the .env file contains extra variables that are not defined above,
#     the app will not crash.
#
#
# settings = Settings():
# ---------------------
# This instantiates the Settings object at import time.
# It loads all environment variables and keeps them in memory.
#
# This behaves like a singleton config object shared across the app.
#
#
# Production Notes:
# -----------------
# In production, sensitive fields should NOT have defaults:
#
#     OPENAI_API_KEY: str
#
# That way the service crashes on startup if secrets are missing,
# instead of failing later at runtime.
#
# ---------------------------------------------------------------------------