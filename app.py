from flask import Flask, request,jsonify,make_response
import datetime
import uuid
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


def token_required(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message":"token Missing"})
        try:
            decoded_token = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
        except Exception as ex:
            print(str(ex))
            return jsonify({"message":"Token in Invalid!"})
        return fn(*args,**kwargs)
    return inner



@app.route("/login",methods=["POST"])
def login():
    """
    Validates the entity and exchanges a token for communication
    with protected routes
    :param None

    :returns None
    """
    user_id = request.args.get('user')
    password = request.args.get('password')
    if user_id:
        if password == "testpass":
            payload = {"iat":datetime.datetime.utcnow(),
            "exp" :datetime.datetime.utcnow()+datetime.timedelta(minutes=30),
            "user":user_id}
            return jwt.encode(payload,app.config['SECRET_KEY'],algorithm="HS256")
    return make_response(jsonify({"Status" : 200}))


@app.route("/protected",methods=["POST","GET"])
@token_required
def protected_route():
    return jsonify({"message":"success passed JWT auth"})


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5500,debug=True)