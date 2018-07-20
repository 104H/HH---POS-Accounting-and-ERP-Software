import pymysql.cursors


# Connect to the database
def connectToDB():
    lines = [line.rstrip('\n') for line in open('data/db.txt')]
    connection = pymysql.connect(host=lines[0],
                                 user=lines[1],
                                 password=lines[2],
                                 db=lines[3],
                                 charset=lines[4],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
    
# 
