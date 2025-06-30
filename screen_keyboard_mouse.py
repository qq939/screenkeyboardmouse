#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图工具模块
提供通过API获取屏幕截图的功能
"""
import cv2
import mss
from PIL import Image
import numpy as np
import pyautogui
class ScreenKeyboardMouse:
    def __init__(self, monitor_index: int = 0):
        """
        初始化截图工具
        
        Args:
            monitor_index (int): 要捕获的显示器索引，默认值为0（主显示器）
        """
        self.monitor_index = monitor_index
        self.sct = None
        self.monitor = None
        self.screen_size = None
        self._initialize_capture()
    def _initialize_capture(self):
        """初始化屏幕捕获"""
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[self.monitor_index]
        self.screen_size = (self.monitor['width'], self.monitor['height'])
        print(f"屏幕尺寸: {self.screen_size}")
    def get_screenshot(self):
        """获取当前屏幕截图
        
        Returns:
            numpy.ndarray: BGR格式的图像数组，如果失败返回None
        """
        try:
            # 如果没有初始化mss对象，初始化一次并保持复用
            if not self.sct:
                self._initialize_capture()
            
            # 使用已有的mss对象截取屏幕
            screenshot = self.sct.grab(self.monitor)


            # 转换为numpy数组
            frame = np.array(screenshot)
            
            # mss返回的是BGRA格式，转换为BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            frame = cv2.resize(frame, self.screen_size)
            # 获取鼠标当前位置
            mouse_x, mouse_y = pyautogui.position()
            
            # 在截图上绘制鼠标指针（简化版箭头）
            cv2.circle(frame, (mouse_x, mouse_y), 5, (0, 0, 255), -1)  # 鼠标位置中心点
            
                    
            return frame
            
        except Exception as e:
            print(f"截图失败: {e}")
            return None

    def save_screenshot(self, filename: str = "screenshot.png") -> bool:
        """
        获取截图并保存到文件
        
        Args:
            api_url (str): 截图API的URL地址
            filename (str): 保存的文件名
            timeout (int): 请求超时时间（秒）
            
        Returns:
            bool: 保存成功返回True，失败返回False
            
        Example:
            >>> # 获取截图并保存
            >>> success = save_screenshot(filename="my_screenshot.png")
            >>> if success:
            ...     print("截图已保存")
        """
        frame = self.get_screenshot()
        image = Image.fromarray(frame)
        if image:
            try:
                image.save(filename)
                print(f"✅ 截图已保存到: {filename}")
                return True
            except Exception as e:
                print(f"❌ 保存截图失败: {e}")
                return False
        return False

    # 移动鼠标，向右向左移动参数所指定的像素
    def move_mouse(self, x_offset: int = 0, y_offset: int = 0):
        """
        移动鼠标
        
        Args:
            x_offset (int): 水平偏移量，正数向右移动，负数向左移动
            y_offset (int): 垂直偏移量，正数向下移动，负数向上移动
            
        Example:
            >>> # 向右移动100像素
            >>> move_mouse(x_offset=100)
            >>> # 向左移动50像素，向上移动20像素
            >>> move_mouse(x_offset=-50, y_offset=-20)
        """
        pyautogui.move(x_offset, y_offset)

    # 获取当前鼠标位置，返回x y
    def get_mouse_position(self):
        """
        获取当前鼠标位置
        
        Returns:
            tuple: 包含x和y坐标的元组
            
        Example:
            >>> x, y = get_mouse_position()
            >>> print(f"当前鼠标位置: ({x}, {y})")
        """
        return pyautogui.position()

    # 键盘按下
    def key_down(self, key: str):
        """
        模拟按下键盘按键
        
        Args:
            key (str): 按键名称，例如 'a', 'b', 'enter', 'space', 'esc', 'tab', 'up', 'down', 'left', 'right' 等
            
        Example:
            >>> # 按下 'a' 键
            >>> key_down('a')
            >>> # 按下 'enter' 键
            >>> key_down('enter')
        """
        pyautogui.keyDown(key)

    # 键盘抬起
    def key_up(self, key: str):
        """
        模拟抬起键盘按键
        
        Args:
            key (str): 按键名称，例如 'a', 'b', 'enter', 'space', 'esc', 'tab', 'up', 'down', 'left', 'right' 等
            
        Example:
            >>> # 抬起 'a' 键
            >>> key_up('a')
            >>> # 抬起 'enter' 键
            >>> key_up('enter')
        """
        pyautogui.keyUp(key)

    # 键盘输入
    def key_input(self, key: str):
        """
        模拟输入键盘按键
        
        Args:
            key (str): 按键名称，例如 'a', 'b', 'enter', 'space', 'esc', 'tab', 'up', 'down', 'left', 'right' 等
            
        Example:
            >>> # 输入 'a' 键
            >>> key_input('a')
            >>> # 输入 'enter' 键
            >>> key_input('enter')
        """
        pyautogui.press(key)

import cv2
import openai
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError

load_dotenv()

class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, image):
        # prompt的意思是用户说的话
        if not prompt:
            return

        print("Prompt:", prompt)

        response = self.chain.invoke(
            {"prompt": prompt, "image_base64": image.decode()},
            config={"configurable": {"session_id": "unused"}},
        ).strip()

        print("Response:", response)

        if response:
            self._tts(response)

    def _tts(self, response):
        player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)

        with openai.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            response_format="pcm",
            input=response,
        ) as stream:
            for chunk in stream.iter_bytes(chunk_size=1024):
                player.write(chunk)

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a witty assistant that will use the chat history and the image 
        provided by the user to answer its questions. Your job is to answer 
        questions.

        Use few words on your answers. Go straight to the point. Do not use any
        emoticons or emojis. 

        Be friendly and helpful. Show some personality.
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )

        chain = prompt_template | model | StrOutputParser()

        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-latest")

# You can use OpenAI's GPT-4o model instead of Gemini Flash
# by uncommenting the following line:
# model = ChatOpenAI(model="gpt-4o")

assistant = Assistant(model)
def audio_callback(recognizer, audio):
    try:
        prompt = recognizer.recognize_whisper(audio, model="base", language="english")
        assistant.answer(prompt, get_screenshot())

    except UnknownValueError:
        print("There was an error processing the audio.")


recognizer = Recognizer()
microphone = Microphone()
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

stop_listening = recognizer.listen_in_background(microphone, audio_callback)

while True:
    cv2.imshow("screenshot", get_screenshot())
    if cv2.waitKey(1) in [27, ord("q")]:
        break

cv2.destroyAllWindows()