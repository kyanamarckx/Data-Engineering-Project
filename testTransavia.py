import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import json


start_date = datetime.date(2023, 4, 1)
# end_date = datetime.date(2023, 10, 1)
end_date = datetime.date(2023, 4, 2)
delta = datetime.timedelta(days=1)

dates = []

while start_date < end_date:
    dates.append(start_date.strftime('%d/%m/%Y'))
    start_date += delta

print(dates)

destinations = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'SPC', 'TFS']
destinations = ['Corfu, Griekenland']
# destinations = ['CFU']


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# chrome_options.add_argument("--incognito")
chrome_options.add_extension("./extension/buster.crx")

for date in dates:
    for destination in destinations:
        # Instantiate the Chrome driver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # chrome_options.add_argument("--incognito")
        chrome_options.add_extension("./extension/buster.crx")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        time.sleep(5)

        URL = "https://www.transavia.com/nl-BE/boek-een-vlucht/vluchten/zoeken/"
        URL = "https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/"

        driver.get(URL)

        time.sleep(5)

        # driver.implicitly_wait(25)

        try:
          cookies = driver.find_element(By.CLASS_NAME, "cb__button--accept-all").click()
        except:
          pass

        # try:
        #   #  captcha = driver.find_element(By.CLASS_NAME, "recaptcha-anchor")
        #   captcha = driver.execute_script("document.getElementById('recaptcha-anchor').click();")
        #   captcha2 = driver.find_element(By.ID, "rc-anchor-container")._execute(Command.CLICK_ELEMENT)
        #   captcha1 = driver.find_element(By.ID, "recaptcha-anchor")
        #   captcha3 = driver.find_element(By.ID, "rc-anchor-alert")._execute(Command.CLICK_ELEMENT)
        #   captcha4 = driver.find_element(By.CLASS_NAME, "rc-anchor-content")._execute(Command.CLICK_ELEMENT)
        #   captcha5 = driver.find_element(By.ID, "recaptcha-accessible-status")._execute(Command.CLICK_ELEMENT)
        #   captcha6 = driver.find_element(By.CLASS_NAME, "form_container")._execute(Command.CLICK_ELEMENT)
        #   captcha7 = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")._execute(Command.CLICK_ELEMENT)
        #   captcha8 = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-checkmark")._execute(Command.CLICK_ELEMENT)
        #   captcha9 = driver.find_element(By.CLASS_NAME, "g-recaptcha")._execute(Command.CLICK_ELEMENT)
        #   captcha10 = driver.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]")._execute(Command.CLICK_ELEMENT)
        #   # captcha1.submit()
        #   captcha1.click()
           
        # except:
        #   pass

        try:
          captcha = driver.find_element(By.TAG_NAME, "iframe")
          # frame = driver.switch_to.frame(captcha)
          body = captcha.find_element(By.TAG_NAME, "body")
          div = body.find_element(By.ID, "rc-anchor-alert")
          body.click()
          div.click()
          # frame.



          solver = driver.find_element(By.ID, "solver-button").click()
        except:
          print("no captcha")


        # time.sleep(30)
           
        time.sleep(5)

        # departureAirport = driver.find_element(By.ID, "countryStationSelection_Origin-input").click()
        # departureAirport.send_keys("Brussel, België")
        # departureAirport = driver.execute_script("document.getElementById('routeSelection_DepartureStation-input').value='Brussel, België'")
        departureAirport = driver.execute_script("document.getElementById('countryStationSelection_Origin-input').value='Brussel, België'")

        time.sleep(5)

        # # arrivalAirport = driver.find_element(By.ID, "countryStationSelection_Destination-input").click()
        # # arrivalAirport.send_keys(destination)
        # arrivalAirport = driver.execute_script("document.getElementById('routeSelection_ArrivalStation-input').value='" + destination + "';")
        arrivalAirport = driver.execute_script("document.getElementById('countryStationSelection_Destination-input').value='" + destination + "';")

        # departureDate = driver.execute_script("document.getElementById('dateSelection_OutboundDate-datepicker').value='" + date + "';")

        # oneway = driver.execute_script("document.getElementById('dateSelection_IsReturnFlight').value='false';")

        titles = driver.find_elements(By.CLASS_NAME, "h5")

        departureTitle = titles[2]
        departureTitle.find_element(By.XPATH, "..")
        departureTitle.click()

        specificDate = driver.find_element(By.ID, "data-type-data")
        specificDate.find_element(By.XPATH, "..").click()

        time.sleep(5)

        selectList = driver.find_element(By.ID, "data-flight-type")
        allOptions = selectList.find_elements(By.TAG_NAME, "option")
        for option in allOptions:
            if option.get_attribute("value") == "Single":
                option.click()
                break
            
        time.sleep(5)
            
        departureDate = driver.execute_script("document.getElementById('timeFrameSelection_SingleFlight_OutboundDate-datepicker').value='" + date + "';")

        time.sleep(5)

        search = driver.find_element(By.CLASS_NAME, "button-primary").click()
            

        
        time.sleep(50)


