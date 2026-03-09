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

    return f"""
<html>
<body style="background:black;color:white;text-align:center;font-family:Segoe UI;">

<img src="{HEADER_IMAGE}" style="width:800px;border-radius:12px;margin-top:20px;">

<h1 style="color:#ff00ff;">HENRY-X Approval</h1>

<p>{device_name} - {device_model}</p>

<h2>Your Approval ID</h2>

<p style="font-size:40px;color:#ff00ff;">{key}</p>

<form action="/check" method="post">

<input type="hidden" name="key" value="{key}">

<button style="padding:15px 30px;font-size:18px;background:#ff00ff;border:none;border-radius:10px;color:white;">
Check Approval
</button>

</form>

</body>
</html>
"""

# ---------- Check ----------
@app.route("/check",methods=["POST"])
def check():

    key = request.form.get("key","")

    try:

        r = requests.get(
            "https://pastebin.com/raw/dS4jJZDY",
            timeout=5
        )

        approved = [x.strip() for x in r.text.splitlines()]

    except:
        approved = []

    if key in approved:
        save_approved_key(key)
        return redirect(url_for("approved",key=key))

    return redirect(url_for("notapproved",key=key))

# ---------- Approved ----------
@app.route("/approved")
def approved():

    key = request.args.get("key","")

    link = "https://apparent-jonie-farman-64b2ec8e.koyeb.app/"

    return f"""
<html>
<head>

<meta http-equiv="refresh" content="2;url={link}">

</head>

<body style="background:black;color:white;text-align:center;font-family:Segoe UI;">

<img src="{HEADER_IMAGE}" style="width:800px;border-radius:12px;margin-top:20px;">

<h1 style="color:#00ff99;">APPROVED</h1>

<p>ID : {key}</p>

<p>Redirecting...</p>

</body>
</html>
"""

# ---------- Not Approved ----------
@app.route("/notapproved")
def notapproved():

    key = request.args.get("key","")

    text = f"Hello I want approval for HENRY-X. My ID is {key}"

    wa = "https://wa.me/919235741670?text="+requests.utils.requote_uri(text)

    return f"""
<html>

<body style="background:black;color:white;text-align:center;font-family:Segoe UI;">

<img src="{HEADER_IMAGE}" style="width:800px;border-radius:12px;margin-top:20px;">

<h1 style="color:red;">ACCESS DENIED</h1>

<p>Your ID</p>

<h2>{key}</h2>

<a href="{wa}" style="background:#25D366;padding:20px 30px;color:white;border-radius:10px;text-decoration:none;">
Request Approval
</a>

</body>

</html>
"""

if __name__ == "__main__":

    port = int(os.environ.get("PORT",5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
