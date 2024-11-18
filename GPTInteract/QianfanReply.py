#import SupportingFunction.feature as ftDetect
#import SupportingFunction.hear as monitoring
# -*- coding: utf-8 -*-
import qianfan
import os


# def windowsPlaysound(filepath):
    # os.system("start "+filepath)
    # os.system("del  "+filepath)

# def macPlaysound(filepath):
    # playsound(filepath)
    # os.remove('./'+filepath)
# ftDetect.findFeature()
# 设置OpenAI API密钥

def getQianfanReply(text="", character="请扮演米法，塞尔达传说中的人物与我对话。",key=[]):
    os.environ["QIANFAN_ACCESS_KEY"] = key[0]
    os.environ["QIANFAN_SECRET_KEY"] = key[1]
    chat_comp = qianfan.ChatCompletion()

    # 定义初始对话历史
    # conversation_history = [
        # 'role': 'system', 'content': 'You are a helpful assistant.'}
    # ]

# 循环交互
    # 将用户输入添加到对话历史中
    conversation_history=([{'role': 'user', 'content': character+text}])

    text_response = chat_comp.do(model="ERNIE-3.5-8K", messages=conversation_history)

    # 获取助手的回复
    assistant_reply = text_response["body"]['result']
    print("Assistant:", assistant_reply)
    return assistant_reply







