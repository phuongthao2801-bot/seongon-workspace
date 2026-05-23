---
name: google-connect
description: Kết nối tài khoản Google (Drive + Docs + Gmail) cho các skill khác dùng. Tạo file `~/.google-credentials.json` qua OAuth 2.0 — chạy 1 lần là dùng được vĩnh viễn. Gọi khi Sếp gõ "/google-connect", "kết nối Google", "đăng nhập Google", hoặc khi 1 skill báo lỗi "thiếu ~/.google-credentials.json".
---

# Skill: Google Connect

## Mục đích
Cấp quyền cho các skill SEONGON dùng Google API (Drive · Docs · Gmail · Calendar). Lưu OAuth token tại `~/.google-credentials.json` — các skill khác đọc file này để xác thực.

## Khi nào dùng
- Lần đầu setup máy
- Khi skill khác báo: `~/.google-credentials.json` không tồn tại
- Khi token hết hạn không tự refresh được (Sếp đổi mật khẩu Google, revoke quyền, v.v.)

## Cấu trúc folder
```
google-connect/
├── SKILL.md                ← file này
├── scripts/
│   └── setup_oauth.py      ← script chạy OAuth flow
└── output/
    └── connect-log.md      ← log lần kết nối gần nhất
```

## Các bước thực hiện

### Bước 0 — Hỏi Sếp đã có OAuth Client ID chưa
Cần 1 file JSON do Google Cloud Console cấp (gọi là **OAuth Client ID**).
- Nếu Sếp **đã có file** `client_secret.json` (hoặc tên tương tự) → nhảy sang Bước 3.
- Nếu **chưa có** → hướng dẫn Sếp tạo qua Bước 1-2.

### Bước 1 — Hướng dẫn Sếp tạo OAuth Client ID (1 lần duy nhất)
Đưa hướng dẫn từng bước cho Sếp:

```
1. Mở https://console.cloud.google.com/
   → Đăng nhập bằng tài khoản Google muốn cấp quyền (ví dụ: ngophuongthao@seongon.com)

2. Tạo Project mới (hoặc dùng project có sẵn):
   → Góc trên trái, click dropdown project → "New Project"
   → Tên: "SEONGON Automation" → Create

3. Bật 3 API cần dùng (vào APIs & Services → Library):
   → Tìm "Google Drive API" → Enable
   → Tìm "Google Docs API" → Enable
   → Tìm "Gmail API" → Enable

4. Cấu hình OAuth Consent Screen:
   → APIs & Services → OAuth consent screen
   → User Type: External → Create
   → App name: "SEONGON Automation"
   → User support email: ngophuongthao@seongon.com
   → Developer contact: ngophuongthao@seongon.com
   → Save → Next → bỏ qua Scopes → Next
   → Test users → Add Users → thêm email ngophuongthao@seongon.com → Save

5. Tạo OAuth Client ID:
   → APIs & Services → Credentials → Create Credentials → OAuth client ID
   → Application type: "Desktop app"
   → Name: "SEONGON Local"
   → Create
   → Popup hiện ra → Download JSON → Lưu vào ~/Downloads/

6. Báo cho Claude đường dẫn file vừa tải về.
```

### Bước 2 — Hỏi Sếp đường dẫn file OAuth Client
Hỏi gọn:
> "Sếp paste đường dẫn file JSON vừa tải về (ví dụ: `/Users/phuongthaongo/Downloads/client_secret_xxx.json`)."

### Bước 3 — Chạy OAuth flow
```bash
python3 /Users/phuongthaongo/.claude/skills/google-connect/scripts/setup_oauth.py \
    --client-secret "[đường dẫn file Sếp paste]"
```

Script sẽ:
- Mở trình duyệt mặc định của Sếp
- Yêu cầu Sếp chọn tài khoản Google
- Hỏi xác nhận cấp quyền cho 4 scope: Drive, Docs, Gmail, Calendar
- Lưu token vào `~/.google-credentials.json`
- Test kết nối bằng cách gọi API lấy email của Sếp

### Bước 4 — Báo kết quả
Sau khi xong, báo:
```
✅ Đã kết nối Google
📧 Tài khoản: ngophuongthao@seongon.com
📁 Token lưu tại: ~/.google-credentials.json
🔑 Scope đã cấp: Drive · Docs · Gmail · Calendar

Sếp đã có thể chạy lại các skill:
- /comment-hop-dong
- /gui-mail-hop-dong
- /doc-gmail
- /ban-tin-sang
```

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Xử lý |
|-----|-------------|-------|
| `redirect_uri_mismatch` | OAuth Client tạo nhầm loại (không phải Desktop) | Quay lại Bước 1, chọn lại "Desktop app" |
| `access_denied` ở popup browser | Sếp chưa add email vào Test users | Thêm email vào OAuth consent screen → Test users |
| `Could not locate runnable browser` | Server không có GUI | Chạy script với cờ `--console-mode` để dùng copy-paste URL |
| Token sinh ra nhưng skill báo 401 | Scope thiếu | Chạy lại setup, xóa `~/.google-credentials.json` trước |

## Tiêu chí tự kiểm
- [ ] File `~/.google-credentials.json` tồn tại sau khi chạy
- [ ] Test gọi Drive API thành công (lấy được email của Sếp)
- [ ] Log lưu vào `output/connect-log.md`
- [ ] Không lộ client_secret ra Bash output (chỉ dùng path, không print nội dung)
