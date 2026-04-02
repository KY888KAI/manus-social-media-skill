# skill.py
# 實現文章社群文案與圖像自動生成流程的核心邏輯

import gspread
from google.oauth2.service_account import Credentials
from PIL import Image, ImageDraw
import requests
import datetime
import os

# --- 1. 設定與初始化 (Constants and Initialization ) ---

# Google Sheets API 的認證設定
# 注意：在實際部署中，應使用更安全的方式管理金鑰，例如環境變數或金鑰管理服務
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
# 假設金鑰檔案名稱為 'credentials.json'
CREDS_FILE = 'credentials.json' 
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE )
client = gspread.authorize(creds)

# Google Sheets 文件和頁籤名稱
N8N_HISTORY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1TAbdOednlWhPgnIdJegHuoJq5kcRll7CwZ7kOTftuDw"
ARTICLE_REQ_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Mzg3a2cJRFpVCxSjkTWkAN1wUNZh2BUX9Wp_YXlemU4"
AUTOMATION_OUTPUT_SHEET_URL = "https://docs.google.com/spreadsheets/d/1W0HYVnwm9EC-KUdWC9S06llzDzf7_ZehxZkqdcwEcZU"

# Gemini 和其他服務的設定
GEMINI_COPY_GEM_URL = "https://gemini.google.com/gem/7cd3474d6eca"
GEMINI_PROMPT_GEM_URL = "https://gemini.google.com/gem/5373c62f9545"
INTERNAL_IMAGE_HOST_URL = "http://192.168.106.88:50002/upload" # 假設上傳的端點是 /upload

# Logo 檔案路徑
LOGO_WHITE_PATH = "logo_white.png"
LOGO_DARK_PATH = "logo_dark.png"

# --- 2. 輔助函式 (Helper Functions ) ---

def get_latest_tasks():
    """從大眾文章需求表獲取今天需要處理的任務"""
    print("正在讀取大眾文章需求表...")
    sheet = client.open_by_url(ARTICLE_REQ_SHEET_URL)
    
    # 根據今天日期判斷頁籤名稱
    today = datetime.date.today()
    worksheet_name = today.strftime("20%y.%m") # 格式化為 "2026.04"
    
    try:
        worksheet = sheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        print(f"錯誤：找不到頁籤 '{worksheet_name}'。")
        return []

    all_records = worksheet.get_all_records()
    
    # 篩選需要生成的內容
    tasks_to_process = []
    for record in all_records:
        product = record.get("文章使用產品", "")
        if product in ["籌碼K線", "起漲K線+籌碼K線"]:
            tasks_to_process.append(record)
            
    print(f"找到 {len(tasks_to_process)} 個待處理任務。")
    return tasks_to_process

def get_doc_content(doc_url):
    """
    從 Google Doc 連結中提取文字內容。
    注意：這是一個簡化實現，實際需要使用 Google Drive API 或網頁抓取。
    """
    print(f"正在從 {doc_url} 讀取文章內容...")
    # 這裡需要一個完整的 Google Drive API 整合來讀取文件內容
    # 以下為示意程式碼
    # drive_service = build('drive', 'v3', credentials=creds)
    # file_id = doc_url.split('/d/')[1].split('/')[0]
    # request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
    # content = request.execute()
    # return content.decode('utf-8')
    return "這是一段從 Google Doc 模擬抓取來的文章內容，用於測試流程。" # 模擬返回內容

def generate_social_copy(article_content):
    """使用 Gemini API 生成社群文案"""
    print("正在生成社群文案...")
    # 這裡需要與 Gemini API 或透過瀏覽器自動化互動
    # 模擬返回三組文案
    return [
        "社群文案一：AI 概念股全面解析！",
        "社群文案二：跟上趨勢，抓住下一個投資機會。",
        "社群文案三：獨家分析，立即閱讀文章。"
    ]

def generate_image_prompts(article_content):
    """使用 Gemini API 生成繪圖指令"""
    print("正在生成繪圖指令...")
    # 這裡需要與 Gemini API 或透過瀏覽器自動化互動
    # 模擬返回三組繪圖指令
    return [
        "一個充滿科技感的電路板背景，中間有一個發光的 'AI' 標誌，風格：賽博龐克",
        "數據圖表和上升箭頭的抽象組合，色調為藍色和金色，象徵成長與洞察",
        "一個機器人正在仔細研究股票市場的K線圖，畫面明亮且充滿希望"
    ]

def generate_and_download_image(prompt):
    """使用 Gemini 圖像生成工具生成並下載圖片"""
    print(f"正在根據指令生成圖片：'{prompt[:30]}...'")
    # 這裡需要與 Gemini 圖像生成 API 或瀏覽器自動化互動
    # 模擬生成一張圖片並儲存
    img = Image.new('RGB', (1024, 1024), color = 'darkblue') # 模擬深色背景圖
    d = ImageDraw.Draw(img)
    d.text((10,10), prompt, fill=(255,255,0))
    image_path = f"generated_image_{hash(prompt)}.png"
    img.save(image_path)
    return image_path

def add_logo_to_image(image_path):
    """判斷圖片背景深淺並疊加 Logo"""
    print(f"正在為圖片 {image_path} 疊加 Logo...")
    with Image.open(image_path).convert("RGBA") as base_image:
        # 簡化判斷：取圖片中心點顏色來判斷深淺
        width, height = base_image.size
        center_pixel = base_image.getpixel((width // 2, height // 2))
        # 計算亮度 (Luminance)
        luminance = 0.299 * center_pixel[0] + 0.587 * center_pixel[1] + 0.114 * center_pixel[2]

        if luminance < 128: # 判定為深色背景
            logo_path = LOGO_WHITE_PATH
            print("檢測到深色背景，使用白色 Logo。")
        else: # 判定為淺色背景
            logo_path = LOGO_DARK_PATH
            print("檢測到淺色背景，使用深色 Logo。")
        
        if not os.path.exists(logo_path):
            print(f"警告：找不到 Logo 檔案 {logo_path}，跳過疊圖。")
            return image_path

        with Image.open(logo_path).convert("RGBA") as logo:
            # 調整 logo 大小並貼到右下角
            logo.thumbnail((width // 5, height // 5))
            logo_w, logo_h = logo.size
            position = (width - logo_w - 20, height - logo_h - 20)
            base_image.paste(logo, position, logo)
            
            output_path = f"processed_{os.path.basename(image_path)}"
            base_image.save(output_path)
            return output_path

def upload_image_and_get_link(image_path):
    """上傳圖片至內部圖床並取得連結"""
    print(f"正在上傳圖片 {image_path} 至內部圖床...")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/png')}
            response = requests.post(INTERNAL_IMAGE_HOST_URL, files=files)
            response.raise_for_status() # 如果請求失敗則拋出異常
            # 假設返回的 JSON 格式為 {"url": "http://..."}
            image_url = response.json( ).get("url")
            print(f"上傳成功，圖片連結：{image_url}")
            return image_url
    except requests.exceptions.RequestException as e:
        print(f"錯誤：上傳圖片失敗 - {e}")
        return None

def update_automation_sheet(theme, social_copies, image_links):
    """將生成的內容回填至自動化工作表"""
    print(f"正在將主題 '{theme}' 的結果回填至目標工作表...")
    sheet = client.open_by_url(AUTOMATION_OUTPUT_SHEET_URL)
    worksheet = sheet.get_worksheet(0) # 假設在第一個頁籤
    
    # 找到最新的空白 A 欄位
    col_a_values = worksheet.col_values(1)
    next_row = len(col_a_values) + 1
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # 準備要寫入的數據 (三列)
    rows_to_append = []
    for i in range(3):
        rows_to_append.append([
            theme if i == 0 else "", # 主題只在第一列填寫
            "", # B欄
            today_str, # C欄 排程時間
            "", # D欄
            "", # E欄
            social_copies[i], # F欄 社群文案
            image_links[i],   # G欄 圖片連結
            "", # H欄
            image_links[i],   # I欄 圖片連結
            "", # J欄 ...
            "", # K欄
            "", # L欄
            "", # M欄
            "", # N欄
            "", # O欄
            "", # P欄
            "", # Q欄
            "", # R欄
            social_copies[i]  # S欄 社群文案
        ])
        
    # 一次性寫入多行以提高效率
    worksheet.append_rows(rows_to_append, table_range=f"A{next_row}")
    print("回填完成。")

# --- 3. 主執行流程 (Main Execution Flow) ---

def run_skill():
    """技能的主要執行入口點"""
    print("--- Manus 生圖流程自動化技能啟動 ---")
    
    # 步驟 1 & 2: 獲取待處理任務
    tasks = get_latest_tasks()
    if not tasks:
        print("今天沒有需要處理的任務。流程結束。")
        return

    for task in tasks:
        theme = task.get("需求主題")
        doc_url = task.get("交稿處")
        
        if not theme or not doc_url:
            print(f"警告：任務 '{task}' 缺少主題或文件連結，已跳過。")
            continue
            
        print(f"\n--- 正在處理主題：{theme} ---")
        
        # 步驟 4: 讀取文章內容
        article_content = get_doc_content(doc_url)
        
        # 步驟 5: 生成社群文案
        social_copies = generate_social_copy(article_content)
        
        # 步驟 6: 生成繪圖指令
        image_prompts = generate_image_prompts(article_content)
        
        image_links = []
        for prompt in image_prompts:
            # 步驟 7: 生成圖片
            generated_image_path = generate_and_download_image(prompt)
            
            # 步驟 8: 疊加 Logo
            processed_image_path = add_logo_to_image(generated_image_path)
            
            # 步驟 9: 上傳圖片
            image_url = upload_image_and_get_link(processed_image_path)
            if image_url:
                image_links.append(image_url)
            else:
                image_links.append("上傳失敗") # 記錄錯誤
        
        # 步驟 10: 回填結果
        if len(social_copies) == 3 and len(image_links) == 3:
            update_automation_sheet(theme, social_copies, image_links)
        else:
            print(f"錯誤：為主題 '{theme}' 生成的內容數量不符，跳過回填。")

    print("\n--- 所有任務處理完畢 ---")


if __name__ == "__main__":
    # 當直接執行此腳本時，調用 run_skill 函式
    run_skill()
