import sqlite3 as sq

def seeAll():
    con = sq.connect("./database/db.sqlite3")
    cur = con.cursor()
    data = cur.execute("SELECT first_name, username FROM auth_user as user inner join account_userprofile as userprofile where user.id = userprofile.id").fetchall()
    return data

for item in seeAll():
    print(item)