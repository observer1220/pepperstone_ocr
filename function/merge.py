# import glob
# import chardet

# # 合併所有 OCR 文字檔案
# output_txt_path = "output_text/output_text.txt"
# with open(output_txt_path, "w", encoding="utf-8") as outfile:
#     for txt_path in sorted(glob.glob("output_text/*.txt")):
#         with open(txt_path, "rb") as infile:
#             raw_data = infile.read()  # 讀取原始二進位內容
#             detected = chardet.detect(raw_data)  # 偵測編碼
#             # 預設使用 UTF-8
#             encoding = detected["encoding"] if detected["encoding"] else "utf-8"

#         with open(txt_path, "r", encoding=encoding, errors="ignore") as infile:
#             outfile.write(infile.read() + "\n")

# print(f"所有 OCR 文字已存入 {output_txt_path}")
