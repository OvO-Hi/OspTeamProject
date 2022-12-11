from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
import math
import sysconfig
application = Flask(__name__)
application.config["SECRET_KEY"] = "anything-you-want"

DB = DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('list_restaurants'))

@application.route("/mypage")
def view_mypage():
    userid = session['id']
    print(userid)
    data = DB.get_review_byid(userid)
    total = len(data)
    return render_template("mypage.html", datas=data, total=total)


#검색화면
@application.route("/search", methods=['POST'])
def view_search_result():
    name = request.form['searchname']
    print(name)
    data = DB.search_restaurants_byname(name)
    print(data)
    tot_count = len(data)
    return render_template("search.html", data=data, name=name, total=tot_count)


#회원가입 화면
@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    print(data)
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")
    
#로그인 화면
@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id']=id_
        session['nickname']=DB.find_nickname(id_, pw_hash)
        return redirect(url_for('list_restaurants'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

#로그아웃 화면
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('list_restaurants'))

    
#식당 리스트 화면
@application.route("/list")
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    limit = 8 #4->8로 변경함.
    
    #화면에서 셀렉트박스 선택한 카테고리 값 받아오기
    category = request.args.get("category", "all")
    price = request.args.get("price", "all")
    area = request.args.get("area", "all")
    headcount = request.args.get("headcount", "all")
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    
    #카테고리로 DB에서 데이터 받아오기
    if category=="all" and price=="all" and area=="all" and headcount=="all":
        data = DB.get_restaurants()
    else:
        if category != "all" and price=="all" and area=="all" and headcount=="all":
            data = DB.get_restaurants_bycategory(category)
        elif price != "all" and category=="all" and area=="all" and headcount=="all":
            data = DB.get_restaurants_byprice(price)
        elif area != "all" and category=="all" and price=="all" and headcount=="all":
            data = DB.get_restaurants_byarea(area)
        elif headcount != "all" and category=="all" and price=="all" and area == "all":
            data = DB.get_restaurants_byheadcount(headcount)
        else:
            data = DB.get_restaurants()

    tot_count = len(data)
    
    #(추가)데이터 개수가 limit보다 크지 않은경우 처리
    if tot_count<=limit:
        data = dict(list(data.items())[:tot_count])
    else:
        data = dict(list(data.items())[start_idx:end_idx])
    
    data = dict(sorted(data.items(), key=lambda x:x[1]['res_name'], reverse=False))
    #print(data)
    page_count=len(data)

    return render_template(
        "list.html",
        datas=data.items(),
        total=tot_count,
        limit=limit,
        page=page,
        page_count=math.ceil(tot_count/8),
        category=category,
        price=price,
        area=area,
        headcount=headcount)


#맛집 리스트 화면 - 맛집 세부화면 연결 
@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    #print("####data:", data)

    res_name = name
    rev_datas = DB.get_review_byname_preview(str(name))
    rev_tot_count = len(rev_datas)
    page_count = len(rev_datas)
    menu_datas = DB.get_food_byname_preview(str(res_name))
    menu_tot_count = len(menu_datas)
    page_count = len(menu_datas)
    index=0
    
    return render_template(
        "detail.html", 
        data=data, 
        avg_rate=avg_rate, 
        rev_datas=rev_datas, 
        rev_total=rev_tot_count, 
        menu_total=menu_tot_count, 
        res_name=res_name, 
        menu_datas=menu_datas,
        index=index)


#맛집 세부화면 – 맛집 대표메뉴 조회화면 연결
@application.route("/list_foods/<res_name>/")
def view_foods(res_name):
    page = request.args.get("page", 0, type=int)
    limit=4
    
    start_idx=limit*page
    end_idx=limit*(page+1)
    data = DB.get_food_byname(str(res_name))
    tot_count = len(data)
    page_count = len(data)
    print("확인")
    print(data[start_idx:end_idx])
    #data = dict(data[start_idx:end_idx])
    data = data[start_idx:end_idx]
    return render_template(
        "food_list.html", 
        menu_datas=data, 
        total=tot_count, 
        res_name=res_name,
        limit=limit,
        page=page,
        page_count=math.ceil(tot_count/4))


#맛집 세부화면 – 맛집 대표메뉴 조회화면 연결
@application.route("/list_reviews/<res_name>/")
def view_reviews(res_name):
    data = DB.get_review_byname(str(res_name))
    avg_rate = DB.get_avgrate_byname(str(res_name))
    tot_count = len(data)
    page_count = len(data)
    return render_template("rev_list.html", rev_datas=data, total=tot_count, res_name=res_name, avg_rate=avg_rate)


#random 추천 화면 연결
@application.route("/random_res")
def random_res():
    rand=DB.get_restaurants_byrandom()
    return render_template("random_res.html", rand=rand)
    
    #return render_template("random_res.html", total=0, limit=4, page=1, page_count=math.ceil(1/4), category='all', price='all', area='all')


#식당 입력 받기 - register_restaurant.html
@application.route("/register_restaurant")
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
        flash("Restaurant name already exists!")
        return redirect(url_for('reg_restaurant'))
    
    
#대표메뉴 입력받기 - register_menu.html
@application.route("/register_menu", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("register_menu.html", data=data)

@application.route("/result2", methods=['POST'])
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
@application.route("/register_review", methods=['POST'])
def reg_review():
    data=request.form
    #print(data)
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

#찜한 식당 추가
@application.route("/add_fav", methods=['POST'])
def add_fav():
    data=request.form
    userid=session['id']
    name=data['res_name']
    img_path=data['img_path']
    print(userid, name, img_path)
    DB.insert_fav(userid, name, img_path)
    
    return redirect(url_for('view_restaurant_detail', name=name))


#찜한 식당 리스트 보여주기
@application.route("/mypage_fav")
def fav_list_restaurants():
    userid=session['id']
    data = DB.get_fav_restaurants(userid)
    try:
        datas=data.items()
        tot_count = len(data)
    except:
        datas=0
        tot_count = 0
        

    return render_template(
        "mypage_fav.html",
        datas=datas,
        total=tot_count)

#찜 등록...- rev_etc 처럼 등록해야할 듯
@application.route("/view_detail/<name>/", methods=['POST'])
def reg_fav():
    data=request.form
    #print(data)
    return render_template(url_for('view_restaurant_detail'), name=name)
#찜 등록...#

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
