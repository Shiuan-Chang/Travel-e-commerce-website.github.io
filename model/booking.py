import pymysql
import bcrypt
import json
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from datetime import datetime
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
    database='booking',
    charset='utf8',
)


def post_booking(data, current_user):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)  # 返回字典格式
        attractionId = data["attractionId"]  # data是從前端接收的資料
        date = data["date"]
        time = data["time"]
        price = data["price"]
        if not all([attractionId, date, time, price]):
            raise ValueError('欄位不得為空')  # raise是拋出異常
        cursor.execute(
            "SELECT user_id FROM booking WHERE user_id=%s", (current_user,))
        user_id = cursor.fetchone()
        if user_id:  # 代表訂單已存在
            sql = "UPDATE booking SET attraction_id=%s,date=%s,time_period=%s,price=%s WHERE user_id=%s"
            val = (attractionId, date, time, price, current_user)
            cursor.execute(sql, val)
        else:  # 代表之前沒訂單，要插入這筆資料
            cursor.execute("INSERT INTO booking (attraction_id, date, time_period, price, user_id) VALUES (%s, %s, %s, %s, %s)",
                           (attractionId, date, time, price, current_user))
        db.commit()  # 確保在交易中的所有更改都已被正確地保存到資料庫中。/結束當前的交易，並使所有更改永久。
        return True
    except Exception as e:
        raise (e)
    finally:
        cursor.close()
        db.close()


def get_booking_from_db(user_id):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)  # 返回字典格式
        cursor.execute("""SELECT travel.travel_info.id,travel.travel_info.name,travel.travel_info.address,travel.travel_info.imgs_str,booking.booking.date as raw_date,booking.booking.time_period,booking.booking.price 
   FROM travel.travel_info INNER JOIN booking.booking ON travel.travel_info.id=booking.booking.attraction_id WHERE booking.user_id=%s""", (user_id,))
        result = cursor.fetchone()
        if result:
            result["imgs_str"] = json.loads(result["imgs_str"])
            raw_date = result["raw_date"]
            result["date"] = raw_date.strftime('%Y-%m-%d')
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def delete_booking_from_db(user_id):
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)
        cursor.execute(
            "DELETE FROM booking WHERE user_id=%s", (user_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
