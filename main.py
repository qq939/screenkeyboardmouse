#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则：鼠标移动后需要截图确认鼠标位置，鼠标已经通过蓝色小圆圈色块标识出来了
获取屏幕截图：get_screenshot
鼠标移动：move_mouse
键盘输入：key_input
"""
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("MCP control screen and keyboard")
import cv2
import mss
from PIL import Image
import numpy as np
import pyautogui


"""初始化屏幕捕获"""
monitor_index = 1
sct = mss.mss()
monitor = sct.monitors[monitor_index]
screen_size = (monitor['width'], monitor['height'])
print(f"屏幕尺寸: {screen_size}")
@mcp.resource("get_screenshot://{}")
def get_screenshot():
    """获取当前屏幕截图
    
    Returns:
        numpy.ndarray: BGR格式的图像数组，如果失败返回None
    """
    try:
        
        # 使用已有的mss对象截取屏幕
        screenshot = sct.grab(monitor)


        # 转换为numpy数组
        frame = np.array(screenshot)
        
        # mss返回的是BGRA格式，转换为BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame = cv2.resize(frame, screen_size)
        # 获取鼠标当前位置
        mouse_x, mouse_y = pyautogui.position()
        
        # 在截图上绘制鼠标指针（简化版箭头）
        cv2.circle(frame, (mouse_x, mouse_y), 5, (0, 0, 255), -1)  # 鼠标位置用蓝色圆圈标识
        
                
        return frame
        
    except Exception as e:
        print(f"截图失败: {e}")
        return None
@mcp.resource("save_screenshot://{filename}")
def save_screenshot( filename: str = "screenshot.png") -> bool:
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
    frame = get_screenshot()
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
@mcp.tool()
def move_mouse( x_offset: int = 0, y_offset: int = 0):
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
def get_mouse_position():
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
def key_down( key: str):
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
def key_up( key: str):
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
@mcp.tool()
def key_input( key: str):
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

if __name__=="__main__":
    mcp.run(transport="stdio")