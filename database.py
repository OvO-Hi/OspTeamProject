import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
    
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    #register1
    def insert_restaurant(self, name, data, img_path):
        restaurant_info ={
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
    
    #register2
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
        menus = self.db.child("menu").child(data['res_name']).get()
        for menu in menus.each():
            if menu.key() == name:
                return False
        return True
    
    
    #register3
    def insert_review(self, name, data, img_path):
        review_info = {
            "img_path": img_path,
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
            "rev_etc_interior": data['rev_etc_interior'],
            "rev_etc_service": data['rev_etc_service'],
            "rev_etc_kind": data['rev_etc_kind'],
            "rev_etc_tasty": data['rev_etc_tasty'],
            "rev_etc_mood": data['rev_etc_mood'],
            "img_path": img_path
        }
        
        self.db.child("review").child(name).child(data['res_name']).push(review_info)
        print(data, img_path)
    
    
        
