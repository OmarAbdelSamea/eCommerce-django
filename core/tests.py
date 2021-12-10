from django.test import TestCase

import json
from rest_framework.test import APIRequestFactory
from core.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from core.serializers import *


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username":"test1234", "email":"test@test.com", "password":"ldfnsdknfNJDnsjk", 
                "confirm_password":"ldfnsdknfNJDnsjk"}
        response = self.client.post("/api/v1/users/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class UserViewTestCase(APITestCase):
    product_id = 0
    def setUp(self):
        data = {"username":"test1234", "email":"test@test.com", "password":"ldfnsdknfNJDnsjk", 
                "confirm_password":"ldfnsdknfNJDnsjk"}
        dataLogin = {"username":"test1234", "password":"ldfnsdknfNJDnsjk"}
        response = self.client.post("/api/v1/users/", data)
        responseLogin = self.client.post("/api/v1/token/login/", dataLogin)                
        self.token = responseLogin.data['auth_token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ self.token)

    def test_user_info_authenticated(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/profile/")        
        self.assertEquals(response.data['user']['username'], "test1234")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_add_cash_correctly(self):
        data = {"value":"1000"}
            
        response = self.client.post("http://127.0.0.1:8000/api/v1/profile/deposit/", data)        
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        profile = self.client.get("http://127.0.0.1:8000/api/v1/profile/")
        self.assertEquals(profile.data['cash'], 1000)
        self.assertEquals(profile.status_code, status.HTTP_200_OK)
        
    def test_user_info_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("http://127.0.0.1:8000/api/v1/profile/")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductCRUDTestCase(APITestCase):    
    def setUp(self):
        data = {"username":"test1234", "email":"test@test.com", "password":"ldfnsdknfNJDnsjk", 
                "confirm_password":"ldfnsdknfNJDnsjk"}
        dataLogin = {"username":"test1234", "password":"ldfnsdknfNJDnsjk"}
        response = self.client.post("/api/v1/users/", data)
        responseLogin = self.client.post("/api/v1/token/login/", dataLogin)                
        self.token = responseLogin.data['auth_token']
        self.api_authentication()        

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION= "Token "+ self.token)

    def test_add_product_correctly(self):
        data = {"name":"test", "description":"test"}
        response = self.client.post("http://127.0.0.1:8000/api/v1/categories/", data)        
        data = {"name":"Pants", "price":10,"category":"1","description":"blue pants", "no_of_pieces":10, "on_sale": 1}    
        response = self.client.post("http://127.0.0.1:8000/api/v1/products/", data)                           
        self.assertEquals(response.data['id'], 1)

    def test_edit_product_correctly(self):
        data = {"name":"test", "description":"test"}
        response = self.client.post("http://127.0.0.1:8000/api/v1/categories/", data)   
        data = {"name":"Pants", "price":10,"category":"1","description":"blue pants", "no_of_pieces":10, "on_sale": 1}    
        response = self.client.post("http://127.0.0.1:8000/api/v1/products/", data)            
        data = {"id": "1", "name":"jacket", "price":"10","category":"1","description":"black jacket", "no_of_pieces":10, "on_sale": 1}    
        response = self.client.put("http://127.0.0.1:8000/api/v1/products/1/", data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'],'jacket')                

    def test_delete_product_correctly(self):
        data = {"name":"test", "description":"test"}
        response = self.client.post("http://127.0.0.1:8000/api/v1/categories/", data)   
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = {"name":"Pants", "price":10,"category":"1","description":"blue pants", "no_of_pieces":10, "on_sale": 1}    
        response = self.client.post("http://127.0.0.1:8000/api/v1/products/", data)                    
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete("http://127.0.0.1:8000/api/v1/products/1/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)