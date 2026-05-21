# Skill: Comment Hợp Đồng Google Doc

## Mục đích
Đọc link Google Doc hợp đồng, thêm comment trực tiếp vào những điều khoản cần lưu ý — giúp người quản lý hợp đồng thấy ngay điểm cần chú ý mà không cần đọc toàn bộ văn bản.

## Khi nào dùng
Khi đã có kết quả từ skill `hop-dong-tom-tat` (danh sách điểm lưu ý) và cần đưa comment vào file Google Doc gốc.

## Cấu trúc folder
```
comment-hop-dong/
├── SKILL.md              ← file skill này
├── scripts/
│   └── add_comments.py   ← script thêm comment qua Google API
└── output/               ← log kết quả sau khi comment
```

## Yêu cầu trước khi chạy
- File `~/.google-credentials.json` phải tồn tại (đăng nhập Google qua skill `google-connect`)
- Có quyền **Commenter** hoặc **Editor** trên file Google Doc đó

## Các bước thực hiện

### Bước 1 — Nhận thông tin đầu vào
Nhận 2 thứ từ agent gọi skill này:
- **Link Google Doc** — URL file hợp đồng (dạng `https://docs.google.com/document/d/FILE_ID/...`)
- **Danh sách điểm lưu ý** — lấy từ kết quả skill `hop-dong-tom-tat` (phần "⚠️ Điểm cần lưu ý")

Trích xuất `FILE_ID` từ URL: phần nằm giữa `/d/` và `/edit`.

### Bước 2 — Kiểm tra xác thực Google
Kiểm tra file credentials:
```bash
ls ~/.google-credentials.json 2>/dev/null && echo "OK" || echo "MISSING"
```
- Nếu **MISSING** → dừng, báo: "Chưa kết nối Google. Sếp chạy skill `google-connect` trước nhé."
- Nếu **OK** → tiếp tục

### Bước 3 — Thêm comment vào Google Doc
> **Load on demand:** Chỉ đọc `scripts/add_comments.py` nếu cần xem cú pháp script.

Chạy script thêm comment:
```bash
python3 scripts/add_comments.py \
  --file-id "FILE_ID" \
  --credentials ~/.google-credentials.json \
  --comments-json 'DANH_SACH_COMMENT_JSON'
```

Format JSON cho `--comments-json`:
```json
[
  {"quote": "đoạn văn bản cần comment", "note": "Nội dung comment của Sếp Thảo"},
  {"quote": "điều khoản thứ 2", "note": "Lưu ý: điều khoản này có rủi ro..."}
]
```

Với mỗi điểm lưu ý từ skill 1, tạo 1 comment tương ứng. Prefix comment bằng: **"[SEONGON Review]"** để dễ nhận ra.

### Bước 4 — Ghi log kết quả
Lưu kết quả vào `output/comment-log-[YYYY-MM-DD].md`:
```markdown
# Log Comment Hợp Đồng — [Ngày]
**File:** [URL Google Doc]
**File ID:** [FILE_ID]
**Số comment đã thêm:** [N]
**Thời gian:** [HH:MM DD/MM/YYYY]

## Danh sách comment đã thêm
1. Đoạn: "[quote ngắn]" → Comment: "[nội dung]"
2. ...

## Kết quả
- ✅ Thành công: [N] comment
- ❌ Lỗi: [N] comment (nếu có, ghi rõ lý do)
```

### Bước 5 — Trả kết quả về agent
Trả về:
- Link Google Doc (giữ nguyên để dùng cho skill gửi mail)
- Số comment đã thêm thành công
- Danh sách tóm tắt các điểm đã comment (để đưa vào mail)

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `~/.google-credentials.json` không tồn tại | Chưa chạy google-connect | Nhắc Sếp chạy `google-connect` trước |
| `403 Forbidden` khi gọi API | Không có quyền comment trên file | Nhắc Sếp kiểm tra quyền truy cập file |
| `404 Not Found` | FILE_ID sai hoặc file đã xóa | Kiểm tra lại URL, trích xuất lại FILE_ID |
| Script Python lỗi `ModuleNotFoundError` | Thiếu thư viện | Chạy: `pip3 install google-auth google-auth-httplib2 google-api-python-client` |
| Quote không tìm thấy trong tài liệu | Đoạn văn bản không khớp chính xác | Dùng đoạn ngắn hơn (5-10 từ) làm quote |

---

## Tiêu chí tự kiểm chất lượng

Trước khi trả kết quả, tự kiểm:
- [ ] Đã trích đúng FILE_ID từ URL
- [ ] Credentials tồn tại và không hết hạn
- [ ] Mỗi điểm lưu ý từ skill 1 có ít nhất 1 comment tương ứng
- [ ] Comment có prefix `[SEONGON Review]`
- [ ] Log đã lưu vào folder `output/`
- [ ] Đã trả về link Google Doc để dùng cho bước gửi mail
