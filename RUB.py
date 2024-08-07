from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import requests
from bs4 import BeautifulSoup
import re

from selenium.common.exceptions import NoSuchElementException




def open_driver():
    driver = webdriver.Edge()
    #time.sleep(5)
    return driver

def get_currency_rates(currency_symbol,price):
    # Set up the Selenium webdriver
    driverr = webdriver.Edge()
    driverr.get("https://converter.somespecial.one/")
    time.sleep(5)  # Wait for the page to load
        
    currency_input = driverr.find_element(By.CSS_SELECTOR, f"input#{currency_symbol}")
    currency_input.clear()
    currency_input.send_keys(price)
    
    # Extract the currency rates from the DOM
    currency_elements = driverr.find_elements(By.CSS_SELECTOR, "div.rate-line input")
    
    currency_rates = {}
    for element in currency_elements:
        currency_name = element.get_attribute("id")
        currency_value = float(element.get_attribute("value"))
        currency_rates[currency_name] = currency_value
    time.sleep(4)
    driverr.quit()
    return currency_rates


def extract_price(s, driver):
    # Find the price in the string using a regular expression
    #print(s)
    
    if '$' in s:
        #print(s)
        price = s.replace("$", "")
        #print(price)
        if len(price) >= 6:
            price = float(price.replace(",", "", 1))
            currency_symbol = 'USD'
            currency_rates = get_currency_rates(currency_symbol,price)
            price = currency_rates['RUB']
            return price
        elif len(price) <= 6:
            if "," in price:
                price = float(price.replace(",", "."))
                currency_symbol = 'USD'
                currency_rates = get_currency_rates(currency_symbol,price)
                price = currency_rates['RUB']
                return price
            
            if not "," in price:
                currency_symbol = 'USD'
                currency_rates = get_currency_rates(currency_symbol,price)
                price = currency_rates['RUB']
                return price
        
    if not '$' in s:
        price_match = re.search(r'(\d+(?:[.,]\d+.\d+))', s)
        if price_match:
            price_str = price_match.group(1)
            #print(price_str)
            if len(price_str) > 6:
                price = float(price_str.replace(",", "", 1))
                
            elif len(price_str) < 6:
                price = float(price_str.replace(",", "."))
    
            # Determine the currency symbol from the string
            currency_symbol = None
            if '€' in s:
                currency_symbol = 'EUR'
            elif '$' in s:
                currency_symbol = 'USD'
            elif '¥' in s:
                currency_symbol = 'CNY'
            elif 'zł' in s:
                currency_symbol = 'PLN'
            elif '₸' in s:
                currency_symbol = 'KZT'
            elif 'pуб.' in s:
                currency_symbol = 'RUB'
            elif '£' in s:
                    currency_symbol = 'CNY'
            else:
                raise ValueError(f"Unsupported currency symbol in string: {s}")
    
            # Get the currency exchange rates
            currency_rates = get_currency_rates(currency_symbol,price)
    
            # Convert the price to RUB using the exchange rate
            price = currency_rates['RUB']
    
            return price
        else:
            return 0



 

 



def processing_page(url):
    driver = open_driver()
    driver.get(url)

    # Wait for the page to load
    time.sleep(15) 
    try:    
        try:
    
            price_elements = driver.find_elements(By.XPATH, "//span[@class='market_commodity_orders_header_promote']")
            price_element_sell = price_elements[1]
            price_element_bay = price_elements[3]
            
            # Get the text of the price element
            price_sell = price_element_sell.text
            price_bay = price_element_bay.text
            price_sell = extract_price(price_sell,driver)
            price_bay = extract_price(price_bay,driver)
            # Print the price
            #print("Запрос на продажу:",price_sell,'pуб.')
            #print()
            #print("Запрос на покупку:",price_bay,'pуб.')
            
            #print()
            neme_elenment_item =  driver.find_element(By.XPATH, "//div[@class='market_listing_nav']")
            neme_item = neme_elenment_item.text
            game, item = neme_item.split(" > ")
            #print("Game:", game)
            #print("Item:", item)
            
            try:
                item_type_match = re.search(r"(StatTrak™)", item)
                item_type = item_type_match.group() if item_type_match else None
                if item_type_match:
                    item = re.sub(r"StatTrak™\s+", "", item)
                
                item_type, item_name_quality = item.split(" | ")
                item_name, item_quality = item_name_quality.split(" (")
                item_quality = item_quality.rstrip(")")
                #print("Item type:", item_type)
                #print("Item name:", item_name)
                #print("Item quality:", item_quality)
                
                url=url
                price_sell=price_sell
                price_bay=price_bay 
                game=game
                item_type=item_type
                item_name=item_name
                item_quality=item_quality
            

                return url, price_sell, price_bay , game ,item_type , item_name , item_quality
                
            except:
                #print("Item:", item)
                #print()
                url=url
                price_sell=price_sell
                price_bay=price_bay 
                game=game
                item_type=None
                item_name=item
                item_quality=None
                
                
   
                return url, price_sell, price_bay , game ,item_type , item_name , item_quality

        except:
            
            
            # Find the price element
            price_elements_sell = driver.find_elements(By.XPATH, "//span[@class='market_table_value']")
            price_element_bay = driver.find_element(By.XPATH, "//div[@id='market_commodity_buyrequests']")
            
            #for price_element in price_elements_sell:
            #    price_sell = price_element.text
                #print(price_sell)
                
            #    items = price_sell.split('\n')
            #    prices_sell = [extract_price(item,driver) for item in items]
            #    
            #    for price_sell in prices_sell:
            #        #print(round(price_sell))
            #        price_sell = round(price_sell)
            #        break
            
            for price_element in price_elements_sell:
                price_sell = price_element.text
            
                items = price_sell.split('\n')
                prices_sell = [extract_price(item, driver) for item in items]
            
                # Extract only the first price from the list
                price_sell = prices_sell[0] if prices_sell else 0
                #price_sell = round(price_sell)
                break  # Break after the first iteration

            
            #print()
            #print("Запрос на продажу:",price_sell,'pуб.')
            #print()
            
            price_bay = price_element_bay.text
    
            starting_price = extract_price(price_bay,driver)
            #rounded_price = round(starting_price)
            price_bay = starting_price
            #print("Запрос на покупку:",price_bay,'pуб.')
            #
            #print()
            
            neme_elenment_item =  driver.find_element(By.XPATH, "//div[@class='market_listing_nav']")
            neme_item = neme_elenment_item.text
            game, item = neme_item.split(" > ")
            #print("Game:", game)
            #print()
            #print("Item:", item)
            #print()
            try:
                item_type_match = re.search(r"(StatTrak™)", item)
                item_type = item_type_match.group() if item_type_match else None
                if item_type_match:
                    item = re.sub(r"StatTrak™\s+", "", item)
                
                item_type, item_name_quality = item.split(" | ")
                item_name, item_quality = item_name_quality.split(" (")
                item_quality = item_quality.rstrip(")")
                #print("Item type:", item_type)
                #print("Item name:", item_name)
                #print("Item quality:", item_quality)
                
                url=url
                price_sell=price_sell
                price_bay=price_bay 
                game=game
                item_type=item_type
                item_name=item_name
                item_quality=item_quality
                

                return url, price_sell, price_bay , game ,item_type , item_name , item_quality
                
            except:
                #print("Item:", item)
                #print()
                
                url=url
                price_sell=price_sell
                price_bay=price_bay 
                game=game
                item_type=None
                item_name=item
                item_quality=None
                

            


                return url, price_sell, price_bay , game ,item_type , item_name , item_quality
            # Close the driver
            driver.quit()



            
    except NoSuchElementException:
        driver.quit()
        time.sleep(15)
        print("Попробуем опять")
        processing_page(url)
        
     


#url = "https://steamcommunity.com/market/listings/730/Kilowatt%20Case"
#processing_page(url)

#url, price_sell, price_bay , game ,item_type , item_name , item_qualit = processing_page(url)

#print(" url=", url ,"\n",
#      "price_sell=", price_sell ,"\n", 
#      "price_bay=", price_bay ,  "\n",
#      "game=", game , "\n",
#      "item_type=", item_type ,  "\n",
#      "item_name=", item_name ,  "\n",
#      "item_qualit=", item_qualit, "\n",)