---
name: hop-dong-tom-tat
description: Đọc file hợp đồng (PDF/DOCX/text) và tóm tắt điều khoản quan trọng thành file .md dễ đọc
version: 1.1
triggers:
  - "tóm tắt hợp đồng"
  - "đọc file hợp đồng"
  - "điều khoản quan trọng"
  - "review hợp đồng"
dependencies:
  - checklist.md    # Danh sách điều khoản cần kiểm tra — load trước khi phân tích
  - template.md     # Mẫu file output — load khi chuẩn bị xuất kết quả
  - input/          # Thư mục Sếp để file hợp đồng vào
  - output/         # Thư mục lưu file tóm tắt sau khi xong
author: SEONGON · Ngô Phương Thảo
---

# Skill: Tóm tắt Hợp đồng

## Mục đích
Đọc file hợp đồng và tóm tắt các điều khoản quan trọng thành file `.md` dễ đọc — giúp Sếp nắm nhanh mà không cần đọc toàn bộ văn bản pháp lý.

---

## Các bước thực hiện

### Bước 1 — Nhận file hợp đồng
Hỏi Sếp: *"Sếp để file hợp đồng vào folder `input/` hoặc paste nội dung vào đây nhé!"*
- Nếu là file → đọc từ `input/[tên file]`
- Nếu paste text → xử lý trực tiếp từ nội dung Sếp gửi
- Nếu không có gì → dừng, nhắc Sếp cung cấp file

### Bước 2 — Load checklist kiểm tra
> **Load on demand:** Đọc `checklist.md` để biết đầy đủ các điều khoản cần trích xuất và dấu hiệu rủi ro cần lưu ý.

### Bước 3 — Phân tích hợp đồng
Đọc toàn bộ nội dung, trích xuất theo đúng các mục trong `checklist.md`:
1. **Thông tin cơ bản** — tên 2 bên, ngày ký, giá trị, người đại diện
2. **Phạm vi công việc** — SEONGON cam kết làm gì, KPI nếu có
3. **Thời hạn & deadline** — từng hạng mục cụ thể
4. **Lịch thanh toán** — đợt, số tiền, điều kiện
5. **Điều khoản phạt** — vi phạm nào, mức phạt bao nhiêu
6. **Điều khoản chấm dứt** — điều kiện 2 bên hủy hợp đồng
7. **⚠️ Điểm rủi ro** — điều khoản bất lợi, mơ hồ, một chiều

### Bước 4 — Tạo file tóm tắt
> **Load on demand:** Đọc `template.md` để lấy format chuẩn, điền nội dung thật vào từng mục.

Lưu file vào: `output/tom-tat-[tên khách hàng]-[YYYY-MM-DD].md`

### Bước 5 — Báo cáo cho Sếp
Thông báo: *"Đã lưu tóm tắt vào `output/tom-tat-[...].md`"* + highlight 2–3 điểm quan trọng nhất cần Sếp chú ý.

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| Không đọc được file PDF | PDF bị scan (ảnh), không có text | Nhắc Sếp dùng PDF có text hoặc paste nội dung trực tiếp |
| Thiếu thông tin thanh toán | Hợp đồng ghi chú riêng trong phụ lục | Hỏi Sếp: *"Có file phụ lục đính kèm không?"* |
| Điều khoản mơ hồ, không rõ | Văn bản pháp lý viết chung chung | Ghi rõ "Cần làm rõ" + trích nguyên văn đoạn đó |
| File output ghi đè file cũ | Cùng tên khách hàng, cùng ngày | Thêm suffix `-v2`, `-v3` vào tên file |

---

## Tiêu chí tự kiểm chất lượng

Trước khi lưu file output, agent tự kiểm:
- [ ] Đủ 7 mục theo checklist (không bỏ sót mục nào)
- [ ] Phần ⚠️ rủi ro có ít nhất 1 điểm (dù hợp đồng tốt cũng phải ghi rõ "không phát hiện rủi ro")
- [ ] Giá trị hợp đồng và lịch thanh toán ghi đúng số, đủ đơn vị (VNĐ/USD)
- [ ] Tên file output đúng định dạng: `tom-tat-[khách hàng]-[YYYY-MM-DD].md`
- [ ] Có dòng cảnh báo cuối: *"Tóm tắt hỗ trợ — không thay thế tư vấn pháp lý"*
- [ ] Với hợp đồng >500 triệu: nhắc Sếp cho luật sư review thêm
