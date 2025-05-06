import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt

st.set_page_config(page_title="Effort Estimation Tool", layout="wide", page_icon="🛠️")

# === Mô hình tính effort ===
def cocomo_ii_effort(kloc, a=2.94, b=0.91, em=1.0):
    return a * (kloc ** b) * em

def function_point_effort(inputs, outputs, queries, files, interfaces, productivity=100, loc_per_fp=53):
    ufp = inputs*4 + outputs*5 + queries*4 + files*10 + interfaces*7
    kloc = ufp * loc_per_fp / 1000
    return kloc / productivity * 100

def ucp_effort(simple_uc, avg_uc, complex_uc, actor_s, actor_a, actor_c, tcf, ecf, productivity=20):
    uucw = simple_uc*5 + avg_uc*10 + complex_uc*15
    uaw = actor_s*1 + actor_a*2 + actor_c*3
    ucp = (uucw + uaw) * tcf * ecf
    return ucp * productivity

# === Hàm đánh giá ===
def evaluate(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    return rmse, mape

st.markdown(
    """
    <style>
    .main {background-color: #f0f6fc;}
    .stButton>button {background-color: #1f77b4; color: white;}
    .stDataFrame {background-color: #f8fafc;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛠️ Software Effort Estimation Tool")
st.markdown("### So sánh các mô hình: **COCOMO II**, **Function Point**, **Use Case Points**")
st.markdown("#### Nhập thông số hoặc tải lên file CSV để bắt đầu")

tab1, tab2 = st.tabs(["🔢 Nhập thông số thủ công", "📤 Tải lên file CSV"])

with tab1:
    st.subheader("🔧 Chỉnh sửa thông số đầu vào")
    col1, col2, col3 = st.columns(3)
    with col1:
        kloc = st.number_input("KLOC (nghìn dòng lệnh)", min_value=1.0, value=10.0, step=0.1)
        em = st.slider("Effort Multiplier (COCOMO II)", 0.5, 2.0, 1.0, 0.01, key="em_manual")
        a = st.slider("Hệ số a (COCOMO II)", 1.0, 5.0, 2.94, 0.01, key="a_manual")
        b = st.slider("Hệ số b (COCOMO II)", 0.5, 1.5, 0.91, 0.01, key="b_manual")
    with col2:
        fp_input = st.number_input("FP Input", 0, 100, 10)
        fp_output = st.number_input("FP Output", 0, 100, 10)
        fp_query = st.number_input("FP Query", 0, 100, 5)
        fp_file = st.number_input("FP File", 0, 100, 2)
        fp_interface = st.number_input("FP Interface", 0, 100, 1)
        loc_per_fp = st.slider("LOC mỗi FP", 10, 100, 53)
        fp_productivity = st.slider("Năng suất Function Point", 10, 500, 100)
    with col3:
        simple_uc = st.number_input("Simple UC", 0, 20, 2)
        avg_uc = st.number_input("Average UC", 0, 20, 2)
        complex_uc = st.number_input("Complex UC", 0, 20, 1)
        actor_s = st.number_input("Actor Simple", 0, 10, 1)
        actor_a = st.number_input("Actor Average", 0, 10, 1)
        actor_c = st.number_input("Actor Complex", 0, 10, 1)
        tcf = st.slider("TCF", 0.5, 1.5, 1.0, 0.01)
        ecf = st.slider("ECF", 0.5, 1.5, 1.0, 0.01)
        ucp_productivity = st.slider("Năng suất UCP", 5, 50, 20)

    if st.button("Tính toán Effort", type="primary"):
        with st.spinner("Đang tính toán..."):
            effort_cocomo = cocomo_ii_effort(kloc, a, b, em)
            effort_fp = function_point_effort(fp_input, fp_output, fp_query, fp_file, fp_interface, fp_productivity, loc_per_fp)
            effort_ucp = ucp_effort(simple_uc, avg_uc, complex_uc, actor_s, actor_a, actor_c, tcf, ecf, ucp_productivity)
            st.success("🎉 Đã tính toán xong!")
            st.balloons()
            st.metric("COCOMO II Effort", f"{effort_cocomo:.2f} person-months")
            st.metric("Function Point Effort", f"{effort_fp:.2f} person-months")
            st.metric("Use Case Points Effort", f"{effort_ucp:.2f} person-months")
            st.progress(100, text="Hoàn thành 100%")

        st.subheader("📊 Biểu đồ Effort")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(["COCOMO II", "Function Point", "Use Case Points"], [effort_cocomo, effort_fp, effort_ucp], color=["#1f77b4", "#ff7f0e", "#2ca02c"])
        ax.set_ylabel("Effort (person-months)")
        ax.set_title("So sánh Effort giữa các mô hình")
        st.pyplot(fig)

with tab2:
    st.subheader("⚙️ Tùy chỉnh thông số mô hình cho dữ liệu CSV")
    col1, col2, col3 = st.columns(3)
    with col1:
        a_csv = st.number_input("Hệ số a (COCOMO II)", 1.0, 5.0, 2.94, 0.01)
        b_csv = st.number_input("Hệ số b (COCOMO II)", 0.5, 1.5, 0.91, 0.01)
        em_csv = st.slider("Effort Multiplier (COCOMO II)", 0.5, 2.0, 1.0, 0.01, key="em_csv")
    with col2:
        loc_fp_csv = st.slider("LOC mỗi FP", 10, 100, 53, key="loc_fp_csv")
        fp_productivity_csv = st.slider("Năng suất Function Point", 10, 500, 100, key="fp_prod_csv")
    with col3:
        tcf_csv = st.slider("TCF", 0.5, 1.5, 1.0, 0.01, key="tcf_csv")
        ecf_csv = st.slider("ECF", 0.5, 1.5, 1.0, 0.01, key="ecf_csv")
        ucp_productivity_csv = st.slider("Năng suất UCP", 5, 50, 20, key="ucp_prod_csv")

    uploaded_file = st.file_uploader("Tải lên file CSV chứa dữ liệu dự án", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.info("Bạn có thể chỉnh sửa dữ liệu trực tiếp bên dưới rồi nhấn 'Áp dụng thay đổi' để tính toán lại.")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edit_csv")
        if st.button("Áp dụng thay đổi"):
            df = edited_df.copy()
            try:
                df["COCOMO_II"] = df["KLOC"].apply(lambda x: cocomo_ii_effort(x, a_csv, b_csv, em_csv))
                df["Function_Point"] = df.apply(
                    lambda row: function_point_effort(
                        row["FP_Input"], row["FP_Output"], row["FP_Query"],
                        row["FP_File"], row["FP_Interface"],
                        productivity=fp_productivity_csv, loc_per_fp=loc_fp_csv
                    ), axis=1)
                df["Use_Case_Points"] = df.apply(
                    lambda row: ucp_effort(
                        row["Simple_UC"], row["Average_UC"], row["Complex_UC"],
                        row["Actor_Simple"], row["Actor_Avg"], row["Actor_Complex"],
                        tcf_csv, ecf_csv, ucp_productivity_csv
                    ), axis=1)
                st.success("Đã tính toán lại effort cho dữ liệu mới!")
                st.dataframe(df[["Project", "ACTUAL_EFFORT", "COCOMO_II", "Function_Point", "Use_Case_Points"]], use_container_width=True)
                models = {
                    "COCOMO II": df["COCOMO_II"],
                    "Function Point": df["Function_Point"],
                    "Use Case Points": df["Use_Case_Points"]
                }
                st.subheader("📈 Đánh giá mô hình")
                for name, preds in models.items():
                    rmse, mape = evaluate(df["ACTUAL_EFFORT"], preds)
                    st.markdown(f"**{name}**: RMSE = `{rmse:.2f}`, MAPE = `{mape:.2f}%`")

                best_model = min(models, key=lambda x: evaluate(df["ACTUAL_EFFORT"], models[x])[0])
                st.success(f"🏆 Mô hình tốt nhất là: **{best_model}**")
                st.subheader("📉 Biểu đồ so sánh effort")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df["Project"], df["ACTUAL_EFFORT"], label="Actual", marker='o')
                ax.plot(df["Project"], df["COCOMO_II"], label="COCOMO II", marker='o')
                ax.plot(df["Project"], df["Function_Point"], label="Function Point", marker='o')
                ax.plot(df["Project"], df["Use_Case_Points"], label="Use Case Points", marker='o')
                ax.set_ylabel("Effort (person-months)")
                ax.set_xlabel("Project")
                ax.set_title("Effort Estimation Comparison")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)
                st.balloons()
            except Exception as e:
                st.error(f"Lỗi khi xử lý dữ liệu: {e}")
                st.markdown("📌 **Lưu ý:** File CSV phải có các cột đúng tên như `KLOC`, `ACTUAL_EFFORT`, `FP_Input`, `Simple_UC`, v.v.")
    else:
        st.info("Vui lòng tải lên file CSV để bắt đầu.")
