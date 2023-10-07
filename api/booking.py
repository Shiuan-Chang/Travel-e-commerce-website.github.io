import pymysql
import jwt
import model.booking
from flask import Blueprint, request, jsonify
from dbutils.pooled_db import PooledDB
from model.booking import post_booking
from common.utils.response import success, failure
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
    database='booking',
    charset='utf8',
)

booking_blueprint = Blueprint('booking', __name__)
SECRET_KEY = "your_hardcoded_secret_key"


@booking_blueprint.route("/booking", methods=["GET"])
def get_booking():
    auth_header = request.headers.get('Authorization')

    if not auth_header or 'Bearer' not in auth_header:
        return jsonify({'error': 'Authorization header is missing or Bearer token is missing'}), 401

    userToken = auth_header.split(" ")[1]
    if not userToken:
        return jsonify({'error': '未登入系統，拒絕存取'}), 403

    try:
        decoded_token = jwt.decode(userToken, SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token['user_id']
        result = model.booking.get_booking_from_db(current_user)
        if not result:
            return success()
        else:
            booking_info = {
                "attraction": {
                    "id": result["id"],
                    "name": result["name"],
                    "address": result["address"],
                    "image": result["imgs_str"][0]
                },
                "date": result["date"],
                "time": result["time_period"],
                "price": result["price"]
            }
            return success(booking_info)
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token 已經過期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '無效的 Token'}), 401
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return failure("建立失敗，輸入不正確", 400)
    except Exception as e:
        print("Error occurred:", e)
        return failure()


@booking_blueprint.route("/booking", methods=["POST"])
def post_booking():
    auth_header = request.headers.get('Authorization')
    print("Received Authorization Header:", auth_header)
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing'}), 401
    if 'Bearer' not in auth_header:
        return jsonify({'error': 'Bearer token is missing in Authorization header'}), 401
    userToken = auth_header.split(" ")[1]
    if not userToken:
        return jsonify({'error': '未登入系統，拒絕存取'}), 403  # 後端在驗證一次(前後端檢驗)
    try:
        decoded_token = jwt.decode(userToken, SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token['user_id']  # 資料的名稱錯誤導致多次error
        data = request.get_json()
        model.booking.post_booking(data, current_user)
        return success()
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token 已經過期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '無效的 Token'}), 401
    except ValueError as e:
        return failure("建立失敗，輸入不正確", 400)
    except Exception as e:
        return failure()

@booking_blueprint.route("/booking", methods=["DELETE"])
def handle_delete():
    auth_header = request.headers.get('Authorization')

    if not auth_header or 'Bearer' not in auth_header:
        return jsonify({'error': 'Authorization header is missing or Bearer token is missing'}), 401

    auth_parts = auth_header.split(" ")
    if len(auth_parts) != 2:
        return jsonify({'error': 'Authorization header format is incorrect'}), 401

    userToken = auth_parts[1]
    if not userToken:
        return jsonify({'error': '未登入系統，拒絕存取'}), 403

    try:
        decoded_token = jwt.decode(userToken, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token['user_id']
        model.booking.delete_booking_from_db(user_id)
        return success()
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 403
    except Exception as e:
        return failure()
