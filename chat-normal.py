import json
import re


def replace_hyphen(text, replace_hyphen):
    """全ての横棒をーに置換する
    Args:
        text (str): 入力するテキスト
        replace_hyphen (str): 置換したい文字列
    Returns:
        (str): 置換後のテキスト
    """
    hyphens = "-˗ᅳ᭸‐‑‒–—―⁃⁻−▬─━➖ーㅡ﹘﹣－ｰ𐄐𐆑 "
    hyphens = "|".join(hyphens)
    return re.sub(hyphens, replace_hyphen, text)


# ラベル付けするためのキーワードパターン
erin = ["えーりん", "エーリン", "EIRIN", "eirin", "Eirin", "ERIN", "erin", "Erin"]
rine = ["りんえ", "リンエ", "RINE", "rine", "Rine"]
opi = ["おっぱい", "オッパイ", "OPPAI", "oppai", "Oppai", "おっπ"]
inaba = ["因幡", "いなば", "イナバ", "INABA", "inaba", "Inaba", "うどん"]
touho = ["東方", "とうほう", "TOUHOU", "Touhou", "touhou", "TOUHO", "touho", "Touho"]
reimu = ["霊夢", "れいむ", "REIMU", "reimu", "Reimu"]
marisa = ["魔理沙", "まりさ", "MARISA", "marisa", "Marisa"]

# 正規表現パターンのリスト
patterns = [
    {"pattern": re.compile("|".join(erin)), "label": "erin"},
    {"pattern": re.compile("|".join(rine)), "label": "rine"},
    {"pattern": re.compile("|".join(opi)), "label": "opi"},
    {"pattern": re.compile("|".join(inaba)), "label": "inaba"},
    {"pattern": re.compile("|".join(touho)), "label": "touho"},
    {"pattern": re.compile("|".join(reimu)), "label": "reimu"},
    {"pattern": re.compile("|".join(marisa)), "label": "marisa"},
]

# JSONファイルの読み込み
with open("chat.json", "r", encoding="utf-8") as f:
    # data = json.loads(f.read().encode("utf-8"))
    data = json.load(f)

print(f"Loaded {len(data)} messages")
# データの前処理とラベル付け
for i in range(len(data)):
    data[i]["message"] = replace_hyphen(data[i]["message"], "ー")
    for pattern in patterns:
        if pattern["pattern"].search(data[i]["message"]):
            data[i]["label"] = pattern["label"]
            break
    else:
        data[i]["label"] = "other"

# 結果を新しいJSONファイルに保存
encoded_data = json.dumps(data, ensure_ascii=False)
with open("encoded_chat.json", "w", encoding="utf-8") as f:
    f.write(encoded_data)
