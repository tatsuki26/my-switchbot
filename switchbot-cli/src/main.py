import json
import os
import click
from api.client import SwitchBotClient
from config.devices import DEVICE_MAPPING

@click.group()
def cli():
    pass

@cli.command()
def setup():
    """デバイス設定ファイルとREADMEを生成するコマンド"""
    client = SwitchBotClient()
    result = client.get_devices()
    mapping = client.format_device_mapping(result)
    devices = result['body']['deviceList']
    
    # configディレクトリがない場合は作成
    os.makedirs('src/config', exist_ok=True)
    
    # デバイス設定ファイルの生成
    with open('src/config/devices.py', 'w', encoding='utf-8') as f:
        f.write('DEVICE_MAPPING = {\n')
        for key, value in mapping.items():
            f.write(f"    '{key}': {{\n")
            f.write(f"        'id': '{value['id']}',\n")
            f.write(f"        'name': '{value['name']}',\n")
            f.write(f"        'type': '{value['type']}'\n")
            f.write('    },\n')
        f.write('}\n')
    
    # README.mdの生成
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('# SwitchBot CLI\n\n')
        f.write('## コマンド一覧\n\n')
        
        # デバイス管理コマンド
        f.write('### デバイス管理\n\n')
        f.write('```bash\n')
        f.write('# デバイス一覧の取得\n')
        f.write('python3 src/main.py devices\n\n')
        f.write('# デバイス設定の更新\n')
        f.write('python3 src/main.py setup\n')
        f.write('```\n\n')
        
        # デバイスコントロール
        f.write('### デバイスコントロール\n\n')
        device_types = {}
        for device in devices:
            device_type = device['deviceType'].lower().replace(' ', '_')
            if device_type not in device_types:
                device_types[device_type] = []
            device_types[device_type].append(device['deviceName'])
        
        for device_type, names in device_types.items():
            f.write(f'#### {device_type}\n\n')
            f.write('```bash\n')
            for i, name in enumerate(names, 1):
                command_key = f"{device_type}{i if i > 1 else ''}"
                f.write(f'# {name}\n')
                f.write(f'python3 src/main.py control {command_key} on\n')
                f.write(f'python3 src/main.py control {command_key} off\n\n')
            f.write('```\n\n')
        
        # ステータス確認
        f.write('### ステータス確認\n\n')
        f.write('```bash\n')
        for device_type, names in device_types.items():
            for i, name in enumerate(names, 1):
                command_key = f"{device_type}{i if i > 1 else ''}"
                f.write(f'# {name}のステータス確認\n')
                f.write(f'python3 src/main.py status {command_key}\n\n')
        f.write('```\n')
    
    click.echo("デバイス設定ファイルとREADMEが生成されました")

@cli.command()
def devices():
    """デバイス一覧を取得するコマンド"""
    client = SwitchBotClient()
    result = client.get_devices()
    click.echo(result)

@cli.command()
@click.argument('device_id')
def status(device_id):
    """デバイスのステータスを取得するコマンド"""
    client = SwitchBotClient()
    result = client.get_device_status(device_id)
    click.echo(result)

from config.devices import DEVICE_MAPPING

@cli.command()
@click.argument('device_name')
@click.argument('action', type=click.Choice(['on', 'off']))
def control(device_name, action):
    """デバイスの電源をオン/オフするコマンド"""
    if device_name not in DEVICE_MAPPING:
        click.echo(f"Error: Device '{device_name}' not found")
        return
    
    device_id = DEVICE_MAPPING[device_name]['id']
    command = "turnOn" if action == "on" else "turnOff"
    client = SwitchBotClient()
    result = client.send_device_command(device_id, command)
    click.echo(result)

if __name__ == "__main__":
    cli()