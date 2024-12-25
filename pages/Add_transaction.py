import streamlit as st
import pandas as pd
import os

# Đường dẫn tới file Excel
duong_dan_excel = "D:/OneDrive/Desktop/Awake Drive JSC/finance-tool/pages/chiphi.xlsx"

def load_data():
    try:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(duong_dan_excel)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo DataFrame rỗng với 6 cột đúng cấu trúc
        df = pd.DataFrame(columns=["Type", "Name", "Category", "Amount", "Date", "Note"])
    return df

def save_data(df):
    try:
        # Kiểm tra và tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(duong_dan_excel)
        if not os.path.exists(directory):
            os.makedirs(directory)  # Tạo thư mục

        # Lưu dữ liệu vào file Excel
        df.to_excel(duong_dan_excel, index=False)
        st.success("Data saved to chiphi.xlsx")
    except Exception as e:
        st.error(f"Error saving data to Excel: {e}")

def add_transaction():
    st.title("Add Transaction")

    # Chọn loại giao dịch: Income hoặc Expense
    transaction_type = st.selectbox("Select Transaction Type", ["Select", "Income", "Expense"])

    # Nhập tên giao dịch
    name = st.text_input("Enter Name")

    # Chọn danh mục và nhập số tiền
    col1, col2 = st.columns(2)
    category = col1.selectbox(
        "Select Category",
        ["Select"] + categories.get(transaction_type, []) if transaction_type != "Select" else ["Select"]
    )
    amount = col2.number_input("Enter Amount", min_value=0.0, step=0.01)

    # Chọn ngày giao dịch
    date = st.date_input("Select Date")

    # Ghi chú tùy chọn
    note = st.text_area("Add Note (Optional)")

    # Xử lý khi nhấn nút "Add Transaction"
    if st.button("Add Transaction"):
        if transaction_type == "Select" or category == "Select" or amount <= 0 or not name:
            st.warning("Please fill in all required fields!")
        else:
            # Tạo một dòng mới cho giao dịch
            new_row = {
                "Type": transaction_type,
                "Name": name,
                "Category": category,
                "Amount": amount,
                "Date": date,
                "Note": note
            }

            # Load dữ liệu hiện có, thêm giao dịch mới và lưu lại
            df = load_data()
            new_df = pd.DataFrame([new_row])  # Tạo DataFrame cho giao dịch mới
            df = pd.concat([df, new_df], ignore_index=True)  # Gộp giao dịch mới vào dữ liệu hiện tại
            save_data(df)

            # Thông báo thành công
            st.success("Transaction added successfully!")

if __name__ == "__main__":
    # Định nghĩa danh mục cho từng loại giao dịch
    categories = {
        "Income": ["Funding", "Competition", "Freelance", "Donate", "Other"],
        "Expense": ["Competition", "Bonding", "Product", "Company", "Marketing", "Sales", "Bonus", "Other"]
    }

    # Gọi hàm thêm giao dịch
    add_transaction()
