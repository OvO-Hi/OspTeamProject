from flask import Flask, render_template, request
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/index.html")
def index():
    return render_template("index.html")

@application.route("/detail1.html")
def detail1():
    return render_template("detail1.html")

@application.route("/detail2.html")
def detail2():
    return render_template("detail2.html")

@application.route("/detail3.html")
def detail3():
    return render_template("detail3.html")

@application.route("/search2.html")
def search2():
    return render_template("search2.html")

@application.route("/search3.html")
def search3():
    return render_template("search3.html")

@application.route("/search4.html")
def search4():
    return render_template("search4.html")

@application.route("/search5.html")
def search5():
    return render_template("search5.html")


#식당 입력 받기 - register_restaurant.html
@application.route("/register_restaurant.html")
def reg_register():
    return render_template("register_restaurant.html")

@application.route("/result.html", methods=['POST'])
def reg_restaurant_submit():
    image_file=request.files['res_img']
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    
    print(data)
    
    #중복 확인
    
    if DB.insert_restaurant(data['res_name'], data, image_file.filename):
        return render_template("result.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Restaurant name already exists!"

#대표메뉴 입력받기 - register_menu.html
@application.route("/register_menu.html")
def reg_menu():
    data=request.form
    print(data)
    return render_template("register2.html", data=data)

@application.route("/result2.html", methods=['POST'])
def reg_menu_submit():
    image_file=request.files['food_img']
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    print(data)

    #중복 확인

    if DB.insert_menu(data['menu_name'], data, image_file.filename):
        return render_template("result2.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Menu already exists!"

#리뷰 등록 화면 - register_review.html
@application.route("/register_review.html")
def reg_review():
    data=request.form
    print(data)
    return render_template("register_review.html", data=data)

@application.route("/result3.html", methods=['POST'])
def reg_review_submit():
    image_file=request.files['review_img']
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    
    print(data)

    #중복 확인
    if DB.insert_review(data['rev_name'], data, image_file.filename):
        return render_template("result3.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Review name already exists!"


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
