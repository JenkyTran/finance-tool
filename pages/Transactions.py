import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Đường dẫn tới file Excel
duong_dan_excel = "pages/chiphi.xlsx"


def load_data():
    try:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel(duong_dan_excel)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo DataFrame rỗng
        df = pd.DataFrame(columns=["Type", "Name", "Category", "Amount", "Date"])
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
        st.subheader("Income Insights")
        income_df = df[df["Type"] == "Income"]
        income_by_category = income_df.groupby("Category")["Amount"].sum()
        st.write("Income by Category:")
        st.write(income_by_category)

        fig, ax = plt.subplots()
        ax.pie(income_by_category, labels=income_by_category.index, autopct='%1.1f%%')
        st.pyplot(fig)

        st.subheader("Expense Insights")
        expense_df = df[df["Type"] == "Expense"]
        expense_by_category = expense_df.groupby("Category")["Amount"].sum()
        st.write("Expense by Category:")
        st.write(expense_by_category)

        fig, ax = plt.subplots()
        ax.pie(expense_by_category, labels=expense_by_category.index, autopct='%1.1f%%')
        st.pyplot(fig)

        st.subheader("Top Expense Categories:")
        sorted_expense = expense_by_category.sort_values(ascending=False)
        st.write(sorted_expense)
    else:
        st.warning("No transactions found!")


def add_expense():
    df = load_data()

    # Input từ người dùng
    date = st.date_input("Date")
    expense = st.text_input("Expense Name")
    amount = st.number_input("Amount $", min_value=0.0, step=0.01)
    category = st.text_input("Category")
    note = st.text_area("Note")

    if st.button("Add Expense"):
        # Tạo một DataFrame mới từ dòng dữ liệu cần thêm
        new_expense = pd.DataFrame([{
            "Type": "Expense",
            "Name": expense,
            "Category": category,
            "Amount": amount,
            "Date": date,
            "Note": note
        }])

        # Dùng pd.concat để thêm dòng mới vào DataFrame hiện tại
        df = pd.concat([df, new_expense], ignore_index=True)

        # Lưu lại dữ liệu vào file Excel
        save_to_excel(df)
        st.success("Expense added!")


def update_expense():
    df = load_data()
    st.write("Update an existing expense")

    # Hiển thị danh sách các chi phí
    if not df.empty:
        expense_name = st.selectbox("Select Expense to Update", df["Name"].unique())
        expense_to_update = df[df["Name"] == expense_name].iloc[0]

        new_amount = st.number_input("New Amount $", value=expense_to_update["Amount"])
        new_category = st.text_input("New Category", value=expense_to_update["Category"])
        new_note = st.text_area("New Note", value=expense_to_update["Note"])

        if st.button("Update Expense"):
            df.loc[df["Name"] == expense_name, "Amount"] = new_amount
            df.loc[df["Name"] == expense_name, "Category"] = new_category
            df.loc[df["Name"] == expense_name, "Note"] = new_note

            # Lưu lại dữ liệu vào file Excel
            save_to_excel(df)
            st.success("Expense updated!")


def delete_expense():
    df = load_data()
    st.write("Delete an existing expense")

    if not df.empty:
        expense_name = st.selectbox("Select Expense to Delete", df["Name"].unique())

        if st.button("Delete Expense"):
            df = df[df["Name"] != expense_name]
            # Lưu lại dữ liệu vào file Excel
            save_to_excel(df)
            st.success(f"Expense '{expense_name}' deleted!")


if __name__ == "__main__":
    action = st.sidebar.selectbox("Select Action",
                                  ["Generate Insights", "Add Expense", "Update Expense", "Delete Expense"])

    if action == "Generate Insights":
        generate_insights()
    elif action == "Add Expense":
        add_expense()
    elif action == "Update Expense":
        update_expense()
    elif action == "Delete Expense":
        delete_expense()
