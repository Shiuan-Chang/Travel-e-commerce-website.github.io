import pymysql
import bcrypt
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from common.utils.error import EmailException

pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    blocking=True,
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='Root!901',
    database='user_info',
    charset='utf8',
)


def user_signup(data):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)

        # 先查詢是否有email註冊過，沒有則插入姓名、郵件以及密碼資訊
        name = data["name"]
        email = data["email"]
        if "password" not in data or not data["password"]:
            raise ValueError("Password not provided or is empty")
        hashed_password = bcrypt.hashpw(
            data["password"].encode('utf-8'), bcrypt.gensalt())

        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        userEmail = cursor.fetchone()
        if userEmail is None:
            cursor.execute(
                "INSERT INTO users(name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            db.commit()
            return True
        else:
            raise EmailException("註冊失敗, Email已被註冊")

    except Exception as e:
        print(f"Error occurred during signup: {str(e)}")
        if db:
            db.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def user_login(data):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)

        # 從data中提取郵件與密碼
        email = data["email"]
        password = data["password"]

        # 從數據庫中查詢郵件對應的密碼
        cursor.execute(
            "SELECT id, name, email, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        # 如果查詢結果為None，表示沒有該郵件的用戶
        if user is None:
            return False

        # 使用 bcrypt 來檢查提供的密碼與資料庫中的加密密碼是否匹配
        if bcrypt.checkpw(data["password"].encode('utf-8'), user['password'].encode('utf-8')):
            # 返回用戶信息
            return {"id": user['id'], "name": user['name'], "email": user['email']}
        else:
            return False

    except Exception as e:
        print(f"Error occurred during login: {str(e)}")
        raise e

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def get_user(user_id):
    connection = pool.connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, name, email FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            user_data = cursor.fetchone()
        return user_data
    finally:
        connection.close()
