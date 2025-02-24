import cv2
import pytesseract
import os
import glob

image_files = sorted(glob.glob("frame/*.jpg"))
for img_path in image_files:
    img = cv2.imread(img_path)  # 讀取圖片
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 將圖片轉換為灰度圖（提高 OCR 準確性）
    cv2.imwrite("denoise/" + os.path.basename(img_path), gray)  # 儲存處理後的圖片
