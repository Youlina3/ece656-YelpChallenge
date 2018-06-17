# !/usr/bin/python

import mysql.connector
import matplotlib.pyplot as plt
from itertools import groupby

def open_conn():
    """open the connection before each test case"""
    conn = mysql.connector.connect(user='myUser', password='myPassword',
                                   host='localhost',
                                   database='final')

    return conn

def close_conn(conn):
    """close the connection after each test case"""
    conn.close()
    
def executeQuery(conn, query, commit=False):
    """ fetch result after query"""
    cursor = conn.cursor()
    query_num = query.count(";")
    if query_num > 1:
        for result in cursor.execute(query, params=None, multi=True):
            if result.with_rows:
                result = result.fetchall()
    else:
        cursor.execute(query)
        result = cursor.fetchall()
    # we commit the results only if we want the updates to the database
    # to persist.
    if commit:
        conn.commit()
    else:
        conn.rollback()
    # close the cursor used to execute the query
    cursor.close()
    return result

if __name__ == '__main__':
    #open connection to the database
    conn = open_conn()
    
    #fetch results from the database
    result = executeQuery(conn, "select date, avg(stars) as avg_stars from review where business_id = '--WsruI0IGEoeRmkErU5Gg' group by date order by date;")
    #retreive results as a list from the list of tuples
    #list advantage: by order and can contain duplicates
    #average rating per date
    avg_stars = [row[1] for row in result]
    date = [row[0] for row in result]

    #count average rating until that date
    count = 0
    avg_rating_trend = []
    sum = 0
    for rating in avg_stars:
        count = count + 1
        sum = rating + sum
        avg_rating_trend.append(sum/count)


    #groupby:used for aggregation

    #plot results
    x = date
    y = avg_rating_trend
    f, ax = plt.subplots(1)
    ax.plot(x, y)
    ax.set_ylim(ymin=0,ymax=5)
    ax.set_ylabel('AVERAGE RATING')
    ax.set_xlabel('DATE(FROM FIRST REVIEW TO LAST REVIEW)')
    ax.set_title('SDial Carpet Cleaning RATING TREND')
    plt.savefig('business_avg_rating_date3.png')

    #close connection to the database
    close_conn(conn)
