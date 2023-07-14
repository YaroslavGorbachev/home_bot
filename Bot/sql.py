import sqlite3 as sq

async def db_start(self):
    global db,cur 

    db = sq.connect('adres_data.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS adres_data (user_id TEXT PRIMARY KEY,name TEXT,surname TEXT ,ap_number TEXT ,phone TEXT)")
    db.commit


async def create_adres_data(self):
    user = cur.execute("SELECT 1 FROM 'adres_data' WHERE user_id =1'")
    if not user:
        cur.execute ("INSERT INTO  adres_data VALUES(?,?,?,?,?)",('','','','',''),(str(user_id), str(name), str(surname), str(ap_number), str(phone)))
        db.commit()


async def edit_adres_data(state):
    async with state():
        cur.execute("UPDATE adres_data SET user_id == '{},name ='{},surname = '{},ap_number = '{},phone = '{}")
          
        db.commit()

# async def receiving_adres_data():
#     cur.execute("SELECT * FROM ap_number;")

