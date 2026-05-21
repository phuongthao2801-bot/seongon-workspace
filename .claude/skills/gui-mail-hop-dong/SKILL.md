# Skill: Gửi Mail Hợp Đồng

## Mục đích
Soạn và gửi email thông báo kết quả review hợp đồng — tổng hợp các điểm lưu ý từ skill `hop-dong-tom-tat` và đính kèm link Google Doc đã có comment từ skill `comment-hop-dong`.

## Khi nào dùng
Sau khi đã có:
1. Danh sách điểm lưu ý (từ skill `hop-dong-tom-tat`)
2. Link Google Doc đã comment (từ skill `comment-hop-dong`)

## Cấu trúc folder
```
gui-mail-hop-dong/
├── SKILL.md      ← file skill này
├── template.md   ← mẫu email (load khi cần)
└── output/       ← lưu bản nháp email đã soạn
```

## Các bước thực hiện

### Bước 1 — Nhận thông tin đầu vào
Nhận từ agent gọi skill:
- **Tên người nhận** — do Sếp nhập thủ công
- **Email người nhận** — do Sếp nhập thủ công
- **Tên hợp đồng** — tên file hoặc tên khách hàng
- **Danh sách điểm lưu ý** — từ skill `hop-dong-tom-tat`
- **Link Google Doc** — URL file hợp đồng đã có comment

### Bước 2 — Hỏi Sếp thông tin gửi mail
Nếu chưa có email người nhận, hỏi:
> "Sếp cho tôi biết email của người nhận mail nhé? (Ví dụ: nguyen.van.a@seongon.com)"

Chờ Sếp trả lời trước khi tiếp tục.

### Bước 3 — Soạn nội dung email
> **Load on demand:** Đọc `template.md` để lấy mẫu email chuẩn nếu chưa có trong bộ nhớ hội thoại.

Soạn email theo mẫu:
```
Tiêu đề: [SEONGON] Review hợp đồng — [Tên hợp đồng]

Thân email:
Chào [Tên người nhận],

Chị đã check hợp đồng [Tên hợp đồng] và có một số điểm lưu ý sau:

[Danh sách điểm lưu ý — đánh số, gọn gàng]

Chị đã comment chi tiết trong hợp đồng theo link dưới đây:
[Link Google Doc]

Bạn vui lòng xem và phản hồi lại nhé.

Trân trọng,
Thảo — SEONGON
```

### Bước 4 — Xin xác nhận từ Sếp
Hiển thị toàn bộ nội dung email đã soạn và hỏi:
> "Đây là nội dung email tôi đã soạn. Sếp xác nhận gửi không? (Sếp có thể sửa nội dung trước khi gửi)"

**DỪNG — đợi Sếp xác nhận.** Không tự động gửi khi chưa có "OK" hoặc "gửi đi" từ Sếp.

### Bước 5 — Tạo bản nháp và gửi mail
Sau khi Sếp xác nhận, dùng Gmail MCP để tạo bản nháp:
```
create_draft:
  to: [email người nhận]
  subject: "[SEONGON] Review hợp đồng — [Tên hợp đồng]"
  body: [nội dung email đã soạn]
```

Sau khi tạo nháp thành công, hỏi Sếp:
> "Tôi đã tạo bản nháp trong Gmail. Sếp vào Gmail kiểm tra và bấm Gửi nhé — hoặc Sếp muốn tôi gửi thẳng luôn?"

Nếu Sếp muốn gửi thẳng → tìm draft ID vừa tạo và gửi qua Gmail MCP.

### Bước 6 — Lưu log
Lưu vào `output/mail-log-[YYYY-MM-DD].md`:
```markdown
# Log Gửi Mail — [Ngày]
**Người nhận:** [Tên] <[email]>
**Tiêu đề:** [Tiêu đề email]
**Hợp đồng:** [Tên]
**Link Google Doc:** [URL]
**Trạng thái:** Đã tạo nháp / Đã gửi
**Thời gian:** [HH:MM DD/MM/YYYY]
```

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| Gmail MCP không kết nối | MCP chưa bật | Nhắc Sếp vào Settings → MCP → bật Gmail |
| `create_draft` thất bại | Lỗi kết nối | Thử lại 1 lần; nếu vẫn lỗi → in nội dung email ra để Sếp gửi thủ công |
| Email người nhận không hợp lệ | Sai định dạng | Hỏi lại Sếp |
| Sếp muốn sửa nội dung | Thay đổi trước khi gửi | Chỉnh sửa theo yêu cầu, hiển thị lại và xin xác nhận lại |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi/tạo nháp, tự kiểm:
- [ ] Có email người nhận hợp lệ (có @)
- [ ] Tiêu đề email có tên hợp đồng
- [ ] Thân email có danh sách điểm lưu ý rõ ràng
- [ ] Thân email có link Google Doc
- [ ] Đã xin xác nhận từ Sếp trước khi gửi
- [ ] Log đã lưu vào folder `output/`
- [ ] Không tự gửi khi chưa có lệnh từ Sếp
