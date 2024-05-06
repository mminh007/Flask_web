from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import os
from pakages import app 

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)
    
def load_categories():
    return read_json(os.path.join(app.root_path, "data/Categories.json"))
    
def load_conferences(cats):
    if cats == 1:
        return load_deadline()
    elif cats == 2:
        return load_running()
    elif cats == 3:
        return load_future()
    else:
        return load_planned()

def load_deadline():
    return read_json(os.path.join(app.root_path, "data/Deadline_ahead.json"))

def load_running():
    return read_json(os.path.join(app.root_path, "data/Running_conferences.json"))

def load_future():
    return read_json(os.path.join(app.root_path, "data/Future_conferences.json"))

def load_planned():
    return read_json(os.path.join(app.root_path, "data/Planned_conferences.json"))

def get_data(url = "https://www.lix.polytechnique.fr/~hermann/conf.php#"):
    
    if url == None:
        return "nhap link"
    
    else:
        driver = webdriver.Chrome()
        driver.get(url)

        # moi table co thiet ke khac nhau nen phai crawl tung table 1
        tables = driver.find_elements(By.CSS_SELECTOR, 'table.conference')

        tbodys = []
        for t in tables:
            tbody = t.find_element(By.CSS_SELECTOR, "tbody")
            tbodys.append(tbody)

        data_0 = []
        tr_0 = tbodys[0].find_elements(By.CSS_SELECTOR, "tr")

        for t in tr_0:
            td = [item.text for item in t.find_elements(By.CSS_SELECTOR, "td")]
            dictionary = {
                "Conference": td[0],
                "City, Country": td[1],
                "Deadline": td[2],
                "Date": td[3],
                "Notification": td[4],
                "Submission": td[5],
            }
            data_0.append(dictionary)

        data_1 = []
        tr_1 = tbodys[1].find_elements(By.CSS_SELECTOR, "tr")

        for t in tr_1:
            td = [item.text for item in t.find_elements(By.CSS_SELECTOR, "td")]
            dictionary = {
                "Conference": td[0],
                "City, Country": td[1],
                "Date": td[2],
                "Remark": td[3],
            }
            data_1.append(dictionary)

        data_2 = []
        tr_2 = tbodys[2].find_elements(By.CSS_SELECTOR, "tr")

        for t in tr_2:
            td = [item.text for item in t.find_elements(By.CSS_SELECTOR, "td")]
            dictionary = {
                "Conference": td[0],
                "City, Country": td[1],
                "Date": td[2],
                "Notification": td[3],
                "Final version": td[4],
                "Early register": td[5],
                "Remarks": td[6],
            }
            data_2.append(dictionary)

        data_3 = []
        tr_3 = tbodys[3].find_elements(By.CSS_SELECTOR, "tr")

        for t in tr_3:
            td = [item.text for item in t.find_elements(By.CSS_SELECTOR, "td")]
            dictionary = {
                "Conference": td[0],
                "Year": td[1],
                "City, Country": td[2],
                "Starting date": td[3],
                "Ending date": td[4],
                "Remark": td[5],
            }
            data_3.append(dictionary)

        #         pass
        driver.close()



# file nay chua cac ham tuong tac voi data