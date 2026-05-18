---
name: phan-tich-doi-thu
description: Tự động nghiên cứu 4 đối thủ của SEONGON và xuất báo cáo HTML chuyên nghiệp theo chuẩn quốc tế (Porter + 4Ps + CPM + SWOT + ERRC)
version: 2.0
triggers:
  - "phân tích đối thủ"
  - "trinh sát đối thủ"
  - "báo cáo cạnh tranh"
  - "so sánh đối thủ"
  - "phan-tich-doi-thu"
dependencies:
  - doi-thu.md      # URL và thông tin nền 4 đối thủ — load ở bước 2
  - output/         # File HTML báo cáo lưu tại đây
author: SEONGON · Ngô Phương Thảo
---

# Skill: Phân tích Đối thủ cạnh tranh SEONGON

## Mục đích
Tự động **nghiên cứu 4 đối thủ cạnh tranh của SEONGON** và xuất ra **báo cáo HTML chuyên nghiệp** theo chuẩn quốc tế — như thuê một analyst làm báo cáo. Không cần Sếp chỉ định gì thêm, skill tự chạy toàn bộ.

---

## Các bước thực hiện

### Bước 1 — Lấy brand kit từ website SEONGON

Dùng `WebFetch` vào `https://thaoseongon.com` để lấy màu thương hiệu:

```bash
grep -oE "#[0-9a-fA-F]{6}" site.html \
  | tr 'A-F' 'a-f' \
  | grep -viE "^#(ffffff|000000|f4f4f4|f0f0f0|fafafa|eeeeee|cccccc|999999|333333|111111|222222)$" \
  | sort | uniq -c | sort -rn | head -3
```

- Lấy màu phổ biến nhất làm `PRIMARY_COLOR`
- Sinh `PRIMARY_DARKER` (giảm brightness ~25%)
- Màu thứ 2 làm `PRIMARY_ACCENT` (nếu không có → dùng `#ff2b80`)
- **Màu thương hiệu SEONGON (cố định):** PRIMARY `#004aef` (70%) · LIGHT `#0dd1ff` (20%) · ACCENT `#ffce00` (10%)

### Bước 2 — Load danh sách 4 đối thủ

> **Load on demand:** Đọc `doi-thu.md` để lấy URL chính xác của từng đối thủ.

4 đối thủ cố định:
1. **SEODO** — https://seodo.vn
2. **TOS (TopOnSeek)** — https://www.toponseek.com
3. **GTV** — https://gtvseo.com
4. **MONA** — https://mona.media

### Bước 3 — WebFetch sâu từng đối thủ (thu thập 8 chỉ số)

Với **MỖI đối thủ**, dùng `WebFetch` URL chính và thu thập đầy đủ **8 fields** theo chuẩn 4Ps + bổ sung:

**Theo 4Ps Marketing Mix:**
1. **Product** — Dịch vụ/sản phẩm chính + danh mục đầy đủ
2. **Price** — Mô hình giá (project/retainer/gói), mức giá nếu công khai
3. **Place** — Kênh phân phối (website, sàn, đại lý, sales team, online/offline)
4. **Promotion** — Kênh marketing chủ lực + thông điệp brand chính

**Bổ sung 4 fields:**
5. **Target Customer** — Phân khúc cụ thể (B2B/B2C, ngành, quy mô doanh nghiệp)
6. **Scale / Snapshot** — Quy mô (số nhân viên ước tính, năm thành lập, số khách hàng nếu có)
7. **USP / Positioning** — Câu định vị trên website (trích nguyên văn 1 câu)
8. **Customer Reputation** — Review/báo chí/case study (nếu fetch được)

Sau đó lập **SWOT cô đọng** cho mỗi đối thủ:
- 3 Strengths (điểm mạnh so với SEONGON)
- 3 Weaknesses (điểm yếu — cơ hội cho SEONGON)

Ghi nhận data thật. Nếu fetch thất bại → dùng data từ search results, ghi rõ "nguồn: search".

### Bước 4 — Phân tích định lượng

**4a. Competitive Profile Matrix (CPM)**

Xác định 5 Critical Success Factors (CSFs) phù hợp ngành Agency Marketing VN:
- Brand recognition (uy tín thương hiệu)
- Service quality (chất lượng dịch vụ)
- Pricing competitiveness (cạnh tranh về giá)
- Client portfolio (danh mục khách hàng)
- Team expertise (chuyên môn đội ngũ)

Mỗi CSF gán weight 0.1–1.0 (tổng = 1.0). Chấm rating 1–4 cho SEONGON + 4 đối thủ. Tính weighted score.

**4b. Porter's 5 Forces — ngành Agency Marketing VN**

Đánh giá 5 lực:
- Đối thủ hiện tại (Cao/Trung/Thấp + 1 dòng lý do)
- Đối thủ mới gia nhập
- Sức mạnh nhà cung cấp
- Sức mạnh khách hàng
- Sản phẩm/dịch vụ thay thế

**4c. Strategic Group Map**

Trục X: Giá (Thấp → Cao), Trục Y: Phạm vi dịch vụ (Chuyên sâu → Toàn diện).
Đặt SEONGON + 4 đối thủ lên 2D map. Đánh dấu khoảng trống Blue Ocean nếu có.

**4d. Threat Level từng đối thủ**
- **Cao** = cùng phân khúc KH + cùng dịch vụ core
- **Trung bình** = khác phân khúc hoặc khác dịch vụ
- **Thấp** = khác cả hai

### Bước 5 — Phân tích SEONGON's Moat + ERRC

**SEONGON Moat** — Tìm 3–4 lợi thế phòng thủ DUY NHẤT từ hồ sơ:
- Đội ngũ chất lượng cao
- Văn hóa doanh nghiệp nổi bật
- Tập khách hàng đa dạng & có thương hiệu

**7 Đề xuất chiến lược** theo ERRC Framework:
- **Eliminate** — yếu tố ngành đang làm mà SEONGON nên bỏ
- **Reduce** — yếu tố nên giảm xuống dưới mức ngành
- **Raise** — yếu tố nên nâng lên trên mức ngành
- **Create** — yếu tố mới mà ngành chưa có

Mỗi đề xuất có: tiêu đề + mô tả + timeline thực hiện.

### Bước 6 — Tạo báo cáo HTML chuyên nghiệp

Viết file `output/bao-cao-doi-thu-[YYYY-MM-DD].html` với cấu trúc **6 trang**:

```
Trang 1 — Cover: Brand color SEONGON + tiêu đề + meta
Trang 2 — Industry Overview: Porter 5 Forces + Bảng matrix 4 đối thủ
Trang 3–4 — Competitor Profiles: Mỗi đối thủ 1 card (4Ps + SWOT + Threat)
Trang 5 — Quantitative: CPM weighted score + Strategic Group Map
Trang 6 — Strategy: SEONGON Moat + 7 đề xuất ERRC + KPI 12 tháng
```

Dùng màu thương hiệu SEONGON đã lấy ở Bước 1. Font Inter từ Google Fonts. Thiết kế đủ đẹp để in hoặc share với team.

Sau khi lưu HTML → thông báo đường dẫn file cho Sếp.

---

## Framework áp dụng

| Framework | Mục đích |
|-----------|----------|
| **Porter's 5 Forces** (HBR 1979) | Phân tích lực ngành Agency Marketing VN |
| **4Ps Marketing Mix** (McCarthy) | So sánh Product/Price/Place/Promotion |
| **CPM — Competitive Profile Matrix** (Fred David) | Chấm điểm có trọng số, xác định ai mạnh nhất |
| **Strategic Group Map** (Porter) | Vẽ bản đồ vị trí cạnh tranh 2D |
| **SWOT** | Điểm mạnh/yếu từng đối thủ |
| **Blue Ocean ERRC** (Kim & Mauborgne) | Tìm khoảng trống thị trường + đề xuất chiến lược |

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| WebFetch bị chặn (403/timeout) | Website chặn crawler | Dùng dữ liệu từ WebSearch, ghi "nguồn: search" |
| Màu SEONGON fetch thất bại | seongon.com chặn hoặc lỗi | Dùng fallback `#0066cc` / `#004a99` / `#ff6600` |
| Không tìm thấy thông tin giá | Đối thủ không công khai | Ghi "Không công khai — báo giá theo yêu cầu" |
| Thông tin quá cũ (>1 năm) | Đối thủ ít update website | Ghi rõ năm thông tin, cảnh báo Sếp có thể outdated |
| File HTML quá lớn | Nhiều data + CSS inline | Vẫn xuất, ghi chú "file nặng, mở bằng Chrome" |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi báo cáo cho Sếp, agent tự kiểm:
- [ ] Màu brand SEONGON đã áp dụng đúng trong HTML (không dùng màu ngẫu nhiên)
- [ ] Đủ 4 đối thủ được phân tích (SEODO, TOS, GTV, MONA)
- [ ] Mỗi đối thủ có đủ 8 fields + SWOT 3+3
- [ ] CPM table có đủ 5 CSFs + trọng số tổng = 1.0
- [ ] Porter 5 Forces có đủ 5 lực, mỗi lực có mức + lý do
- [ ] Có ít nhất 7 đề xuất chiến lược với ERRC tag
- [ ] File HTML đã lưu vào `output/bao-cao-doi-thu-[YYYY-MM-DD].html`
- [ ] Không có số liệu bịa — thiếu data ghi rõ "không tìm thấy"
