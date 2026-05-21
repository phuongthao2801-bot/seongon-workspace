#!/usr/bin/env python3
"""
Script thêm comment vào Google Doc qua Google Drive API v3.
Dùng bởi skill comment-hop-dong của SEONGON.

Cài thư viện trước khi chạy:
    pip3 install google-auth google-auth-httplib2 google-api-python-client

Cách chạy:
    python3 add_comments.py \
        --file-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms" \
        --credentials ~/.google-credentials.json \
        --comments-json '[{"quote": "điều khoản thanh toán", "note": "[SEONGON Review] Lưu ý..."}]'
"""

import argparse
import json
import sys
import os
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Thiếu thư viện Google API. Chạy lệnh sau để cài:")
    print("   pip3 install google-auth google-auth-httplib2 google-api-python-client")
    sys.exit(1)


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]


def load_credentials(credentials_path: str) -> Credentials:
    """Tải credentials từ file JSON."""
    if not os.path.exists(credentials_path):
        print(f"❌ Không tìm thấy file credentials: {credentials_path}")
        print("   Chạy skill google-connect để đăng nhập Google trước.")
        sys.exit(1)

    try:
        creds = Credentials.from_authorized_user_file(credentials_path, SCOPES)
    except Exception as e:
        print(f"❌ File credentials không hợp lệ: {e}")
        sys.exit(1)

    # Làm mới token nếu hết hạn
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Ghi lại token mới
            with open(credentials_path, "w") as f:
                f.write(creds.to_json())
            print("✅ Token đã được làm mới tự động.")
        except Exception as e:
            print(f"❌ Không thể làm mới token: {e}")
            print("   Sếp cần chạy lại skill google-connect để đăng nhập lại.")
            sys.exit(1)

    return creds


def add_comment_to_doc(service, file_id: str, quote: str, note: str) -> dict:
    """
    Thêm 1 comment vào Google Doc.

    Args:
        service: Google Drive API service
        file_id: ID của file Google Doc
        quote: Đoạn văn bản cần comment (anchor)
        note: Nội dung comment

    Returns:
        dict với keys: success (bool), comment_id (str), error (str)
    """
    try:
        comment_body = {
            "content": note,
        }

        # Nếu có quote, thêm anchor
        if quote and len(quote.strip()) > 0:
            comment_body["quotedFileContent"] = {
                "mimeType": "text/plain",
                "value": quote.strip()
            }

        result = service.comments().create(
            fileId=file_id,
            body=comment_body,
            fields="id,content,quotedFileContent"
        ).execute()

        return {
            "success": True,
            "comment_id": result.get("id", ""),
            "error": ""
        }

    except HttpError as e:
        error_msg = str(e)
        if "403" in error_msg:
            error_msg = "Không có quyền comment trên file này. Kiểm tra quyền truy cập."
        elif "404" in error_msg:
            error_msg = "Không tìm thấy file. Kiểm tra lại FILE_ID."
        return {
            "success": False,
            "comment_id": "",
            "error": error_msg
        }
    except Exception as e:
        return {
            "success": False,
            "comment_id": "",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Thêm comment vào Google Doc — SEONGON Contract Review"
    )
    parser.add_argument("--file-id", required=True, help="ID của file Google Doc")
    parser.add_argument(
        "--credentials",
        default=os.path.expanduser("~/.google-credentials.json"),
        help="Đường dẫn đến file credentials (mặc định: ~/.google-credentials.json)"
    )
    parser.add_argument(
        "--comments-json",
        required=True,
        help='JSON array: [{"quote": "đoạn văn", "note": "nội dung comment"}, ...]'
    )

    args = parser.parse_args()

    # Parse danh sách comment
    try:
        comments_list = json.loads(args.comments_json)
        if not isinstance(comments_list, list):
            raise ValueError("Phải là JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ comments-json không hợp lệ: {e}")
        print('   Ví dụ đúng: \'[{"quote": "điều khoản X", "note": "[SEONGON Review] Lưu ý..."}]\'')
        sys.exit(1)

    if not comments_list:
        print("⚠️  Danh sách comment rỗng. Không có gì để thêm.")
        sys.exit(0)

    # Tải credentials
    print(f"🔐 Đang tải credentials từ: {args.credentials}")
    creds = load_credentials(args.credentials)

    # Khởi tạo Google Drive API service
    try:
        service = build("drive", "v3", credentials=creds)
        print(f"✅ Kết nối Google Drive API thành công.")
    except Exception as e:
        print(f"❌ Không thể kết nối Google Drive API: {e}")
        sys.exit(1)

    print(f"\n📄 File ID: {args.file_id}")
    print(f"💬 Số comment cần thêm: {len(comments_list)}\n")

    # Thêm từng comment
    success_count = 0
    fail_count = 0
    results = []

    for i, item in enumerate(comments_list, 1):
        quote = item.get("quote", "").strip()
        note = item.get("note", "").strip()

        if not note:
            print(f"  [{i}] ⚠️  Bỏ qua — note rỗng")
            continue

        # Đảm bảo prefix SEONGON Review
        if not note.startswith("[SEONGON Review]"):
            note = f"[SEONGON Review] {note}"

        quote_preview = quote[:40] + "..." if len(quote) > 40 else quote
        note_preview = note[:60] + "..." if len(note) > 60 else note
        print(f"  [{i}] Thêm comment...")
        print(f"       Quote: \"{quote_preview}\"")
        print(f"       Note:  \"{note_preview}\"")

        result = add_comment_to_doc(service, args.file_id, quote, note)

        if result["success"]:
            success_count += 1
            print(f"       ✅ Thành công (ID: {result['comment_id']})")
        else:
            fail_count += 1
            print(f"       ❌ Lỗi: {result['error']}")

        results.append({
            "index": i,
            "quote": quote,
            "note": note,
            "success": result["success"],
            "comment_id": result["comment_id"],
            "error": result["error"]
        })

    # Tổng kết
    print(f"\n{'='*50}")
    print(f"📊 KẾT QUẢ:")
    print(f"   ✅ Thành công: {success_count} comment")
    print(f"   ❌ Lỗi:       {fail_count} comment")
    print(f"{'='*50}")

    # Xuất kết quả JSON để agent đọc
    output = {
        "file_id": args.file_id,
        "google_doc_url": f"https://docs.google.com/document/d/{args.file_id}/edit",
        "total": len(comments_list),
        "success_count": success_count,
        "fail_count": fail_count,
        "timestamp": datetime.now().strftime("%H:%M %d/%m/%Y"),
        "results": results
    }
    print("\n=== JSON OUTPUT ===")
    print(json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
