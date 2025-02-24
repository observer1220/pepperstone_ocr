## 步驟 1：使用 FFmpeg 擷取影片畫面

安裝 FFmpeg：Windows：下載 FFmpeg 可執行檔，並將路徑加入環境變數。
執行以下命令擷取畫面(每秒擷取 2 張)：ffmpeg -i pepperstone.mp4 -vf "fps=1" frame/%04d.jpg

## 步驟 2：圖片的前置處理

指令：denoise.py

## 步驟 2：使用 Tesseract OCR 進行文字識別&合併

安裝 Tesseract OCR：Windows：下載安裝 Tesseract，並將 tesseract.exe 加入環境變數。
執行以下命令辨識圖片中的文字：python tesseract.py

## 步驟 3：合併文字識別結果

執行以下命令合併文字識別結果：python merge.py

## 步驟 4：整理交易數據到 EXCEL

安裝 Pandas：pip install pandas
執行以下命令將文字檔彙整成 EXCEL：python to_excel.py
