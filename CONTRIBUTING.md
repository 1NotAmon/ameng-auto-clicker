# Contributing

歡迎回報錯誤、提出改善建議或提交 Pull Request。請先搜尋既有 Issues，避免重複開單。

## 回報問題

請附上 Windows 版本、Python 版本（若執行原始碼）、連點模式、設定的間隔，以及完整錯誤文字。請不要貼出 `%APPDATA%\AmengClicker2\settings.json` 中可能含個人偏好的資料。

## 修改流程

1. Fork repository 並建立獨立分支。
2. 使用 Python 3.10+ 建立虛擬環境，安裝 `requirements.txt`。
3. 修改後執行：

   ```powershell
   python -m unittest discover -s tests -p "SmokeTest.py" -v
   python .\AmengClicker.py --smoke
   ```

4. 描述變更內容、測試方式與任何 UI 行為差異，再提交 Pull Request。

請勿加入個人設定檔、建置快取、虛擬環境或未經確認的第三方圖片／圖示。輸入監聽與點擊功能的變更應清楚說明觸發條件、停止方式及測試範圍。
