#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : utils
# @Time         : 2022/10/18 下午1:29
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import streamlit as st
from streamlit.components.v1 import html
from streamlit.elements.image import image_to_url

from meutils.pipe import *


def hide_st_style(footer_content='🔥'):
    _ = f"""
        <style>.css-18e3th9 {{padding-top: 2rem;}}
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}        
        footer:after {{content:"{footer_content}";visibility: visible;display: block;position: absolute;left: 50%;transform: translate(-50%, -100%);}}
        </style>
        """

    st.markdown(_, unsafe_allow_html=True)


def set_footer(prefix="Made with 🔥 by ", author='Betterme', url=None):  # 链接门户、微信
    _ = f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F5F5F5;
        color: #000000;
        text-align: center;
        border-style: solid;
        border-width: 1px;
        border-color: #DDDDDD;
        padding: 8px;
        }}
    </style>
    <div class="footer">
    <p>{prefix}<a href="{url}" target="_blank">{author}</a></p> 
    </div>
    """
    st.sidebar.markdown(_, unsafe_allow_html=True)


# 设置文本字体
def set_font():
    _ = f"""
    <style>
    h1,h2,h3,h4,h5,h6 {{
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-weight: 400;
    }}
    </style>
    """
    st.markdown(_, unsafe_allow_html=True)


# 设置页面背景色
def set_background_color(color='#f1f1f1'):
    _ = f"""
    <style>
    body {{
        background-color: {color};
    }}
    </style>
    """
    st.markdown(_, unsafe_allow_html=True)


def set_background_image(image=get_module_path('./pics/夕阳.png', __file__)):
    image_url = image_to_url(image, width=-1, clamp=False, channels="RGB", output_format="auto", image_id="")
    _ = f'''
        <style>
            .css-fg4pbf {{
            background-image:url({image_url});
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center center;
            height: 100vh;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            }}
        </style>
    '''
    st.markdown(_, unsafe_allow_html=True)


def set_space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def set_columns_placed(bins=2, default_position=0, gap='small'):  # ("small", "medium", or "large")
    _ = st.columns(spec=bins, gap=gap)
    if len(_) < default_position:
        default_position = -1
    return _[default_position]


def display_pdf(base64_pdf, width='100%', height=1000):
    _ = f"""<embed src="data:application/pdf;base64,{base64_pdf}" width="{width}" height="{height}" type="application/pdf">"""
    st.markdown(_, unsafe_allow_html=True)


def display_pdf4file(file, width='100%', height=500):  # 上传PDF文件
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    display_pdf(base64_pdf, width, height)


def display_html(text='会飞的文字'):  # html("""<marquee bgcolor="#00ccff" behavior="alternate">这是一个滚动条</marquee>""")
    _ = f"""
        <marquee direction="down" width="100%" height="100%" behavior="alternate" style="border:solid"  bgcolor="#00FF00">

          <marquee behavior="alternate">

            {text}

          </marquee>

        </marquee>
        """
    st.markdown(_, unsafe_allow_html=True)


def st_chat(
        input,
        history=None,
        reply_func=lambda input: f'{input}的答案',
        max_turns=3,
        container=None,
        previous_messages=None,
        user_avatar_style="adventurer",
        bot_avatar_style="Big Smile",
        seed=42,
):
    """https://www.dicebear.com/styles/big-smile
        container = st.container()  # 占位符
        text = st.text_area(label="用户输入", height=100, placeholder="请在这儿输入您的问题")

        if st.button("发送", key="predict"):
            with st.spinner("AI正在思考，请稍等........"):
                history = st.session_state.get('state')
                st.session_state["state"] = st_chat(text, history, container=container)
                print(st.session_state['state'])
    """
    from streamlit_chat import message
    user_message = partial(
        message, avatar_style=user_avatar_style.strip().replace(' ', '-').lower(), is_user=True, seed=seed)
    bot_message = partial(
        message, avatar_style=bot_avatar_style.strip().replace(' ', '-').lower(), is_user=False, seed=seed)

    history = history or []  # [(input/query, response)]

    container = container or st.container()
    with container or st.container():
        if previous_messages:
            for msg in previous_messages:
                bot_message(msg)  # display all the previous message

        if max_turns > 1 and len(history) > 0:  # 展示历史
            for i, (query, response) in enumerate(history[-max_turns + 1:]):
                user_message(query, key=str(i) + "_user")
                bot_message(response, key=str(i))

        user_message(input, key=str(len(history)) + "_user")
        # st.write("AI正在回复:")
        with st.empty():
            response = reply_func(input)
            if isinstance(response, types.GeneratorType):
                for i, _response in enumerate(response):
                    bot_message(_response, key=f"stream{i}")
                response = _response
            else:
                bot_message(response)

    history.append((input, response))
    return history


def set_button():
    css = """<style>
     .stDownloadButton>button {
         background-color: #0099ff;
        color:#ffffff;
    }

    .stDownloadButton>button:hover {
       background-color: #00ff00;
        color:#ff0000;
       }
    </style>
    """
    html(css)  # st.markdown


def set_config(conf: BaseConfig, conf_path='conf.yaml'):  # todo: 数值改为 slider
    """
    :param conf:
    :param conf_path:
    :return:
    """
    if Path(conf_path).is_file():
        conf = conf.parse_yaml(conf_path)

    form = st.sidebar.form('配置项')  # 位置
    with form:
        for k, v in conf:
            v = type(v)(form.text_input(label=k.title(), value=v, help=k))  # 配置类型
            setattr(conf, k, v)  # 更新配置

        if form.checkbox("是否保存配置"):
            yaml.safe_dump(conf.dict(), open(conf_path, 'w'))  # 固化

        if form.form_submit_button('刷新配置'):
            # form.balloons()
            form.json(conf.dict())

            st.session_state.init = True  # 初始化标识

        return conf


def text_align(text, position='center'):
    """中显示标题"""
    st.markdown(f"<h1 style='text-align: {position};'>{text}</h1>", unsafe_allow_html=True)
