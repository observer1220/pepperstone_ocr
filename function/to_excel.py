import pandas as pd
import re

# 讀取 OCR 文字檔案
with open("output_text/output_text.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 初始化變數
data = []
current_trade = {}

# 解析 OCR 內容
for line in lines:
    line = line.strip()
    print(line)

    # 匹配訂單號碼
    order_match = re.search(r'\d{8,}', line)
    if order_match:
        current_trade["訂單號碼"] = int(order_match.group(0))
        continue

    # 匹配匯率兌
    pair_match = re.match(r"^[A-Z]{6}$", line)
    if pair_match:
        # print("匯率兌", pair_match)
        current_trade["匯率兌"] = str(pair_match.group(0))
        continue

    # 匹配日期(2024/4/10)
    date_match = re.match(r"^\d{4}/\d{1,2}/\d{1,2}", line)
    if date_match:
        current_trade["日期"] = date_match.group()
        continue

    # 匹配時間(8:58:20)
    time_match = re.search(r"\d{1,2}:\d{1,2}:\d{1,2}$", line)
    if time_match:
        current_trade["時間"] = time_match.group()
        continue

    # 匹配手數
    volume_match = re.search(r"\b0\.0\d+\b", line)
    if volume_match:
        print("手數", volume_match)
        current_trade["手數"] = float(volume_match.group(0))
        continue

    # 匹配獲利金額（負數或正數）
    profit_match = re.search(r"(-?\$\d+\.\d{2})", line)
    if profit_match:
        current_trade["獲利金額"] = profit_match.group(0)
        data.append(current_trade)
        current_trade = {}
        continue

# 轉換成 DataFrame
df = pd.DataFrame(data, columns=["訂單號碼", "匯率兌", "日期", "時間", "手數", "獲利金額"])

# 存成 Excel 檔案
df.to_excel("交易數據.xlsx", index=False)
