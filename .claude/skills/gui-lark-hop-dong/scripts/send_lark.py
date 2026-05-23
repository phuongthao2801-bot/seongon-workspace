#!/usr/bin/env python3
"""
Gửi tin nhắn Lark cho người nhận (qua email hoặc open_id).
Dùng bot "Trợ lý Bà Bơ" của SEONGON — app_id cli_aa8b214cceb81eef.

Cách dùng:
    python3 send_lark.py \
        --to "ngophuongthao@seongon.com" \
        --to-type email \
        --message-file /tmp/mail-body.txt

Hoặc inline:
    python3 send_lark.py --to "..." --to-type email --message "Nội dung..."
"""
import argparse, json, sys, urllib.request, urllib.error

# Bot credentials — Trợ lý Bà Bơ
APP_ID = "cli_aa8b214cceb81eef"
APP_SECRET = "BPfivof5HSoPAmCPFYF2AhRqwdc1oJmV"
BASE = "https://open.larksuite.com/open-apis"


def get_tenant_token():
    req = urllib.request.Request(
        f"{BASE}/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get("code") != 0:
        raise RuntimeError(f"Token error: {resp}")
    return resp["tenant_access_token"]


def send_text(token, receive_id, receive_id_type, text):
    body = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False)
    }
    req = urllib.request.Request(
        f"{BASE}/im/v1/messages?receive_id_type={receive_id_type}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        return resp
    except urllib.error.HTTPError as e:
        return {"code": -1, "msg": f"HTTP {e.code}: {e.read().decode()}"}


def main():
    parser = argparse.ArgumentParser(description="Gửi tin nhắn Lark")
    parser.add_argument("--to", required=True, help="ID người nhận (email/open_id/user_id/...)")
    parser.add_argument("--to-type", default="email",
                        choices=["email", "open_id", "user_id", "union_id", "chat_id"])
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--message", help="Nội dung tin nhắn (inline)")
    grp.add_argument("--message-file", help="Đường dẫn file chứa nội dung")
    args = parser.parse_args()

    if args.message_file:
        with open(args.message_file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.message

    print(f"Gửi Lark đến {args.to} (type={args.to_type})...")
    token = get_tenant_token()
    resp = send_text(token, args.to, args.to_type, text)

    if resp.get("code") == 0:
        msg_id = resp.get("data", {}).get("message_id")
        print(f"✅ Đã gửi — Message ID: {msg_id}")
        sys.exit(0)
    else:
        print(f"❌ Gửi fail: code={resp.get('code')} msg={resp.get('msg')}")
        print(json.dumps(resp, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
