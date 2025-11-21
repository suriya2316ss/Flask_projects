from flask import Flask,request
from flask_restful import Api,Resource
from security import auth,identity
# from flask_jwt import JWT,
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from user import signup


app=Flask(__name__)
app.secret_key='#0#'
api=Api(app)
# jwt=JWT(app,auth,identity) #auth
jwt = JWTManager(app)
items=[]

class Item(Resource):
    @jwt_required()
    def get(self,name):
        item=next(filter(lambda x:x['name']==name,items),None)
        return {'item':item},200 if item else 404
    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return {'message':'item'+name+'exist'}
        data=request.get_json()
        new_item={'name':name,'price':data['price']}
        items.append(new_item)

    def delete(self,name):
        global items
        items=list(filter(lambda x:x['name']!=name,items))
        return items
    def put(self,name):
        data=request.get_json()
        item=next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item={'name':name,'price':data['price']}
            items.append(item)
            if item is None:
                item={'name':name,'price':data['price']}
                items.append(item)
            else:
                item.update(data)
class ItemList(Resource):
    def get(self):
        return {'item':items}
if __name__=="__main__":
    api.add_resource(Item,'/items/<string:name>')
    api.add_resource(ItemList,'/items')
    api.add_resource(signup,'/signup')
    app.run(port=4000,debug=True)