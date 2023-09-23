import pymysql
import re
import jwt
import model.user
from flask import Blueprint, request, jsonify, make_response
from dbutils.pooled_db import PooledDB
from common.utils.error import EmailException
from common.utils.response import success, failure
from datetime import datetime, timedelta
from decouple import config

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    blocking=True,
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='Root!901',
    database='travel',
    charset='utf8',
)

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/user", methods=["POST"])
def sign_user():
    data = request.get_json()
    # 檢查是否接收到 JSON 數據
    if not data:
        return {"error": True, "message": "缺少請求參數"}, 400
    # 檢查必要的參數是否存在
    required_params = ["name", "email", "password"]
    for param in required_params:
        if param not in data:
            return {"error": True, "message": f"請求缺少必要參數: {param}"}, 400

    data = request.get_json()
    pattern = re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")  # email正則表達
    if not pattern.match(data['email']):
        return failure("Email格式錯誤", 400)
    try:
        result = model.user.user_signup(data)
        return success()
    except EmailException as e:
        return failure(str(e), 400)
    except Exception as e:
        return failure()
# 取得會員資料


@user_blueprint.route("/user/auth", methods=["GET", "PUT", "DELETE"])
def user_auth():
    SECRET_KEY = "your_hardcoded_secret_key"  # 將密鑰移至函數的開頭

    if request.method == "PUT":
        data = request.get_json()
        try:
            result = model.user.user_login(data)
            if result:
                load = {
                    "user_id": result['id'],
                    "name": result['name'],
                    "email": result['email'],
                    "exp": datetime.utcnow() + timedelta(days=7)
                }
                token = jwt.encode(load, SECRET_KEY, algorithm='HS256')
                return jsonify({
                    "token": token
                })
            else:
                return failure("登入失敗，帳號或密碼錯誤", 400)
        except Exception as e:
            return failure(str(e), 500)

    elif request.method == "GET":
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"data": "Public information or message."}), 200#沒收到訊息做的反應
        if 'Bearer' not in auth_header:
            return failure("Token format is incorrect", 401)
        token = auth_header.split('Bearer ')[1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = decoded.get('user_id')
            user_data = model.user.get_user(user_id)
            if not user_data:
                return failure("User not found", 404)
            return jsonify({"data": user_data})
        except jwt.ExpiredSignatureError:
            return failure("Token has expired", 401)
        except jwt.InvalidTokenError:
            return failure("Invalid token", 401)
    elif request.method == "DELETE":
        try:
            return jsonify({"ok": True, "message": "User logged out successfully."}), 200
        except Exception as e:
            return jsonify({"ok": False, "message": str(e)}), 500
