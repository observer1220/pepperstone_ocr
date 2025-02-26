import cv2
import pytesseract
import os
import glob
import pandas as pd
import re
from pathlib import Path


def getFrames(video_path, output_dir, fps_interval=1):
    """將影片轉換為圖片，可指定每秒擷取頻率"""
    # 確保輸出資料夾存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 讀取影片
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("無法讀取影片")
        return

    # 取得影片fps和每秒擷取幀數
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / fps_interval)  # fps_interval=1 表示每秒1幀
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            saved_count += 1
            output_path = os.path.join(output_dir, f"{saved_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
        frame_count += 1

    cap.release()
    print(f"已儲存 {saved_count} 張圖片")


def preprocess_images(input_dir, output_dir):
    """將圖片轉換為灰度圖並儲存"""
    # 確保輸出資料夾存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 取得所有圖片檔案
    image_files = sorted(glob.glob(f"{input_dir}/*.jpg"))

    for img_path in image_files:
        try:
            # 讀取並處理圖片
            img = cv2.imread(img_path)
            if img is None:
                print(f"無法讀取圖片: {img_path}")
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            output_path = os.path.join(output_dir, os.path.basename(img_path))
            cv2.imwrite(output_path, gray)
        except Exception as e:
            print(f"處理圖片 {img_path} 時發生錯誤: {e}")


def extract_text(input_dir, output_file):
    """使用OCR提取文字並儲存"""
    # 確保輸出資料夾存在
    output_dir = os.path.dirname(output_file)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 如果檔案已存在，先清空
    if os.path.exists(output_file):
        os.remove(output_file)

    image_files = sorted(glob.glob(f"{input_dir}/*.jpg"))

    for img_path in image_files:
        try:
            # OCR提取文字（支援繁體中文）
            text = pytesseract.image_to_string(img_path, lang='chi_tra')
            if text.strip():  # 只儲存非空的文字
                with open(output_file, "a", encoding="utf-8") as file:
                    file.write(text + "\n")
        except Exception as e:
            print(f"OCR處理 {img_path} 時發生錯誤: {e}")


def parse_text_to_excel(input_file, output_excel):
    """解析文字並轉換為Excel"""
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_file):
        print(f"找不到文字檔案: {input_file}")
        return

    # 讀取OCR文字
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data = []
    current_trade = {}

    # 解析每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳過空行
            continue

        # 匹配訂單號碼 (8位以上數字)
        if order_match := re.search(r'\d{8,}', line):
            current_trade["訂單號碼"] = int(order_match.group(0))
            continue

        # 匹配匯率兌 (6個大寫字母)
        if pair_match := re.match(r"^[A-Z]{6}$", line):
            current_trade["匯率兌"] = pair_match.group(0)
            continue

        # 匹配日期 (YYYY/M/D or YYYY/MM/DD)
        if date_match := re.match(r"^\d{4}/\d{1,2}/\d{1,2}", line):
            current_trade["日期"] = date_match.group(0)
            continue

        # 匹配時間 (H:MM:SS or HH:MM:SS)
        if time_match := re.search(r"\d{1,2}:\d{1,2}:\d{1,2}$", line):
            current_trade["時間"] = time_match.group(0)
            continue

        # 匹配手數 (0.0X格式)
        if volume_match := re.search(r"\b0\.0\d+\b", line):
            current_trade["手數"] = float(volume_match.group(0))
            continue

        # 匹配獲利金額 (帶$符號的正負數)
        if profit_match := re.search(r"(-?\$\d+\.\d{2})", line):
            current_trade["獲利金額"] = profit_match.group(0)
            if current_trade:  # 確保有資料才添加
                data.append(current_trade.copy())
            current_trade = {}

    # 轉換為DataFrame並儲存
    if data:
        df = pd.DataFrame(
            data, columns=["訂單號碼", "匯率兌", "日期", "時間", "手數", "獲利金額"])
        df.to_excel(output_excel, index=False)
        print(f"已成功生成Excel檔案: {output_excel}")
    else:
        print("未解析到任何交易數據")


def main():
    """主函數執行整個流程"""
    try:
        print("開始處理影片...")
        getFrames('pepperstone.mp4', 'frame', fps_interval=1)

        print("開始處理圖片...")
        preprocess_images("frame", "denoise")

        print("開始提取文字...")
        extract_text("denoise", "output_text/output_text.txt")

        print("開始解析並生成Excel...")
        parse_text_to_excel("output_text/output_text.txt", "trasaction.xlsx")

        print("處理完成！")
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")


if __name__ == "__main__":
    main()
