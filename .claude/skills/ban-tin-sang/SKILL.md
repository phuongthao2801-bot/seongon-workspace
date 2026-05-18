---
name: ban-tin-sang
description: Đọc Gmail + cào tin tức từ Cafef, The Leader, Brandsvietnam và tóm tắt thành bản tin buổi sáng phù hợp với ngành Marketing và SEONGON
version: 1.0
triggers:
  - "bản tin sáng"
  - "tin tức hôm nay"
  - "đọc tin"
  - "có gì mới không"
  - "ban-tin-sang"
dependencies:
  - nguon-tin.md      # Danh sách URL các nguồn tin + từ khóa lọc — load trước bước fetch
  - keywords.md       # Từ khóa lọc email quan trọng — load on demand nếu Sếp không chỉ định
  - template.md       # Mẫu bản tin output — load on demand lần đầu chạy
  - output/           # Thư mục lưu bản tin theo ngày
requires_mcp: gmail
author: SEONGON · Ngô Phương Thảo
---

# Skill: Bản tin sáng — Gmail + Tin tức ngành

## Mục đích
Tổng hợp bản tin buổi sáng gồm 2 phần: **(1) Email quan trọng trong Gmail** và **(2) Tin tức ngành Marketing từ Cafef, The Leader, Brandsvietnam** — lọc những gì liên quan trực tiếp đến SEONGON và ngành Digital Marketing.

---

## Các bước thực hiện

### Bước 1 — Kiểm tra kết nối Gmail MCP
Gọi `search_threads` với query đơn giản để kiểm tra kết nối.
- Lỗi → báo Sếp bật Gmail MCP, nhưng **vẫn tiếp tục** phần tin tức (bước 3)
- OK → tiếp tục bình thường

### Bước 2 — Đọc Gmail
> **Load on demand:** Chỉ đọc `keywords.md` nếu Sếp không chỉ định loại email cần lọc.

Dùng `search_threads` với query: `is:unread newer_than:1d`, lấy tối đa 20 email.
Dùng `get_thread` để đọc chi tiết top 5 email quan trọng nhất.
Phân loại:
- 🔴 Cần xử lý ngay — khách hàng chờ, deadline, khiếu nại
- 🟡 Cần xử lý hôm nay — báo giá, meeting, phản hồi đối tác
- 🟢 Đọc khi rảnh — newsletter, thông báo chung

### Bước 3 — Load danh sách nguồn tin
> **Load on demand:** Đọc `nguon-tin.md` để lấy URL và từ khóa lọc của từng nguồn.

### Bước 4 — Fetch tin tức từ 3 nguồn
Dùng `WebFetch` song song 3 nguồn:
- **Cafef:** https://cafef.vn/marketing.chn
- **The Leader:** https://theleader.vn
- **Brandsvietnam:** https://www.brandsvietnam.com

Với mỗi nguồn, lấy **top 5 bài mới nhất** trong 24h qua.

### Bước 5 — Lọc tin liên quan đến SEONGON
Chỉ giữ lại bài viết có liên quan đến ít nhất 1 trong các chủ đề:
- Digital Marketing, SEO, Performance Marketing, Content Marketing
- Agency, quảng cáo, thương hiệu, branding
- Doanh nghiệp vừa & lớn tại Việt Nam
- AI trong marketing, xu hướng công nghệ marketing
- Đối thủ: SEODO, TOS, GTV, MONA (nếu có tin)

Bỏ qua: chứng khoán, bất động sản, thể thao, giải trí (trừ khi có góc marketing).

### Bước 6 — Tổng hợp và xuất bản tin
> **Load on demand:** Chỉ đọc `template.md` nếu là lần đầu chạy skill này.

Xuất bản tin theo format chuẩn gồm 2 phần: Email + Tin tức.
Lưu file vào `output/ban-tin-sang-[YYYY-MM-DD].md`.

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| Gmail MCP không kết nối | MCP chưa bật | Vẫn chạy phần tin tức, ghi chú "Gmail không khả dụng" |
| WebFetch bị chặn (403/bot detection) | Trang chặn crawler | Thử URL trang chủ thay vì category page, ghi "không lấy được tin từ [nguồn]" |
| Không có tin liên quan trong 24h | Ngày ít tin ngành | Mở rộng sang 48h, ghi rõ "(tin từ 2 ngày qua)" |
| Quá nhiều tin (>20 bài) | Nhiều nguồn active | Ưu tiên theo thứ tự: Brandsvietnam → The Leader → Cafef |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi bản tin, agent tự kiểm:
- [ ] Phần Email: đủ 3 nhóm 🔴🟡🟢, mỗi email có action cụ thể
- [ ] Phần Tin tức: có ít nhất 3 bài liên quan ngành Marketing
- [ ] Không có tin chứng khoán/BĐS/giải trí lọt vào bản tin
- [ ] Mỗi tin có: tiêu đề + nguồn + 1 câu tóm tắt + lý do liên quan SEONGON
- [ ] File output đã lưu đúng tên `ban-tin-sang-[YYYY-MM-DD].md`
- [ ] Tổng bản tin đọc không quá 3 phút (khoảng 400–600 từ)
