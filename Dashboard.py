import streamlit as st
import sqlite3
from pages import Add_transaction, Insights, Transactions


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

    with st.sidebar:
        st.image("logo.png", use_column_width=True)
        st.markdown('<p style="text-align: center; font-size: small;">Awake Drive Joint Stock Company</p>', unsafe_allow_html=True)


    st.title("Finance - Awake Drive JSC")

    st.write("""
    Welcome to the Awake Drive Financial Management Tool! This app is designed to help Awake Drive JSC manage and track financial transactions efficiently.
    
    With this tool, you can:
    
     - Record new transactions
     - View detailed financial analysis
     - Explore your transaction history
     - Interact with the AI chatbot for financial queries and support
    """)

    pages = {
        "Add transaction": "./pages/Add_transaction.py",
        "Insights": "./pages/Insights.py",
        "Your transactions": "./pages/Your_transactions.switch⚊pages.py",
    }



    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Add transaction"):
            st.switch_page("pages/Add_transaction.py")

    with col2:
        if st.button("AI assistant"):
            st.switch_page("pages/ChatBot.py")

if __name__ == "__main__":
    Dashboard()