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
background:#0a0a0a;
color:white;
text-align:center;
}

.container{
width:90%;
max-width:520px;
margin:40px auto;
}

.image-box{
width:100%;
border-radius:16px;
overflow:hidden;
box-shadow:0 0 20px rgba(255,0,255,0.4);
}

.image-box img{
width:100%;
display:block;
}

.card{
margin-top:25px;
background:#111;
border-radius:16px;
padding:30px;
box-shadow:0 0 20px rgba(0,0,0,0.6);
}

.title{
font-size:32px;
color:#ff00ff;
margin-bottom:10px;
}

.device{
opacity:0.8;
margin-bottom:20px;
}

.key{
font-size:34px;
letter-spacing:3px;
color:#00ffe7;
margin:20px 0;
word-break:break-all;
}

button{

background:#ff00ff;
border:none;
padding:14px 30px;
border-radius:10px;
color:white;
font-size:16px;
cursor:pointer;

}

button:hover{
background:#cc00cc;
}

</style>

</head>

<body>

<div class="container">

<div class="image-box">
<img src="{{header}}">
</div>

<div class="card">

<div class="title">HENRY-X ACCESS</div>

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

<body style="background:#0a0a0a;color:white;font-family:Segoe UI;text-align:center;">

<div style="width:90%;max-width:520px;margin:40px auto;">

<div style="border-radius:16px;overflow:hidden;box-shadow:0 0 20px #00ff99;">
<img src="{HEADER_IMAGE}" style="width:100%;">
</div>

<div style="background:#111;border-radius:16px;padding:30px;margin-top:25px;">

<h1 style="color:#00ff99;">ACCESS APPROVED</h1>

<p style="opacity:0.8;">Your ID</p>

<h2>{key}</h2>

<p>Redirecting...</p>

</div>

</div>

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

<body style="background:#0a0a0a;color:white;font-family:Segoe UI;text-align:center;">

<div style="width:90%;max-width:520px;margin:40px auto;">

<div style="border-radius:16px;overflow:hidden;box-shadow:0 0 20px red;">
<img src="{HEADER_IMAGE}" style="width:100%;">
</div>

<div style="background:#111;border-radius:16px;padding:30px;margin-top:25px;">

<h1 style="color:red;">ACCESS DENIED</h1>

<p>Your Approval ID</p>

<h2>{key}</h2>

<a href="{wa}" style="background:#25D366;padding:14px 28px;color:white;border-radius:10px;text-decoration:none;display:inline-block;margin-top:15px;">
Request Approval
</a>

</div>

</div>

</body>

</html>

"""
