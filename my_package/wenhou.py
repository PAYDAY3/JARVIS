import datetime  # 导入 datetime 库
from my_package.shuo import speak

def wishme():
    print("欢迎回来")
    hour = datetime.datetime.now().hour
    if hour >= 4 and hour < 12:
        print("旱上好")
        speak("旱上好")
    elif hour >= 12 and hour < 22:
        print("下午好")
        speak("下午好")
    elif hour >= 22 and hour < 24:
        print("太晚了")
        speak("太晚了")
    else:
        print("晚安，先生，明天见。")
        
if __name__ == "__main__":
    wishme()