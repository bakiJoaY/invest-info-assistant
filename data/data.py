import akshare as ak
from bs4 import BeautifulSoup as BS

import time
from selenium.webdriver.edge.options import Options
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException

from langchain_community.document_loaders import WebBaseLoader
import bs4

# todo 该部分后续改为schdule任务
def init_hot_stock_concept():
    print(r"today's hotest concept is: ")
    #通过akshare库获取今天最火的概念板块
    hottestStock = ak.stock_board_concept_name_em().iloc[0]['板块名称']
    print(hottestStock)
    hottestList = ak.stock_board_concept_cons_em(symbol=hottestStock)['代码'].astype(str).to_list()
    print(hottestList)

    reportAddrList = []

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    #由于存放研报链接的网页是异步加载的，所以此处使用selenium进行爬取
    #先跳过 “广告” 遮罩层modal
    edge_option = Options()
    browser = wd.Edge(edge_option)
    targetUrl = f'https://data.eastmoney.com/report/{hottestList[0]}.html'
    browser.get(targetUrl)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.wztctg')))
    closeBtn = browser.find_element(By.CSS_SELECTOR, 'img.wztctg')
    closeBtn.click()

    for stockCode in hottestList:
        targetUrl = f'https://data.eastmoney.com/report/{stockCode}.html'
        browser.get(targetUrl)
        try:
            WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#singlestock_table tbody')))
            listOfALink = browser.find_elements(By.CSS_SELECTOR, '#singlestock_table tbody tr td:nth-child(2) a')
            for aLink in listOfALink:
                reportAddrList.append(aLink.get_attribute('href'))
            # todo 此处就先加载1页数据，后续可以改为加载多页数据
            break
        except NoSuchElementException:
            continue
    browser.close()
    print(reportAddrList)

    #获取到研报地址后，通过webBaseLoader获取研报数据

    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = bs4.SoupStrainer(class_=(["ctx-content"]))

    docList = []
    for reportAddr in reportAddrList:
        loader = WebBaseLoader(
            web_paths=(reportAddr,),
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = loader.load()
        docList.append(docs)
    
    return docList


