# SwitchBot CLI

## コマンド一覧

### デバイス管理

```bash
# デバイス一覧の取得
python3 src/main.py devices

# デバイス設定の更新
python3 src/main.py setup
```

### デバイスコントロール

#### humidifier

```bash
# 加湿器 A6
python3 src/main.py control humidifier on
python3 src/main.py control humidifier off

```

#### robot_vacuum_cleaner_s1

```bash
# ロボット掃除機S1
python3 src/main.py control robot_vacuum_cleaner_s1 on
python3 src/main.py control robot_vacuum_cleaner_s1 off

```

#### color_bulb

```bash
# ダイニングライト
python3 src/main.py control color_bulb on
python3 src/main.py control color_bulb off

```

#### hub_mini

```bash
# ハブミニ リビング
python3 src/main.py control hub_mini on
python3 src/main.py control hub_mini off

```

#### meter

```bash
# 温湿度計　リビング
python3 src/main.py control meter on
python3 src/main.py control meter off

```

### ステータス確認

```bash
# 加湿器 A6のステータス確認
python3 src/main.py status humidifier

# ロボット掃除機S1のステータス確認
python3 src/main.py status robot_vacuum_cleaner_s1

# ダイニングライトのステータス確認
python3 src/main.py status color_bulb

# ハブミニ リビングのステータス確認
python3 src/main.py status hub_mini

# 温湿度計　リビングのステータス確認
python3 src/main.py status meter

```
