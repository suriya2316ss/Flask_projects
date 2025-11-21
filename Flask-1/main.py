from flask import Flask, jsonify,request

app = Flask(__name__)
data = {
    1: {"data": "", "done": True, "task": "Learn Python"},
    2: {"data": "", "done": False, "task": "Build a Flask app"},
    3: {"data": "", "done": False, "task": "Practice Python projects"}
}


@app.route("/todos",methods=["GET"])
def get_todos():
    response=[]
    for key,value in data.items():
        temp=value
        temp["id"]=key
        response.append(temp)
    return jsonify(response)



@app.route("/todos/<int:id>",methods=["GET"])
def get_todo(id):
    if id in data:
        temp=data[id]
        temp["id"]=id
        return jsonify(temp)

    else:
        return {"error":"Todo not found"},404

@app.route("/todos",methods=["POST"])
def post_todos():
    request_data=request.get_json()
    todo = {"data":"","task": request_data["task"], "done": False}
    data[len(data)+1]=todo
    todo["id"]=len(data)
    return jsonify(todo), 201

@app.route("/todos/<int:id>", methods=["PUT"]) 
def put_todos(id):
    requestdata = request.get_json()
    if id in data:
        temp = data[id]
        temp["task"] = requestdata.get("task", temp["task"])
        temp["done"] = requestdata.get("done", temp["done"])
        data[id] = temp
        temp["id"] = id
        return temp
    else:
        return {
            "error": "Todo not found"
        }, 404

@app.route("/todos/<int:id>",methods=["DELETE"])
def delete_todos(id):
    data.pop(id,None)
    return {
        "message":"Todo deleted  successfully"
    }

if __name__ == "__main__":
    app.run(debug=True)
