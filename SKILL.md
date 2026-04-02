---
name: manus_social_media_and_image_generation
description: 自動化處理大眾文章需求，生成社群文案與配圖，並回填至 Google Sheets。
author: Manus
version: 1.1
---

# Manus 生圖流程自動化技能

本技能會執行一個完整的內容自動化流程：從 Google Sheets 讀取文章需求，使用 Gemini 產生文案和圖片，處理圖片後上傳，最後將所有結果回填至指定的工作表中。

## 執行邏輯

以下的程式碼區塊定義了此技能的入口點。它會匯入 `skill.py` 檔案中定義的主函式 `run_skill` 並執行它。

```python
# 匯入外部的 skill.py 檔案中的主函式
from skill import run_skill

def main():
    """
    技能執行的主入口函式。
    """
    try:
        print("--- Manus 生圖流程自動化技能啟動 ---")
        # 呼叫定義在 skill.py 中的核心邏輯
        run_skill()
        print("--- 技能執行成功 ---")
        return "所有任務已成功處理完畢。"
    except Exception as e:
        # 捕捉並回報任何在執行過程中發生的錯誤
        error_message = f"技能執行失敗：{e}"
        print(error_message)
        # 在實際應用中，可能還需要將錯誤記錄到日誌系統
        return error_message

# 執行主函式
if __name__ == "__main__":
    main()
