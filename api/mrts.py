import pymysql,json,re,requests
from flask import Blueprint, request, jsonify
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
    database='travel',
    charset='utf8',
)

mrts_blueprint = Blueprint('mrts', __name__)

@mrts_blueprint.route("/mrts", methods=["GET"])
def mrts():
    try:
        connection = pool.connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)#注意轉成字典格式
        query=""" SELECT MRT, COUNT(name) AS attraction_count
        FROM travel_info
        GROUP BY MRT
        ORDER BY attraction_count DESC;
        """
        cursor.execute(query)
        results=cursor.fetchall()

        mrt_names=[result['MRT']for result in results if result['MRT']]
        response_data={
            "data":mrt_names
        }
        return jsonify(response_data)
    except Exception as e:
        error_data={
            "error":True,
            "message":str(e)
        }
        return jsonify(error_data),500
    finally:
        cursor.close()
        connection.close()
    