# Mẫu Email Review Hợp Đồng — SEONGON

## Tiêu đề
```
[SEONGON] Review hợp đồng — {TEN_HOP_DONG}
```

## Nội dung email

```
Chào {TEN_NGUOI_NHAN},

Chị đã check hợp đồng {TEN_HOP_DONG} và có một số điểm lưu ý sau:

{DANH_SACH_LUU_Y}

Chị đã comment chi tiết trong hợp đồng theo link dưới đây:
{LINK_GOOGLE_DOC}

Bạn vui lòng xem và phản hồi lại nhé.

Trân trọng,
Thảo — SEONGON
```

---

## Hướng dẫn điền placeholder

| Placeholder | Thay bằng |
|-------------|-----------|
| `{TEN_NGUOI_NHAN}` | Tên người nhận (ví dụ: "Anh Minh", "Chị Hoa") |
| `{TEN_HOP_DONG}` | Tên file hợp đồng hoặc tên khách hàng |
| `{DANH_SACH_LUU_Y}` | Danh sách điểm lưu ý từ skill `hop-dong-tom-tat`, đánh số thứ tự |
| `{LINK_GOOGLE_DOC}` | URL đầy đủ của file Google Doc |

---

## Ví dụ đã điền

**Tiêu đề:** `[SEONGON] Review hợp đồng — Hợp đồng SEO Công ty ABC`

**Nội dung:**
```
Chào Anh Nam,

Chị đã check hợp đồng Hợp đồng SEO Công ty ABC và có một số điểm lưu ý sau:

1. Điều khoản thanh toán (Điều 5): Thời hạn thanh toán 45 ngày kể từ ngày xuất hóa đơn — cần rút ngắn xuống 30 ngày theo chính sách SEONGON.
2. Điều khoản chấm dứt hợp đồng (Điều 8): Hai bên có thể chấm dứt mà không cần lý do với thông báo 30 ngày — rủi ro nếu khách hàng hủy giữa chừng.
3. Phạm vi công việc (Điều 2): Chưa ghi rõ số từ khóa cam kết mỗi tháng — cần bổ sung phụ lục kỹ thuật.

Chị đã comment chi tiết trong hợp đồng theo link dưới đây:
https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms/edit

Bạn vui lòng xem và phản hồi lại nhé.

Trân trọng,
Thảo — SEONGON
```

---

## Lưu ý khi soạn email

- Giọng văn nhã nhặn, rõ ràng, không quá formal
- Danh sách lưu ý: mỗi điểm 1 dòng, ghi rõ điều khoản nào và rủi ro là gì
- Link Google Doc để nguyên URL đầy đủ, không rút gọn
- Không đính kèm file — chỉ share link Google Doc
