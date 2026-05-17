# Skill: Đọc Gmail & Tóm tắt email quan trọng

## Mục đích
Đọc Gmail của Sếp, lọc email quan trọng trong ngày/tuần và tóm tắt thành bản tin gọn gàng.

## Khi nào dùng
Khi Sếp gõ: "đọc gmail", "tóm tắt email hôm nay", "có email quan trọng nào không"

## Các bước thực hiện

### Bước 1 — Tìm email chưa đọc / quan trọng
Dùng Gmail MCP tool `search_threads` để tìm:
- Email chưa đọc trong 24 giờ qua
- Email từ khách hàng, đối tác (ưu tiên)
- Email có từ khóa: hợp đồng, báo giá, khiếu nại, thanh toán

### Bước 2 — Đọc nội dung từng email
Dùng `get_thread` để lấy nội dung chi tiết top 5-10 email quan trọng nhất.

### Bước 3 — Tóm tắt và phân loại
Phân loại theo mức độ:
- 🔴 **Cần xử lý ngay** (khách hàng chờ phản hồi, deadline)
- 🟡 **Cần xử lý hôm nay** (báo giá, meeting request)
- 🟢 **Đọc khi rảnh** (newsletter, thông báo chung)

### Bước 4 — Xuất báo cáo
Trả lời Sếp theo format:

```
📬 BẢN TIN EMAIL — [Ngày]
SEONGON · [Tên CEO]

🔴 CẦN XỬ LÝ NGAY (N email)
1. [Người gửi] — [Chủ đề] → [1 câu tóm tắt + action cần làm]

🟡 CẦN XỬ LÝ HÔM NAY (N email)
...

🟢 ĐỌC KHI RẢNH (N email)
...

💡 Gợi ý: [1-2 việc Sếp nên làm trước tiên]
```

## Lưu ý
- Không đọc email cá nhân/nhạy cảm trừ khi Sếp yêu cầu rõ ràng
- Cần kết nối MCP Gmail trước khi dùng skill này
- Nếu chưa kết nối: nhắc Sếp vào Settings → MCP → bật Gmail
