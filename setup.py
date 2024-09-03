import setuptools
from distutils.core import setup

setup(
    name="telegram_storage",
    version="0.0.0",
    description="you can send files directly from your command line to telegram using this bot https://t.me/AbicoooooooBot",
    author="Abemelek",
    author_email="abemelekdd@gmail.com",
    packages=["telegram_storage"],
    entry_points = {
        "console_scripts":["telegram_storage=telegram_storage.entry:cli_entry_point"]
    },
    install_requires = [
        "requests",
        "python-dotenv",
        "tqdm",
        "requests-toolbelt"
    ]
    
)