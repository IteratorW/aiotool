import os


def get_env(key: str, default_value: any):
    return os.environ.get(f"aiotool_{key}") or default_value


TELEGRAM_TOKEN = get_env("telegram_token", None)
EXTENSION_DIRS = get_env("extension_dirs", "extensions").split(",")
DEBUG = get_env("debug", False) or False
