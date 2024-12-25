import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Đường dẫn tới file Excel
duong_dan_excel = "pages/chiphi.xlsx"
def load_data():
    try:
        # Đọc dữ liệu từ file Excel
        print(os.access(duong_dan_excel, os.R_OK))
        df = pd.read_excel(duong_dan_excel)
        print(df)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo DataFrame rỗng
        df = pd.DataFrame(columns=["Type", "Name", "Category", "Amount", "Date", "Note"])
    return df

def save_to_excel(df):
    try:
        # Lưu dữ liệu vào file Excel
        df.to_excel(duong_dan_excel, index=False)
        st.success("Data saved to chiphi.xlsx")
    except Exception as e:
        st.error(f"Error saving data to Excel: {e}")

def generate_insights():
    st.title("Insights")
    df = load_data()

    # Hiển thị nếu DataFrame không rỗng
    if not df.empty:
        # Phân tích Income và Expense
        income_df = df[df["Type"] == "Income"]
        expense_df = df[df["Type"] == "Expense"]

        # Tổng hợp dữ liệu theo Category
        income_by_category = income_df.groupby("Category")["Amount"].sum()
        expense_by_category = expense_df.groupby("Category")["Amount"].sum()

        # Chia thành 2 cột ngang
        col1, col2 = st.columns(2)

        # Hiển thị Income trong cột đầu tiên
        with col1:
            st.subheader("Income Insights")
            st.write("Income by Category:")
            st.write(income_by_category)

            # Biểu đồ Pie cho Income
            fig1, ax1 = plt.subplots()
            ax1.pie(income_by_category, labels=income_by_category.index, autopct='%1.1f%%')
            ax1.set_title("Income Distribution")
            st.pyplot(fig1)

        # Hiển thị Expense trong cột thứ hai
        with col2:
            st.subheader("Expense Insights")
            st.write("Expense by Category:")
            st.write(expense_by_category)

            # Biểu đồ Pie cho Expense
            fig2, ax2 = plt.subplots()
            ax2.pie(expense_by_category, labels=expense_by_category.index, autopct='%1.1f%%')
            ax2.set_title("Expense Distribution")
            st.pyplot(fig2)

        # Phân nhóm theo tuần, tháng, năm
        st.subheader("Income and Expense Trends")
        time_frame = st.selectbox("Select Time Frame", ["Week", "Month", "Year"])

        # Convert "Date" to datetime if it's not already
        df["Date"] = pd.to_datetime(df["Date"])

        # Thêm cột "Time Period" cho thu nhập và chi phí
        if time_frame == "Week":
            df["Time Period"] = df["Date"].dt.isocalendar().week
        elif time_frame == "Month":
            df["Time Period"] = df["Date"].dt.month
        elif time_frame == "Year":
            df["Time Period"] = df["Date"].dt.year

        # Phân nhóm thu nhập và chi phí theo "Time Period"
        income_df["Time Period"] = df[df["Type"] == "Income"]["Time Period"]
        expense_df["Time Period"] = df[df["Type"] == "Expense"]["Time Period"]

        # Group by Time Period và tính tổng Amount
        income_by_time = income_df.groupby("Time Period")["Amount"].sum()
        expense_by_time = expense_df.groupby("Time Period")["Amount"].sum()

        # Combine income và expense data để plot
        combined_data = pd.DataFrame({
            "Income": income_by_time,
            "Expense": expense_by_time
        }).fillna(0)

        # Plot line chart cho trends
        fig, ax = plt.subplots(figsize=(10, 6))
        combined_data.plot(ax=ax, marker='o')

        # Tùy chỉnh biểu đồ
        ax.set_title(f"Income and Expense Trends by {time_frame}", fontsize=16)
        ax.set_xlabel(time_frame, fontsize=12)
        ax.set_ylabel("Amount (VND)", fontsize=12)  # Thêm đơn vị của Amount, ví dụ: VND
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))  # Định dạng số có dấu phẩy

        # Tùy chỉnh giao diện
        ax.grid(True, linestyle="--", alpha=0.7)  # Thêm lưới nhẹ
        ax.legend(["Income", "Expense"], fontsize=10)  # Chú thích biểu đồ

        # Hiển thị biểu đồ trên Streamlit
        st.pyplot(fig)

    else:
        st.warning("No transactions found!")

if __name__ == "__main__":
    generate_insights()
