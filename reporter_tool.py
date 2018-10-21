#!/usr/bin/python3


# Reporter tool from news database

import psycopg2

DBNAME = "news"

try:
    db = psycopg2.connect(database=DBNAME)
except TimeoutError as e:
    print("Unable to connect to the database")
cursor = db.cursor()

cursor.execute("select articles.title, count(*) as views from articles,\
               log where articles.slug = substring(log.path from 10) \
               group by articles.title order by count(*) desc limit 3;")

articles = cursor.fetchall()

cursor.execute("select authors.name, count(*) as views from log, authors,\
                articles where authors.id = articles.author \
                and articles.slug = substring(log.path from 10) \
                group by authors.name order by count(*) desc;")

authors = cursor.fetchall()

cursor.execute("select to_char(total_req.date,'Month-dd-yyyy'),\
               round(CAST(NOK_req.nok_requests as DECIMAL)\
               /CAST(total_req.count as DECIMAL)*100,2) \
               as error_rate from NOK_req,total_req where\
                NOK_req.time = total_req.date and \
                (CAST(NOK_req.nok_requests as DECIMAL)\
                /CAST(total_req.count as DECIMAL))*100 > 1;")

date_error = cursor.fetchall()

db.close()

# 1. What are the most popular three articles of all time?
print("\nThe most popular three articles of all time are:\n")
i = 0
for article in articles:
    i += 1
    print("%s. %s - %s views " % (i, article[0], article[1]))
# 2.Who are the most popular article authors of all time?
print("\n\nThe most popular article authors of all time are:\n")
j = 0
for author in authors:
    j += 1
    print("%s. %s - %s views " % (j, author[0], author[1]))
# 3.On which days did more than 1% of requests lead to errors?
print("\nThe days which more than 1% of requests led to errors were:\n")
print("{} {}, {} - {}% errors\n".format(date_error[0][0][0:4],
                                        date_error[0][0][10:12],
                                        date_error[0][0][-4:18],
                                        date_error[0][1]))
