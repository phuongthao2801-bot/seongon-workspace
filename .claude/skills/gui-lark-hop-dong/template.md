# Mẫu tin nhắn Lark — SEONGON Review Hợp đồng

> Lark text message KHÔNG hỗ trợ markdown — dùng emoji + ngắt dòng để cấu trúc visual.

## Mẫu chuẩn

```
[SEONGON Review] {TEN_HOP_DONG}

Đã hoàn tất review {TEN_HOP_DONG}, giá trị {GIA_TRI}.

🎯 3 ƯU TIÊN ĐÀM PHÁN TRƯỚC KHI KÝ:

1. {UU_TIEN_1_TIEU_DE} — {DIEU_KHOAN}
   {UU_TIEN_1_NOI_DUNG}

2. {UU_TIEN_2_TIEU_DE} — {DIEU_KHOAN}
   {UU_TIEN_2_NOI_DUNG}

3. {UU_TIEN_3_TIEU_DE} — {DIEU_KHOAN}
   {UU_TIEN_3_NOI_DUNG}

📋 DANH SÁCH {N} ĐIỂM (★ = ưu tiên hàng đầu):
[1] {DIEM_1}
[2] {DIEM_2}
...
[N] {DIEM_N}

📎 BẢN REVIEW Google Doc (có {N} comment + highlight cam):
{LINK_GOOGLE_DOC}

⚠️ Tóm tắt hỗ trợ, không thay thế tư vấn pháp lý. {NEU_CAN_LUAT_SU}
```

## Placeholder

| Placeholder | Thay bằng |
|-------------|-----------|
| `{TEN_HOP_DONG}` | "HĐ 176-PCU/2026/HĐ-SB · SeABank × SEONGON" |
| `{GIA_TRI}` | "378.318.600 VND đã VAT" |
| `{UU_TIEN_X_*}` | 3 ưu tiên hàng đầu — emoji tiêu đề + điều khoản + nội dung ngắn |
| `{N}` | Tổng số điểm lưu ý (vd: 11) |
| `{DIEM_N}` | "Bên A đơn phương đánh giá chất lượng" — kèm ★ nếu thuộc 3 ưu tiên |
| `{LINK_GOOGLE_DOC}` | URL bản review |
| `{NEU_CAN_LUAT_SU}` | "Đề xuất chuyển luật sư SEONGON rà soát thêm trước khi ký" nếu HĐ >500tr hoặc có nhiều rủi ro |

## Ví dụ đã điền (HĐ SeABank 2026-05-21)

```
[SEONGON Review] HĐ 176-PCU/2026/HĐ-SB · SeABank × SEONGON

Đã hoàn tất review Hợp đồng cung cấp Dịch vụ Quảng cáo "Phát triển thương hiệu SeABank trên môi trường số 2026" — giá trị 378.318.600 VND (đã VAT 8%).

🎯 3 ƯU TIÊN ĐÀM PHÁN TRƯỚC KHI KÝ:

1. NÂNG TẠM ỨNG 50tr (13%) → 30% (~113tr) — Điều 3
   Hiện tại 87% giá trị HĐ treo đến cuối dự án. Rủi ro dòng tiền lớn nhất.

2. GIẢM PHẠT VI PHẠM — Điều 8 khoản 1+2
   Hiện tại: 1%/ngày, max 8% + 8% chất lượng (cộng dồn = 16%).
   Đề xuất: 0.5%/ngày + max 5%, KHÔNG cộng dồn.

3. LOẠI TRỪ RỦI RO AI OVERVIEW — Phụ lục 01 Mục 5
   KPI 50% AIO phụ thuộc Google rollout — ngoài tầm SEONGON.

📋 DANH SÁCH 11 ĐIỂM (★ = ưu tiên hàng đầu):
[1] Bên A đơn phương đánh giá chất lượng
[2] Khắc phục 3 ngày quá ngắn
[3] Tạm ứng 50tr (13%) quá thấp ★
[4] Tạm ngừng dịch vụ không bồi thường standby
[5] Xóa toàn bộ dữ liệu trong 3 ngày — mất archive
[6] Phạt 1%/ngày max 8% ★
[7] Phạt chất lượng 8% có thể cộng dồn ★
[8] Lãi chậm thanh toán bất đối xứng
[9] Bên A tự quyết thời hạn khắc phục
[10] KPI AIO 50% rủi ro công nghệ ★
[11] "Tăng trưởng 120% traffic" mơ hồ

📎 BẢN REVIEW Google Doc:
https://docs.google.com/document/d/1KWaxNS_zFQaKB0W-MYQGWHTLt2BmNkQ1aetF6FHDrig/edit

⚠️ Tóm tắt hỗ trợ, không thay thế tư vấn pháp lý. Đề xuất chuyển luật sư SEONGON rà soát thêm trước khi ký.
```

## Lưu ý khi soạn tin Lark

- Giọng văn nhã nhặn, đi thẳng vào vấn đề (tin Lark được đọc nhanh, không phải thư trang trọng)
- Đặt 3 ưu tiên Ở TRÊN danh sách 11 điểm — Sếp đọc 30 giây có thể nắm việc cần làm
- Link Google Doc PHẢI để URL đầy đủ — Lark không tự rút gọn link
- KHÔNG đính kèm file — Lark message text không hỗ trợ; chỉ share link
- Đảm bảo tin <5000 ký tự (Lark giới hạn) — nếu dài hơn, cắt 11 điểm còn 5-7 điểm quan trọng nhất
