import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = "AIzaSyBtL9pH7na1PF4Y-AxI51bxv83dCsS89nY"

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.5)

transaction_path = "D:/OneDrive/Desktop/Awake Drive JSC/finance-tool/pages/chiphi.xlsx"
plan_path = "D:/OneDrive/Desktop/Awake Drive JSC/finance-tool/pages/plan.xlsx"

task_prompt_template = """
    Bạn là ChatBot AI tương tác với người dùng về các dữ liệu tài chính của công ty Awake Drive.
    Công ty cổ phần Awake Drive là công ty cung cấp sản phẩm giúp giám sát và duy trì độ tỉnh táo của tài xế dựa trên công nghệ AI và công nghệ sóng não.
    Phân loại xem người dùng đang muốn thực hiện nhiệm vụ gì từ câu hỏi của người dùng:
    {context}
    ####
    Các loại nhiệm vụ:
    1. Nhiệm vụ liên quan đến ghi chép thu chi, phân tích thu chi (transactions)
    2. Nhiệm vụ liên quan đến kế hoạch 6 tháng (plan)
    3. Nhiệm vụ liên quan đến cả thu chi và kế hoạch 
    Yêu cầu trả về duy nhất 1 số thể hiện cho nhiệm vụ
"""

detailed_prompt_template = """
    Bạn là ChatBot AI tương tác với người dùng về các dữ liệu tài chính của công ty Awake Drive.
    Công ty cổ phần Awake Drive là công ty cung cấp sản phẩm giúp giám sát và duy trì độ tỉnh táo của tài xế dựa trên công nghệ AI và công nghệ sóng não.
    Dựa vào file dữ liệu dưới đây:
    {data}
    ####
    Hãy thực hiện nhiệm vụ sau và đưa ra đề xuất hợp lý (nếu có) cho yêu cầu:
    {question}
    Nếu là kế hoạch thì nó bắt đầu từ tháng 12
"""

def load_excel_data(file_path):
    try:
        return pd.read_excel(file_path,engine='openpyxl')
    except FileNotFoundError:
        return pd.DataFrame()
data2 = load_excel_data(plan_path)
data1 = load_excel_data(transaction_path)
da = str(data1.to_json)
ta = str(data2.to_json)
data = da+ta
print("---")
print(data)
def create_task_prompt(context):
    return task_prompt_template.format(context=context)

def create_detailed_prompt(data, question):
    return detailed_prompt_template.format(data=data, question=question)

def get_response(prompt):
    response = llm.invoke(prompt).content.strip()
    return response


st.set_page_config(
    page_title="Financial AI Chatbot",
    page_icon="📑",
    layout="wide"
)

st.title("💬 Financial AI Chatbot Assistant")
st.write(
    "Hello! I am your financial AI assistant, ready to help you analyze income and expense data, plan for the next 6 months, answer financial-related questions, and provide personalized recommendations to optimize your financial decisions based on your data."
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("💬 Đặt câu hỏi về tài chính tại đây...")

if user_input:

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    task_prompt = create_task_prompt(user_input)
    task_response = get_response(task_prompt)
    task_type = int(task_response) if task_response.isdigit() else None

    assistant_response = "Xin lỗi, tôi không thể hiểu yêu cầu của bạn. Vui lòng thử lại."
    if task_type == 1:  # Nhiệm vụ "transactions"
        detailed_prompt = create_detailed_prompt(data=data1, question=user_input)
        assistant_response = get_response(detailed_prompt)

    elif task_type == 2:  # Nhiệm vụ "plan"
        detailed_prompt = create_detailed_prompt(data=data2, question=user_input)
        assistant_response = get_response(detailed_prompt)
    elif task_type == 3:
        detailed_prompt = create_detailed_prompt(data=data, question=user_input)
        assistant_response = get_response(detailed_prompt)

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})