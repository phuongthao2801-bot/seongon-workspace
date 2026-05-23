---
name: gui-lark-hop-dong
description: Gửi tin nhắn Lark cho người phụ trách (hoặc Sếp) báo cáo kết quả review hợp đồng — qua bot "Trợ lý Bà Bơ" của SEONGON. Dùng sau khi đã có tóm tắt từ `hop-dong-tom-tat` và bản review Google Doc từ `comment-hop-dong`. THAY THẾ cho Gmail vì Workspace SEONGON chặn third-party Gmail API.
---

# Skill: Gửi Lark Hợp Đồng — v2.0 (2026-05-21)

## Mục đích
Gửi thông báo kết quả review hợp đồng qua **Lark** thay vì Gmail. Workspace `seongon.com` chặn third-party Gmail API (`Precondition check failed` cho mọi request) — Lark là kênh nội bộ chính thức cho thông báo công việc.

## Khi nào dùng
Sau khi đã có:
1. Tóm tắt + 11 điểm rủi ro (từ skill `hop-dong-tom-tat`)
2. Link Google Doc review đã có 3-yếu-tố comment (từ skill `comment-hop-dong`)

## Cấu trúc folder
```
gui-lark-hop-dong/
├── SKILL.md                ← file này
├── scripts/
│   └── send_lark.py        ← script gửi Lark qua bot Trợ lý Bà Bơ
├── template.md             ← mẫu nội dung tin nhắn
└── output/
    └── lark-log-*.md
```

## Yêu cầu trước khi chạy
- Bot **Trợ lý Bà Bơ** (app_id `cli_aa8b214cceb81eef`) đã được add vào Lark workspace SEONGON
- Người nhận đã từng tương tác với bot ÍT NHẤT 1 LẦN (Lark policy: bot không gửi được message đến user chưa "biết" bot)

## Các bước thực hiện

### Bước 1 — Nhận thông tin đầu vào
Nhận từ agent gọi skill:
- **Tên người nhận** — vd: "Sếp Thảo"
- **Email Lark người nhận** — vd: `ngophuongthao@seongon.com` (dùng làm receive_id với type=email)
- **Tên hợp đồng** — vd: "HĐ 176-PCU/2026/HĐ-SB · SeABank × SEONGON"
- **Giá trị HĐ** — vd: "378.318.600 VND đã VAT"
- **Link Google Doc review** — link bản đã có 3-yếu-tố comment
- **3 ưu tiên đàm phán** — danh sách ưu tiên hàng đầu
- **Danh sách 11 điểm** — đầy đủ với số [N] và emoji

### Bước 2 — Soạn nội dung tin nhắn
> **Load on demand:** Đọc `template.md` để lấy format chuẩn.

Format chuẩn tin Lark (plain text vì Lark text msg không hỗ trợ markdown):
```
[SEONGON Review] [Tên HĐ]

Đã hoàn tất review [Tên HĐ], giá trị [Giá trị].

🎯 3 ƯU TIÊN ĐÀM PHÁN TRƯỚC KHI KÝ:

1. [Ưu tiên 1 — Điều khoản cụ thể]
2. [Ưu tiên 2]
3. [Ưu tiên 3]

📋 DANH SÁCH 11 ĐIỂM (★ = ưu tiên hàng đầu):
[1] ...
...
[11] ...

📎 BẢN REVIEW Google Doc (có 11 comment + highlight cam):
[link]

⚠️ Tóm tắt hỗ trợ, không thay thế tư vấn pháp lý.
```

### Bước 3 — Xin xác nhận từ Sếp
Hiển thị toàn bộ nội dung tin nhắn ĐÃ SOẠN và hỏi:
> "Sếp duyệt nội dung trên không? (1) gửi luôn · (2) sửa · (3) huỷ"

**DỪNG — đợi Sếp trả lời.** Không tự gửi khi chưa có lệnh.

### Bước 4 — Lưu nội dung vào file tạm
Lưu nội dung vào `/tmp/lark-msg-[hopdong].txt` để pass cho script.

### Bước 5 — Chạy script gửi Lark
```bash
python3 /Users/phuongthaongo/.claude/skills/gui-lark-hop-dong/scripts/send_lark.py \
    --to "ngophuongthao@seongon.com" \
    --to-type email \
    --message-file /tmp/lark-msg-[hopdong].txt
```

Script tự động:
1. Lấy `tenant_access_token` từ bot credentials
2. Gọi API `im/v1/messages?receive_id_type=email` để gửi text message
3. Trả về `message_id` nếu thành công

### Bước 6 — Lưu log
Lưu vào `output/lark-log-[YYYY-MM-DD].md`:
```markdown
# Log Gửi Lark — [Ngày]
**Người nhận:** [Tên] <[email Lark]>
**Hợp đồng:** [Tên + giá trị]
**Link Google Doc review:** [URL]
**Message ID:** [Lark message ID]
**Trạng thái:** Đã gửi
**Thời gian:** [HH:MM DD/MM/YYYY]
```

---

## Bài học QUAN TRỌNG

### Vì sao dùng Lark thay Gmail?
- Workspace `seongon.com` (Google Workspace business) BẬT **App access control** chặn tất cả third-party app chưa được admin approve
- Lỗi gặp: `Precondition check failed` (HTTP 400) khi gọi BẤT KỲ Gmail API nào — kể cả `getProfile`
- Verify cách fix Gmail: chỉ admin Workspace SEONGON mới approve được app "SEONGON Automation" trong Admin Console → Security → API Controls
- Trong khi đó: Lark Open API hoạt động bình thường — bot "Trợ lý Bà Bơ" đã được setup từ trước

### Lark vs Gmail — khác biệt khi dùng cho thông báo nội bộ
| Tiêu chí | Gmail | Lark |
|----------|-------|------|
| Tốc độ | Tức thời | Tức thời (push notification) |
| Format | HTML/markdown đẹp | Plain text (text msg) hoặc rich card phức tạp |
| Lưu trữ | Inbox vĩnh viễn | Lưu trong chat history |
| Tìm kiếm | Mạnh (gmail search) | OK |
| Phù hợp | Báo cáo formal cho ngoài | Thông báo nội bộ nhanh |

→ Với SEONGON: **Lark cho thông báo nội bộ**, Gmail chỉ dùng cho khách hàng/đối tác (qua UI thủ công).

### Quy tắc kỹ thuật
- Bot credentials hardcode trong `send_lark.py` (app_id + secret) — tạm chấp nhận vì là bot nội bộ, không expose public
- Lark text message TỐI ĐA 5000 ký tự — tin dài hơn cần dùng rich card hoặc tách nhiều message
- Plain text Lark KHÔNG hỗ trợ markdown — viết nội dung như tin nhắn thông thường, dùng emoji + ngắt dòng để cấu trúc

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `code=99991663` user not found | Email người nhận không có trong Lark workspace | Verify email đúng (`ngophuongthao@seongon.com`); hoặc user chưa setup Lark |
| `code=230002` bot not in chat / receive_id invalid | Người nhận chưa từng tương tác với bot | Sếp nhắn 1 câu "hi" cho bot Trợ lý Bà Bơ trước; sau đó bot mới gửi được |
| `code=99991668` tenant token error | App credentials sai hoặc expired | Verify APP_ID + APP_SECRET trong send_lark.py |
| Tin nhắn quá dài (>5000 ký tự) | Nội dung HĐ phức tạp | Cắt ngắn — chỉ giữ 3 ưu tiên + link Google Doc cho chi tiết |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi:
- [ ] Người nhận đúng email Lark
- [ ] Có đủ 3 ưu tiên đàm phán
- [ ] Có link Google Doc review
- [ ] Tin nhắn <5000 ký tự
- [ ] Có cảnh báo cuối "không thay thế tư vấn pháp lý"
- [ ] Đã xin xác nhận từ Sếp TRƯỚC KHI gửi
- [ ] Log đã lưu vào `output/`
