from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from pymongo import MongoClient

# establish a MongoDB instance
client = MongoClient('mongodb://127.0.0.1:27017')

#db name is sample. collection name is contacts. Use whatever you want here.
db = client.sample
contacts = db.contacts

# create a new Firefox session
# driver = webdriver.Chrome(executable_path=r'C:/Users/{your_comp}/AppData/Local/ChromeDriver/chromedriver.exe')
driver.implicitly_wait(30)
driver.maximize_window()
driver.get("https://www.fakepersongenerator.com/Index/generate")


# Navigate to the application home page
def generate_fake_person_generator():
    driver.find_element_by_name("state").click()
    driver.find_element_by_name("state").send_keys("New Hampshire")
    driver.find_element_by_name("state").click()
    driver.find_element_by_name("city").click()
    driver.find_element_by_name("city").clear()
    driver.find_element_by_name("city").send_keys("Manchester")
    driver.find_element_by_id("generate").click()

def get_seed_values():
    street = driver.find_element_by_xpath("//p[contains(text(),'Street')]//b").text
    name = driver.find_element_by_xpath("//p[@class='text-center name']/b").text
    city = driver.find_element_by_xpath("//p[contains(text(),'City, State, Zip')]//b").text
    phone = driver.find_element_by_xpath("//p[contains(text(),'Mobile')]//b").text
    lat_lng = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/div[2]/div[10]/div[8]/input[1]").get_attribute("value")
    push_to_mongo(name, phone, city, street, lat_lng)

def push_to_mongo(name, phone, city, street, lat_lng):
        # makes a collection document in MongoDB!
    contact = {
        "firstName": name.split(" ")[0],
        "lastName": name.split(" ")[2],
        "phonenumber": phone,
        "city": split_area_info_city(city),
        "state": split_area_info_state(city.split(",")[1]),
        "zipcode": split_area_info_zipcode(city),
        "geoLocation_lat": split_lat_lng(lat_lng.split(",")[0]),
        "geoLocation_lng": split_lat_lng(lat_lng.split(",")[1]),
        "address": street
    }
    result = contacts.insert_one(contact)
    print('One post: {0}'.format(result.inserted_id))

def split_area_info_state(area_string):
    state_string = re.split("\(([^)]+)\)", area_string)
    return state_string[1]

def split_area_info_city(area_string):
    city = area_string.split(",")[0]
    return city

def split_area_info_zipcode(area_string):
    zipcode = area_string.split(",")[2]
    return zipcode

def split_lat_lng(lat_lng):
    new_num = lat_lng.split("(")
    return new_num[0]

def refresh_values():
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div/p/a").click()

def file_process():
    for x in range(0, 100):
        get_seed_values()
        refresh_values()

# all the goodies are here!
def main():
        generate_fake_person_generator()
        file_process()
        driver.close()

# this is where it all happens!
main()
