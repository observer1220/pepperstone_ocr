import os
import glob
import pytesseract

# 確保 output_text 資料夾存在
os.makedirs("output_text", exist_ok=True)

# 取得 frame 資料夾內所有符合 frame_xxxx.jpg 格式的圖片
image_files = sorted(glob.glob("denoise/*.jpg"))

# 迭代處理每張圖片
for img_path in image_files:
    text = pytesseract.image_to_string(
        img_path, lang='chi_tra')  # 支援繁體中文和英文
    print(text)

    # 將 OCR 文字存入文字檔案
    with open("output_text/output_text.txt", "a", encoding="utf-8") as file:
        file.write(text.encode("utf-8").decode("utf-8") + "\n")
