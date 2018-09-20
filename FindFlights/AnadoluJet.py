from selenium.webdriver.common.keys import Keys
import time

class AnadoluJet():

    def __init__(self):

        self.url = "https://online.anadolujet.com/schedule"
        self.date = ""
        self.departure_location = ""
        self.arrival_location = ""
        self.departure_times = []
        self.arrival_times = []
        self.prices = []

    def find(self, browser, departure_city, arrival_city, when):

        try:
            print("\n--> Getting " + self.url + "..")
            browser.get(self.url)
        except:
            print("\n>>> ERROR --> Getting " + self.url + ".")
            return "error"


        print("--> Waiting for page to load..")

        initialTime = time.time()
        while(True):
            if (time.time() - initialTime) < 10:
                try:
                    browser.find_element_by_class_name('loading')
                    time.sleep(0.20)
                except:
                    print("\t--> Page loaded.")
                    break
            else:
                print("\n>>> ERROR --> Time out. Page not loaded.")
                return "error"


        print("--> Choosing cities..")

        try:
            browser.find_element_by_xpath('//*[@id="whereFrom"]').click()
        except:
            print("\n>>> ERROR --> Could not be click to @id='whereFrom'.")
            return "error"

        try:
            browser.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(departure_city + Keys.TAB)
        except:
            print("\n>>> ERROR --> Could not be sent keys of " + departure_city + ".")
            return "error"

        try:
            browser.find_element_by_xpath('/html/body/span/span/span[1]/input').send_keys(arrival_city + Keys.ENTER)
        except:
            print("\n>>> ERROR --> Could not be sent keys of " + arrival_city + ".")
            return "error"


        print("--> Looking for date..")
        print("\t--> Looking for month..")

        user_day = when.split(' ')[0]
        user_month = when.split(' ')[1]

        initialTime = time.time()
        while True:
            if (time.time() - initialTime) < 10:
                try:
                    fly_month = browser.find_element_by_class_name('ui-datepicker-month').text

                    if user_month.lower() == fly_month.lower():
                        datepicker_ID = browser.find_element_by_class_name('datepicker-wrapper').get_attribute('id')
                        dates = browser.find_element_by_xpath('//*[@id="' + datepicker_ID + '"]/div/div[1]/table/tbody')

                        print("\t\t--> Looking for day..")
                        for day in dates.find_elements_by_tag_name('td'):
                            if day.text == user_day:
                                day.click()
                                break
                        break
                    else:
                        next_month = browser.find_element_by_class_name('ui-datepicker-next')
                        next_month.click()
                except:
                    print("\n>>> ERROR --> Date could not selected.")
                    return "error"
            else:
                print("\n>>> ERROR --> Time out. Date could not found.")
                return "error"


        try:
            print("--> Clicking to one-way..")
            one_way = browser.find_element_by_class_name('onoffswitch-cont')
            one_way.click()
        except:
            print("\n>>> ERROR --> Could not click to 'one way' button.")
            return "error"


        try:
            print("--> Submitting..")
            submit = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/form/div/div[11]/button')
            submit.click()
        except:
            print("\n>>> ERROR --> Could not click to 'submit' button.")
            return "error"


        print("--> Waiting for page to load..")

        initialTime = time.time()
        while True:
            if (time.time() - initialTime) < 10:
                try:
                    browser.find_element_by_class_name('loading')
                    time.sleep(0.20)
                except:
                    print("\t--> Page loaded.")
                    break
            else:
                print("\n>>> ERROR --> Time out. Page not loaded.")
                return "error"

        try:
            print("--> Pulling data..")
            self.date = browser.find_element_by_class_name('date-title')
            self.departure_location = browser.find_element_by_class_name('departure-location')
            self.arrival_location = browser.find_element_by_class_name('arrival-location')
            departure_times = browser.find_elements_by_class_name('departure-time')
            arrival_times = browser.find_elements_by_class_name('arrival-time')
            prices = browser.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[2]/div[5]').find_elements_by_class_name(
                'price')
        except:
            print("\n>>> ERROR --> Could not pull data successfully.")
            return "error"

        try:
            self.date = self.date.text
            self.departure_location = self.departure_location.text
            self.arrival_location = self.arrival_location.text

            for i in departure_times:
                self.departure_times.append(i.text)

            for i in arrival_times:
                self.arrival_times.append(i.text)

            for i in prices:
                self.prices.append(i.text)
        except:
            print("\n>>> ERROR --> Could not edit data successfully.")
            return "error"

        print("\t--> Returning data..")
        return [self.date, self.departure_location, self.arrival_location,
                self.departure_times, self.arrival_times, self.prices]