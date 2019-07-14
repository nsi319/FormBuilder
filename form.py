from flask import Flask, render_template, url_for, flash, redirect, request,session,jsonify
import random, json
from datetime import date,datetime
from flaskext.mysql import MySQL
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

app = Flask(__name__)
app.secret_key = 'secret'

app.config['MYSQL_DATABASE_USER'] = 'naren'
app.config['MYSQL_DATABASE_PASSWORD'] = 'nopassword'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)
@app.route("/")


@app.route("/welcome",methods=['GET', 'POST'])
def welcome():
	session.pop("_flashes",None)
	return redirect(url_for('login'))
	return render_template('welcome.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    error=None
    msg=None
    val=0

    if request.method == 'POST':
    	username = request.form['username']
    	password = request.form['password']
    	cur = mysql.connect().cursor()
    	cur.execute('''SELECT * FROM user WHERE username =%s''',(str(username)))
    	result = cur.fetchone()

    	if result is not None and password == str(result[2]):
    		session['name'] = str(result[0])
    		session['username']=username
    		session['password']=password
    		session.pop('_flashes',None)
    		flash("Welcome " + str(result[0]))
    		return redirect(url_for('home'))
    	else:
    		error="Invalid credentials "
    		return render_template('login.html',error=error)

    return render_template('login.html',error=error)


@app.route("/register",methods = ['GET','POST'])    
def register():
    error = None
    msg = None
    con = mysql.connect()
    cur = con.cursor()

    if request.method == 'POST':

        if request.form['password'] != request.form['cpassword']:
            error = "Passwords not matching"
            return render_template('register.html',error=error)
        else:
        	cur.execute('''SELECT * FROM USER WHERE username=%s''',request.form['username'])
        	result = cur.fetchone()

        	if result is not None:
        		error = "Username already exists"
        		return render_template('register.html',error=error)
        	else:
        		cur.execute('''INSERT INTO USER VALUES(%s,%s,%s)''',(str(request.form['name']),str(request.form['username']),str(request.form['password'])))
        		con.commit()
        		return redirect(url_for('login'))

    return render_template('register.html',error=error)

@app.route("/home",methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route("/delete",methods=['GET','POST'])

def delete():
     error=None
     return render_template('delete.html',error=error)

@app.route("/response",methods=['GET','POST'])

def response():

	error="No links found"
	con = mysql.connect()
	cur = con.cursor()
	today = date.today()
	date1 = today.strftime("%Y/%m/%d")
	cur.execute('''SELECT * FROM FORM GROUP BY title ORDER BY submission DESC''')
	result = cur.fetchall()

	if result is not None:
		return render_template('response.html',result=result)
	else:
		return render_template('response.html',error=error)

@app.route("/custom",methods=['GET','POST'])

def custom():
	error=None
	con = mysql.connect()
	cur = con.cursor()

	if request.method == "POST":

		data = request.form
		name = str(session['username'])
		title = str(data['title'])
		query='''SELECT * FROM FORM WHERE username=%s AND title =%s'''
		cur.execute(query,(name,title))
		result=cur.fetchone()
		if result is not  None:
			return render_template("create.html",error="Title not available")
	
		desc = str(data['desc'])
		deadline = data['deadline']
		if deadline == "":
			deadline = "3000-12-12"
		sub_limit = data['sub_limit']
		if not sub_limit:
			sub_limit=100

		submission = 0
		query ='''INSERT INTO FORM VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

		cur.execute(query,(name,title,desc,"Name?","yes","text",0,"NA",0,deadline,0,sub_limit))
		con.commit()
		cur.execute(query,(name,title,desc,"Age?","yes","number",0,"NA",1,deadline,0,sub_limit))
		con.commit()
		cur.execute(query,(name,title,desc,"Mobile Number:","yes","number",2,"NA",0,deadline,0,sub_limit))
		con.commit()
		cur.execute(query,(name,title,desc,"Email Address?","yes","email",3,"NA",0,deadline,0,sub_limit))
		con.commit()

		session.pop('_flashes',None)
		flash("Welcome " + session['name'])
		flash("Form " + title + " added successfully")
		return redirect(url_for('home'))

	return render_template('custom.html',error=error)


@app.route("/create",methods=['GET','POST'])

def create():
	error=None
	q = "ques"
	a = "anstype"
	i=0
	j=0
	k=0
	cnum=0
	con = mysql.connect()
	cur = con.cursor()

	if request.method == "POST":

		data = request.form
		name = str(session['username'])
		title = str(data['title'])
		noques = int(data['total'])
		query='''SELECT * FROM FORM WHERE username=%s AND title =%s'''
		cur.execute(query,(name,title))
		result=cur.fetchone()
		if result is not  None:
			return render_template("create.html",error="Title not available")
	
		desc = str(data['desc'])
		deadline = data['deadline']
		if deadline == "":
			deadline = "3000-12-12"
		sub_limit = data['sub_limit']
		if not sub_limit:
			sub_limit=100

		ques = data.getlist('ques')
		ans = data.getlist('ans')
		anstype = data.getlist('anstype')

		submission = 0
		while(int(i)< int(noques)):
			query ='''INSERT INTO FORM VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
			addit = int(i+1)
			reqd = data.get('reqd' + str(addit))

			if anstype[i] in ('text','number','date'):
				cur.execute(query,(name,title,desc,str(ques[i]),str(reqd),str(anstype[i]),0,"NA",int(ques_num[i]),deadline,0,sub_limit))
				con.commit()
			else:
				j=0
				while (j<int(optnum[k])):
					cur.execute(query,(name,title,desc,str(ques[i]),str(reqd),str(anstype[i]),int(optnum[k]),str(opts[cnum+j]),int(ques_num[i]),deadline,0,sub_limit))
					con.commit()
					j = int(j)+1

				cnum=cnum+j
				k=k+1
			i = int(i) + 1

		session.pop('_flashes',None)
		flash("Welcome " + session['name'])
		flash("Form " + title + " added successfully")
		return redirect(url_for('home'))

	return render_template('create.html',error=error)



@app.route("/view",methods=['GET','POST'])

def view():
	con = mysql.connect()
	cur = con.cursor()
	query = '''SELECT * FROM FORM WHERE username=%s GROUP BY title'''
	cur.execute(query,str(session['username']))
	result = cur.fetchall()
	if(result is not None):
		return render_template('view.html',result=result)
	else:
		error="no responses created"
		return render_template('view.html',error=error)

@app.route("/analytics/<name>/<title>",methods=['GET','POST'])

def analytics(name,title):
	con = mysql.connect()
	cur = con.cursor()
	cur.execute(''' SELECT MAX(noques) FROM FORM WHERE username=%s AND title=%s ''',(str(name),str(title)))
	result = cur.fetchone()
	noques = int(result[0])

	query = '''SELECT DISTINCT noques,anstype FROM FORM WHERE username=%s AND title=%s  ORDER BY noques'''
	cur.execute(query,(name,title))
	form = cur.fetchall()

	query = '''SELECT noques,answer FROM RESPONSE WHERE creator=%s AND title=%s  ORDER BY noques'''
	cur.execute(query,(name,title))
	resp = cur.fetchall()

	query = '''SELECT count(*) FROM RESPONSE WHERE creator=%s AND title=%s  ORDER BY noques'''
	cur.execute(query,(name,title))
	row = cur.fetchone()[0]
	n1 = noques + 1
	i=0
	k=1
	arr = []

	while(i < n1):
		arr=[]

		if(form[i][1] == "radio" or form[i][1] == "checkbox"):
			j=0
			while(j<row):
				if (resp[j][0]==i):
					arr.append(resp[j][1])
				j=j+1
			plt.subplot(n1,n1-1,k)
			sns.countplot(x=arr)
			plt.title("Response graph QNO" + str(i+1))
			k=k+1
			arr=[]
		i=i+1
	plt.show()

	return redirect(url_for('view'))

@app.route("/form_response/<name>/<title>", methods=['GET','POST'])

def form_response(name,title):

	con = mysql.connect()
	cur = con.cursor()
	query = '''SELECT * FROM RESPONSE WHERE CREATOR=%s AND TITLE=%s ORDER BY noques'''
	cur.execute(query,(name,title))
	resp = cur.fetchall()
	query = '''SELECT * FROM FORM WHERE username=%s AND title=%s ORDER BY noques'''
	cur.execute(query,(name,title))
	form = cur.fetchall()

	return render_template('user_response.html',result=resp,name=name,title=title,resform=form)

@app.route("/form_view/<name>/<title>", methods=['GET','POST'])

def form_view(name,title):
	con = mysql.connect()
	cur = con.cursor()
	i=0
	j=0
	error = "error submitting"
	query ='''SELECT DISTINCT deadline FROM form WHERE username=%s AND title=%s'''
	cur.execute(query,(name,title))
	result = cur.fetchone()
	
	if date.today() > result[0]:
		error = "Form deadline reached"
		return render_template('fill.html',error=error)

	if request.method == 'POST':

		data = request.form
		quest= data.getlist('quest')
		creator = data['creator']
		title = data['title']
		respuser = session['username']
		cur.execute(''' SELECT MAX(noques),submission,sub_limit FROM FORM WHERE username=%s AND title=%s''',(str(creator),str(title)))
		result = cur.fetchone()
		noques = int(result[0]) + 1
		sub_limit = int(result[2])
		submission = int(result[1]) + 1


		query = '''SELECT * FROM LIMITUSER WHERE creator=%s AND title=%s AND respuser=%s'''
		cur.execute(query,(creator,title,respuser))
		result = cur.fetchone()
		if result is not None:
			if int(result[3])>=sub_limit:
				error = "You have reached maximum submissions"
				return render_template('fill.html',error=error)
			else:
				lim = int(result[3]) + 1
				query = ''' UPDATE LIMITUSER SET SUBUSER=%s WHERE creator=%s AND title=%s AND respuser=%s'''
				cur.execute(query,(lim,creator,title,respuser))
				con.commit()
		else:
			query = ''' INSERT INTO LIMITUSER VALUES(%s,%s,%s,%s) '''
			cur.execute(query,(creator,title,respuser,1))
			con.commit()

		while (i<noques):
			query = '''INSERT INTO RESPONSE VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
			answer = data.getlist("answer" + str(i))
			j=0
			while (j<len(answer)):
				cur.execute(query,(creator,title,respuser,str(answer[j]),submission,datetime.now(),i,str(quest[i])))
				con.commit()
				j=j+1
			i=i+1

		query = '''UPDATE FORM SET submission=%s WHERE username=%s and title=%s'''
		cur.execute(query,(submission,creator,title))
		con.commit()

		session.pop("_flashes",None)
		flash("Welcome " + session['username'])
		flash("FORM: " + title + ", Response submitted")
		return redirect(url_for('home'))
	else:
		cur.execute(''' SELECT * FROM FORM WHERE username=%s AND title=%s ORDER BY submission DESC''',(str(name),str(title)))
		result = cur.fetchall()
		return render_template('fill.html',result=result)

@app.route('/fill', methods=['GET','POST'])

def fill():
	return render_template('fill.html')

@app.route('/dynuser',methods=['POST'])

def dynuser():
    conn=mysql.connect()
    cur=conn.cursor()
    usern=request.form['username']
    query='''SELECT * FROM USER WHERE username=%s'''
    cur.execute(query,(usern))
    result=cur.fetchone()
    if result is not  None:
        return jsonify({'output':'Username NOT available'})
    else:
        return jsonify({'output':'Username available'})


@app.route('/dyntitle',methods=['POST'])

def dyntitle():
    conn=mysql.connect()
    cur=conn.cursor()
    t=request.form['title']
    query='''SELECT * FROM FORM WHERE username=%s AND title =%s'''
    cur.execute(query,(session['username'],t))
    result=cur.fetchone()
    if result is not  None:
        return jsonify({'output':'Title NOT available'})
    else:
        return jsonify({'output':'Title available'})
	
@app.route("/logout",methods=['GET','POST'])

def logout():

    session.pop('name',None)
    session.pop('username',None)
    session.pop('_flashes',None)
    flash("Log out successfull")
    return redirect(url_for('welcome'))

    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
