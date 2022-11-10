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


#식당 입력 받기 - register1.html
@application.route("/register1.html")
def register1():
    return render_template("register1.html")

@application.route("/result1.html", methods=['POST'])
def reg_restaurant_submit():
    image_file1=request.files["res_img"]
    image_file1.save("static/image/{}".format(image_file1.filename))
    save1=request.form["res_name"]+"_"+image_file1.filename
    data1=request.form
    return render_template("result1.html", data=data1)

#대표메뉴 입력받기 - register2.html
@application.route("/register2.html")
def register2():
    return render_template("register2.html")

@application.route("/result2.html", methods=['POST'])
def reg_menu_submit():
    image_file2=request.files["food_img"]
    image_file2.save("static/image/{}".format(image_file2.filename))
    save2=request.form["menu_name"]+"_"+image_file2.filename
    data2=request.form
    return render_template("result2.html", data=data2)

#리뷰 등록 화면 -register3.html
@application.route("/register3.html")
def register3():
    return render_template("register3.html")

@application.route("/result3.html", methods=['POST'])
def reg_review_submit():
    image_file3=request.files["review_img"]
    image_file3.save("static/image/{}".format(image_file3.filename))
    save3=request.form["rev_menu"]+"_"+image_file2.filename
    data3 = request.form
    return render_template("result3.html", data=data3)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
