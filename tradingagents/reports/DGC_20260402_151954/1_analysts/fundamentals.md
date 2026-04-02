Dưới đây là báo cáo cập nhật **fundamental (cơ bản)** cho mã **DGC** tại thời điểm giao dịch **2026-04-02**, dựa trên dữ liệu công cụ khả dụng.

---

## 1) Hồ sơ doanh nghiệp (Company Profile)

- **Tên doanh nghiệp:** Công ty Cổ phần Tập đoàn Hóa chất Đức Giang  
- **Tên tiếng Anh:** Duc Giang Chemicals Group Joint Stock Company  
- **Mã chứng khoán:** **DGC**  
- **Sàn niêm yết:** **HOSE**  
- **ISIN:** VN000000DGC1  
- **Mệnh giá:** 10,000 VND/cp  
- **Số cổ phiếu niêm yết:** 379,779,286 cp  
- **Room ngoại còn lại:** 163,745,890 cp (còn khá lớn, chưa bị “full room”)

### Nhận định nhanh hồ sơ
DGC là doanh nghiệp hóa chất quy mô lớn trên HOSE, thanh khoản tốt và có khả năng thu hút dòng vốn ngoại nhờ room còn rộng.

---

## 2) Dữ liệu thị trường hiện tại (proxy cho diễn biến tuần gần nhất)

> Lưu ý: Công cụ hiện cung cấp snapshot giao dịch tại ngày 2026-04-02, không trả đầy đủ chuỗi BCTC hoặc toàn bộ dữ liệu theo từng ngày trong tuần.

- **Giá tham chiếu:** 50,500  
- **Giá mở cửa:** 50,400  
- **Giá cao nhất:** 54,000  
- **Giá thấp nhất:** 49,600  
- **Giá cuối/khớp gần nhất:** **54,000 (trần)**  
- **+3,500 VND, tương ứng +6.93%**  
- **Khối lượng:** 4,398,300 cp  
- **Giá bình quân:** 51,840  

### Đọc tín hiệu giao dịch
1. **Đóng cửa trần (54,000)** + khối lượng lớn ⇒ lực cầu mạnh, khả năng có catalyst (kỳ vọng KQKD, thông tin ngành, hoặc dòng tiền ngắn hạn).
2. **Biên dao động trong phiên rộng** (49,600 → 54,000) ⇒ biến động cao, phù hợp trader chủ động quản trị rủi ro.
3. **Order book cuối phiên:** bên mua trần lớn, bên bán gần như trống tại mức hiển thị ⇒ cầu áp đảo cung ngắn hạn.

---

## 3) Dòng vốn ngoại (Foreign Flow)

- **Mua:** 1,379,500 cp  
- **Bán:** 51,471 cp  
- **Mua ròng:** **1,328,029 cp**  
- Ước tính giá trị mua ròng theo giá bình quân 51,840 ≈ **68.85 tỷ VND**

### Ý nghĩa
- Mua ròng ngoại ở quy mô lớn trong phiên tăng trần là tín hiệu củng cố xu hướng ngắn hạn.
- Room ngoại còn nhiều nên về kỹ thuật, chưa có áp lực “kẹt room” hạn chế lực mua thêm.

---

## 4) Phần tài chính doanh nghiệp (BCTC, lịch sử tài chính)

### Trạng thái dữ liệu từ công cụ
Các công cụ `get_balance_sheet`, `get_cashflow`, `get_income_statement` hiện **không trả được số liệu BCTC chi tiết** cho cổ phiếu Việt Nam qua SSI iBoard API (chỉ trả thông báo tham chiếu sang nguồn ngoài).

### Hệ quả phân tích
Hiện **chưa thể xác nhận định lượng** các chỉ tiêu cốt lõi (Doanh thu, LN gộp, LN ròng, biên lợi nhuận, nợ vay, dòng tiền HĐKD, capex…) trực tiếp từ tool trong phiên này.

---

## 5) Insight hành động cho trader (actionable)

Vì thiếu dữ liệu BCTC chi tiết từ API, cách hành động nên theo 2 lớp:

### Lớp A – Trading ngắn hạn (dựa trên dòng tiền/giá)
- **Thiên hướng:** Tích cực ngắn hạn do đóng trần + mua ròng ngoại mạnh.
- **Chiến lược:**  
  - Không FOMO đuổi giá nếu mở gap mạnh đầu phiên kế tiếp.  
  - Ưu tiên chờ nhịp retest quanh vùng giá bình quân/giá breakout gần nhất để có R:R tốt hơn.  
  - Đặt stop-loss theo nguyên tắc phần trăm hoặc thủng vùng hỗ trợ gần nhất.
- **Rủi ro:** Phiên tăng trần có thể dẫn tới rung lắc T+; biến động nội phiên có thể lớn.

### Lớp B – Position trung hạn (cần xác nhận fundamental thật)
Trước khi nâng tỷ trọng nắm giữ trung hạn, cần xác nhận:
1. **Xu hướng lợi nhuận 4 quý gần nhất** (QoQ, YoY)  
2. **Biên LN gộp/LN ròng** có duy trì hay co hẹp  
3. **CFO (dòng tiền kinh doanh)** có đi cùng lợi nhuận hay không  
4. **Nợ vay ròng / vốn chủ** và áp lực lãi vay  
5. **Vòng quay tồn kho + phải thu** (đặc biệt quan trọng với doanh nghiệp hóa chất có chu kỳ giá hàng hóa)

Nếu các điểm trên đồng thuận tích cực, nhịp tăng giá hiện tại có xác suất bền hơn.

---

## 6) Kết luận tạm thời

- **Điểm mạnh hiện quan sát được:** động lượng giá rất mạnh, cầu ngoại mua ròng lớn, thanh khoản tốt, room ngoại còn rộng.
- **Điểm còn thiếu để kết luận “fundamental đầy đủ”:** bộ số liệu BCTC chi tiết (KQKD, CĐKT, LCTT) chưa truy xuất được qua tool hiện tại.
- **Khuyến nghị vận hành:** ưu tiên chiến lược linh hoạt theo giá trong ngắn hạn; với quyết định nắm giữ lớn/trung hạn, cần bổ sung xác minh BCTC từ nguồn chuẩn (BCTC kiểm toán/quý, thuyết minh, công bố DN).

---

### Bảng tóm tắt nhanh (Markdown)

| Hạng mục | Dữ liệu chính | Đánh giá/Ý nghĩa giao dịch |
|---|---:|---|
| Doanh nghiệp | CTCP Tập đoàn Hóa chất Đức Giang (DGC), HOSE | Cổ phiếu hóa chất vốn hóa lớn, thanh khoản tốt |
| Giá hiện tại (2026-04-02) | 54,000 (+6.93%), **đóng trần** | Tín hiệu momentum mạnh ngắn hạn |
| Biên độ trong phiên | 49,600 – 54,000 | Biến động cao, cần quản trị rủi ro điểm vào |
| Khối lượng | 4,398,300 cp | Dòng tiền tham gia tốt |
| Giá bình quân | 51,840 | Mốc tham chiếu để theo dõi retest |
| Ngoại mua/bán | 1,379,500 / 51,471 cp | Mua ròng mạnh |
| Ngoại mua ròng | **1,328,029 cp** (~68.85 tỷ VND, ước tính) | Củng cố xu hướng tăng ngắn hạn |
| Room ngoại còn lại | 163,745,890 cp | Chưa bị giới hạn room, còn dư địa cầu ngoại |
| Bảng cân đối kế toán | Chưa có từ tool | Cần lấy thêm để đánh giá nợ, vốn, tài sản |
| KQKD (income statement) | Chưa có từ tool | Chưa xác nhận tăng trưởng doanh thu/lợi nhuận |
| Dòng tiền (cashflow) | Chưa có từ tool | Chưa xác nhận chất lượng lợi nhuận |
| Hành động đề xuất | Ngắn hạn theo momentum có kỷ luật; trung hạn chờ xác nhận BCTC | Tránh ra quyết định lớn khi thiếu dữ liệu nền tảng |

Nếu bạn muốn, tôi có thể tiếp tục dựng luôn một **khung chấm điểm fundamental (10 tiêu chí)** cho DGC để bạn chỉ cần điền số liệu BCTC vào là ra tín hiệu **Mạnh/Trung tính/Yếu** ngay.