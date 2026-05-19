# Template: Báo cáo Soi Quỹ Thời Gian — phan-tich-calendar

> Skill `/phan-tich-calendar` xuất file **PDF** (qua HTML → Chrome headless).
> File này mô tả cấu trúc 7 block báo cáo để agent tham chiếu khi viết HTML.

---

## Màu thương hiệu SEONGON (cố định)

| Biến | Mã màu | Tỷ lệ | Dùng cho |
|------|--------|--------|----------|
| `PRIMARY` | `#004aef` | 70% | Header gradient, circle số, border |
| `LIGHT` | `#0dd1ff` | 20% | Badge khoảng thời gian, đề xuất |
| `ACCENT` | `#ffce00` | 10% | Cảnh báo, badge Sales thấp, số thứ tự cảnh báo |
| `DARKER` | `#0035c0` | — | Gradient tối header + bar nhiều nhất |

---

## Cấu trúc HTML báo cáo (794px — A4)

### Block 1 — Header
- Gradient: `#004aef → #0035c0`, border-radius 12px
- Tiêu đề: `🔍 Soi Quỹ Thời Gian`
- Sub: `Ngô Phương Thảo (CCO) · SEONGON · Phân tích từ Lark Calendar`
- Badge vàng `#ffce00` (text `#004aef`): `SEONGON`
- 4 stat box: Tổng giờ | Số events | Events declined | % Align mục tiêu 2026
- Badge khoảng: `📅 [DD/MM] – [DD/MM/YYYY]` màu `#0dd1ff`

### Block 2 — Bar Chart Ngang (6 nhóm)
```
🚀 GEO & Sản phẩm mới     ████████████░░░░  Xh · Y%   [✓ MỤC TIÊU 2026]
💰 Sales & Ký mới          ██░░░░░░░░░░░░░░  Xh · Y%   [⚠ THIẾU]
📣 Marketing & Thương hiệu ████░░░░░░░░░░░░  Xh · Y%
🏗️ Phát triển đội ngũ     ██████░░░░░░░░░░  Xh · Y%
⚙️ Vận hành & OKRs        ████████████████  Xh · Y%   [⚠ NHIỀU NHẤT]
🎉 Sự kiện / Cá nhân      ███░░░░░░░░░░░░░  Xh · Y%
```
- Bar fill màu theo nhóm, border-radius 6px
- Nhóm nhiều nhất: gradient `#0035c0→#004aef` + badge đỏ `⚠ NHIỀU NHẤT`
- Nhóm gắn mục tiêu: badge xanh `✓ MỤC TIÊU 2026`
- Sales thấp: badge vàng `⚠ THIẾU`

### Block 3 — Điểm Soi Nổi Bật (3 box)
- Box 1 ✅ (viền xanh): Điểm tốt — nhóm đang đầu tư đúng
- Box 2 ⚠️ (viền vàng): Cảnh báo nhẹ — nhóm thiếu giờ
- Box 3 🚨 (viền đỏ, full-width): Cảnh báo nặng — tên event cụ thể + số giờ

### Block 4 — 3 Cảnh Báo Lạc Mục Tiêu
- Card: border-left `#ffce00`, bg `#fffbdc`
- Số thứ tự: circle `#ffce00`, text `#004aef`
- Tiêu đề: `#0035c0`, bold
- Nội dung: tên event thật + số giờ thật + gắn mục tiêu 50 tỷ

### Block 5 — 3 Đề Xuất Tuần Tới
- Card: border-left `#004aef`, bg `#f0f5ff`
- Số thứ tự: circle `#004aef`, text white
- Badge `+Xh` màu `#0dd1ff`
- Nội dung: việc cụ thể + số giờ ước tính

### Block 6 — Bảng Event Log (đầy đủ)
| Cột | Mô tả |
|-----|-------|
| Ngày | DD/MM, thứ tiếng Việt |
| Tên event | Tên gốc từ Lark |
| Giờ | HH:MM – HH:MM |
| Thời lượng | Xh Ym |
| Nhóm | Dot màu + tên nhóm |
| RSVP | ✓ Accept (xanh) / ✗ Decline (đỏ) / Mời (xám) |

### Block 7 — Footer
- Note nguồn: `Nguồn: Lark Calendar · [khoảng ngày]`
- Watermark: `⚡ Skill /phan-tich-calendar · SEONGON 2026`

---

## Output file

```
output/soi-quy-thoi-gian-[YYYY-MM-DD].html   ← HTML tạm
~/Desktop/Soi_quy_thoi_gian_tuan[N].pdf      ← PDF final (mở ngay)
```

Mở HTML bằng Chrome → Ctrl+P → Save as PDF nếu Chrome headless lỗi.

---

## 6 Nhóm phân loại & màu sắc

| Nhóm | Màu | Từ khóa nhận diện |
|------|-----|-------------------|
| 🚀 GEO & Sản phẩm mới | `#004aef` | GEO, webinar, ra mắt, BD+GEO |
| 💰 Sales & Ký mới | `#ffce00` (text `#5c4400`) | SAL, Sales, ký mới, pitch, KH, deal |
| 📣 Marketing & Thương hiệu | `#0dd1ff` | Marketing, định vị, thương hiệu |
| 🏗️ Phát triển đội ngũ | `#22b573` | ĐTNB, Claude Code, HR, training |
| ⚙️ Vận hành & OKRs | `#8894b0` | OKRs, Checkin PM, Review dự án |
| 🎉 Sự kiện / Cá nhân | `#ffce00` (text `#5c4400`) | WAS, văn hóa, sport, giảng dạy |
