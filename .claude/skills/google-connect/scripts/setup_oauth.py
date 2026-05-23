#!/usr/bin/env python3
"""
Setup OAuth Google cho SEONGON Automation.
Chạy 1 lần để sinh file ~/.google-credentials.json.

Yêu cầu trước:
    pip3 install --user google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Cách chạy:
    python3 setup_oauth.py --client-secret ~/Downloads/client_secret_xxx.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Thiếu thư viện. Chạy:")
    print("   pip3 install --user google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

CREDENTIALS_PATH = os.path.expanduser("~/.google-credentials.json")
LOG_PATH = os.path.expanduser(
    "~/.claude/skills/google-connect/output/connect-log.md"
)


def main():
    parser = argparse.ArgumentParser(description="Setup OAuth Google cho SEONGON")
    parser.add_argument(
        "--client-secret",
        required=True,
        help="Đường dẫn file OAuth Client ID JSON tải từ Google Cloud Console",
    )
    parser.add_argument(
        "--console-mode",
        action="store_true",
        help="Dùng khi không mở được browser (server SSH). Yêu cầu copy-paste URL.",
    )
    args = parser.parse_args()

    client_path = os.path.expanduser(args.client_secret)
    if not os.path.exists(client_path):
        print(f"Không tìm thấy file: {client_path}")
        sys.exit(1)

    # Validate it's a desktop OAuth client
    try:
        with open(client_path) as f:
            client_data = json.load(f)
        if "installed" not in client_data:
            print("File OAuth Client phải là loại 'Desktop app'.")
            print("   File hiện tại có vẻ là Web app hoặc Service account.")
            print("   Quay lại Google Cloud Console → Credentials → tạo lại với 'Desktop app'.")
            sys.exit(1)
    except json.JSONDecodeError:
        print("File JSON không hợp lệ.")
        sys.exit(1)

    print(f"Đang chạy OAuth flow với {client_path}...")
    print(f"Yêu cầu {len(SCOPES)} scope: Drive · Docs · Gmail · Calendar\n")

    flow = InstalledAppFlow.from_client_secrets_file(client_path, SCOPES)

    if args.console_mode:
        creds = flow.run_console()
    else:
        print("Mở trình duyệt — Sếp đăng nhập + cấp quyền...")
        creds = flow.run_local_server(port=0, open_browser=True)

    # Lưu credentials
    with open(CREDENTIALS_PATH, "w") as f:
        f.write(creds.to_json())
    os.chmod(CREDENTIALS_PATH, 0o600)
    print(f"\nĐã lưu token: {CREDENTIALS_PATH}")

    # Test bằng cách lấy email
    try:
        oauth2 = build("oauth2", "v2", credentials=creds)
        info = oauth2.userinfo().get().execute()
        email = info.get("email", "UNKNOWN")
        print(f"Tài khoản đã kết nối: {email}")
    except Exception as e:
        print(f"Token lưu OK nhưng test API lỗi: {e}")
        email = "UNKNOWN"

    # Ghi log
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w") as f:
        f.write(f"# Google Connect — Log\n\n")
        f.write(f"- Tài khoản: {email}\n")
        f.write(f"- Thời gian: {datetime.now().strftime('%H:%M %d/%m/%Y')}\n")
        f.write(f"- Token path: {CREDENTIALS_PATH}\n")
        f.write(f"- Scopes: {len(SCOPES)} (Drive · Docs · Gmail · Calendar)\n")

    print(f"\nXong. Các skill khác có thể dùng credentials này ngay.")
    print(f"   Thử: /comment-hop-dong hoặc /gui-mail-hop-dong")


if __name__ == "__main__":
    main()
