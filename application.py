from flask import Flask, render_template, request, flash, redirect, url_for
from database import DBhandler
import sys
import sysconfig
application = Flask(__name__)
application.config["SECRET_KEY"] = "anything-you-want"

DB = DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('list_restaurants'))

@application.route("/index.html")
def index():
    return render_template("index.html")

#식당 리스트 화면
@application.route("/list.html")
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    limit = 8 #12 -> 4로 수정함.
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    
    data = DB.get_restaurants()
    tot_count = len(data)
    
    data = dict(list(data.items())[start_idx:end_idx])
    
    return render_template(
        "list.html",
        datas=data.items(),
        total=tot_count,
        limit=limit,
        page=page,
        page_count=int((tot_count/8)+1)) #12 -> 4로 수정함.


#맛집 리스트 화면 - 맛집 세부화면 연결 
@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:", data)
    
    res_name = name
    rev_datas = DB.get_review_byname(str(name))
    rev_tot_count = len(rev_datas)
    page_count = len(rev_datas)
    menu_datas = DB.get_food_byname(str(res_name))
    menu_tot_count = len(menu_datas)
    page_count = len(menu_datas)
    
    
    return render_template("detail.html", data=data, avg_rate=avg_rate, rev_datas=rev_datas, rev_total=rev_tot_count, menu_total=menu_tot_count, res_name=res_name, menu_datas=menu_datas)


#맛집 세부화면 – 맛집 대표메뉴 조회화면 연결
@application.route("/list_foods/<res_name>/")
def view_foods(res_name):
    data = DB.get_food_byname(str(res_name))
    tot_count = len(data)
    page_count = len(data)
    return render_template("food_list.html", menu_datas=data, total=tot_count, res_name=res_name)


#맛집 세부화면 – 맛집 대표메뉴 조회화면 연결
@application.route("/list_reviews/<res_name>/")
def view_reviews(res_name):
    data = DB.get_review_byname(str(res_name))
    tot_count = len(data)
    page_count = len(data)
    return render_template("rev_list.html", rev_datas=data, total=tot_count, res_name=res_name)


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
def reg_restaurant():
    return render_template("register_restaurant.html")

@application.route("/result.html", methods=['POST'])
def reg_restaurant_submit():
    global idx
    image_file=request.files['res_img']
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    print(data)
    
    #중복 확인
    if DB.insert_restaurant(data['res_name'], data, image_file.filename):
        return render_template("result.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        #return "Restaurant name already exists!"
        flash("Restaurant name already exists!")
        return redirect(url_for('reg_restaurant'))
    
    
#대표메뉴 입력받기 - register_menu.html
@application.route("/register_menu.html", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("register_menu.html", data=data)

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
        flash("Menu already exists!")
        return render_template("register_menu.html", data=data)

#리뷰 등록 화면 - register_review.html
@application.route("/register_review.html", methods=['POST'])
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
    etc_list = []
    try:
        if data['rev_etc_1']:
            etc_list.append(data['rev_etc_1'])
    except:
        print("")
    try:
        if data['rev_etc_2']:
            etc_list.append(data['rev_etc_2'])
    except:
        print("")
    try:
        if data['rev_etc_3']:
            etc_list.append(data['rev_etc_3'])
    except:
        print("")
    try:
        if data['rev_etc_4']:
            etc_list.append(data['rev_etc_4'])
    except:
        print("")
    try:
        if data['rev_etc_5']:
            etc_list.append(data['rev_etc_5'])
    except:
        print("")
        
    if len(etc_list) == 0:
        etc_list.append('null')
        
    
    DB.insert_review(data['rev_name'], data, etc_list, image_file.filename)
    return render_template("result3.html", data=data, image_path="static/image/"+image_file.filename)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
