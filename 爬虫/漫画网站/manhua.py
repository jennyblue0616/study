import os
import random
import time
import requests
from io import BytesIO
from PIL import Image
from comic.compare_helper import get_compare
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 获取图片
def get_resuorce(url):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None


# 保存大的图片
def save_img():
    str = '1234567890'
    s = ''
    for i in range(13):
        s += random.choice(str)
    url = f'http://www.1kkk.com/vipindex/image3.ashx?t={s}'
    img = get_resuorce(url)
    with open(f'./images/{s}.jpeg', 'wb') as f:
        f.write(img)


# 把大图拿出来
def img():
    list = os.listdir('./images')
    for item in list:
        crop_picture(item)


# 切小图
def crop_picture(name):
    image = Image.open('./images/%s' % name)
    for i in range(4):
        x1 = i * 76
        y1 = 0
        x2 = i * 76 + 76
        y2 = 76
        index = (x1, y1, x2, y2)
        cropImg = image.crop(index)
        name = name.split('.')[0]
        cropImg.save('./crop_images/%s_%d.jpeg' % (name, i))


# 图片去重
def unique():
    little_list = os.listdir('./crop_images')
    list = []
    for i in range(len(little_list)):
        for j in range(i+1, len(little_list)):
            filename1 = './crop_images/'+little_list[i]
            filename2 = './crop_images/'+little_list[j]
            compare = get_compare(filename1, filename2)
            # 要删除的图片
            if compare > 80:
                print(compare)
                if little_list[i] not in list:
                    list.append(little_list[i])
                    # print(list)

    for item in list:
        os.remove('./crop_images/%s' % item)


chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
# 显式等待 针对某个节点的等待
wait = WebDriverWait(browser, 10)


def get_page():
    url = 'http://www.1kkk.com/'
    browser.get(url)
    btn1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.header-avatar')))
    btn1.click()
    time.sleep(5)
    # 保存网页截图
    big_image = browser.get_screenshot_as_png()
    big_image = Image.open(BytesIO(big_image))
    big_image.save('./web_code_img/big_image.png')
    time.sleep(2)
    username = '522495731@qq.com'
    password = '0616ymj'
    # 用户名
    input_username = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="form-wrap"]/p/input[@name="txt_name"]')))
    # 密码
    input_password = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="form-wrap"]/p/input[@name="txt_password"]')))
    # 换一组
    change = wait.until(
        EC.presence_of_element_located((By.XPATH, '//a[@class="rotate-refresh"]')))
    # 登录
    submit = wait.until(EC.presence_of_element_located((By.XPATH, '//p/button[@id="btnLogin"]')))
    # 验证码的图
    code = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="form-wrap"]/div/div[@class="rotate-background"]')))
    print(code)
    # 填写用户名和密码
    input_username.send_keys(username)
    input_password.send_keys(password)

    # 第一张验证码的坐标
    x1 = code[0].location['x']
    y1 = code[0].location['y']
    size = code[0].size
    width = size['width']
    height = size['height']
    x2 = x1 + width
    y2 = y1 + height
    crop_img1 = big_image.crop((x1, y1, x2, y2))
    crop_img1.save('./web_code_img/1.png')

    # 第二张验证码
    crop_img2 = big_image.crop((x1+2+width, y1, x2+2+width, y2))
    crop_img2.save('./web_code_img/2.png')
    # 第三张验证码
    crop_img2 = big_image.crop((x1+4+width*2, y1, x2+4+width*2, y2))
    crop_img2.save('./web_code_img/3.png')
    # 第四张验证码
    crop_img2 = big_image.crop((x1+6+width*3, y1, x2+6+width*3, y2))
    crop_img2.save('./web_code_img/4.png')

    # 旋转图片进行对比
    result= rotate()
    # 例[0,0,3,0]
    print(result)
    if len(result) < 4:
        change.click()
    # i是循环几个图
    for i in range(len(result)):
        # j是循环点击的次数
        for j in range(result[i]):
            code[i].click()

    submit.click()


def rotate():
    little_list = os.listdir('./crop_images')
    result_list = []
    # 取到截屏的四张验证码小图
    for i in range(1,5):
        count = 0
        flag = False
        filename1 = './web_code_img/'+str(i)+'.png'
        img = Image.open(filename1)
        # 旋转4次
        for j in range(4):
            if j != 0:
                img = img.rotate(-90)
                img.save(filename1)
                count += 1
            for crop_img in little_list:
                filename2 = './crop_images/'+crop_img
                compare = get_compare(filename1, filename2)
                if compare > 90:
                    result_list.append(count)
                    flag = True
                    break
            if flag:
                break
    return result_list





def main():
    # for i in range(100):
    #     save_img()
    #     print(i)
    # img()
    # unique()
    get_page()


if __name__ == '__main__':
    main()

