import pyrebase
import json

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
            "img_path": img_path
        }
        
        #self.db.child("review").push(review_info)
        self.db.child("review").child(data['res_name']).push(review_info)
        #self.db.child("review").child(data['res_name']).child(name).push(review_info)
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
    
    def get_avgrate_byname(self, name):
        reviews = self.db.child("review").get()
        rates=[]
        if reviews.key() == name:
            for res in reviews.each():
                value = res.val()
                rates.append(float(value['rev_score']))
        if len(rates) == 0:
            return 0
        return sum(rates)/len(rates)

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
