import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

# Selenium设置
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

# 获取货币名称
def get_currency_names(driver):
    try:
        currency_names = driver.find_element(By.XPATH, '//*[@id="pjname"]').text.split('\n')
        currency_names = [item.strip() for item in currency_names if item.strip() != '']
    except Exception as e:
        print(f"Error getting currency names: {e}")
        currency_names = []
    return currency_names

# 主程序
def main():
    url = 'https://www.boc.cn/sourcedb/whpj/'
    driver.get(url)

    date = input("请输入日期(如20211231)：")
    currency_code = input("请输入货币代号(如USD)")

    finally_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"  # 获取日期
    currency_names = get_currency_names(driver)
    currency_names.pop(0)

    code = ['GBP', 'HKD', 'USD', 'CHF', 'SGD', 'SEK', 'DKK', 'NOK', 'JPY', 'CAD', 'AUD', 'EUR', 'MOP', 'PHP', 'THP',
            'NZD', 'KRW', 'SUR', 'BND', 'TWD', 'ESP', 'ITL', 'NLG', 'BEF', 'FIM', 'IDR', 'BRC', 'AED', 'INR', 'ZAR',
            'SAR', 'TRY']
    currency_dict = dict(zip(code, currency_names))  # 组合成一个货币代码和对应货币的字典
    symbol = currency_dict.get(currency_code, "")  # 根据货币代码映射对应货币名

    # 输入日期
    driver.find_element(By.XPATH, '//*[@id="erectDate"]').click()
    driver.find_element(By.XPATH, '//*[@id="erectDate"]').send_keys(finally_date)
    driver.find_element(By.XPATH, '//*[@id="nothing"]').click()
    driver.find_element(By.XPATH, '//*[@id="nothing"]').send_keys(finally_date)
    driver.find_element(By.XPATH, '//*[@id="calendarClose"]').click()

    # 选择下拉框中的选项
    driver.find_element(By.XPATH, '//*[@id="pjname"]').click()
    dropdown = Select(driver.find_element(By.XPATH, '//*[@id="pjname"]'))
    dropdown.select_by_value(symbol)

    # 点击查询
    driver.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]').click()

    # 获取现汇卖出价
    sell_rate = driver.find_element(By.XPATH, '/html/body/div/div[4]/table/tbody/tr[2]/td[4]').text
    print(sell_rate)

if __name__ == "__main__":
    main()
