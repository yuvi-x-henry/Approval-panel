from flask import Flask, render_template_string, request, redirect, url_for, session
import os, json, uuid, re, random, requests, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

APPROVED_KEYS_FILE="approved_keys.txt"
DEVICE_KEYS_FILE="device_keys.json"
HEADER_IMAGE="https://i.imgur.com/DmqE91t.jpeg"


# -------- Load Device Keys --------
def load_device_keys():
    try:
        if os.path.exists(DEVICE_KEYS_FILE):
            with open(DEVICE_KEYS_FILE,"r") as f:
                return json.load(f)
    except:
        pass
    return {}

# -------- Save Device Keys --------
def save_device_keys(keys):
    try:
        with open(DEVICE_KEYS_FILE,"w") as f:
            json.dump(keys,f)
    except:
        pass

# -------- Generate Numeric Key --------
def generate_key():
    return str(random.randint(10**15,10**16-1))

# -------- Device Key --------
def get_or_create_device_key(device_id):

    keys=load_device_keys()

    if device_id in keys:
        return keys[device_id]["key"]

    new_key=generate_key()

    keys[device_id]={"key":new_key}

    save_device_keys(keys)

    return new_key

# -------- Device Info --------
def get_device_info(agent):

    if "Android" in agent:
        return "Android Device","Android"

    if "iPhone" in agent:
        return "iOS Device","iPhone"

    if "iPad" in agent:
        return "iOS Device","iPad"

    return "Unknown Device","Unknown Model"


# -------- Approved Check --------
def is_key_approved(key):

    if not os.path.exists(APPROVED_KEYS_FILE):
        return False

    with open(APPROVED_KEYS_FILE) as f:
        data=[x.strip() for x in f.readlines()]

    return key in data


def save_approved(key):
    with open(APPROVED_KEYS_FILE,"a") as f:
        f.write(key+"\n")


# -------- Splash --------
@app.route("/")
def splash():

    return render_template_string("""

<html>

<head>

<meta name="viewport" content="width=device-width,initial-scale=1">

<style>

body{
margin:0;
background:black;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
overflow:hidden;
}

img{
position:absolute;
width:100%;
height:100%;
object-fit:cover;
}

.loader{

width:70px;
height:70px;
border:6px solid rgba(255,255,255,0.2);
border-top:6px solid #ff00ff;
border-radius:50%;
animation:spin 1s linear infinite;
z-index:5;
}

@keyframes spin{
0%{transform:rotate(0)}
100%{transform:rotate(360deg)}
}

</style>

<script>
setTimeout(()=>{
window.location="/approval"
},3000)
</script>

</head>

<body>

<img src="https://i.imgur.com/B2iRAOX.jpeg">

<div class="loader"></div>

</body>

</html>

""")


# -------- Approval Page --------
@app.route("/approval")
def approval():

    agent=request.headers.get("User-Agent","")

    device_name,device_model=get_device_info(agent)

    if "device_id" not in session:
        session["device_id"]=str(uuid.uuid4())

    device_id=session["device_id"]

    key=get_or_create_device_key(device_id)

    if is_key_approved(key):
        return redirect(url_for("approved",key=key))

    return render_template_string("""

<html>

<head>

<meta name="viewport" content="width=device-width,initial-scale=1">

<style>

body{

margin:0;
font-family:Segoe UI;
color:white;

background:linear-gradient(270deg,#000,#0b0015,#000);
background-size:600% 600%;

animation:bgmove 15s infinite;

text-align:center;
}

@keyframes bgmove{

0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}

}

.header{

width:90%;
max-width:800px;

border-radius:18px;
margin-top:25px;

box-shadow:0 0 40px #ff00ff;
}

.card{

margin:40px auto;
width:90%;
max-width:500px;

background:rgba(255,255,255,0.05);

backdrop-filter:blur(20px);

border-radius:20px;

padding:40px;

box-shadow:
0 0 30px rgba(255,0,255,0.5),
inset 0 0 15px rgba(255,255,255,0.05);

}

.title{

font-size:38px;

color:#ff00ff;

text-shadow:0 0 20px #ff00ff;

}

.device{

opacity:0.8;

margin-top:10px;
}

.key{

font-size:40px;

margin:25px 0;

color:#00ffe7;

letter-spacing:4px;

text-shadow:

0 0 10px #00ffe7,
0 0 30px #00ffe7,
0 0 60px #00ffe7;

animation:keypulse 2s infinite;

}

@keyframes keypulse{

0%{transform:scale(1)}
50%{transform:scale(1.06)}
100%{transform:scale(1)}

}

button{

padding:15px 35px;

font-size:18px;

border:none;

border-radius:12px;

background:linear-gradient(45deg,#ff00ff,#7a00ff);

color:white;

cursor:pointer;

box-shadow:0 0 20px #ff00ff;

transition:0.3s;

}

button:hover{

transform:scale(1.1);

box-shadow:
0 0 40px #ff00ff;

}

</style>

</head>

<body>

<img src="{{header}}" class="header">

<div class="card">

<div class="title">
HENRY-X ACCESS
</div>

<div class="device">
{{device}} • {{model}}
</div>

<div>Your Approval ID</div>

<div class="key">
{{key}}
</div>

<form action="/check" method="post">

<input type="hidden" name="key" value="{{key}}">

<button>
Check Approval
</button>

</form>

</div>

</body>

</html>

""",header=HEADER_IMAGE,key=key,device=device_name,model=device_model)


# -------- Check --------
@app.route("/check",methods=["POST"])
def check():

    key=request.form.get("key","")

    try:

        r=requests.get(
        "https://pastebin.com/raw/dS4jJZDY",
        timeout=5)

        approved=[x.strip() for x in r.text.splitlines()]

    except:
        approved=[]

    if key in approved:
        save_approved(key)
        return redirect(url_for("approved",key=key))

    return redirect(url_for("notapproved",key=key))


# -------- Approved --------
@app.route("/approved")
def approved():

    key=request.args.get("key","")

    link="https://apparent-jonie-farman-64b2ec8e.koyeb.app/"

    return f"""

<html>

<head>

<meta http-equiv="refresh" content="2;url={link}">

</head>

<body style="background:black;color:white;text-align:center;font-family:Segoe UI;">

<img src="{HEADER_IMAGE}" style="width:90%;max-width:800px;border-radius:15px;margin-top:20px;box-shadow:0 0 30px #00ff99;">

<h1 style="color:#00ff99;font-size:40px;">ACCESS APPROVED</h1>

<p>ID : {key}</p>

<p>Redirecting...</p>

</body>

</html>

"""


# -------- Not Approved --------
@app.route("/notapproved")
def notapproved():

    key=request.args.get("key","")

    text=f"Hello I want approval for HENRY-X. My ID is {key}"

    wa="https://wa.me/919235741670?text="+requests.utils.requote_uri(text)

    return f"""

<html>

<body style="background:black;color:white;text-align:center;font-family:Segoe UI;">

<img src="{HEADER_IMAGE}" style="width:90%;max-width:800px;border-radius:15px;margin-top:20px;box-shadow:0 0 35px red;">

<h1 style="color:red;font-size:40px;">ACCESS DENIED</h1>

<p>Your ID</p>

<h2>{key}</h2>

<a href="{wa}" style="background:#25D366;padding:18px 35px;color:white;border-radius:12px;text-decoration:none;">
Request Approval
</a>

</body>

</html>

"""
