from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import keys
import time

#Consts#
choromeDriverPath = "D:\Program Files\choromedriver.exe"
cookieGameURL = "http://orteil.dashnet.org/experiments/cookie/"

#Driver Setup#
driverService = Service(executable_path=choromeDriverPath)
driver = webdriver.Chrome(service=driverService)

driver.get(cookieGameURL)

cookie = driver.find_element("id", "cookie")

upgrades = driver.find_elements("css selector", "#store div")
upgradesIds = [upgrade.get_attribute("id") for upgrade in upgrades]

#Game state variable#
gameOver = False

#Time variables#
timeOut = time.time() + 60*5
buyTime = time.time() + 2

#Main loop#
while not gameOver:
    cookie.click()

    if time.time() > buyTime:
        upgradesPrices = driver.find_elements("css selector", "#store b")
        priceList = []

        for price in upgradesPrices:
            content = price.text
            if content != "":
                value = int(content.split("-")[1].strip().replace(",", ""))
                priceList.append(value)

        cookiesUpgrades = {}
        for i in range(len(priceList)):
            cookiesUpgrades[priceList[i]] = upgradesIds[i]

        moneyElement = driver.find_element("id", "money").text
        if "," in moneyElement:
            moneyElement = moneyElement.replace(",", "")
        money = int(moneyElement)

        affordableUpgrades = {}

        for cost, id in cookiesUpgrades.items():
            if money > cost:
                affordableUpgrades[cost] = id

        fancierUpgrade = max(affordableUpgrades)
        print(fancierUpgrade)
        fancierUpgradeID = affordableUpgrades[fancierUpgrade]

        if fancierUpgradeID != "":
            driver.find_element("id", fancierUpgradeID).click()
        else:
            pass

        buyTime = time.time() + 5

    if time.time() > timeOut:
        gameOver = True

time.sleep(3)