import random
import time
from selenium import webdriver
url_name = input('请输入问卷调查的网址：')
url = url_name
def mutile_random(a,b,c):
    p = []
    while len(p)<c:
        number = random.randint(a,b)
        if number not in p:
            p.append(number)
    return p

# 修改driver的值为false
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
# driver = webdriver.Chrome()
# f = open('stealth.min.js',mode = 'r',encoding='utf-8').read()
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{'source':f})
#对付单选
def single(number):
    time.sleep(1)
    driver.get(url)
    for i in number:
        one_option = driver.find_elements_by_xpath(f'//*[@id="div{i}"]'+'/div[2]/div')
        number = random.randint(1,len(one_option))
        driver.find_element_by_css_selector(f'#div{i} > div.ui-controlgroup.column1 > div:nth-child({number}) > div').click()

#对付多选
def mutile(numbers):
    for j in numbers:
        mutile_option = driver.find_elements_by_xpath(f'//*[@id="div{j}"]'+'/div[2]/div')
        number = random.randint(2,len(mutile_option))
        a = mutile_random(1,len(mutile_option),number)
        for click_number in a:
            driver.find_element_by_css_selector(f'#div{j} > div.ui-controlgroup.column1 > div:nth-child({click_number}) > div').click()
def summit():
    driver.find_element_by_xpath('//*[@id="ctlNext"]').click()
    time.sleep(1)
    if '<div class="sm-ico-wave"></div>' in driver.page_source: #检测这个元素是否在网页源代码中
        driver.find_element_by_xpath('//*[@id="SM_BTN_1"]/div[1]/div[4]').click()
        time.sleep(3)
    if 'class="nc_iconfont btn_slide' in driver.page_source:
        splide = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        webdriver.ActionChains(driver).click_and_hold(on_element=splide).perform()#让鼠标执行，点击元素并按住
        webdriver.ActionChains(driver).move_by_offset(xoffset=300,yoffset=0).perform()#往x轴移动
        webdriver.ActionChains(driver).pause(0.5).release().perform()#暂停0.5s后松开
if __name__ =='__main__':
    x = input('请输入单选题号(注意用逗号隔开哦!)：')
    x_lst = x.split(',')
    x_lst = [int(x_lst[i]) for i in range(len(x_lst))]  # 将字符串整形化

    mutile_options = input('请输入多选题号(注意用逗号隔开哦!)：')
    j_lst = mutile_options.split(',')
    j_lst = [int(j_lst[i]) for i in range(len(j_lst))]  # 将字符串整形化
    while(1):
        single(x_lst)
        mutile(j_lst)
        summit()
