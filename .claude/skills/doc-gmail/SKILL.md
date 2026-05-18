---
name: doc-gmail
description: Đọc Gmail và tóm tắt email quan trọng thành bản tin phân loại theo mức độ ưu tiên
version: 1.1
triggers:
  - "đọc gmail"
  - "tóm tắt email hôm nay"
  - "có email quan trọng nào không"
  - "bản tin email"
dependencies:
  - keywords.md     # Danh sách từ khóa lọc email — load khi cần lọc
  - template.md     # Mẫu bản tin output — load khi cần xuất báo cáo
  - output/         # Thư mục lưu bản tin email theo ngày
requires_mcp: gmail
author: SEONGON · Ngô Phương Thảo
---

# Skill: Đọc Gmail & Tóm tắt email quan trọng

## Mục đích
Đọc Gmail của Sếp, lọc email quan trọng trong ngày/tuần và tóm tắt thành bản tin gọn gàng — phân loại theo 3 mức độ ưu tiên.

---

## Các bước thực hiện

### Bước 1 — Kiểm tra kết nối MCP Gmail
Kiểm tra Gmail MCP có hoạt động không bằng cách gọi `search_threads` với query đơn giản.
- Nếu lỗi kết nối → dừng, báo Sếp: *"Gmail MCP chưa kết nối. Vào Settings → MCP → bật Gmail."*
- Nếu OK → tiếp tục bước 2

### Bước 2 — Load danh sách từ khóa ưu tiên
> **Load on demand:** Chỉ đọc `keywords.md` nếu Sếp không chỉ định rõ loại email cần lọc. Nếu Sếp đã nói *"chỉ xem email khách hàng"* hoặc *"tìm email về hợp đồng"* → bỏ qua bước load file này, dùng yêu cầu của Sếp trực tiếp.

### Bước 3 — Tìm email chưa đọc
Dùng `search_threads` với query: `is:unread newer_than:1d`
- Lấy tối đa 20 email
- Ưu tiên email từ người gửi trong danh sách `keywords.md`

### Bước 4 — Đọc nội dung email quan trọng
Dùng `get_thread` để đọc chi tiết top 5–10 email có vẻ quan trọng nhất (dựa trên chủ đề + người gửi).
- **Không đọc** email từ danh sách "Bỏ qua hoàn toàn" trong `keywords.md`
- **Không đọc** email cá nhân/nhạy cảm trừ khi Sếp yêu cầu rõ ràng

### Bước 5 — Phân loại và tóm tắt
Phân loại mỗi email vào 1 trong 3 nhóm:
- 🔴 **Cần xử lý ngay** — khách hàng chờ, deadline hôm nay, khiếu nại
- 🟡 **Cần xử lý hôm nay** — báo giá, meeting request, phản hồi đối tác
- 🟢 **Đọc khi rảnh** — newsletter, thông báo chung, quảng cáo

### Bước 6 — Xuất bản tin
> **Load on demand:** Chỉ đọc `template.md` nếu Sếp chưa từng nhận bản tin từ skill này trước đó (lần đầu chạy). Nếu Sếp đã quen format → dùng format từ bộ nhớ hội thoại, không cần load lại file.

Trả lời Sếp theo đúng format template. Kết thúc bằng 1–2 gợi ý việc nên làm trước tiên.
Lưu bản tin vào `output/ban-tin-[YYYY-MM-DD].md` để tra cứu lại sau.

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `Gmail MCP not connected` | MCP Gmail chưa bật | Nhắc Sếp vào Settings → MCP → bật Gmail |
| Không tìm thấy email nào | Inbox trống hoặc query sai | Thử mở rộng: `newer_than:7d` |
| Email hiển thị nhưng không đọc được | `get_thread` timeout | Bỏ qua email đó, ghi chú "không đọc được" |
| Phân loại sai mức độ | Từ khóa không đủ | Cập nhật `keywords.md` thêm từ khóa mới |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi bản tin cho Sếp, agent tự kiểm:
- [ ] Có đủ 3 nhóm (🔴🟡🟢) — dù nhóm nào đó có thể là "0 email"
- [ ] Mỗi email có: người gửi + chủ đề + 1 câu tóm tắt + action cụ thể
- [ ] Không có email quảng cáo lọt vào nhóm 🔴 hoặc 🟡
- [ ] Gợi ý cuối bản tin có ít nhất 1 việc cụ thể (không chung chung)
- [ ] Không tiết lộ nội dung email cá nhân/nhạy cảm
