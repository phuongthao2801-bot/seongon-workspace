---
name: phan-tich-doi-thu
description: Nhận tên đối thủ, tự động search web và xuất báo cáo phân tích cạnh tranh so với SEONGON
version: 1.1
triggers:
  - "phân tích đối thủ"
  - "nghiên cứu [tên công ty]"
  - "so sánh SEONGON với"
  - "trinh sát đối thủ"
dependencies:
  - doi-thu.md      # Danh sách đối thủ đã biết + lịch sử phân tích — load ở bước 1
  - template.md     # Mẫu báo cáo output — load khi chuẩn bị xuất kết quả
author: SEONGON · Ngô Phương Thảo
---

# Skill: Phân tích Đối thủ cạnh tranh

## Mục đích
Nhận tên đối thủ từ Sếp, tự động search web và tổng hợp báo cáo phân tích cạnh tranh — phục vụ chiến lược marketing của SEONGON.

---

## Các bước thực hiện

### Bước 1 — Xác nhận đối thủ
Hỏi Sếp: *"Sếp muốn phân tích đối thủ nào?"*

> **Load on demand:** Chỉ đọc `doi-thu.md` khi Sếp đã xác nhận tên đối thủ — để kiểm tra xem đối thủ đó đã từng phân tích chưa và lấy dữ liệu nền. Không đọc trước khi biết Sếp cần phân tích ai.
- Nếu đối thủ đã có trong `doi-thu.md` → dùng dữ liệu nền + update thêm từ search mới
- Nếu đối thủ mới → search từ đầu hoàn toàn

### Bước 2 — Search thông tin
Dùng `WebSearch` với 4 từ khóa lần lượt:
1. `[Tên đối thủ] agency marketing dịch vụ Việt Nam`
2. `[Tên đối thủ] bảng giá khách hàng`
3. `[Tên đối thủ] review đánh giá`
4. `[Tên đối thủ] case study portfolio`

Ghi nhận top 5 kết quả mỗi lần search.

### Bước 3 — Fetch website đối thủ
Dùng `WebFetch` vào website chính để lấy:
- Dịch vụ cung cấp (danh sách đầy đủ)
- Phân khúc khách hàng mục tiêu
- Câu định vị / tagline thương hiệu
- Giá (nếu công khai)

### Bước 4 — Phân tích và so sánh
> **Load on demand:** Chỉ đọc `template.md` khi đã thu thập đủ data từ bước 2 và 3. Nếu data quá ít (fetch thất bại, search không ra kết quả) → báo Sếp trước thay vì load template rồi để trống.

So sánh với SEONGON trên các tiêu chí: dịch vụ, phân khúc KH, kênh bán, điểm khác biệt.
Gán mức đe dọa: **Cao** (cùng phân khúc + cùng dịch vụ core) / **Trung bình** / **Thấp**.

### Bước 5 — Xuất báo cáo
Hỏi Sếp: *"Sếp có muốn lưu báo cáo ra file không?"*
- Nếu có → lưu file `phan-tich-[tên đối thủ]-[YYYY-MM-DD].md` trong thư mục hiện tại
- Cập nhật `doi-thu.md`: ghi ngày phân tích + mức đe dọa mới nhất

---

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| WebFetch không vào được website | Website chặn bot | Dùng dữ liệu từ search results, ghi rõ "website không cho phép truy cập" |
| Không tìm thấy thông tin giá | Đối thủ không công khai | Ghi "Không công khai — cần liên hệ trực tiếp" |
| Thông tin search quá cũ (>1 năm) | Đối thủ ít hoạt động online | Ghi rõ năm của thông tin, cảnh báo Sếp có thể đã outdated |
| Nhầm với công ty cùng tên | Tên đối thủ không đặc thù | Hỏi thêm Sếp: *"Đây có phải [URL] không?"* |

---

## Tiêu chí tự kiểm chất lượng

Trước khi gửi báo cáo cho Sếp, agent tự kiểm:
- [ ] Có đủ 5 mục: Tổng quan / Điểm mạnh / Điểm yếu / So sánh với SEONGON / Gợi ý
- [ ] Điểm mạnh và điểm yếu mỗi mục có ít nhất 3 ý (không ghi chung chung)
- [ ] Gợi ý cho SEONGON có ít nhất 2 hành động **cụ thể** (không phải "cải thiện chất lượng")
- [ ] Mức đe dọa được gán rõ ràng với lý do
- [ ] Không có thông tin bịa — nếu thiếu data ghi rõ "không tìm thấy"
- [ ] `doi-thu.md` đã được cập nhật ngày phân tích mới nhất
