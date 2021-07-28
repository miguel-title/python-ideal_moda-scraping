#import the datetime in order to get the current time
from datetime import datetime

#import the csv in order to write the data to csv
import csv

#Import the Selenium 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Import the webdriver_manager in order to download the latest chrome driver
from webdriver_manager.chrome import ChromeDriverManager

import time
import random

#Import the os in order to get the current directory
import os
ROOT_PATH = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

class ModaApp():
    def __init__(self, name=""):
        self.name: str = name
        self.driver: webdriver.Chrome = self.make_driver()

        #Set the Constant
        self.BaseUrl = "https://it.trustpilot.com/review/idealmoda.it"


    def make_driver(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        user_data_dir = f"{ROOT_PATH}/cache/user_data{self.name}"

        #Set the Chrome option
        chrome_options.add_argument("--user-data-dir=%s" % user_data_dir)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--log-level=3")

        #download the latest chromedriver automatically
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(10)

        return driver


    def close(self):

    	#Close the slenium driver
        self.driver.quit()


    def home(self):
        driver = self.driver
        try:
            driver.get(self.BaseUrl)
        except Exception as e:
            return False
        return True


    def time_sleep(self, type):
        if type == 1:
            sleeptime = random.randrange(10,100)/100
        elif type == 2:
            sleeptime = random.randrange(70, 200)/100
        elif type == 3:
            sleeptime = random.randrange(100, 300)/100
        elif type == 4:
            sleeptime = random.randrange(150, 400)/100
        elif type == 5:
            sleeptime = random.randrange(400, 500)/100
        elif type == 401:
            sleeptime = random.randrange(60, 100)
        time.sleep(sleeptime)



    def processing(self):
        result = []

        # Get productList and Check(with RTX, GTX, RX)
        driver = self.driver

        isNext = True
        curPage = 1
        while isNext:
            #Get Review Cards
            CardElements = driver.find_elements_by_class_name('review-card  ')

            print('Current Page:{}'.format(curPage))
            print('review count in this page:{}'.format(len(CardElements)))

            for CardElement in CardElements:
                cardResultDic = {'firstName':'', 'lastName':'', 'buyerStatement':'', 'shopComment':'', 'shopComment_creationDate':''}

                #Get Full Name
                name = CardElement.find_element_by_xpath('.//div[@class="consumer-information__name"]').text
                firstName = name.split(' ')[0].strip()
                lastName = name.replace(firstName, '').strip()

                #Get BuyerStatement
                statement_parentelement = CardElement.find_element_by_class_name('star-rating')
                statement = statement_parentelement.find_element_by_xpath('./img').get_attribute('src')

                statementImg = statement.split('/')[-1].strip()

                switcher = {'stars-0.svg':'0', 'stars-1.svg':'1', 'stars-2.svg':'2', 'stars-3.svg':'3', 'stars-4.svg':'4', 'stars-5.svg':'5'}
                statement = switcher.get(statementImg, "Invalid State")

                #Get ShopComment
                
                driver.implicitly_wait(1)
                try:
                    comment = CardElement.find_element_by_class_name('review-content__text').text
                except Exception as e:
                    comment = CardElement.find_element_by_class_name('review-content__title').text
                    
                driver.implicitly_wait(10)
                    
                #Get ShopComment Date
                date = CardElement.find_element_by_class_name('review-content-header__dates').text

                cardResultDic['firstName'] = firstName
                cardResultDic['lastName'] = lastName
                cardResultDic['buyerStatement'] = statement
                cardResultDic['shopComment'] = comment
                cardResultDic['shopComment_creationDate'] = date

                result.append(cardResultDic)

            #Get Next Button
            try:
                nextbutton = driver.find_element_by_class_name('next-page')
                driver.execute_script("arguments[0].click();", nextbutton)
                
                self.time_sleep(4)
                curPage += 1
            except Exception as e:
                print('finished')
                isNext = False

        self.outputToCsv(result)

        return

    def outputToCsv(self, data):
    	#Write the data to CSV file
        keys = data[0].keys()
        outputfilename = datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'
        with open(outputfilename, 'w', newline='', encoding='utf8')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        return


if __name__ == "__main__":
    app = ModaApp()
    app.home()
    app.processing()