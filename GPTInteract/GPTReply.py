#import SupportingFunction.feature as ftDetect
#import SupportingFunction.hear as monitoring
# -*- coding: utf-8 -*-

from openai import OpenAI
from datetime import datetime


# def windowsPlaysound(filepath):
    # os.system("start "+filepath)
    # os.system("del  "+filepath)

# def macPlaysound(filepath):
    # playsound(filepath)
    # os.remove('./'+filepath)
# ftDetect.findFeature()
# 设置OpenAI API密钥

def getGPTReply(text, conversation_history= [{'role': 'system', 'content': 'You are mipha, a character from legends of Zelda'}],key="",toAudio=True):
    client=OpenAI(api_key=key)

    # 定义初始对话历史
    # conversation_history = [
        # 'role': 'system', 'content': 'You are a helpful assistant.'}
    # ]

# 循环交互
    # 将用户输入添加到对话历史中
    conversation_history.append({'role': 'user', 'content': text})

    # 发送聊天请求
    text_response = client.chat.completions.create(
        model='gpt-4o',
        messages=conversation_history,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )

    # 获取助手的回复
    assistant_reply = text_response.choices[0].message.content
    print("Assistant:", assistant_reply)
    if not toAudio:
        return assistant_reply

    # 打印助手的回复
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=assistant_reply,
    )
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    audio_file_path="ANSWERED"+current_time+".mp3"

    audio_response.stream_to_file(audio_file_path)
    # windowsPlaysound(audio_file_path)
    conversation_history.append({'role': 'assistant', 'content': assistant_reply})
    return [conversation_history,assistant_reply,audio_file_path]





