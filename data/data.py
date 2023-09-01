import json,pymysql,re
from dbutils.pooled_db import PooledDB

pool=PooledDB(
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


def get_conn():
    return pool.connection()


try:
    with open("taipei-attractions.json",mode="r",encoding="utf-8") as file:
        data=json.load(file)
    connection = pool.connection()
    cursor=connection.cursor()
    results=data["result"]["results"]
    
    for result in results:
        rate=result["rate"]
        direction=result["direction"]
        name=result["name"]
        date=result["date"]
        longitude=result["longitude"]
        ref_wp=result["REF_WP"]
        avBegin=result["avBegin"]
        langinfo=result["langinfo"]
        mrt=result["MRT"]
        serial_no=result["SERIAL_NO"]
        rownumber=result["RowNumber"]
        cat=result["CAT"]
        memo_time=result["MEMO_TIME"]
        poi=result["POI"]
        file=result["file"]
        imgs_link=[]
        pattern=r'https://www\.travel\.taipei/[\w\/\-\.]+\.jpg|https://www\.travel\.taipei/[\w\/\-\.]+\.png'
        matches=re.findall(pattern,file,re.IGNORECASE)#IGNORECASE是忽略大小寫
        for match in matches:
            imgs_link.append(match)
        imgs_str = json.dumps(imgs_link)
        idpt=result["idpt"]
        latitude=result["latitude"]
        description=result["description"]
        id=result["_id"]
        avEnd=result["avEnd"]
        address=result["address"]
        insert_sql="""INSERT INTO travel_info(rate,direction,name,date,longitude,ref_wp,avBegin,langinfo,mrt,serial_no,rownumber,cat,memo_time,poi,imgs_str,idpt,latitude,description,id,avEnd,address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_sql,(rate,direction,name,date,longitude,ref_wp,avBegin,langinfo,mrt,serial_no,rownumber,cat,memo_time,poi,imgs_str,idpt,latitude,description,id,avEnd,address))

    connection.commit()
finally:
    if 'cursor' in locals():
        cursor.close()

