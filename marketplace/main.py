import pymongo
import web
import json
from urllib import response

urls = ("/","index", "/usuarios", "usuarios", "/monedas", "monedas")

connection = pymongo.MongoClient("mongodb+srv://mauri:qt13oWw0dMvIpR1G@market.phxils5.mongodb.net/?retryWrites=true&w=majority")
db = connection.Marketplace

users = db.Usuarios
coins = db.monedas

class index:
    def GET(self):
        coin = coins.find()
        return coin

class usuarios : 
    def GET(self):
        user =  users.find()
        return user

class monedas:
    def GET(self):
        coin = coins.find()
        return coin

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()