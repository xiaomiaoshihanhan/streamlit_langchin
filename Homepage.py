# First
import openai
import streamlit as st

# 侧边栏
# with st.sidebar:
#      openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# openai密钥
openai_api_key = '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'

# 页面的标题文字
st.title("💬 Chatbot")

# 会话状态没有消息时添加默认消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "请问有什么我可以帮助你的？"}]

# 将会话状态的消息添加到聊天会话中去
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
# print(st.session_state)

# 如果聊天输入框中有消息
if prompt := st.chat_input():

    # 如果没有密钥时，提示添加密钥
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # 密钥
    openai.api_key = openai_api_key
    # 将消息添加到会话状态中
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 将消息添加到聊天会话中
    st.chat_message("user").write(prompt)

    # 发送消息
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # 获取返回内容
    msg = response.choices[0].message
    # 将返回内容添加会话状态中
    st.session_state.messages.append(msg)
    # 将返回内容添加聊天会话中
    st.chat_message("assistant").write(msg.content)
