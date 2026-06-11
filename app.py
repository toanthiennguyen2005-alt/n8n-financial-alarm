import json
import requests
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Local LLM Financial Analyzer cho n8n")

# Cấu hình địa chỉ của Local Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5"

class TitleData(BaseModel):
    ticker: str
    article_title: str

@app.post("/analyze_title")
async def analyze_title(data: TitleData):
    # Hệ thống Prompt (System Prompt) ép LLM trả về đúng JSON Schema bạn cần
    prompt = f"""
Bạn là một hệ thống phân tích tin tức tài chính nâng cao cho thị trường chứng khoán Việt Nam.
Hãy bóc tách tiêu đề bài báo về mã cổ phiếu {data.ticker} thành đối tượng JSON duy nhất.

BẮT BUỘC có 6 trường sau:
{{
    "market_sentiment": "Tích cực" | "Tiêu cực" | "Trung lập"
    "event_category": "Báo cáo tài chính" | "M&A" | "Cổ tức" | "Biến động Lãnh đạo" | "Chính sách Vĩ mô" | "Mở rộng Kinh doanh" | "Khác"
    "financial_metrics": Các con số (VD: "5.000 tỷ", "tăng 40%"). Nếu không có, để rỗng "".
    "growth_catalysts": 1 câu về động lực. Nếu không có, để "".
    "risk_warnings": 1 câu về rủi ro. Nếu không có, để "".
    "ai_action_signal": Số nguyên từ -5 đến 5.
}}

Ví dụ mẫu để bạn học theo:
Tiêu đề: "Khối lượng giao dịch đột biến, khối ngoại gom mạnh 1.000 tỷ đồng cổ phiếu HPG"
JSON trả về:
{{
    "market_sentiment": "Tích cực",
    "event_category": "Khác",
    "financial_metrics": "1.000 tỷ đồng",
    "growth_catalysts": "Dòng tiền lớn từ khối ngoại mua gom tạo lực đỡ cho giá cổ phiếu",
    "risk_warnings": "",
    "ai_action_signal": 3
}}

Tiêu đề bài báo thực tế cần phân tích: "{data.article_title}"
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json", # Ép Ollama trả về chuẩn JSON
        "stream": False,
        "options": {
            "temperature": 0.1 # Giữ temperature thấp để câu trả lời nhất quán, ít bị ảo giác
        }
    }

    try:
        # Gọi API nội bộ sang Ollama
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        llm_output = result.get("response", "{}")

        print("========== RAW OUTPUT TỪ QWEN ==========")
        print(llm_output)
        print("========================================")
        
        llm_parsed = json.loads(llm_output)
       
        # Parse chuỗi JSON LLM trả về thành Python Dictionary
        parsed_data = json.loads(llm_output)
        
        # Gắn thêm ticker để n8n dễ map vào Database
        parsed_data["ticker"] = data.ticker
        parsed_data["article_title"] = data.article_title
        await asyncio.sleep(1)
        
        return parsed_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="LLM không trả về đúng định dạng JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lệnh chạy: python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level trace