import pymysql
import json
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    blocking=True,
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='Root!901',
    database='orderdb',
    charset='utf8',
)


def get_order(order_number):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)  # %Y-%m-%d被視為格式化字符串，故要在前方再加上%
        sql = """SELECT orderdb.orders.order_number,orderdb.orders.price,orderdb.orders.name,orderdb.orders.email,orderdb.orders.phone,DATE_FORMAT(orders.date, '%%Y-%%m-%%d') as date,
        orderdb.orders.time_period,orderdb.orders.attraction_id,orderdb.orders.status,travel.travel_info.name as attraction_name,travel.travel_info.address,travel.travel_info.imgs_str 
        FROM orderdb.orders INNER JOIN travel.travel_info ON orderdb.orders.attraction_id=travel.travel_info.id WHERE orderdb.orders.order_number=%s"""
        val = (order_number,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def post_order(current_user, order_number, data, status):
    db = None
    cursor = None
    try:
        db = pool.connection()
        cursor = db.cursor(DictCursor)
        sql = "Insert Into orders(order_number, price, user_id, name, email, phone, date, time_period, attraction_id, status) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (order_number, data["order"]["price"], current_user, data["order"]["contact"]["name"], data["order"]["contact"]["email"], data["order"]["contact"]["phone"],
               data["order"]["trip"]["date"], data["order"]["trip"]["time"], data["order"]["trip"]["attraction"]["id"], status)
        cursor.execute(sql, val)
        cursor.execute(
            "DELETE FROM booking.booking WHERE user_id=%s", (current_user,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
