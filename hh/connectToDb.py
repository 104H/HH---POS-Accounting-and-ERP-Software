import pymysql.cursors


# Connect to the database
def connectToDB():
    lines = [line.rstrip('\n') for line in open('data/db.txt')]
    connection = pymysql.connect(host=lines[0],
                                 user=lines[2],
                                 password=lines[3],
                                 db=lines[4],
                                 charset=lines[5],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
    
# 
