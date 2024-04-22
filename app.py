from flask import Flask,render_template, url_for,request,redirect,flash
import mysql.connector
from time import sleep

app = Flask(__name__)
app.secret_key = 'mahima@codegnan'
mydb = mysql.connector.connect(host='localhost',user='root',password='Admin',db='forfa')

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        card = int(request.form['card'])
        pin = int(request.form['pin'])
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select count(*) from atm where cardno=%s',[card])
        count = cursor.fetchone()[0]
        cursor.execute('select cardno from atm where cardno=%s',[card])
        card_sql = cursor.fetchone()[0]
        cursor.execute('select pin from atm where cardno=%s',[card])
        pin_sql = cursor.fetchone()[0]
        cursor.execute('select name from atm where cardno=%s',[card])
        name_sql = cursor.fetchone()[0]
        cursor.close()
        if count == 0:
            flash('Sorry there is an error please contact the bank')
            return redirect(url_for('home'))
        else:
            if card == card_sql and pin == pin_sql:
                return redirect(url_for('menu',name=name_sql, cardno=card_sql))
            elif card != card_sql:
                flash('Please check the card number again')
                return redirect(url_for('home'))
            elif pin != pin_sql:
                flash('Please check the pin number again')
                return redirect(url_for('home'))
    else:
        return render_template('home.html')

@app.route('/menu/<name>/<int:cardno>')
def menu(name, cardno):
    name1 = name
    cardno1=cardno
    return render_template('menu.html', name=name1, cardno=cardno1)

@app.route('/balanceenq/<int:cardno>', methods=['GET','POST'])
def balanceenq(cardno):
    card = cardno
    cursor = mydb.cursor(buffered=True)
    cursor.execute('select amount from atm where cardno=%s',[card])
    balance = float(cursor.fetchone()[0])
    cursor.close()
    return render_template('balanceenq.html', balance=balance,cardno=card)

@app.route('/changepin/<int:cardno>', methods=['GET','POST'])
def changepin(cardno):
    card=cardno
    if request.method == 'POST':
        accountno = int(request.form.get('account'))
        newpin = int(request.form.get('npin'))
        cnewpin = int(request.form.get('cnpin'))
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select account,pin from atm where cardno=%s',[card])
        data = cursor.fetchall()[0]
        account_sql = data[0]
        pin_sql = data[1]
        if newpin != cnewpin:
            flash("Pin and confirm pin doesn't match")
            return render_template('changepin.html')
        elif accountno != account_sql:
            flash('Please check and retype account number')
            return render_template('changepin.html')
        elif newpin == pin_sql:
            flash('New pin cannot be same as exisiting pin')
            return render_template('changepin.html')
        elif accountno == account_sql and newpin != pin_sql:
            cursor.execute('update atm set pin=%s where cardno=%s',[newpin,card])
            mydb.commit()
            cursor.close()
            flash('Successfully updated the new pin')
            return render_template('last.html')
    else:
        return render_template('changepin.html')

@app.route('/ministat/<int:cardno>')
def ministat(cardno):
    card=cardno
    cursor = mydb.cursor(buffered=True)
    cursor.execute('select cardno,name,account,amount from atm where cardno=%s',[card])
    data = cursor.fetchall()
    cardno_sql= data[0][0]
    name_sql=data[0][1]
    account_sql=data[0][2]
    amount_sql=data[0][3]
    cursor.close()
    return render_template('ministat.html', cardno=cardno_sql,name=name_sql,account=account_sql,amount=amount_sql)

@app.route('/withdrawal/<int:cardno>', methods=['GET','POST'])
def withdrawal(cardno):
    card=cardno
    cursor = mydb.cursor(buffered=True)
    cursor.execute('select amount from atm where cardno=%s',[card])
    amount_sql= cursor.fetchone()[0]
    if request.method=='POST':
        draw_amt = int(request.form.get('draw'))
        account = int(request.form.get('account'))
        cursor.execute('select account from atm where cardno=%s',[card])
        account_sql=cursor.fetchone()[0]
        if account != account_sql:
            flash('Please enter correct Account number')
            return render_template('withdrawal.html')
        else:
            if amount_sql < draw_amt:
                flash('You have entered more than your balance please check ')
                return render_template('withdrawal.html')
            else:
                cursor.execute('update atm set amount=amount-%s where cardno=%s',[draw_amt,card])
                mydb.commit()
                cursor.close()
                sleep(10)
                return render_template('last.html')
    else:
        return render_template('withdrawal.html', amount=amount_sql)

@app.route('/deposit/<int:cardno>', methods=['GET','POST'])
def deposit(cardno):
    card=cardno
    if request.method=='POST':
        deposit_amt = int(request.form.get('deposit'))
        account = int(request.form.get('account'))
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select account from atm where cardno=%s',[card])
        account_sql=cursor.fetchone()[0]
        if account != account_sql:
            flash('Please enter correct Account number')
            return render_template('deposit.html')
        else:
            cursor.execute('update atm set amount=amount+%s where cardno=%s',[deposit_amt,card])
            mydb.commit()
            cursor.close()
            sleep(10)
            return render_template('last.html')
    else:
        return render_template('deposit.html')

@app.route('/last')
def last():
    return render_template('last.html')

app.run(debug=True, use_reloader=True)