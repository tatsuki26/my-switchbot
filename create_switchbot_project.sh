#!/bin/bash

# プロジェクトディレクトリの作成
mkdir -p switchbot-cli/src/api

# requirements.txtの作成
cat > switchbot-cli/requirements.txt << 'EOL'
requests==2.31.0
python-dotenv==1.0.0
click==8.1.7
EOL

# Makefileの作成
cat > switchbot-cli/Makefile << 'EOL'
.PHONY: install
install:
	python -m pip install -r requirements.txt

.PHONY: run
run:
	python src/main.py
EOL

# .envの作成
cat > switchbot-cli/.env << 'EOL'
SWITCHBOT_TOKEN=your_token_here
SWITCHBOT_SECRET=your_secret_here
EOL

# setup.pyの作成
cat > switchbot-cli/setup.py << 'EOL'
from setuptools import setup, find_packages

setup(
    name="switchbot-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "switchbot=src.main:cli",
        ],
    },
)
EOL

# __init__.pyファイルの作成
touch switchbot-cli/src/__init__.py
touch switchbot-cli/src/api/__init__.py

# main.pyの作成
cat > switchbot-cli/src/main.py << 'EOL'
import click
from api.client import SwitchBotClient

@click.group()
def cli():
    pass

@cli.command()
def devices():
    """デバイス一覧を取得するコマンド"""
    client = SwitchBotClient()
    result = client.get_devices()
    click.echo(result)

if __name__ == "__main__":
    cli()
EOL

# client.pyの作成
cat > switchbot-cli/src/api/client.py << 'EOL'
import requests
import time
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

class SwitchBotClient:
    BASE_URL = "https://api.switch-bot.com/v1.1"
    
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("SWITCHBOT_TOKEN")
        self.secret = os.getenv("SWITCHBOT_SECRET")
        
    def _generate_sign(self):
        nonce = ''
        t = int(round(time.time() * 1000))
        string_to_sign = bytes(f'{self.token}{t}{nonce}', 'utf-8')
        secret = bytes(self.secret, 'utf-8')
        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        return sign.decode('utf-8'), t

    def _get_headers(self):
        sign, t = self._generate_sign()
        return {
            "Authorization": self.token,
            "sign": sign,
            "t": str(t),
            "nonce": ""
        }

    def get_devices(self):
        """デバイス一覧を取得"""
        response = requests.get(
            f"{self.BASE_URL}/devices",
            headers=self._get_headers()
        )
        return response.json()
EOL

echo "プロジェクト構造が作成されました！"