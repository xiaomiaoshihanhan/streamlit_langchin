import streamlit as st

from Homepage import openai_api_key
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun


# 显示侧边栏
with st.sidebar:
    if openai_api_key:
        openai_api_key=openai_api_key
    else:
        openai_api_key = st.text_input("OpenAI API Key", key="search_api_key_openai", type="password")


# title初始化聊天机器人
st.title("🔎 联网搜索聊天机器人")

"""
该页面输入要搜索类型的信息才可以正常回复,正常聊天如“你好”无法给出适合的回复。
"""

# 会话状态没有消息时添加默认消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "我是一个聊天机器人,我可以搜索网页,我能为你做些什么?"}
    ]

# 将会话状态的消息添加到聊天会话中去
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 如果聊天输入框中有消息
if prompt := st.chat_input(placeholder="日本排放核废水的时间？"):

    # 将消息添加到会话状态中
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 将消息添加到聊天会话中
    st.chat_message("user").write(prompt)

    # 如果没有密钥时，提示添加密钥
    if not openai_api_key:
        st.info("请先添加您的openai密钥")
        st.stop()

    # 初始化聊天模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    # 初始化搜索引擎
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)