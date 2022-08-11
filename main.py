from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image
import cv2 as cv
import pytesseract
import time

# 学号和密码
id=""
keywords=""
# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(r'd:\webdrivers\chromedriver.exe')

def recognize_text(image):
    # 边缘保留滤波 去噪
    blur = cv.pyrMeanShiftFiltering(image, 8, 60)
    # 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # 识别
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    return text

def get_pictures(wd):
    wd.save_screenshot('pictures.png')  # 全屏截图
    page_snap_obj = Image.open('pictures.png')
    img = wd.find_element(By.ID,'captchaImg')  # 验证码元素位置
    time.sleep(1)
    location = img.location
    size = img.size  # 获取验证码的大小参数
    left = location['x']*1.5
    top = location['y']*1.5
    right = left + size['width']*1.5
    bottom = top + size['height']*1.5  # 比例根据个人显示器比例确定
    im = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
    im.save('save.png')
    src = cv.imread('save.png')
    text = recognize_text(src)
    text = ''.join(filter(str.isalnum, text))
    wd.find_element(By.XPATH,"//input[@id='captchaResponse']").send_keys(text)
    wd.find_element(By.XPATH,"//button[@type='submit']").click()

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('http://yun.ujs.edu.cn/xxhgl/yqsb/grmrsb')
wd.maximize_window()
wd.find_element(By.XPATH,"//input[@placeholder='一卡通号']").send_keys(id)
wd.find_element(By.XPATH,"//input[@placeholder='密码']").send_keys(keywords)
get_pictures(wd)
sleep(2)
k=wd.find_element(By.CLASS_NAME,"weui_btn_area")
print(k)
if(wd.find_element(By.CLASS_NAME,"weui_btn_area")!=" "):
    wd.find_element(By.CLASS_NAME, "weui_btn_area").click()
    wd.find_element(By.ID, "button1").click()
    wd.close()
else:
    wd.find_element(By.XPATH, "//input[@placeholder='密码']").send_keys(keywords)
    get_pictures(wd)
