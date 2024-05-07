from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import os
from pakages import app 
from transformers import AutoImageProcessor, DetrForObjectDetection
import torch
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


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

def DetrDetection(path):
    if path == None:
        return "nhap link"
    
    else:

        image = Image.open(path)

        image_processor = AutoImageProcessor.from_pretrained("facebook/detr-resnet-50")
        model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        draw = ImageDraw.Draw(image)
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            x, y, x2, y2 = tuple(box)
            draw.rectangle((x, y, x2, y2), outline="red", width=1)
            draw.text((x, y), model.config.id2label[label.item()], fill="white")

        save_path = f"Flask/images/pred_{path}"
        Image.save(save_path)
        return show_image(save_path)

def show_image(path):
    image_path = path
    return image_path
# Object detection

