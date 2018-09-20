from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from AnadoluJet import AnadoluJet
from PegasusFly import PegasusFly
from DataBase import DataBase

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")

if __name__ == '__main__':

    if input("Do you want headless mode (yes:no) --> ").lower() == 'yes':
        chrome_options.add_argument("--headless")

    whereFrom = "İzmir"
    whereTo = "Ankara"
    when = "26 Kasım"

    while True:
        mainStart = time.time()

        print("--> Browser creating..")
        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.maximize_window()
        except:
            print("\n>>> ERROR --> Could not create a browser.")
            print("--> Program was terminated.")
            break


        anadoluJetData = AnadoluJet().find(browser, whereFrom, whereTo, when)
        if anadoluJetData == "error":
            print("\n>>> Yukarıdaki hata 'anadolujet' kısmında oluşmuştur.")
            print("--> Program was terminated.")
            break
        dataBaseSituation1 = DataBase().write("AnadoluJet", anadoluJetData, 0)
        dataBaseSituation2 = DataBase().write("NewAnadoluJet", anadoluJetData, 1)
        if dataBaseSituation1 == "error" or dataBaseSituation2 == "error":
            print("\n>>> Yukarıdaki hata 'database write - AnadoluJet' kısmında oluşmuştur.")
            print("--> Program was terminated.")
            break


        whereFrom = "Izmir"
        pegasusFlyData = PegasusFly().find(browser, whereFrom, whereTo, when)
        if pegasusFlyData == "error":
            print("\n>>> Yukarıdaki hata 'pegasus' kısmında oluşmuştur.")
            print("--> Program was terminated.")
            break
        dataBaseSituation1 = DataBase().write("Pegasus", pegasusFlyData, 0)
        dataBaseSituation2 = DataBase().write("NewPegasus", pegasusFlyData, 1)
        if dataBaseSituation1 == "error" or dataBaseSituation2 == "error":
            print("\n>>> Yukarıdaki hata 'database write - PegasusFly' kısmında oluşmuştur.")
            print("--> Program was terminated.")
            break


        print("\n--> Closing from browser..")
        try:
            browser.close()
            print("\t--> Close successfully.")
        except:
            print("\n>>> ERROR --> Could not close browser.")

        print("--> Program was terminated successfully.")

        mainEnd = time.time()
        print("\nTotal Main Time: " + str(mainEnd - mainStart) + " seconds.")


        DataBase().display("NewAnadoluJet")
        DataBase().display("NewPegasus")
        break