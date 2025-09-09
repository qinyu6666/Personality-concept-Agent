import mysql.connector
import cv2
import numpy as np
import pymysql
# 连接到 MySQL 数据库

connection = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="frame_db"
            )
cursor = connection.cursor()

# 查询图片数据
select_query = "SELECT * FROM frame_db.captured_frames WHERE id = %s"
cursor.execute(select_query, (1,))  # 假设图片的 ID 是 1
result = cursor.fetchone()

if result:
    # name, image_data = result
    id, time, image_data = result


    # 将二进制数据转换为图片
    image_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

    # 显示图片
    cv2.imshow('Retrieved Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #保存图片到本地文件
    # cv2.imwrite(name, image)
    cv2.imwrite('na', image)

    print(f"图片已保存为 {'na'}")

# 关闭连接
cursor.close()
connection.close()