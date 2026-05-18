# Template: Báo cáo Trinh sát Đối thủ SEONGON v2.0

> Skill `/phan-tich-doi-thu` xuất file HTML — không dùng markdown template này nữa.
> File này mô tả **cấu trúc 6 trang HTML** để agent tham chiếu khi viết code.

---

## Màu thương hiệu SEONGON (cố định)

| Biến | Mã màu | Tỷ lệ | Dùng cho |
|------|--------|--------|----------|
| `PRIMARY` | `#004aef` | 70% | Header, button, tiêu đề, h2 |
| `LIGHT` | `#0dd1ff` | 20% | Cột SEONGON, border accent, glow |
| `ACCENT` | `#ffce00` | 10% | Timeline tag, dot SEONGON trên map, highlight |
| `DARKER` | `#0035c0` | — | Gradient tối hơn của PRIMARY |

---

## Cấu trúc 6 trang HTML

### Trang 1 — Cover
- Background gradient: `#001a6e → #003ac4 → #004aef`
- Glow trên-phải: `#0dd1ff` · Glow dưới-trái: `#ffce00`
- Tiêu đề: **SEONGON vs. 4 Đối thủ**
- Accent bar: gradient `#ffce00 → #0dd1ff`
- Meta: Phạm vi · Nguồn · Mục tiêu

### Trang 2 — Industry Overview
- Bối cảnh SEONGON (6 ctx-card, border-left `#0dd1ff`)
- Porter's 5 Forces (5 force cards)
- Bảng so sánh tổng quan 4 đối thủ (matrix table)
  - Cột SEONGON header: `#0dd1ff`, background: `#e8f3ff`

### Trang 3 — Competitor Profiles (SEODO + TOS)
- Mỗi đối thủ: 1 comp-card với
  - Header: tên + threat badge + URL
  - USP positioning (in nghiêng)
  - Meta stats (nhân sự, khách hàng, năm)
  - 4Ps grid (2×2)
  - SWOT grid (strengths xanh lá + weaknesses đỏ nhạt)

### Trang 4 — Competitor Profiles (GTV + MONA)
- Cùng format trang 3

### Trang 5 — Quantitative Analysis
- CPM table: 5 CSFs × 5 công ty, rating 1–4, weighted score
  - Cột SEONGON header: `#0dd1ff`, total: `#0dd1ff` text `#001a6e`
- Strategic Group Map (SVG/CSS positioning)
  - Trục X: Giá thấp → cao · Trục Y: Chuyên sâu → Toàn diện
  - Dot SEONGON: `#ffce00`, các dot khác: `#004aef`
  - Blue Ocean zone: viền dashed `#ffce00`

### Trang 6 — Strategy
- SEONGON Moat box: gradient `#004aef → #0035c0`, 4 moat items (2×2 grid)
- 7 đề xuất ERRC (rec-card, border-left `#ffce00`, timeline tag `#ffce00`)
  - ERRC tags: eliminate=đỏ · reduce=vàng · raise=xanh lá · create=xanh dương
- KPI table (12 tháng, giá trị KPI màu `#004aef`)
- Footer note: màu brand + ngày tạo

---

## Output file

```
output/bao-cao-doi-thu-[YYYY-MM-DD].html
```

Mở bằng Chrome → Ctrl+P → Save as PDF để in hoặc chia sẻ.
