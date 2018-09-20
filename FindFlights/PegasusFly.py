import time

class PegasusFly():

    def __init__(self):

        self.url = "https://www.flypgs.com"
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


        try:
            print("--> Clicking to one-way..")
            one_way = browser.find_element_by_xpath('//*[@id="fligth-searh"]/div[1]/label[2]')
            one_way.click()
        except:
            print("\n>>> ERROR --> Could not click to 'one way' button.")
            return "error"


        print("--> Choosing cities..")

        try:
            browser.find_element_by_xpath('//*[@id="fligth-searh"]/div[2]/span[1]/span[1]/span[1]/span/span[2]').click()
        except:
            print("\n>>> ERROR --> Could not be click to @id='flight-searh'.")
            return "error"

        try:
            for departure_location in browser.find_elements_by_class_name('select2-results__option'):
                if departure_city == departure_location.text:
                    departure_location.click()
                    break
        except:
            print("\n>>> ERROR --> Could not select departure city.")
            return "error"

        time.sleep(0.5)

        try:
            for arrival_location in browser.find_elements_by_class_name('select2-results__option'):
                if arrival_city == arrival_location.text:
                    arrival_location.click()
                    break
        except:
            print("\n>>> ERROR --> Could not select arrival city.")
            return "error"


        print("--> Looking for date..")
        print("\t--> Looking for month..")

        months = {"OCAK": "ocak", "ŞUBAT": "şubat", "MART": "mart", "NISAN": "nisan",
                 "MAYIS": "mayıs", "HAZIRAN": "haziran", "TEMMUZ": "temmuz", "AĞUSTOS": "ağustos",
                 "EYLÜL": "eylül", "EKIM": "ekim", "KASIM": "kasım", "ARALIK": "aralık"}

        user_day = when.split(' ')[0]
        user_month = when.split(' ')[1]

        initialTime = time.time()
        while True:
            if (time.time() - initialTime) < 10:
                try:
                    fly_month = browser.find_element_by_class_name('ui-datepicker-month').text
                except:
                    print("\n>>> ERROR --> Could not get current month.")
                    return "error"

                if len(fly_month) > 0:
                    try:
                        if user_month.lower() == months[fly_month]:
                            dates = browser.find_element_by_xpath('//*[@id="pgs-departure-datepicker"]/div/div[1]/table/tbody')

                            print("\t\t--> Looking for day..")
                            for day in dates.find_elements_by_tag_name('td'):
                                if (day.text == user_day):
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
            print("--> Submitting..")
            submit = browser.find_element_by_xpath('//*[@id="fligth-searh"]/button')
            submit.click()
        except:
            print("\n>>> ERROR --> Could not click to 'submit' button.")
            return "error"


        try:
            print("--> Pulling data..")
            self.date = browser.find_element_by_class_name('date')
            self.departure_location = browser.find_element_by_class_name('start')
            self.arrival_location = browser.find_element_by_class_name('end')

            currentDay = browser.find_element_by_id('flightActualDayContainerDEP')
            departure_times = currentDay.find_elements_by_class_name('sleft')
            arrival_times = currentDay.find_elements_by_class_name('sright')
            prices = currentDay.find_elements_by_class_name('flightPrice')
        except:
            print("\n>>> ERROR --> Could not pull data successfully.")
            return "error"

        try:
            self.date = self.date.text
            self.departure_location = self.departure_location.text
            self.arrival_location = self.arrival_location.text

            for i in departure_times:
                self.departure_times.append(i.text.split('\n')[1])

            for i in arrival_times:
                self.arrival_times.append(i.text.split('\n')[1])

            for i in range(0, len(prices), 3):
                self.prices.append(prices[i].text)
        except:
            print("\n>>> ERROR --> Could not edit data successfully.")
            return "error"

        print("\t--> Returning data..")
        return [self.date, self.departure_location, self.arrival_location,
                self.departure_times, self.arrival_times, self.prices]