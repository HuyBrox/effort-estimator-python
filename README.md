# 🛠️ Software Effort Estimation Tool

Ứng dụng này gồm **2 công cụ độc lập**:

---

## 1. `tool.py` – Dự đoán Effort phát triển phần mềm

Ứng dụng Streamlit giúp bạn ước lượng effort phát triển phần mềm dựa trên các mô hình phổ biến: **COCOMO II**, **Function Point**, và **Use Case Points**.

### 🚀 Tính năng nổi bật

- Nhập thông số thủ công cho từng mô hình và xem kết quả ngay lập tức.
- Tải lên file CSV, chỉnh sửa dữ liệu trực tiếp trên giao diện.
- Tùy chỉnh các tham số mô hình (hệ số, năng suất, v.v.) cho từng lần tính toán.
- So sánh kết quả effort giữa các mô hình bằng bảng và biểu đồ.
- Đánh giá sai số (RMSE, MAPE) và gợi ý mô hình phù hợp nhất với dữ liệu.
- Hiệu ứng động đẹp mắt (bóng bay, progress bar, v.v.).

### 🖥️ Hướng dẫn sử dụng

1. **Cài đặt thư viện cần thiết:**
    ```bash
    pip install streamlit pandas matplotlib scikit-learn
    ```

2. **Chạy ứng dụng:**
    ```bash
    streamlit run tool.py
    ```

3. **Sử dụng:**
    - Chọn tab "Nhập thông số thủ công" để nhập liệu từng mô hình.
    - Chọn tab "Tải lên file CSV" để upload dữ liệu dự án, chỉnh sửa và tính toán hàng loạt.
    - Xem kết quả effort, biểu đồ so sánh và gợi ý mô hình phù hợp.

#### 📄 Định dạng file CSV mẫu

```csv
Project,KLOC,FP_Input,FP_Output,FP_Query,FP_File,FP_Interface,Simple_UC,Average_UC,Complex_UC,Actor_Simple,Actor_Avg,Actor_Complex,TCF,ECF,ACTUAL_EFFORT
Project A,10,10,10,5,2,1,2,2,1,1,1,1,1.0,1.0,120
Project B,20,15,12,7,3,2,3,3,2,2,2,2,1.1,1.0,250
```

---

## 2. `web_crawler.py` – Công cụ cào web lấy chỉ số phần mềm

Script này cho phép bạn thu thập (crawl) các chỉ số phần mềm (như số dòng lệnh, số use case, v.v.) từ các trang web hoặc nguồn dữ liệu công khai, hỗ trợ cho việc nhập liệu vào tool dự đoán effort.

### ⚙️ Hướng dẫn sử dụng

1. **Cài đặt thư viện cần thiết:**
    ```bash
    pip install requests beautifulsoup4 pandas
    ```

2. **Chạy script:**
    ```bash
    python web_crawler.py
    ```

3. **Cấu hình:**
    - Chỉnh sửa các URL, selector, hoặc logic trong file `web_crawler.py` để phù hợp với nguồn dữ liệu bạn muốn lấy.

4. **Kết quả:**
    - Dữ liệu sẽ được lưu ra file CSV hoặc hiển thị trên terminal tùy theo cấu hình script.

---

## 📚 Tham khảo

- [COCOMO II Model](https://en.wikipedia.org/wiki/COCOMO)
- [Function Point Analysis](https://en.wikipedia.org/wiki/Function_point)
- [Use Case Points](https://en.wikipedia.org/wiki/Use_Case_Points)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Tác giả:** Huy Brox
**Liên hệ:** (https://www.facebook.com/huybrox/)
**Deploy link**
[tool: ](https://effort-estimator.streamlit.app/)
[toolpaw: ](https://effort-tool-paw.streamlit.app/)