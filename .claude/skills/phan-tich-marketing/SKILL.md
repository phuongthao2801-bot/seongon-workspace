---
name: phan-tich-marketing
description: Nghiên cứu và so sánh hiệu quả kênh truyền thông marketing của SEONGON với các đối thủ (TOS, MONA, SEODO, GTVSEO) — Website/Blog, Facebook, YouTube, LinkedIn, PR báo chí, Giải thưởng quốc tế. Đánh giá số lượng lẫn chất lượng. Xuất báo cáo PDF chuyên nghiệp có biểu đồ, ma trận cạnh tranh, màu thương hiệu SEONGON.
version: 1.1
triggers:
  - "phân tích kênh marketing"
  - "so sánh kênh truyền thông"
  - "đối thủ đang làm gì trên mạng"
  - "SEONGON so với TOS"
  - "report marketing"
  - "phan-tich-marketing"
author: SEONGON · Ngô Phương Thảo
---

# Skill: Phân Tích Kênh Truyền Thông Marketing

## Mục đích

Nghiên cứu thực tế, so sánh toàn diện **6 kênh truyền thông** của SEONGON và 4 đối thủ cạnh tranh, rồi xuất thành **báo cáo PDF chuyên nghiệp** có biểu đồ và ma trận cạnh tranh — màu thương hiệu SEONGON xuyên suốt.

---

## Màu sắc thương hiệu SEONGON (cố định — không fetch website)

| Biến | Mã màu | Dùng cho |
|------|--------|----------|
| `PRIMARY` | `#004aef` | Header, button, tiêu đề chính |
| `LIGHT` | `#0dd1ff` | Accent phụ, highlight, border |
| `ACCENT` | `#ffce00` | Điểm nhấn, badge, viền cột SEONGON |
| `DARKER` | `#0035c0` | Gradient tối, cover page |

---

## Các công ty nghiên cứu

| Công ty | Website | Fanpage |
|---------|---------|---------|
| SEONGON | seongon.com | facebook.com/seongonvietnam |
| TOS | toponseek.com | facebook.com/TopOnSeekCom |
| MONA | mona.media | facebook.com/thietkewebsitemonamedia |
| SEODO | seodo.vn | facebook.com/seodo |
| GTVSEO | gtvseo.com | facebook.com/gtvseo |

---

## Bước 1 — Thu thập dữ liệu song song

Spawn 3 agent hoặc chạy search song song để tiết kiệm thời gian. Với mỗi công ty, thu thập:

### 1a. Website & Blog
- Fetch trang chủ và trang blog/kiến thức
- Đếm số bài viết (hoặc ước tính từ pagination)
- Đánh giá: chất lượng nội dung, case study có số liệu, portfolio KH lớn, CTA, UX

### 1b. Mạng xã hội
**Facebook:**
```
Search: "[tên công ty] fanpage followers"
```
Ghi: số followers, "talking about" nếu có, tần suất đăng, loại nội dung chủ yếu

**YouTube:**
```
Search: "[tên công ty] youtube subscribers channel"
```
Ghi: số subscribers, số video, chất lượng, có CEO cá nhân không

**LinkedIn:**
```
Search: "[tên công ty] linkedin company followers"
```
Ghi: số followers, chất lượng B2B, có CEO thought leadership không

### 1c. PR & Giải thưởng
**PR báo chí:**
```
Search: "[tên công ty] site:cafef.vn OR site:brandsvietnam.com OR site:vnexpress.net"
```
Đánh giá: tần suất xuất hiện, CEO có được quote không, có bài editorial hay chỉ community

**Giải thưởng quốc tế:**
```
Search: "[tên công ty] award winner finalist global 2024 2025 2026"
```
Ghi rõ: tên giải, hạng mục, **Winner hay chỉ Shortlist/Finalist** (hai loại này khác nhau)

> ⚠️ **Độ chính xác dữ liệu — 3 mức bắt buộc:**
> - ✅ **Đã xác nhận** — có URL nguồn cụ thể
> - ⚠️ **Ước tính** — dựa trên tín hiệu gián tiếp, ghi rõ "ước tính"
> - ❓ **Chưa xác nhận** — không bịa số, ghi "chưa xác nhận"

---

## Bước 2 — Chấm điểm cạnh tranh

Sau khi có dữ liệu, chấm điểm **1–5** cho từng kênh × từng công ty:

| Điểm | Ý nghĩa |
|------|---------|
| 5 | Tốt nhất trong nhóm |
| 4 | Tốt, trên trung bình |
| 3 | Trung bình |
| 2 | Yếu |
| 1 | Rất yếu / bỏ ngỏ |

**8 chiều đánh giá:** Website/Blog · Facebook · YouTube · LinkedIn · PR/Báo chí · Giải thưởng QT · Case Study · CEO Brand

---

## Bước 3 — Tạo báo cáo PDF

Quy trình 2 giai đoạn: **(A) Generate biểu đồ PNG** → **(B) Build PDF từ HTML + PNG → convert**

---

### 3A. Kiểm tra công cụ convert (chạy trước)

```bash
# Ưu tiên 1: wkhtmltopdf (hỗ trợ JS, gradient đẹp nhất)
which wkhtmltopdf

# Ưu tiên 2: WeasyPrint (Python, không cần cài thêm nếu đã có pip)
python3 -c "import weasyprint; print('ok')" 2>/dev/null || pip3 install weasyprint --quiet
```

Dùng công cụ nào available trước. Nếu cả hai đều thiếu → cài WeasyPrint.

---

### 3B. Generate biểu đồ bằng matplotlib (PNG)

WeasyPrint không chạy JavaScript, nên cần pre-render chart thành ảnh PNG trước.

```python
# Cài nếu chưa có
# pip3 install matplotlib numpy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Màu 5 công ty (nhất quán xuyên suốt)
COLORS = {
    'SEONGON': '#004aef',
    'TOS':     '#e53e3e',
    'MONA':    '#dd6b20',
    'SEODO':   '#38a169',
    'GTVSEO':  '#805ad5',
}
companies = list(COLORS.keys())
bar_colors = list(COLORS.values())

out_dir = '.'  # thay bằng thư mục làm việc nếu cần

def save_bar(filename, title, values, ylabel=''):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.bar(companies, values, color=bar_colors, width=0.55, zorder=3)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                f'{val:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, filename), dpi=150, bbox_inches='tight')
    plt.close()

# Bar charts (điền số liệu thực tế từ Bước 1)
save_bar('chart_facebook.png',  'Facebook Followers',    [22000, 859, 13895, 13000, 18897])
save_bar('chart_linkedin.png',  'LinkedIn Followers',    [938, 464, 505, 362, 443])
save_bar('chart_blog.png',      'Số bài Blog',           [500, 150, 1400, 286, 99])
save_bar('chart_youtube.png',   'YouTube Subscribers',   [3000, 500, 2000, 2500, 106000])

# Radar chart
dimensions = ['Website\n/Blog','Facebook','YouTube','LinkedIn','PR\n/Báo chí',
              'Giải thưởng','Case\nStudy','CEO\nBrand']
scores = {                     # điền điểm từ Bước 2
    'SEONGON': [4,5,2,4,3,4,2,2],
    'TOS':     [3,1,1,3,4,5,4,2],
    'MONA':    [4,3,2,3,2,1,2,1],
    'SEODO':   [4,3,2,2,5,1,4,5],
    'GTVSEO':  [5,4,5,2,3,1,3,4],
}
N = len(dimensions)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
for name, vals in scores.items():
    v = vals + vals[:1]
    ax.plot(angles, v, color=COLORS[name], linewidth=2, label=name)
    ax.fill(angles, v, color=COLORS[name], alpha=0.08)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(dimensions, fontsize=8.5)
ax.set_yticks([1,2,3,4,5]); ax.set_yticklabels(['1','2','3','4','5'], fontsize=7)
ax.set_ylim(0,5)
ax.grid(color='#dde6ff', linestyle='--', linewidth=0.6)
ax.set_title('Radar — Đánh giá tổng thể', fontsize=12, fontweight='bold', pad=18)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'chart_radar.png'), dpi=150, bbox_inches='tight')
plt.close()

print("✅ Charts generated")
```

> Chạy script này trước, lưu 5 file PNG vào cùng thư mục với file HTML/PDF.

---

### 3C. Build file HTML trung gian (dùng để convert)

Tạo file `_report_tmp.html` với toàn bộ nội dung. Cấu trúc 9 phần, **nhúng PNG thay vì Chart.js**:

```html
<!-- Thay thế phần Chart.js bằng: -->
<div class="charts-grid">
  <div class="chart-card">
    <div class="chart-title">Facebook Followers</div>
    <img src="chart_facebook.png" style="width:100%;border-radius:8px;">
  </div>
  <div class="chart-card">
    <div class="chart-title">LinkedIn Followers</div>
    <img src="chart_linkedin.png" style="width:100%;border-radius:8px;">
  </div>
  <div class="chart-card">
    <div class="chart-title">Số bài Blog</div>
    <img src="chart_blog.png" style="width:100%;border-radius:8px;">
  </div>
  <div class="chart-card">
    <div class="chart-title">YouTube Subscribers</div>
    <img src="chart_youtube.png" style="width:100%;border-radius:8px;">
  </div>
  <div class="chart-card full">
    <div class="chart-title">Radar — Đánh giá tổng thể 8 chiều</div>
    <img src="chart_radar.png" style="max-width:520px;display:block;margin:0 auto;">
  </div>
</div>
```

CSS bổ sung cho PDF (đặt trong `<style>`):
```css
@page { size: A4; margin: 15mm 12mm; }
@media print { .page-break { page-break-before: always; } }
body { font-size: 12px; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
```

Cấu trúc 9 phần giữ nguyên như trước (cover, exec summary, charts, 3 bảng so sánh, ma trận, ưu/nhược, giải thưởng, 5 đề xuất, footer).

---

### 3D. Convert HTML → PDF

```bash
# === Cách 1: wkhtmltopdf (khuyên dùng nếu có) ===
wkhtmltopdf \
  --page-size A4 \
  --margin-top 15mm --margin-bottom 15mm \
  --margin-left 12mm --margin-right 12mm \
  --enable-local-file-access \
  --print-media-type \
  --javascript-delay 500 \
  _report_tmp.html \
  "SEONGON_Marketing_Analysis_$(date +%Y%m).pdf"

# === Cách 2: WeasyPrint (Python) ===
python3 -c "
from weasyprint import HTML, CSS
HTML('_report_tmp.html').write_pdf(
    'SEONGON_Marketing_Analysis_$(date +%Y%m).pdf',
    stylesheets=[CSS(string='@page{size:A4;margin:15mm 12mm}')]
)
print('PDF saved')
"

# Dọn file tạm
rm -f _report_tmp.html chart_*.png
```

File output: `SEONGON_Marketing_Analysis_YYYYMM.pdf`

---

### Checklist trước khi hoàn thành
- [ ] 5 file PNG chart được generate thành công (không lỗi matplotlib)
- [ ] PDF mở được, không bị trắng trang
- [ ] Cover page có gradient màu SEONGON (#0035c0 → #004aef)
- [ ] Ma trận có viền vàng cột SEONGON
- [ ] Giải thưởng phân biệt rõ Winner vs Shortlist
- [ ] File tạm (`_report_tmp.html`, `chart_*.png`) đã được xóa

---

## Gợi ý định hướng chiến lược

Khi viết đề xuất, luôn gắn với bối cảnh SEONGON:
- **LinkedIn + Case Study** → ảnh hưởng trực tiếp nhất đến quyết định mua của C-level KH Ưu tiên 1
- **Google Agency Excellence Award** (Winner 2024, Measurement Solutions) → tài sản credibility cần trưng bày nổi bật hơn
- **Facebook Group** → cạnh tranh với GTVSEO (70K members) nếu muốn xây community
- **YouTube** → GTVSEO đang dẫn xa (66K+); cần chiến lược rõ trước khi đầu tư
