# !/usr/bin/python

import mysql.connector
import matplotlib.pyplot as plt
from itertools import groupby
import numpy as np
from sklearn import neighbors


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
    # open connection to the database
    conn = open_conn()

    # fetch results from the database
    result = executeQuery(conn,('select business_id, user.id as user_id, business.stars as otherUser_rate_thisBusiness, user.average_stars as thisUser_rate_otherBusiness, review.stars as thisUser_rate_thisBusiness from business inner join review on business.id = review.business_id inner join user on user.id = review.user_id order by business_id limit 500;'))
    # retreive results as a list from the list of tuples
    # list advantage: by order and can contain duplicates

    #knn clssifier
    knn = neighbors.KNeighborsClassifier()
    otherUser_rate_thisBusiness = [[row[2],row[3]] for row in result]
    data = np.array(otherUser_rate_thisBusiness)
    thisUser_rate_thisBusiness = [row[4] for row in result]
    labels = np.array(thisUser_rate_thisBusiness)
    knn.fit(data, labels)
    valid = []
    i = 0
    flag = 0
    for input_dt in otherUser_rate_thisBusiness:
        pred = knn.predict(np.reshape(input_dt, (1, -1)))
        if (pred - thisUser_rate_thisBusiness[i]) > 1 or (pred - thisUser_rate_thisBusiness[i]) < -1:
            flag = flag + 1
        i = i + 1
    error= float(flag) / float(500)
    if flag < 100:
        print "validation pass"
        print "error percentage:" + str(error)


    # close connection to the database
    close_conn(conn)
