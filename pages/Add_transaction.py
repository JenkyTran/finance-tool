import streamlit as st
import pandas as pd

# Đường dẫn tới file Excel
duong_dan_excel = "chiphi.xlsx"

def load_data():
    try:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(duong_dan_excel)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo DataFrame rỗng
        df = pd.DataFrame(columns=["Type", "Name", "Category", "Amount", "Date", "Note"])
    return df

def save_data(df):
    try:
        # Lưu dữ liệu vào file Excel
        df.to_excel(duong_dan_excel, index=False)
        st.success("Data saved to chiphi.xlsx")
    except Exception as e:
        st.error(f"Error saving data to Excel: {e}")

def add_transaction():
    st.title("Add Transaction")
    transaction_type = st.selectbox("Select Transaction Type", ["Select", "Income", "Expense"])
    name = st.text_input("Enter Name")
    col1, col2 = st.columns(2)
    category = col1.selectbox("Select Category", ["Select"] + categories.get(transaction_type, []))
    amount = col2.number_input("Enter Amount", min_value=0, value=0)
    date = st.date_input("Select Date")
    st.text("")

    if st.button("Add Transaction"):
        if transaction_type == "Select" or amount == 0 or not name or category == "Select":
            st.warning("Please ensure that you have filled all the fields.")
        else:
            new_row = {"Type": transaction_type, "Name": name, "Category": category, "Amount": amount, "Date": date, "Note": ""}
            df = load_data()
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)
            save_data(df)
            st.success("Transaction added successfully!")

if __name__ == "__main__":
    categories = {
        "Income": ["Salary", "Allowance", "Freelance", "Gift", "Other"],
        "Expense": ["Housing", "Transportation", "Food", "Groceries", "Utilities", "Grooming", "Entertainment", "Healthcare", "Other"]
    }
    add_transaction()
