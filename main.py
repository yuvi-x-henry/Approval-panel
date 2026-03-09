from flask import Flask, render_template_string, request, redirect, url_for, session
import os, json, uuid, re, random, requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.debug = True

APPROVED_KEYS_FILE = 'approved_keys.txt'
DEVICE_KEYS_FILE = 'device_keys.json'
HEADER_IMAGE = "https://i.imgur.com/DmqE91t.jpeg"

# -------- Device keys storage --------
def load_device_keys():
    if os.path.exists(DEVICE_KEYS_FILE):
        try:
            with open(DEVICE_KEYS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_device_keys(keys):
    with open(DEVICE_KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def get_or_create_device_key(device_id):
    keys = load_device_keys()
    if device_id in keys:
        return keys[device_id]["key"]

    new_key = str(random.randint(10**14, 10**15 - 1))
    keys[device_id] = {"key": new_key}
    save_device_keys(keys)
    return new_key

# -------- Device info extractor --------
def get_device_name_and_model(user_agent):
    if not user_agent:
        return "Unknown Device", "Unknown Model"
    if "Android" in user_agent:
        match = re.search(r'\b([\w\s\-]+)\sBuild', user_agent)
        device_model = match.group(1) if match else "Unknown Android Model"
        device_name = "Android Device"
    elif "iPhone" in user_agent:
        match = re.search(r'\biPhone\s?([\w\d]+)?', user_agent)
        device_model = f"iPhone {match.group(1)}" if match and match.group(1) else "iPhone"
        device_name = "iOS Device"
    elif "iPad" in user_agent:
        device_name = "iOS Device"
        device_model = "iPad"
    else:
        device_name = "Unknown Device"
        device_model = "Unknown Model"
    return device_name, device_model

# -------- Approved keys helpers --------
def is_key_approved(unique_key):
    if os.path.exists(APPROVED_KEYS_FILE):
        with open(APPROVED_KEYS_FILE, 'r') as f:
            approved = [line.strip() for line in f.readlines() if line.strip()]
        return unique_key in approved
    return False

def save_approved_key(unique_key):
    with open(APPROVED_KEYS_FILE, 'a') as f:
        f.write(unique_key + '\n')

# -------- Splash --------
@app.route('/')
def splash():
    return render_template_string("""
<html>
<head>
<style>
body {
margin:0;
padding:0;
background:black;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
height:100vh;
overflow:hidden;
color:white;
font-family:'Segoe UI',sans-serif;
}
img.splash-image {
width:100%;
height:100%;
object-fit:cover;
position:absolute;
top:0;
left:0;
z-index:0;
}
.loader {
border:6px solid rgba(255,255,255,0.2);
border-top:6px solid #ff00ff;
border-radius:50%;
width:60px;
height:60px;
animation:spin 1s linear infinite;
z-index:1;
}
@keyframes spin {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}
</style>
<script>setTimeout(()=>{window.location.href="/approval";},3000);</script>
</head>
<body>
<img class="splash-image" src="https://i.imgur.com/B2iRAOX.jpeg">
<div class="loader"></div>
</body>
</html>
""")

# -------- Approval --------
@app.route('/approval')
def approval():
    user_agent = request.headers.get('User-Agent', '')
    device_name, device_model = get_device_name_and_model(user_agent)

    if 'device_id' not in session:
        session['device_id'] = str(uuid.uuid4())

    device_id = session['device_id']
    unique_key = get_or_create_device_key(device_id)

    if is_key_approved(unique_key):
        return redirect(url_for('approved', key=unique_key))

    return f"""
<html>
<head>
<style>
body {{
background:black;
color:white;
font-family:'Segoe UI';
text-align:center;
margin:0;
padding:0;
}}
img {{
width:800px;
height:auto;
border-radius:12px;
margin-top:20px;
box-shadow:0 0 35px #ff00ff;
}}
.key-card {{
background:rgba(255,255,255,0.05);
border:2px solid #ff00ff;
border-radius:25px;
max-width:800px;
margin:30px auto;
padding:30px 40px;
box-shadow:0 0 40px #ff00ff;
}}
.key-text {{
font-size:45px;
color:#ff00ff;
font-weight:bold;
word-break:break-word;
margin:15px 0;
}}
</style>
</head>
<body>

<img src="{HEADER_IMAGE}">
<h1 style="color:#ff00ff;">HENRY-X Approval</h1>

<div class="key-card">
<p>Device: {device_name} - {device_model}</p>
<p><b>HENRY-X Approval ID</b></p>
<p class="key-text">{unique_key}</p>

<form action="/check-permission" method="post">
<input type="hidden" name="unique_key" value="{unique_key}">
<input type="submit" value="Check Approval">
</form>
</div>

</body>
</html>
"""

# -------- Check --------
@app.route('/check-permission', methods=['POST'])
def check_permission():
    unique_key = request.form.get('unique_key', '')
    try:
        response = requests.get("https://pastebin.com/raw/dS4jJZDY", timeout=6)
        approved_tokens = [t.strip() for t in response.text.splitlines() if t.strip()]
    except:
        approved_tokens = []

    if unique_key in approved_tokens:
        save_approved_key(unique_key)
        return redirect(url_for('approved', key=unique_key))
    else:
        return redirect(url_for('not_approved', key=unique_key))

# -------- Approved --------
@app.route('/approved')
def approved():
    key = request.args.get('key', '')
    redirect_link = "https://apparent-jonie-farman-64b2ec8e.koyeb.app/"
    return f"""
<html>
<head>
<meta http-equiv="refresh" content="2;url={redirect_link}">
<style>
body {{
background:black;
color:white;
text-align:center;
font-family:'Segoe UI';
}}
img {{
width:800px;
margin-top:20px;
border-radius:12px;
box-shadow:0 0 25px #00ff99;
}}
</style>
</head>
<body>
<img src="{HEADER_IMAGE}">
<h1 style="color:#00ff99;">✅ APPROVED</h1>
<p>ID: {key}</p>
<p>Redirecting...</p>
</body>
</html>
"""

# -------- Not Approved --------
@app.route('/not-approved')
def not_approved():
    key = request.args.get('key', '')
    wa_text = f"Hello I want approval for HENRY-X. My ID is {key}"
    wa_link = "https://wa.me/919235741670?text=" + requests.utils.requote_uri(wa_text)

    return f"""
<html>
<head>
<style>
body {{
background:black;
color:white;
text-align:center;
font-family:'Segoe UI';
}}
img {{
width:800px;
margin-top:20px;
border-radius:12px;
box-shadow:0 0 35px #ff0033;
}}
</style>
</head>
<body>

<img src="{HEADER_IMAGE}">
<h1 style="color:#ff0033;">ACCESS DENIED</h1>
<p>Your ID:</p>
<p style="font-size:28px;">{key}</p>

<a href="{wa_link}" style="background:#25D366;color:white;padding:20px 30px;border-radius:12px;text-decoration:none;display:inline-block;margin-top:20px;">
📱 Request Approval on WhatsApp
</a>

</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
