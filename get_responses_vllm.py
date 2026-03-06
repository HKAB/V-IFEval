import argparse
import json
import os
import requests
from datetime import datetime
import concurrent.futures

def process_prompt(prompt_data, base_url, api_key, model):
    """Gửi một prompt đến server vLLM và trả về kết quả."""
    prompt = prompt_data.get("prompt", "")
    if not prompt:
        return {"prompt": prompt, "response": ""}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Payload chuẩn tương thích với OpenAI API của vLLM
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        # Bạn có thể thêm các tham số generation ở đây (ví dụ: "temperature": 0.7, "max_tokens": 1024)
    }
    
    try:
        url = f"{base_url.rstrip('/')}/chat/completions"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return {"prompt": prompt, "response": reply}
        
    except requests.exceptions.RequestException as e:
        return {"prompt": prompt, "response": f"ERROR: {str(e)}"}
    except KeyError as e:
        return {"prompt": prompt, "response": f"ERROR: Cấu trúc response không hợp lệ - {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="Gửi prompt hàng loạt đến vLLM server bằng ThreadPoolExecutor.")
    parser.add_argument("--base_url", required=True, help="URL gốc của vLLM (VD: http://localhost:8000/v1)")
    parser.add_argument("--api_key", required=True, help="API key của server vLLM")
    parser.add_argument("--model", required=True, help="Tên model đang được deploy trên vLLM")
    parser.add_argument("--input_file", required=True, help="Đường dẫn đến file input JSONL")
    parser.add_argument("--output_folder", required=True, help="Thư mục lưu file output")
    parser.add_argument("--workers", type=int, default=10, help="Số lượng thread chạy song song (mặc định: 10)")
    
    args = parser.parse_args()

    # Đọc dữ liệu từ file JSONL
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            lines = [json.loads(line) for line in f if line.strip()]
    except Exception as e:
        print(f"Lỗi khi đọc file input: {e}")
        return

    print(f"Đã tải {len(lines)} prompts từ {args.input_file}")

    # Chuẩn bị đường dẫn output
    os.makedirs(args.output_folder, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Xử lý ký tự '/' nếu tên model là đường dẫn từ HuggingFace (vd: meta-llama/Llama-2-7b)
    safe_model_name = args.model.replace("/", "-") 
    output_filename = f"vi_input_response_data_{safe_model_name}_{date_str}.jsonl"
    output_path = os.path.join(args.output_folder, output_filename)

    print(f"File output sẽ được lưu tại: {output_path}")
    print(f"Bắt đầu xử lý với {args.workers} workers...")

    # Xử lý đa luồng
    success_count = 0
    with open(output_path, 'w', encoding='utf-8') as out_f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            # Tạo dictionary lưu trữ các task (futures)
            futures = {
                executor.submit(process_prompt, line, args.base_url, args.api_key, args.model): line 
                for line in lines
            }
            
            # as_completed giúp ghi ngay kết quả xuống file khi một thread chạy xong
            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                result = future.result()
                
                # Ghi từng dòng JSON vào file output
                out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
                out_f.flush() 
                
                if not result["response"].startswith("ERROR:"):
                    success_count += 1
                
                # Hiển thị tiến độ
                if i % 10 == 0 or i == len(lines):
                    print(f"Đã xử lý {i}/{len(lines)} prompts...")

    print(f"\nHoàn tất! Cào dữ liệu thành công {success_count}/{len(lines)} prompts.")

if __name__ == "__main__":
    main()