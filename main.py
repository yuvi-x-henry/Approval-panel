from flask import Flask, render_template_string, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "henry_secret"

USER_FILE="users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE,"w") as f:
        json.dump({},f)

def load_users():
    with open(USER_FILE) as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE,"w") as f:
        json.dump(data,f)


STYLE="""

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial;
}

body{
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:linear-gradient(to top,#021a40,#3da0ff);
}

.panel{
width:90%;
max-width:420px;
background:rgba(0,0,0,0.25);
padding:25px;
border-radius:20px;
text-align:center;
}

.panel img{
width:100%;
border-radius:15px;
margin-bottom:20px;
}

.title{
font-size:32px;
color:white;
margin-bottom:30px;
font-weight:bold;
}

input{
width:100%;
padding:14px;
margin:10px 0;
border-radius:10px;
border:none;
}

.btn{
display:block;
width:100%;
padding:16px;
margin:12px 0;
border:none;
border-radius:12px;
font-size:18px;
font-weight:bold;
color:white;
background:linear-gradient(45deg,#7b00ff,#003d1f);
}

.footer{
margin-top:15px;
font-size:13px;
color:white;
}

</style>

"""

# ---------------- HOME ----------------

@app.route("/")
def home():

    html=f"""

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HENRY-X</title>

{STYLE}

</head>

<body>

<div class="panel">

<img src="https://i.imgur.com/5rIeORl.jpeg">

<div class="title">COOKIE-X-X</div>

<a href="/login"><button class="btn">LOGIN'X</button></a>
<a href="/signup"><button class="btn">SIGNUP'X</button></a>

<div class="footer">Coookie Automation Tool / By / Owner Henry !!</div>

</div>

</body>
</html>

"""

    return render_template_string(html)

# ---------------- LOGIN ----------------

@app.route("/login",methods=["GET","POST"])
def login():

    msg=""

    if request.method=="POST":

        user=request.form["username"]
        pwd=request.form["password"]

        users=load_users()

        if user in users and users[user]==pwd:
            session["user"]=user
            return redirect("/dashboard")

        else:
            msg="Invalid Login!"

    html=f"""

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>

{STYLE}

</head>

<body>

<div class="panel">

<img src="https://i.imgur.com/5rIeORl.jpeg">

<div class="title">LOGIN</div>

<form method="POST">

<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>

<button class="btn">LOGIN'X</button>

</form>

<div class="footer">{msg}</div>

</div>

</body>
</html>

"""

    return render_template_string(html)

# ---------------- SIGNUP ----------------

@app.route("/signup",methods=["GET","POST"])
def signup():

    msg=""

    if request.method=="POST":

        user=request.form["username"]
        pwd=request.form["password"]

        users=load_users()

        if user in users:
            msg="Username Already Exists!"

        else:
            users[user]=pwd
            save_users(users)
            return redirect("/login")

    html=f"""

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Signup</title>

{STYLE}

</head>

<body>

<div class="panel">

<img src="https://i.imgur.com/5rIeORl.jpeg">

<div class="title">SIGNUP</div>

<form method="POST">

<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>

<button class="btn">SIGNUP'X</button>

</form>

<div class="footer">{msg}</div>

</div>

</body>
</html>

"""

    return render_template_string(html)

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    user=session["user"]

    html=f"""

<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

{STYLE}

</head>

<body>

<div class="panel">

<img src="https://i.imgur.com/BhkciB4.jpeg">

<div class="title">WELCOME {user}</div>

<a href="/logout"><button class="btn">LOGOUT</button></a>

</div>

</body>
</html>

"""

    return render_template_string(html)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
