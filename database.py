import pyrebase
import json
from random import shuffle
import random

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
    
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    #register_restaurant
    def insert_restaurant(self, name, data, img_path):
        restaurant_info ={
            "res_name": data['res_name'],
            "res_addr": data['res_addr'],
            "res_addr_detail": data['res_addr_detail'],
            "res_tel": data['res_tel'],
            "res_site": data['res_site'],
            "res_area": data['res_area'],
            "res_category": data['res_category'],
            "res_price": data['res_price'],
            "parking": data['parking'],
            "appt_open": data['appt_open'],
            "appt_close": data['appt_close'],
            "break_open": data['break_open'],
            "break_close": data['break_close'],
            "img_path": img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").child(name).set(restaurant_info)
            print(data, img_path)
            return True
        else:
            return False
    
    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            if res.key() == name:
                return False
        return True
    
    #register_menu
    def insert_menu(self, name, data, img_path):
        menu_info = {
            "img_path":img_path,
            "res_name":data['res_name'],
            "menu_name":data['menu_name'],
            "menu_price":data['menu_price']
        }
        
        #중복 확인
        if self.menu_duplicate_check(data, name):
            self.db.child("menu").child(data['res_name']).child(name).set(menu_info)
            print(data, img_path)
            return True
        else:
            return False
    
    def menu_duplicate_check(self, data, name):
        menus = self.db.child("menu").get()
        for m in menus.each():
            if m.key() == data['res_name']:
                print(m.key())
                menus = self.db.child("menu").child(data['res_name']).get()
                for menu in menus.each():
                    if menu.key() == name:
                        return False
                return True
        return True
    
    
    #register_review
    def insert_review(self, name, data, etc_list, img_path):
        review_info = {
            "res_name": data['res_name'],
            "rev_name": data['rev_name'],
            "rev_menu": data['rev_menu'],
            "rev_price": data['rev_price'],
            "rev_score": data['rev_score'],
            "rev_time": data['rev_time'],
            "rev_memo": data['rev_memo'],
            "rev_headcount": data['rev_headcount'],
            "rev_amount": data['rev_amount'],
            "rev_vegan": data['rev_vegan'],
            "rev_etc": etc_list,
            "id": data['id'],
            "img_path": img_path
        }
        
        self.db.child("review").child(data['res_name']).push(review_info)
        print(data, img_path)
        
    
        
    #맛집등록 테이블에서 데이터 가져오기
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants

    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value=""
        for res in restaurants.each():
            value = res.val()
            if value['res_name'] == name:
                target_value=value
        return target_value
    
    #식당 별점 평균 구하기
    def get_avgrate_byname(self, name):
        reviews = self.db.child("review").get()
        rates=[]
        for res in reviews.each():
            if res.key() == name:
                items = res.val().items()
                for item in items:
                    rates.append(float(item[1]['rev_score']))
        if len(rates) == 0:
            return 0
        rate = sum(rates)/len(rates)
        rate = round(rate, 1)
        return rate

    def get_food_byname(self, name):
        target_value=[]
        
        check = self.db.child("menu").get()
        count = 0;
        for c in check.each():
            if c.key() == name:
                count += 1;
        if count == 0:
            return target_value
                
        restaurants = self.db.child("menu").child(name).get()
        for res in restaurants.each():
            value = res.val()
            target_value.append(value)
        return target_value
    
    def get_food_byname_preview(self, name):
        target_value=[]
        
        check = self.db.child("menu").get()
        count = 0;
        for c in check.each():
            if c.key() == name:
                count += 1;
        if count == 0:
            return target_value
                
        restaurants = self.db.child("menu").child(name).get()
        for res in restaurants.each():
            if len(target_value) >= 3:
                break
            value = res.val()
            target_value.append(value)
        return target_value  
    
    def get_review_byname(self, name):
        target_value=[]
        
        check = self.db.child("review").get()
        count = 0;
        for c in check.each():
            if c.key() == name:
                count += 1;
        if count == 0:
            return target_value
                
        restaurants = self.db.child("review").child(name).get()
        for res in restaurants.each():
            value = res.val()
            target_value.append(value)
        return target_value
    
    
    def get_review_byname_preview(self, name):
        target_value=[]
        
        check = self.db.child("review").get()
        count = 0;
        for c in check.each():
            if c.key() == name:
                count += 1;
        if count == 0:
            return target_value
                
        restaurants = self.db.child("review").child(name).get()
        for res in restaurants.each():
            if len(target_value) >= 3:
                break
            value = res.val()
            target_value.append(value)
        return target_value 
    
    def get_restaurants_bycategory(self, cate):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['res_category'] == cate:
                target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict
    
    def get_restaurants_byprice(self, price):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['res_price'] == price:
                target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict
    
    def get_restaurants_byarea(self, area):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['res_area'] == area:
                target_value.append(value)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict
    
    #검색-search
    def search_restaurants_byname(self, name):
        target_value=[]
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            val = res.val()
            if val['res_name'] == name:
                target_value.append(val)
        return target_value
    
    #인원수에 따른 레스토랑 필터링
    def get_restaurants_byheadcount(self, headcount):
        target_value=[]
        restaurants = self.db.child("review").get()
        value=""
        for res in restaurants.each():
            items = res.val().items()
            for item in items:
                if item[1]['rev_headcount'] == headcount:
                    res_name = item[1]['res_name']
                    print(item[1]['res_name'])
                    restaurants = self.db.child("restaurant").get()
                    for res in restaurants.each():
                        val = res.val()
                        if val['res_name'] == res_name:
                            target_value.append(val)
        new_dict={}
        for k,v in enumerate(target_value):
            new_dict[k]=v
        return new_dict
    
    #mypage에서 리뷰 가져오기
    def get_review_byid(self, userid):
        target_value=[]                
        restaurants = self.db.child("review").get()
        for res in restaurants.each():
            items = res.val().items()
            for item in items:
                if item[1]['id'] == userid:
                    target_value.append(item[1])
        print(target_value)
        return target_value
    
    #회원가입
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        #print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
                
            return True
        
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
            
        return False
    
    def find_nickname(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return value['nickname']
    
            
    #무작위 추천
    def get_restaurants_byrandom(self):
        restaurants = self.db.child("restaurant").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            target_value.append(value)
        rand = random.choice(target_value)
        return rand  #restaurant 랜덤으로 하나 받아온다.
    
    #찜 등록 - duplicate check해야함. 
    def insert_fav(self, id_string, name, img_path):
        fav_info = {
            "res_name": name,
            "img_path": img_path
        }
        val_key = self.fav_key(id_string)
        if val_key != None:
            self.db.child("user").child(val_key).child("fav").child(name).set(fav_info)
        print(name, img_path)
    #찜 등록  
    
    def fav_key(self, id_string):
        users = self.db.child("user").get()
        if str(users.val()) == "None":
            return None
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return res.key()
        
    
    #찜한 식당 리스트 가져오기
    def get_fav_restaurants(self, userid):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == userid:
                try:
                    return value['fav']
                except:
                    return None
        return None
    
