from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HENRY-X</title>

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

/* Blue Gradient */

background:linear-gradient(to top,#021a40,#3da0ff);

}

/* Panel */

.panel{

width:90%;
max-width:420px;

background:rgba(0,0,0,0.25);
padding:25px;

border-radius:20px;
text-align:center;

}

/* Image */

.panel img{

width:100%;
border-radius:15px;
margin-bottom:20px;

}

/* Title */

.title{

font-size:32px;
color:white;
margin-bottom:30px;
font-weight:bold;

}

/* Buttons */

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

/* Purple + Dark Green */

background:linear-gradient(45deg,#7b00ff,#003d1f);

}

/* Footer */

.footer{

margin-top:15px;
font-size:13px;
color:white;

}

</style>
</head>

<body>

<div class="panel">

<img src="https://i.imgur.com/BhkciB4.jpeg">

<div class="title">COOKIE-X-X</div>

<button class="btn">LOGIN'X</button>
<button class="btn">SIGNUP'X</button>

<div class="footer">Coookie Automation Tool / By / Owner Henry !!</div>

</div>

</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
