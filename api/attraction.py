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
    password='root',
    database='travel',
    charset='utf8',
)

attraction_blueprint = Blueprint('attraction', __name__)

#attraction的設定

def attractions_data(index, keyword):
    connection = pool.connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)#注意轉成字典格式
    try:
        select_data = "id, name, cat, description, address, direction, mrt, latitude, longitude, imgs_str"
        if keyword is not None:
            data = f"SELECT {select_data} FROM travel_info WHERE name LIKE %s or mrt = %s LIMIT %s OFFSET %s"
            result = (f'%{keyword}%', keyword, index+13, index)  
        else:
            data = f"SELECT {select_data} FROM travel_info LIMIT %s OFFSET %s"
            result = (13, index)
        
        cursor.execute(data, result)
        attractions = cursor.fetchall()
        
        for item in attractions:
            item["imgs_str"] = json.loads(item["imgs_str"])#轉成python結構，如果這邊不先做轉換，之後即使轉成json格式，會直接拿原先資料庫倒出來的json格式顯示，會有/\這種符號參雜出現。
        
        return attractions

    finally:
        cursor.close()
        connection.close()

def attraction_IDdata(attractionId):
    connection = pool.connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)#注意轉成字典格式
    try:
        select_data = "id, name, cat, description, address, direction, mrt, latitude, longitude, imgs_str"       
        cursor.execute(
            f"SELECT  {select_data} FROM travel_info WHERE id = %s", (attractionId,))
        attraction = cursor.fetchone()
        attraction["imgs_str"] = json.loads(attraction["imgs_str"])       
        return attraction
    finally:
        cursor.close()
        connection.close()

def page_render(page, keyword=None):
    index = page * 12
    attractions = attractions_data(index, keyword)
    if len(attractions) == 13:
        attractions.pop()
        NextPage = page + 1
    else:
        NextPage = None
    return NextPage, attractions

@attraction_blueprint.route("/attractions", methods=["GET"])
def get_attractions():
    try:
        page = int(request.args.get('page', 0))
        keyword = request.args.get('keyword')
        nextPage, attractions = page_render(page, keyword)
        response_data = {
            "nextPage": nextPage,
            "data": []
        }
        for attraction in attractions:
            item = {
                "id": attraction["id"],
                "name": attraction["name"],
                "category": attraction["cat"],
                "description": attraction["description"],
                "address": attraction["address"],
                "transport": attraction["direction"],
                "mrt": attraction["mrt"],
                "lat": attraction["latitude"],
                "lng": attraction["longitude"],
                "images": attraction["imgs_str"]
            }
            response_data["data"].append(item)
        return jsonify(response_data)
    except Exception as e:
        error_data = {
            "error": True,
            "message": str(e)
        }
        return jsonify(error_data), 500
@attraction_blueprint.route("/attraction/<int:attractionId>", methods=["GET"])
def get_attractionID(attractionId):
    try:
        attraction=attraction_IDdata(attractionId)
        if not attraction:
            return jsonify({"error":True,"message":"Attraction not found"}),404
        response_data={
            "data": {
                "id": attraction["id"],
                "name": attraction["name"],
                "category": attraction["cat"],
                "description": attraction["description"],
                "address": attraction["address"],
                "transport": attraction["direction"],
                "mrt": attraction["mrt"],
                "lat": attraction["latitude"],
                "lng": attraction["longitude"],
                "images": attraction["imgs_str"]
            }
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error":True,"message":str(e)}),500

