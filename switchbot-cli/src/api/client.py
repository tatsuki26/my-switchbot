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
    
    def format_device_mapping(self, devices_response):
        """デバイス情報をマッピング形式に変換"""
        mapping = {}
        device_type_count = {}  # デバイスタイプの出現回数を追跡
        
        if devices_response.get('statusCode') == 100:
            for device in devices_response['body']['deviceList']:
                device_type = device['deviceType'].lower().replace(' ', '_')
                
                # デバイスタイプの出現回数をカウント
                if device_type in device_type_count:
                    device_type_count[device_type] += 1
                    key = f"{device_type}{device_type_count[device_type]}"
                else:
                    device_type_count[device_type] = 1
                    key = device_type
                
                mapping[key] = {
                    'id': device['deviceId'],
                    'name': device['deviceName'],
                    'type': device['deviceType']
                }
        return mapping

    def get_device_status(self, device_id: str):
        """特定のデバイスのステータスを取得"""
        response = requests.get(
            f"{self.BASE_URL}/devices/{device_id}/status",
            headers=self._get_headers()
        )
        return response.json()

    def send_device_command(self, device_id: str, command: str):
        """デバイスにコマンドを送信"""
        command_data = {
            "command": command,
            "parameter": "default",
            "commandType": "command"
        }
        response = requests.post(
            f"{self.BASE_URL}/devices/{device_id}/commands",
            headers=self._get_headers(),
            json=command_data
        )
        return response.json()