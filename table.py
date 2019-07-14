import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="naren",
  passwd="nopassword"
)

cur=mydb.cursor()

cur.execute("CREATE DATABASE mydb")

cur.execute('''USE mydb''')

cur.execute('''CREATE TABLE User(
                 name varchar(30)
                 username varchar(30),
                 password varchar(30))''')

cur.execute('''CREATE TABLE form(
                  username varchar(30),
                  title varchar(30),
                  description varchar(50),
                  ques VARCHAR(100),
                  reqd varchar(10),
                  anstype varchar(30),
                  opnum int,
                  opts varchar(50),
                  noques int,
                  deadline date,
                  submission int,
                  sub_limit int''')

cur.execute('''CREATE TABLE Response(
                  creator varchar(30),
                  title varchar(50),
                  respuser varchar(30),
                  answer varchar(100),
                  submission int,
                  timesub datetime,
                  noques int,
                  question varchar(50)''')

cur.execute('''CREATE TABLE Limituser(
                 creator varchar(30)
                 title varchar(50),
                 respuser varchar(30),
                 subuser int''')



