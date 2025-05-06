import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Thiết lập giao diện trang web
st.set_page_config(page_title="Effort Estimation Tool", layout="wide")

st.title("🌐 Web Effort Estimation Tool")

# Nhập URL của dự án cần phân tích
url = st.text_input("🔗 Nhập URL của dự án web:")
if st.button("Quét mã nguồn"):
    if not url.startswith("http"):
        st.error("URL không hợp lệ! Vui lòng nhập URL đầy đủ (ví dụ: http://www.example.com).")
    else:
        try:
            # Cào mã nguồn từ URL
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            # Lấy tên dự án từ thẻ <title> của trang
            project_name = soup.title.string.strip() if soup.title else "Unknown Project"

            # Tính KLOC (Số dòng mã)
            js_files = soup.find_all('script', src=True)
            css_files = soup.find_all('link', rel='stylesheet')
            html_code = res.text

            # Đếm số dòng trong các file JavaScript và HTML
            js_code = ""
            for js in js_files:
                js_url = js['src']
                if not js_url.startswith('http'):
                    js_url = url + js_url  # Đảm bảo URL đầy đủ
                js_res = requests.get(js_url)
                js_code += js_res.text

            # Đếm số dòng trong mã HTML
            lines_html = len(html_code.split('\n'))
            lines_js = len(js_code.split('\n'))
            total_lines = lines_html + lines_js
            kloc = total_lines / 1000  # KLOC (1 KLOC = 1000 dòng mã)

            # Tính Actual Effort (giả sử: KLOC * 3)
            actual_effort = kloc * 3

            # Tính các chỉ số khác (giả lập)
            simple_uc = 5
            avg_uc = 3
            complex_uc = 2
            actor_s = 2
            actor_a = 1
            actor_c = 1
            tcf = 1.0
            ecf = 1.0
            fp_input = 10
            fp_output = 8
            fp_query = 5
            fp_file = 4
            fp_interface = 2

            # Tạo DataFrame để hiển thị kết quả
            data = {
                "Project": [project_name],
                "KLOC": [kloc],
                "ACTUAL_EFFORT": [actual_effort],
                "Simple_UC": [simple_uc],
                "Average_UC": [avg_uc],
                "Complex_UC": [complex_uc],
                "Actor_Simple": [actor_s],
                "Actor_Avg": [actor_a],
                "Actor_Complex": [actor_c],
                "TCF": [tcf],
                "ECF": [ecf],
                "FP_Input": [fp_input],
                "FP_Output": [fp_output],
                "FP_Query": [fp_query],
                "FP_File": [fp_file],
                "FP_Interface": [fp_interface]
            }
            df = pd.DataFrame(data)

            st.success("✅ Đã trích xuất dữ liệu thành công!")

            st.dataframe(df)

            # Tạo file CSV và cung cấp link tải về
            csv = df.to_csv(index=False)
            st.download_button("📥 Tải về CSV", csv, file_name="effort_data.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Lỗi khi quét mã nguồn: {e}")
