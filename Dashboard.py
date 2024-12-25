import streamlit as st
import sqlite3
import os


def create_table():
    conn = sqlite3.connect("transactions.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    Type TEXT,
                    Name TEXT,
                    Category TEXT,
                    Amount REAL,
                    Date TEXT
                 )''')
    conn.commit()
    conn.close()


def Dashboard():
    create_table()

    logo_path = "Logo.png"  # Sử dụng đường dẫn tương đối
    with st.sidebar:
        # Kiểm tra sự tồn tại của logo
        if os.path.exists(logo_path):
            st.image(logo_path, use_column_width=True)
        else:
            st.warning("Logo file not found. Please ensure 'Logo.png' is in the same folder as 'Dashboard.py'.")
        st.markdown('<p style="text-align: center; font-size: small;">Awake Drive Joint Stock Company</p>',
                    unsafe_allow_html=True)

    st.title("Finance - Awake Drive JSC")

    st.write("""
    Welcome to the Awake Drive Financial Management Tool! This app is designed to help Awake Drive JSC manage and track financial transactions efficiently.

    With this tool, you can:

     - Record new transactions
     - View detailed financial analysis
     - Explore your transaction history
     - Interact with the AI chatbot for financial queries and support
    """)

    # Các trang tương ứng
    pages = {
        "Add transaction": "./pages/Add_transaction.py",
        "Insights": "./pages/Insights.py",
        "AI Assistant": "./pages/ChatBot.py",
    }

    col1, col2 = st.columns([1, 1])

    # Sử dụng st.session_state để lưu trạng thái nút được nhấn
    if "page" not in st.session_state:
        st.session_state.page = None

    with col1:
        if st.button("Add transaction"):
            st.session_state.page = "Add transaction"

    with col2:
        if st.button("AI Assistant"):
            st.session_state.page = "AI Assistant"

    # Chuyển trang dựa vào trạng thái nút
    if st.session_state.page == "Add transaction":
        st.write("Redirecting to Add Transaction page...")
        st.write("This would load: ", pages["Add transaction"])
        # Thay thế bằng logic thực sự để hiển thị nội dung từ Add_transaction.py

    elif st.session_state.page == "AI Assistant":
        st.write("Redirecting to AI Assistant page...")
        st.write("This would load: ", pages["AI Assistant"])
        # Thay thế bằng logic thực sự để hiển thị nội dung từ ChatBot.py


if __name__ == "__main__":
    Dashboard()
