import json
from PIL import Image
import keyboard
import os
import shutil
import speech_recognition as sr
import threading

# 存档文件路径
archive_file = "archive.json"
file_path="/" #文件夹位置

# 创建存档
def create_archive(data):
    with open(archive_file, "w") as file:
        json.dump(data, file)

# 读取存档
def load_archive():
    try:
        with open(archive_file, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None

# 更新存档
def update_archive(data):
    existing_data = load_archive()

    if existing_data is not None:
        existing_data.update(data)
        create_archive(existing_data)
    else:
        create_archive(data)

# 保存存档的回调函数
def save_archive(file_path=None, content=None, save_image=None, new_name=None):
    if file_path is None and content is None and save_image is None:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("请说出文件路径：")
            audio = recognizer.listen(source)

        try:
            file_path = recognizer.recognize_google(audio, language="zh-CN")
            print("文件路径：", file_path)

            # 判断文件类型并保存
            if file_path.endswith(".txt"):
                with sr.Microphone() as source:
                    print("请说出文本内容：")
                    audio = recognizer.listen(source)

                try:
                    content = recognizer.recognize_google(audio, language="zh-CN")
                    with open(file_path, "w") as file:
                        file.write(content)
                    print("已保存文本文件。")
                except sr.UnknownValueError:
                    print("无法识别语音输入。")
            elif file_path.endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(file_path)
                image.show()

                with sr.Microphone() as source:
                    print("是否保存图片？(是/否)")
                    audio = recognizer.listen(source)

                try:
                    save_image = recognizer.recognize_google(audio, language="zh-CN")
                    if save_image == "是":
                        with sr.Microphone() as source:
                            print("请说出新的文件名（不包含扩展名）：")
                            audio = recognizer.listen(source)

                        try:
                            new_name = recognizer.recognize_google(audio, language="zh-CN")
                            save_dir = os.path.dirname(file_path)
                            save_path = os.path.join(save_dir, new_name + os.path.splitext(file_path)[1])
                            image.save(save_path)
                            print("已保存图片文件。")
                        except sr.UnknownValueError:
                            print("无法识别语音输入。")
                    else:
                        print("未保存图片文件。")
                except sr.UnknownValueError:
                    print("无法识别语音输入。")
            else:
                print("不支持该文件类型。")
        except sr.UnknownValueError:
            print("无法识别语音输入。")
    elif file_path is not None and content is not None:
        with open(file_path, "w") as file:
            file.write(content)
        print("已保存文本文件。")
    elif file_path is not None and save_image is not None and new_name is not None:
        image = Image.open(file_path)
        image.save(new_name)
        print("已保存图片文件。")

# 查找文件的回调函数
def find_file(file_path=None):
    if file_path is None:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("请说出要查找的文件或文件夹名：")
            audio = recognizer.listen(source)

        try:
            file_path = recognizer.recognize_google(audio, language="zh-CN")
            result = []

            for root, dirs, files in os.walk(".", topdown=True):
                for file in files:
                    if file_path in file:
                        result.append(os.path.join(root, file))

            if len(result) > 0:
                print("找到以下文件：")
                for i, file_path in enumerate(result):
                    print(i+1, ":", file_path)
            else:
                print("未找到符合条件的文件。")
        except sr.UnknownValueError:
            print("无法识别语音输入。")
    else:
        result = []

        for root, dirs, files in os.walk(".", topdown=True):
            for file in files:
                if file_path in file:
                    result.append(os.path.join(root, file))

        if len(result) > 0:
            print("找到以下文件：")
            for i, file_path in enumerate(result):
                print(i+1, ":", file_path)
        else:
            print("未找到符合条件的文件。")

# 删除文件的回调函数
def delete_file(file_path=None):
    if file_path is None:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("请说出要删除的文件路径：")
            audio = recognizer.listen(source)

        try:
            file_path = recognizer.recognize_google(audio, language="zh-CN")
            if os.path.exists(file_path):
                os.remove(file_path)
                print("已成功删除文件。")
            else:
                print("文件不存在。")
        except sr.UnknownValueError:
            print("无法识别语音输入。")
    else:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("已成功删除文件。")
        else:
            print("文件不存在。")

# 删除指定文件的回调函数
def delete_specified_file(number=None):
    if number is None:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("请说出要删除的文件序号：")
            audio = recognizer.listen(source)

        try:
            number = int(recognizer.recognize_google(audio, language="zh-CN"))
            files_to_delete = []
            result = []

            for root, dirs, files in os.walk(".", topdown=True):
                for file in files:
                    if file_path in file:
                        result.append(os.path.join(root, file))

            if len(result) > 0:
                for i, file_path in enumerate(result):
                    if i+1 == number:
                        files_to_delete.append(file_path)
                if len(files_to_delete) > 0:
                    for file_path in files_to_delete:
                        os.remove(file_path)
                        print(f"已成功删除文件 {file_path}")
                else:
                    print(f"找不到序号为 {number} 的文件。")
            else:
                print("未找到符合条件的文件。")
        except sr.UnknownValueError:
            print("无法识别语音输入。")
        except ValueError:
            print("输入不是有效的数字。")
    else:
        files_to_delete = []
        result = []

        for root, dirs, files in os.walk(".", topdown=True):
            for file in files:
                if file_path in file:
                    result.append(os.path.join(root, file))

        if len(result) > 0:
            for i, file_path in enumerate(result):
                if i+1 == number:
                    files_to_delete.append(file_path)
            if len(files_to_delete) > 0:
                for file_path in files_to_delete:
                    os.remove(file_path)
                    print(f"已成功删除文件 {file_path}")
            else:
                print(f"找不到序号为 {number} 的文件。")
        else:
            print("未找到符合条件的文件。")

# 开启命令行输入线程
command_thread = threading.Thread(target=command_listener)
command_thread.daemon = True
command_thread.start()

# 开启语音输入线程
speech_thread = threading.Thread(target=speech_listener)
speech_thread.daemon = True
speech_thread.start()

while True:
    pass
    

    