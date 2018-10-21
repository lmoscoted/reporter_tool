# Reporter Tool

Reporting tool  prints out reports (in plain text) based on the data in a database, which contain information about the articles on a newspaper site. This reporting tool is a Python program using the psycopg2 module to connect to the database.

This program will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

## What our code need to report
**1. What are the most popular three articles of all time?**     Which articles have been accessed the most? 

**2. Who are the most popular article authors of all time?**     That is, when you sum up all of the articles each author  has written, which authors get the most page views?

**3. On which days did more than 1% of requests lead to       errors?**

## Tables
The _news_ database already has three tables:

* The **authors** table includes information about     the    authors of articles. It has three columns: _id, bio, name._
* The **articles** table includes the articles themselves. It has seven columns: _id, time, body, lead, slug, title, author._
* The **log** table includes one entry for each time a      user has accessed the site. Which has six columns: _id, time, status, method, ip, path._


# What you need to have installed

This project makes use of a Linux-based virtual machine (VM).
You need to have installed:
* Python: I used Python 3, which can be downloaded [here](https://www.python.org/downloads/release/python-371/).
* VirtualBox: For this project I used VirtualBox 5.1.38. This tool can be donwloaded [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.
* Vagrant: Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download the 2.2.0 version of this tool in this [link](https://www.vagrantup.com/).

You'll need to use a Unix-style terminal on your computer. If you are using a Mac or Linux system, your regular terminal program will do just fine. On Windows, we recommend using the Git Bash terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads).


## Download the VM configuration
You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
Alternately if you are familiar with GitHub, you can use Github to fork and clone the repository (https://github.com/udacity/fullstack-nanodegree-vm).

 This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.


This will give you the PostgreSQL database and support software needed for this project.

## Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!

## Donwload the data
The data that the database will use is in the _newsdata.sql._ This file can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.


Then, you need to load the data. In order to do that, you need to be logged on  your linux session by running  _vagrant up_ and then _vagrant ssh_, inside the vagrant directory. After that you need to run:

```
psql -d news -f newsdata.sql
```

Running this command will connect to the installed database and create the tables with their respective data.

# How to run it?

The python file `reporter_tool.py` must be put in the vagrant directory. 
Before run the code, we need to create the views used in this project. So that, you need to be logged on the linux session by running _vagrant up_ and _vagrant ssh_ inside the vagrant directory on your terminal. Then, You need to _run psql news_ to connect to the database. Finally, you need to run the SQL statements for both views, which is described in the final part of this documentation.

 You can open a new linux session or used the existent one from the previous step. If choose the last one, you need to exit from the news database -run _ctrl + d_-, then cd into the directory where you have the python file and run:

```
python reporter_tool.py
```

After that step, you will be able to see the answers for every question clearly printed out. 

# How does it work?
Basically, our code consist of three parts:
* The firts one, which will connect our code to the database
* The second one, which will execute three single queries for each question.
* The last one, will print out the results as plain text. 

For the question: **What are the most popular three articles of all time?** I used join operation with both the log and articles tables, by linking the slug column from the article table to the path column from the log table. I used _substring function_ in order to extract the slug part from the path column. And finally, I counted the number of times that one article was accessed by one user and ordered this result in a descendent way.

In the second question: **Who are the most popular article authors of all time?** I needed to link all the three tables. So, I just added the linking part between the article table - column author- and the author table -id column-  to the first query and replaced the article column with the author column as resulting column.

For the last question: **On which days did more than 1% of requests lead to       errors?** I used two views, which are described later. I linked the two views using join with the date column in the total_req view and the time column in the NOK_req view. Moreover, I cast the integer values from the total_req column and NOk_req column into decimal in order to compute the error rate for every day. And I converted into a string the date due to formatting output required. Finally, I selected all values greater than one. 


## Views 

In order to answer the third question I created two views:    total_req and NOK_req. The first one computes the total requests _-200 OK status and 404 error status-_ gotten on every day by using aggregation on the log table. The second one applies the same technique but, this time, computes the NOK requests (404 error code).   

```
1. create view total_req as select time::DATE as date, count(*) from log group by date order 
        by date asc;

2. create view NOK_req as select time::DATE, count(status) as NOK_requests from log where status 
        like '%404%' group by  time::DATE order by time::DATE asc;

        ```

