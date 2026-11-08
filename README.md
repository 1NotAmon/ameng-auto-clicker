# 阿孟萬能連點器 2.0

A bilingual, grayscale Windows auto-clicker built with Python, customtkinter, and pynput.

以 Python、customtkinter 與 pynput 製作的 Windows 連點工具。介面提供繁體中文／English，深淺主題採黑白灰配色；滑鼠與鍵盤輸入皆在本機執行。

目前版本：`2.0.0`

## Download / 下載

Windows 10 或更新版本、64 位元：可直接下載已通過封裝自測的單檔程式：[AmengClicker-2.0.0-Windows-x64.exe](https://github.com/1NotAmon/ameng-auto-clicker/raw/refs/heads/main/AmengClicker-2.0.0-Windows-x64.exe)。原始碼可由 GitHub 的 **Code → Download ZIP** 取得。

SHA-256：`C78D0A09F5A941E21F6CB9A9BD45A4E3241CEC7D0F1E8717D5610382926D6E00`

此 EXE 未經程式碼簽署，Windows SmartScreen 可能顯示未知發行者警告。請只從此官方 repository 下載，並依自己的安全政策決定是否執行。

## Features / 功能

- 滑鼠左鍵、右鍵、中鍵連點；支援鍵盤大多數一般按鍵與功能鍵。
- 可設定連點間隔、次數上限（`0` 為不限次數）、單擊／雙擊與雙擊間隔。
- 全域快捷鍵預設為 F6 開始／暫停、F7 立即停止，可自訂。
- 繁體中文／English；跟隨 Windows 外觀或手動選擇深色／淺色，全介面只用黑、白、灰階。
- 設定僅保存在本機 `%APPDATA%\AmengClicker2\settings.json`；程式不會上傳設定或輸入內容。

## Run from source / 執行原始碼

需要 Windows 與 Python 3.10 或更新版本。在 PowerShell 執行：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\AmengClicker.py
```

`AmengClicker.py`、`monochrome.json` 與 `67.ico` 必須放在同一資料夾。

## Build / 建置單檔 EXE

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

## Testing / 測試

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "SmokeTest.py" -v
python .\AmengClicker.py --smoke
```

`--smoke` 只建立隱藏 UI，不會啟動全域輸入監聽或送出點擊。GitHub Actions 會在 Windows runner 執行語法與 smoke tests。

## Safety / 安全

開始前請確認目標程式已取得焦點，並遵守該程式及服務的使用條款。極短間隔的實際速度會受 Windows 排程與目標程式影響。關閉程式會停止連點並解除鍵盤監聽。

## License / 授權

MIT License，詳見 `LICENSE`。
