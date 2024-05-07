from pakages import app
from flask import render_template, request
import utils

@app.route("/")
def home():
    url = request.args.get("fname")
    utils.get_data(url)

    cats = utils.load_categories()
    return render_template("index.html",
                           categories = cats)


@app.route("/conferences")
def conferences_list():
    cate_id = int(request.args.get("category_id"))
    conference = utils.load_conferences(cats = cate_id)

    if cate_id == 1:
        return deadline_list(conference)
    elif cate_id == 2:
        return running_list(conference)
    elif cate_id == 3:
        return future_list(conference)
    else:
        return planned_list(conference)


def deadline_list(conferences):
    return render_template("deadline.html",
                           conf = conferences)

def running_list(conferences):
    return render_template("running.html",
                           conf = conferences)

def future_list(conferences):
    return render_template("future.html",
                           conf = conferences)

def planned_list(conferences):
    return render_template("planned.html",
                           conf = conferences)

@app.route("/detect")
def DetrDetection():
    image_path = request.args.get("filename")
    show_image = utils.DetrDetection(image_path)
    return render_template("detection.html",
                           show_img = show_image)
    
if __name__ == "__main__":
    app.run(debug=True)
    