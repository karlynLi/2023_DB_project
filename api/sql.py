from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_member(mid):
        sql = "SELECT MID, NAME, PASSWORD, IDENTITY, NAME FROM MEMBER WHERE MID = :mid"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mid' : mid}))
    
    def get_all_account():
        sql = "SELECT MID FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (:mid, :name, :password, :identity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(vid):
        sql ='SELECT * FROM VACANCY NATURAL JOIN DEPARTMENT WHERE VID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': vid}))

    def get_all_product():
        sql = 'SELECT * FROM VACANCY NATURAL JOIN DEPARTMENT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def add_vacancy(input):
        sql = 'INSERT INTO VACANCY VALUES (:vid, :workTime, :vName, :content, :salary, :skill, :required, :status, :did)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        input['required'] = int(input['required'])
        sql = 'UPDATE VACANCY SET WORKTIME=:workTime, VNAME=:vName, CONTENT=:content, SALARY=:salary, REQUIRED=:required, SKILL=:skill WHERE VID=:vid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_status(vid, status):
        if status == 'open':
            sql = 'UPDATE VACANCY SET STATUS=1 WHERE VID=:vid'
        else:
            sql = 'UPDATE VACANCY SET STATUS=0 WHERE VID=:vid'
        DB.execute_input(DB.prepare(sql), {'vid': vid})
        DB.commit()
    def get_dept(office, unit):
        sql = 'SELECT DID FROM DEPARTMENT WHERE OFFICE = :office AND DIVISION = :unit'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'office': office, 'unit': unit}))
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))