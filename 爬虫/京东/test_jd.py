from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import sqlalchemy_helper_jd

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)


def get_page(page):
    if page == 1:

        url = 'https://www.jd.com'
        browser.get(url)

    # print(browser.page_source)

        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key')))
        input.clear()
        input.send_keys('无人机')

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search button.button')))
        submit.click()

        time.sleep(5)
        # print(browser.current_url)

    if page > 1:
        # 填入页码编号
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage input.input-txt')))
        input.clear()
        input.send_keys(page)

        # 点击下一页
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage .btn.btn-default')))
        submit.click()

    for i in range(16):
        str_js = 'var step = document.body.scrollHeight / 16; window.scrollTo(0, step * %d)' % (i + 1)
        browser.execute_script(str_js)
        time.sleep(1)

    return browser.page_source


    # 16是分割页面的,document.body.scrollHeight整个页面可以滚的总高度



def parse_page(page_source):
    html_etree = etree.HTML(page_source)
    big_content = html_etree.xpath('//div[@id="J_goodsList"]//li')
    list1 = []
    for item in big_content:

        picture = item.xpath('./div[@class="gl-i-wrap"]//img/@src')
        if len(picture) == 0:
            picture = ''
        else:
            picture = picture[0]

        sku = item.xpath('./@data-sku')[0]
        title = item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/em//text()')
        title = ''.join(title)
        price = item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]//i/text()')[0]
        comment = item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-commit"]//a/text()')[0]
        detail = item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@href')[0]
        store = item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-shop"]//a/text()')
        if len(store) == 0:
            store = ''
        else:
            store = store[0]

        # 放列表
        dict1 = {}
        dict1['sku'] = sku
        dict1['title'] = title
        dict1['price'] = price
        dict1['picture'] = picture
        dict1['comment'] = comment
        dict1['detail'] = detail
        dict1['store'] = store
        list1.append(dict1)
    return list1


def main():
    for page in range(100):
        # print(page)
        html = get_page(page + 1)
        result_list = parse_page(html)
        sqlalchemy_helper_jd.save_db(result_list)

if __name__ == '__main__':
    main()