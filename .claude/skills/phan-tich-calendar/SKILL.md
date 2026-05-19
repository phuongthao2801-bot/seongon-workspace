---
name: phan-tich-calendar
description: Huấn luyện viên thời gian cá nhân — kéo Lark Calendar theo khoảng tùy chọn, phân loại event theo mục tiêu 2026 của SEONGON, tạo báo cáo HTML/PDF với bar chart, cảnh báo lạc mục tiêu và đề xuất cụ thể tuần tới. Dùng khi Sếp hỏi "phân tích lịch", "soi quỹ thời gian", "tuần tôi làm gì", "thời gian của tôi có đúng mục tiêu không", hoặc gõ /phan-tich-calendar.
---

# Skill: /phan-tich-calendar — Huấn Luyện Viên Thời Gian

Skill phân tích quỹ thời gian của Sếp từ Lark Calendar, đối chiếu với mục tiêu 2026 SEONGON,
xuất báo cáo PDF chuyên nghiệp có bar chart + cảnh báo + đề xuất.

---

## BƯỚC 1 — Đọc hồ sơ (tự động, không hỏi Sếp)

Đọc block `<!-- BEGIN AGENT-BOSS-STARTER -->` trong `~/.claude/CLAUDE.md`.
Ghi nhớ:
- Tên: Ngô Phương Thảo · Chức danh: CCO · Công ty: SEONGON
- Mục tiêu 2026: Doanh thu 50 tỷ | Ký mới SEO 50 tỷ | Tập trung KH >1.000 tỷ/năm
- Dịch vụ: SEO 70% · Ads 30%
- Brand colors SEONGON: PRIMARY #004aef · LIGHT #0dd1ff · ACCENT #ffce00 · DARKER #0035c0

---

## BƯỚC 2 — Hỏi khoảng thời gian (DỪNG đợi Sếp trả lời)

Hỏi chính xác câu sau:

> "Sếp muốn phân tích **KHOẢNG NÀO**? *(Mặc định: 7 ngày qua)*
>
> Gõ: `tuần qua` / `14 ngày` / `tháng qua` / hoặc khoảng cụ thể như `12/5 - 18/5`"

**DỪNG và đợi Sếp trả lời trước khi tiếp tục.**

---

## BƯỚC 3 — Tính khoảng thời gian & kéo calendar

### 3a. Tính timestamps UTC+7

Từ câu trả lời của Sếp, tính `startISO` và `endISO` dạng ISO 8601 với +07:00.

Ví dụ nếu Sếp nói "tuần qua" và hôm nay là 2026-05-18:
- startISO = `2026-05-11T00:00:00+07:00`
- endISO   = `2026-05-18T23:59:59+07:00`

Nếu Sếp nói "14 ngày": lùi 14 ngày từ hôm nay.
Nếu Sếp nói "12/5 - 18/5": parse thành ngày cụ thể trong năm hiện tại.

### 3b. Chạy script kéo data

```bash
cd /Users/phuongthaongo/.lark-mcp && \
node /Users/phuongthaongo/.claude/skills/phan-tich-calendar/scripts/fetch_calendar_range.js \
  "<startISO>" "<endISO>"
```

Script trả về JSON: `{ total, items: [{ id, summary, start, end, recurrence, organizer, self_rsvp, ... }] }`

### 3c. Xử lý timestamps

Mỗi event có `start.timestamp` (Unix seconds, UTC) hoặc `start.date` (all-day).
Đổi sang giờ UTC+7: cộng 25200 giây rồi tính ngày/giờ.

**Bỏ qua** events có `self_rsvp = "decline"` khi tính giờ (vẫn liệt kê trong bảng).

**Xử lý events chồng chéo (overlap):**
- Nếu nhiều events cùng giờ → tính max time block (không cộng 2 lần)
- Ghi chú overlap trong bảng event log

**Xử lý recurring events (`_0` suffix):**
- API trả về base event với timestamp gốc (có thể rất cũ)
- Tìm giờ xảy ra trong tuần bằng cách: `base_start_time mod 86400` = giờ trong ngày
- Áp dụng giờ đó vào ngày đúng trong tuần (dựa vào BYDAY trong recurrence)

---

## BƯỚC 4 — Phân loại events thành 6 nhóm

Dựa vào tên event, organizer, và mục tiêu SEONGON 2026:

| Nhóm | Màu | Mô tả | Gắn mục tiêu |
|------|-----|-------|-------------|
| 🚀 GEO & Sản phẩm mới | #004aef | Checkin GEO, webinar, ra mắt sp, đào tạo BD về GEO | ✅ GEO/SEO 37 tỷ |
| 💰 Sales & Ký mới | #ffce00 (text #5c4400) | Review SAL, gặp KH, pitch, follow deal | ✅ Ký mới 50 tỷ |
| 📣 Marketing & Thương hiệu | #0dd1ff | Định vị, OKRs Marketing, Checkin Marketing | ✓ Hỗ trợ |
| 🏗️ Phát triển đội ngũ | #22b573 | ĐTNB, Claude Code, HR Review, đào tạo nội bộ | ✓ Hỗ trợ |
| ⚙️ Vận hành & OKRs | #8894b0 | Review OKRs, Checkin PM, họp định kỳ | Trung tính |
| 🎉 Sự kiện / Cá nhân / Khác | #ffce00 (text: #5c4400) | WAS, văn hóa, sport, giảng dạy bên ngoài | Trung tính |

**Quy tắc phân loại:**
- Event có "SAL", "Sales", "ký mới", "pitch", "KH", "deal" → Sales
- Event có "GEO", "webinar GEO", "ra mắt", "BD" kèm "GEO" → GEO/Sản phẩm
- Event có "Marketing", "định vị", "thương hiệu" → Marketing
- Event có "ĐTNB", "Claude Code", "HR", "Performance review", "training" → Đội ngũ
- Event có "OKRs", "Checkin PM", "Review dự án" → Vận hành
- Còn lại → Sự kiện/Khác

**Event không rõ** → nhóm "Cần Sếp làm rõ" (nếu có ≥3 event không rõ)

---

## BƯỚC 5 — Tạo file HTML báo cáo

```bash
mkdir -p /tmp/abs8
```

Tạo file `/tmp/abs8/report.html` với cấu trúc sau:

### Nội dung bắt buộc:

**(1) HEADER** — gradient #004aef→#0035c0, góc tròn 12px:
- Tiêu đề: "🔍 Soi Quỹ Thời Gian"
- Sub: "Ngô Phương Thảo (Bơ) · CCO – SEONGON · Phân tích từ Lark Calendar"
- Badge vàng #ffce00 (text #004aef): "SEONGON"
- Stats: Tổng giờ | Số events | Events declined | % Align mục tiêu 2026
- Badge khoảng phân tích: "📅 11/05 – 18/05/2026" (màu #0dd1ff)

**(2) BAR CHART NGANG** — dùng `<div>` + `width: X%`:
- Mỗi nhóm: label (230px) + bar track (flex:1) + số giờ (70px)
- Bar fill dùng màu nhóm, border-radius 6px, hiển thị "Xh · Y%"
- Nhóm nhiều giờ nhất: gradient #0035c0→#004aef (DARKER→PRIMARY) + glow xanh + badge "⚠ NHIỀU NHẤT"
- Nhóm gắn mục tiêu: badge xanh "✓ MỤC TIÊU 2026"
- Nhóm Sales thấp: badge vàng #ffce00 (text #5c4400) "⚠ THIẾU"

**(3) ĐIỂM SOI NỔI BẬT** — 3 box (2-col grid, box thứ 3 full-width):
- Box 1 (✅): Điểm tốt — nhóm gắn mục tiêu được đầu tư đúng
- Box 2 (⚠️): Cảnh báo nhẹ — nhóm quan trọng đang thiếu giờ
- Box 3 (🚨): Cảnh báo nặng nhất — tên event cụ thể + số giờ cụ thể

**(4) 3 CẢNH BÁO LẠC MỤC TIÊU** — card với border-left #ffce00, bg #fffbdc:
- Mỗi cảnh báo: số thứ tự (circle #ffce00, text #004aef) + tiêu đề #0035c0 + mô tả chi tiết
- PHẢI dùng tên event thật, số giờ thật, gắn với mục tiêu 50 tỷ

**(5) 3 ĐỀ XUẤT TUẦN TỚI** — card với border-left xanh #004aef:
- Mỗi đề xuất: số thứ tự (circle xanh) + việc cụ thể + số giờ ước tính
- Badge suggest-tag (xanh đậm) hiển thị "+Xh" hoặc tên nhóm gắn mục tiêu

**(6) BẢNG EVENT LOG** — đầy đủ, có cột: Ngày | Tên | Giờ | Thời lượng | Nhóm | RSVP
- Decline: chữ đỏ "✗ Decline"
- Accept: chữ xanh "✓ Accept"
- Mời (needs_action/none): chữ xám "Mời"
- Màu dot theo nhóm

**(7) FOOTER** — note nguồn data + "⚡ Agent Boss Starter · SEONGON 2026"

### CSS quan trọng:
- Width: 794px (A4), background: #fff, padding: 36px 40px
- Font: Segoe UI / Arial, base 13px
- PRIMARY: #004aef | DARKER: #0035c0 | LIGHT: #0dd1ff | ACCENT: #ffce00 (text trên nền vàng: #5c4400 hoặc #004aef)

---

## BƯỚC 6 — Convert sang PDF và mở

```bash
PDF_SAFE_NAME="Soi_quy_thoi_gian_tuan$(date +%V).pdf"
PDF="$HOME/Desktop/$PDF_SAFE_NAME"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="$PDF" --print-to-pdf-no-header \
  "file:///tmp/abs8/report.html" 2>&1
open "$PDF"
```

> **Lưu ý tên file:** Dùng tên không có dấu/khoảng trắng để tránh lỗi shell.

---

## BƯỚC 7 — Báo Sếp (ngắn gọn)

Trả lời theo template:

```
PDF đã mở trên Desktop ✅

📊 Tóm tắt tuần [ngày] – [ngày]:
• Tổng giờ phân tích: **Xh** (N events)
• Nhóm chiếm nhiều nhất: [tên nhóm] — Xh (Y%)
• Cảnh báo nặng nhất: [1 câu ngắn cụ thể]

3 việc cần làm tuần tới: [liệt kê bullet ngắn]
```

---

## Xử lý lỗi

| Lỗi | Cách xử lý |
|-----|-----------|
| Token hết hạn | Báo Sếp chạy: `/Users/phuongthaongo/.lark-mcp/node_modules/.bin/lark-mcp login -a cli_aa8b214cceb81eef -s BPfivof5HSoPAmCPFYF2AhRqwdc1oJmV -d https://open.larksuite.com` |
| 0 events returned | Kiểm tra lại khoảng thời gian — có thể Sếp đang không có lịch trên calendar này |
| Script lỗi path | Đảm bảo chạy từ `/Users/phuongthaongo/.lark-mcp` |
| Chrome headless lỗi | Fallback: chỉ tạo HTML, báo Sếp mở file `file:///tmp/abs8/report.html` bằng Chrome |

---

## Nguyên tắc bất biến

- **KHÔNG bịa events** — chỉ dùng data thật từ Lark
- **KHÔNG phán xét** việc cá nhân — chỉ soi % align với mục tiêu Sếp đã đặt
- **Cảnh báo và đề xuất PHẢI** gắn trực tiếp với mục tiêu 2026: 50 tỷ doanh thu, ký mới SEO 50 tỷ, KH Ưu tiên 1
- Tiếng Việt · Xưng "tôi" · Gọi "Sếp Thảo" hoặc "Sếp"
- Script node.js chạy từ thư mục `/Users/phuongthaongo/.lark-mcp` (vì cần `node_modules/keytar`)
