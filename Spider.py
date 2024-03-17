from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import argparse

class Spider:
    def __init__(self, args):
        self.date = args.date
        self.code = args.code
        self.url = "https://www.boc.cn/sourcedb/whpj/"
        self.savePath = "D:\\面经\\世游科技\\笔试\\result.txt"
        self.encoding = "gbk"
        self.isPrint = False
        self.year, self.month, self.day = self.deal_date()
        self.currency = self.map_code()

    def deal_date(self):
        year = self.date[:4]
        month = self.date[4:6]
        day = self.date[6:]
        return str(year), str(month), str(day)

    def map_code(self):
        currency_name_mapping = {
            "GBP": "英镑",
            "HKD": "港币",
            "USD": "美元",
            "CHF": "瑞士法郎",
            "DEM": "德国马克",
            "FRF": "法国法郎",
            "SGD": "新加坡元",
            "SEK": "瑞典克朗",
            "DKK": "丹麦克朗",
            "NOK": "挪威克朗",
            "JPY": "日元",
            "CAD": "加拿大元",
            "AUD": "澳大利亚元",
            "EUR": "欧元",
            "MOP": "澳门元",
            "PHP": "菲律宾比索",
            "THB": "泰国铢",
            "NZD": "新西兰元",
            "KRW": "韩国元",
            "RUB": "卢布",
            "MYR": "林吉特",
            "TWD": "新台币",
            "ESP": "西班牙比塞塔",
            "ITL": "意大利里拉",
            "NLG": "荷兰盾",
            "BEF": "比利时法郎",
            "FIM": "芬兰马克",
            "INR": "印度卢比",
            "IDR": "印尼卢比",
            "BRL": "巴西里亚尔",
            "AED": "阿联酋迪拉姆",
            "ZAR": "南非兰特",
            "SAR": "沙特里亚尔",
            "TRY": "土耳其里拉"
        }
        return currency_name_mapping.get(self.code)

    def run(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(2)

        elsments = driver.find_elements(By.XPATH, "//div[@class='search_bar']/input[@class='search_ipt']")
        if len(elsments) >= 3:
            buttonStartTime = elsments[1]
            buttonEndTime = elsments[2]

        # 起始时间
        buttonStartTime.click()
        time.sleep(2)
        dropdownStartYear = driver.find_element(By.XPATH, "//select[@id='calendarYear']")
        dropdownStartMonth = driver.find_element(By.XPATH, "//select[@id='calendarMonth']")
        select = Select(dropdownStartYear)
        select.select_by_value(self.year)
        select = Select(dropdownStartMonth)
        select.select_by_value(self.month)
        time.sleep(2)
        day = driver.find_element(By.XPATH, "//table[@id='calendarTable']//td[text()='1']")
        day.click()
        time.sleep(2)

        # 结束时间
        buttonEndTime.click()
        time.sleep(2)
        dropdownEndYear = driver.find_element(By.XPATH, "//select[@id='calendarYear']")
        dropdownEndMonth = driver.find_element(By.XPATH, "//select[@id='calendarMonth']")
        select = Select(dropdownEndYear)
        select.select_by_value(self.year)
        select = Select(dropdownEndMonth)
        select.select_by_value("10")
        time.sleep(2)
        day = driver.find_element(By.XPATH, "//table[@id='calendarTable']//td[text()='1']")
        day.click()
        time.sleep(2)

        # 牌价选择
        dropdownCurrency= driver.find_element(By.XPATH, "//select[@id='pjname']")
        select = Select(dropdownCurrency)
        select.select_by_value(self.currency)
        time.sleep(2)

        # 点击查询
        searchBtn = driver.find_elements(By.XPATH, "//input[@class='search_btn']")[1]
        searchBtn.click()
        time.sleep(2)

        # 找出共多少页
        totalPage = driver.find_element(By.XPATH, "//div[@class='turn_page']//li[contains(text(),'共') and contains(text(),'页')]")
        totalPage_text = totalPage.text
        totalPages = int(totalPage_text.split('共')[1].split('页')[0])
        print("共{}页".format(totalPages))

        data = []
        # 遍历每一页
        while totalPages > 0:

            # 现汇卖出价
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")[1:]
            if len(rows) == 0:
                print("没有数据")
            
            
            # 遍历每个tr元素
            for row in rows:
                # 找到tr元素下的第1、第2和第3个td元素
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 7:
                    publishTime = columns[6].text
                    currency = columns[0].text
                    sellRate = columns[3].text
                    if not self.isPrint:
                        print(sellRate)
                        self.isPrint = True
                    # 将数据添加到列表中
                    data.append([publishTime, currency, sellRate])

            # 下一页
            nextPage = driver.find_element(By.XPATH, "//li[@class='turn_next']")
            nextPage.click()

            totalPages -= 1
            time.sleep(2)

        # 关闭浏览器
        driver.quit()

        # 保存数据
        df = pd.DataFrame(data, columns=["发布时间", "货币名称", "现汇卖出价"])
        # 将数据写入文件
        df.to_csv(self.savePath, index=False, encoding=self.encoding)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default="20221001")
    parser.add_argument("--code", type=str, default="USD")
    args = parser.parse_args()
    spider = Spider(args)
    spider.run()