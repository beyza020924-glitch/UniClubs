from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)  
app.secret_key = 'key' 


db = mysql.connector.connect(
    host="localhost",
    user="hilal",  
    password="hilal123",
    database="UniClubs"
)

@app.route("/logIn", methods=["POST", "GET"])
def log_in():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if user['password'] == password: 
                session['user_id'] = user['id']
                session['username'] = f"{user['name']} {user['surname']}"
                return redirect(url_for("events"))
            else:
                error_message = "Invalid password. Please try again."
                return render_template('logIn.html', error_message=error_message)
        else:
            error_message = "No account found with this email."
            return render_template('logIn.html', error_message=error_message)

    return render_template('logIn.html')  

@app.route("/signIn", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        name = request.form.get("userName")
        surname = request.form.get("userSurname")
        email = request.form.get("email")
        password = request.form.get("password")
        phone_number = request.form.get("phone-number")
        user_type = request.form.get("userType")


        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (name, surname, email, password, phone_number, user_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, surname, email, password, phone_number, user_type))
        db.commit()

        return redirect(url_for("log_in"))

    return render_template("signIn.html")

@app.route("/bookEvent", methods=["POST"])
def book_event():
    if request.method == "POST":
        name = request.form.get("userName")
        surname = request.form.get("userSurname")
        email = request.form.get("email")
        event_name = request.form.get("event_name")  


        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('log_in'))  


        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO bookings (user_id, user_name, user_surname, email, event_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, name, surname, email, event_name))
        db.commit()

        return redirect(url_for("events"))


@app.route('/myProfile')
def my_profile():
    user_id = session.get('user_id')

    if user_id:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()


        cursor.execute("SELECT * FROM bookings WHERE user_id = %s", (user_id,))
        bookings = cursor.fetchall()

        if user:
            return render_template('myProfile.html', user=user, bookings=bookings)
        else:

            return redirect(url_for('log_in'))
    else:
        return redirect(url_for('log_in'))
    

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/clubsPage1')
def clubs_page1():
    return render_template('clubsPage1.html')

@app.route('/clubsPage2')
def clubs_page2():
    return render_template('clubsPage2.html')

if __name__ == "__main__":
    app.run(debug=True)




