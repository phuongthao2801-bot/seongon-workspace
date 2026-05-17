# Skill: Tóm tắt Hợp đồng

## Mục đích
Đọc file hợp đồng (PDF/DOCX) và tóm tắt các điều khoản quan trọng thành file .md dễ đọc — giúp Sếp nắm nhanh mà không cần đọc toàn bộ văn bản pháp lý.

## Khi nào dùng
Khi Sếp gõ: "tóm tắt hợp đồng này", "đọc file hợp đồng", "điều khoản quan trọng trong hợp đồng là gì"

## Cấu trúc folder
```
hop-dong-tom-tat/
├── hop-dong-tom-tat.md   ← file skill này
├── input/                ← Sếp để file hợp đồng vào đây
└── output/               ← file tóm tắt sẽ được lưu vào đây
```

## Các bước thực hiện

### Bước 1 — Nhận file hợp đồng
Hỏi Sếp: "Sếp cho tôi biết tên file hợp đồng hoặc paste nội dung vào đây"
- Nếu là file: đọc từ folder `input/`
- Nếu paste text: xử lý trực tiếp

### Bước 2 — Phân tích và tóm tắt
Đọc toàn bộ hợp đồng, trích xuất:

1. **Thông tin cơ bản** — Tên 2 bên, ngày ký, giá trị hợp đồng
2. **Phạm vi công việc** — SEONGON cam kết làm gì
3. **Thời hạn** — Deadline từng hạng mục, thời hạn hợp đồng
4. **Thanh toán** — Lịch thanh toán, điều kiện, hình thức
5. **Điều khoản phạt** — Vi phạm nào bị phạt, mức phạt
6. **Điều khoản chấm dứt** — Điều kiện để 2 bên hủy hợp đồng
7. **⚠️ Điểm cần lưu ý** — Các điều khoản bất lợi, mơ hồ, rủi ro

### Bước 3 — Lưu file output
Lưu file tóm tắt vào `output/tom-tat-[tên khách hàng]-[ngày].md`

Format file output:
```markdown
# TÓM TẮT HỢP ĐỒNG
**Khách hàng:** [Tên]
**Ngày ký:** [...]
**Giá trị:** [...]
**Người phụ trách:** [...]

## Phạm vi công việc
...

## Lịch thanh toán
...

## ⚠️ Điểm cần lưu ý
...
```

## Lưu ý
- Đây là tóm tắt hỗ trợ, không thay thế tư vấn pháp lý
- Với hợp đồng giá trị lớn (>500 triệu), nên cho luật sư review thêm
