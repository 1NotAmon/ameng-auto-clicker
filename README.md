# 阿孟萬能連點器 2.0

A bilingual, grayscale Windows auto-clicker built with Python, customtkinter, and pynput.

一個以 Python、customtkinter 與 pynput 製作的 Windows 連點工具。介面提供繁體中文／English，深淺主題採黑白灰配色；滑鼠與鍵盤輸入都在本機執行。

目前版本：`2.0.0`（原始碼公開版）

## 功能

- 滑鼠左鍵、右鍵、中鍵連點，或選擇鍵盤的大多數一般按鍵與功能鍵。
- 設定點擊間隔（秒）、次數上限；次數設為 `0` 表示不限次數。
- 單擊／雙擊及雙擊間隔設定。
- 全域快捷鍵預設為 F6 開始／暫停、F7 立即停止，可自行重新設定。
- 跟隨 Windows 外觀，或手動選擇深色／淺色；介面只用黑、白、灰階。
- 繁體中文與 English 介面。
- 使用真正的 `67.ico` 圖示；設定會存在本機使用者資料夾。

## 系統需求

- Windows 10 或更新版本。
- 一般使用者可使用本機建置的單檔 EXE；原始碼執行需要 Python 3.10 或更新版本。
- 不支援 macOS、Linux 或瀏覽器執行。

## 使用方式

### 執行原始碼

在專案資料夾開啟 PowerShell：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\AmengClicker.py
```

`AmengClicker.py`、`monochrome.json` 與 `67.ico` 必須放在同一個資料夾。第一次設定 PowerShell 虛擬環境時，若執行原則阻擋啟用指令，可直接使用 `.venv\Scripts\python.exe` 執行，不必修改系統執行原則。

### 建置單檔 EXE

```powershell
pyinstaller --noconfirm --clean --onefile --windowed `
  --name "阿孟萬能連點器2.0" `
  --icon "67.ico" `
  --add-data "67.ico;." `
  --add-data "monochrome.json;." `
  --collect-all customtkinter `
  --hidden-import pynput.keyboard._win32 `
  --hidden-import pynput.mouse._win32 `
  .\AmengClicker.py
```

PyInstaller 產生的 EXE 位於 `dist/`。Repository 刻意不追蹤建置好的 EXE；請在 Releases 發布經測試的二進位檔。

## 設定與安全

設定檔儲存在 `%APPDATA%\AmengClicker2\settings.json`。程式會用 `pynput` 監聽全域快捷鍵並模擬滑鼠／鍵盤輸入；連點在背景執行緒進行，介面更新會排回 Tk 主執行緒。程式不會上傳設定或輸入內容。

開始前請確認目前焦點位於正確的目標程式。極短間隔的實際速度會受 Windows 排程與目標程式影響。請勿用於違反服務條款、規避反作弊或造成他人困擾的用途。關閉程式會停止連點並解除鍵盤監聽。

## 專案結構

```text
.
├── .github/workflows/windows-smoke.yml
├── tests/SmokeTest.py
├── 67.ico
├── AmengClicker.py
├── monochrome.json
├── requirements.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── ROADMAP.md
├── VERSION
└── 使用說明.txt
```

## 開發與測試

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "SmokeTest.py" -v
python .\AmengClicker.py --smoke
```

`--smoke` 只建立隱藏的 UI 與設定視窗，不會啟動全域輸入監聽或送出點擊。GitHub Actions 會在 Windows runner 執行語法與 smoke tests。

## 授權

本專案採用 MIT License，詳見 `LICENSE`。
