from flask import Flask, render_template_string, request, redirect, url_for, session
import os, json, uuid, re, random, requests, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

APPROVED_KEYS_FILE = "approved_keys.txt"
DEVICE_KEYS_FILE = "device_keys.json"
HEADER_IMAGE = "https://i.imgur.com/DmqE91t.jpeg"

# ---------- Load Device Keys ----------
def load_device_keys():
    try:
        if os.path.exists(DEVICE_KEYS_FILE):
            with open(DEVICE_KEYS_FILE,"r") as f:
                return json.load(f)
    except:
        pass
    return {}

# ---------- Save Device Keys ----------
def save_device_keys(keys):
    try:
        with open(DEVICE_KEYS_FILE,"w") as f:
            json.dump(keys,f,indent=2)
    except:
        pass

# ---------- Generate Numeric Key ----------
def generate_numeric_key():
    return str(random.randint(10**15, 10**16-1))

# ---------- Get Device Key ----------
def get_or_create_device_key(device_id):
    keys = load_device_keys()

    if device_id in keys:
        return keys[device_id]["key"]

    new_key = generate_numeric_key()
    keys[device_id] = {"key": new_key}
    save_device_keys(keys)

    return new_key

# ---------- Device Info ----------
def get_device_info(user_agent):

    if not user_agent:
        return "Unknown Device","Unknown Model"

    if "Android" in user_agent:
        match = re.search(r';\s?([^)]+)\sBuild', user_agent)
        model = match.group(1) if match else "Android"
        return "Android Device", model

    if "iPhone" in user_agent:
        return "iOS Device","iPhone"

    if "iPad" in user_agent:
        return "iOS Device","iPad"

    return "Unknown Device","Unknown Model"

# ---------- Approved Check ----------
def is_key_approved(key):

    if not os.path.exists(APPROVED_KEYS_FILE):
        return False

    with open(APPROVED_KEYS_FILE,"r") as f:
        keys = [k.strip() for k in f.readlines()]

    return key in keys

# ---------- Save Approved ----------
def save_approved_key(key):
    with open(APPROVED_KEYS_FILE,"a") as f:
        f.write(key+"\n")

# ---------- Splash ----------
@app.route("/")
def splash():

    return render_template_string("""
<html>
<head>
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
border:6px solid rgba(255,255,255,0.2);
border-top:6px solid #ff00ff;
border-radius:50%;
width:60px;
height:60px;
animation:spin 1s linear infinite;
z-index:10;
}
@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
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

# ---------- Approval ----------
@app.route("/approval")
def approval():

    user_agent = request.headers.get("User-Agent","")
    device_name,device_model = get_device_info(user_agent)

    if "device_id" not in session:
        session["device_id"] = str(uuid.uuid4())

    device_id = session["device_id"]

    key = get_or_create_device_key(device_id)

    if is_key_approved(key):
        return redirect(url_for("approved",key=key))

    
    return redirect(url_for("notapproved",key=key))


return f"""
<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body {{
margin:0;
font-family:Segoe UI;
background:linear-gradient(270deg,#000000,#0a0015,#000000);
background-size:600% 600%;
animation:bgmove 15s infinite;
color:white;
text-align:center;
}}

@keyframes bgmove {{
0%{{background-position:0% 50%;}}
50%{{background-position:100% 50%;}}
100%{{background-position:0% 50%;}}
}}

.header-img {{
width:90%;
max-width:800px;
border-radius:18px;
margin-top:20px;
box-shadow:0 0 40px #ff00ff;
}}

.card {{

margin:40px auto;
width:90%;
max-width:550px;

background:rgba(255,255,255,0.05);
backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,0.15);
border-radius:20px;

padding:40px;

box-shadow:
0 0 30px rgba(255,0,255,0.4),
inset 0 0 20px rgba(255,255,255,0.05);

}}

.title {{
font-size:38px;
color:#ff00ff;
text-shadow:0 0 15px #ff00ff;
}}

.device {{
opacity:0.8;
margin-bottom:25px;
}}

.key {{

font-size:42px;
letter-spacing:4px;
margin:25px 0;

color:#00ffe7;

text-shadow:
0 0 10px #00ffe7,
0 0 25px #00ffe7,
0 0 45px #00ffe7;

animation:keypulse 2s infinite;
}}

@keyframes keypulse {{

0%{{transform:scale(1)}}
50%{{transform:scale(1.06)}}
100%{{transform:scale(1)}}

}}

.btn {{

padding:16px 40px;

font-size:18px;

border:none;
border-radius:12px;

background:linear-gradient(45deg,#ff00ff,#7a00ff);

color:white;

cursor:pointer;

transition:0.4s;

box-shadow:0 0 15px #ff00ff;

}}

.btn:hover {{

transform:scale(1.08);

box-shadow:
0 0 25px #ff00ff,
0 0 45px #ff00ff;

}}

</style>

</head>

<body>

<img src="{HEADER_IMAGE}" class="header-img">

<div class="card">

<div class="title">HENRY-X ACCESS</div>

<div class="device">{device_name} • {device_model}</div>

<div>Your Approval ID</div>

<div class="key">{key}</div>

<form action="/check" method="post">

<input type="hidden" name="key" value="{key}">

<button class="btn">
Check Approval
</button>

</form>

</div>

</body>

</html>
"""
if __name__ == "__main__":

    port = int(os.environ.get("PORT",5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
