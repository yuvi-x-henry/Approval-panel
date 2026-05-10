from flask import Flask, render_template_string, request, redirect, url_for, jsonify, session
import threading, time, requests

app = Flask(__name__)
app.secret_key = "henryx_secret_2025"

# ----------------- GLOBALS -----------------
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'www.google.com'
}

tasks = {}  # task_id : {...}
users = {}  # {username: password}

# ==================== CONVO'X Homepage ====================
CONVOX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CONVO'X MODERNIZE</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', sans-serif;
  background: #0a0a0a; /* Dark background to make cards pop */
  background: linear-gradient(160deg, #1a0a1f 0%, #000 100%);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: hidden;
}

/* Container for Full Screen Cards */
.main-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  padding: 40px 20px;
  width: 100%;
  max-width: 1400px;
}

/* The Card Unit */
.mega-card {
  width: 400px; /* Bada size */
  position: relative;
  transition: transform 0.4s ease;
  cursor: pointer;
}

.mega-card:hover {
  transform: translateY(-15px);
}

/* Image Card (The actual top part) */
.image-card {
  width: 100%;
  height: 450px; /* Image ki height */
  border-radius: 30px 30px 0 0; /* Sirf upar se round */
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.image-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Attached Info Panel (Satik Panel) */
.info-panel {
  width: 100%;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-top: none; /* Image se judne ke liye */
  border-radius: 0 0 30px 30px; /* Sirf niche se round */
  padding: 25px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.info-panel h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  color: #fff;
  letter-spacing: 3px;
  margin-bottom: 10px;
  text-transform: uppercase;
  background: linear-gradient(90deg, #fff, #ff1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.info-panel p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* Status Indicator on Image */
.status-tag {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 255, 136, 0.2);
  padding: 5px 15px;
  border-radius: 20px;
  color: #00ff88;
  font-size: 10px;
  font-weight: bold;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(0, 255, 136, 0.4);
}

/* Styled Button */
.action-btn {
  background: linear-gradient(135deg, #ff00cc, #7a00ff);
  color: white;
  border: none;
  padding: 12px 35px;
  border-radius: 50px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 5px 15px rgba(255, 0, 204, 0.3);
}

.action-btn:hover {
  box-shadow: 0 8px 25px rgba(255, 0, 204, 0.6);
  transform: scale(1.05);
}

/* Responsive */
@media (max-width: 450px) {
  .mega-card {
    width: 100%;
  }
  .image-card {
    height: 350px;
  }
}
</style>
</head>
<body>

<div class="main-wrapper">

  <!-- CARD 1 -->
  <div class="mega-card">
    <div class="image-card">
      <div class="status-tag">● ONLINE</div>
      <!-- APNI IMAGE YAHAN LAGAYEIN -->
      <img src="https://raw.githubusercontent.com/yuvi-x-henry/Pf/refs/heads/main/7bc21a7c678acafd78cfff47b2d14668.jpg" alt="HENRY BOT">
    </div>
    <div class="info-panel">
      <h1>HENRY'X-BOT</h1>
      <p>This is a Premium Fighter & Masti Bot made by Henry. Optimized for VIP users with extreme run speed and automation.</p>
      <button class="action-btn" onclick="window.open('http://51.75.118.17:20058/')">Launch Bot</button>
    </div>
  </div>

  <!-- CARD 2 -->
  <div class="mega-card">
    <div class="image-card">
      <div class="status-tag">● ACTIVE</div>
      <!-- APNI IMAGE YAHAN LAGAYEIN -->
      <img src="https://raw.githubusercontent.com/yuvi-x-henry/Pf/refs/heads/main/7bc21a7c678acafd78cfff47b2d14668.jpg" alt="CONVO'X">
    </div>
    <div class="info-panel">
      <h1>CONVO'X PANEL</h1>
      <p>Full Access VIP Login and Multi-Token Control Panel. Manage your sessions with high-grade security and speed.</p>
      <button class="action-btn" onclick="window.location.href='/login'">Open Panel</button>
    </div>
  </div>

</div>

</body>
</html>
'''

# ==================== HENRY-X Auth HTML ====================
AUTH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} | HENRY-X</title>
<style>
:root{
  --max-w:700px;
  --card-h:1000px;
}
body{
  margin:0;
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:Poppins, sans-serif;
  background:linear-gradient(to bottom left, #ff0000, #800080);
}
.card{
  max-width:var(--max-w);
  height:var(--card-h);
  width:90%;
  background:rgba(0,0,0,0.6);
  border:3px solid black;
  border-radius:20px;
  box-shadow:0 10px 30px rgba(0,0,0,0.5);
  display:flex;
  flex-direction:column;
  align-items:center;
  padding:20px;
  color:white;
}
.card img{
  width:600px;
  max-width:100%;
  border-radius:15px;
  margin-bottom:20px;
}
h1{
  font-size:2rem;
  margin:0;
  margin-bottom:20px;
}
form{
  display:flex;
  flex-direction:column;
  gap:15px;
  width:80%;
}
input{
  padding:12px 15px;
  border-radius:12px;
  border:none;
  font-size:1rem;
  outline:none;
}
button{
  padding:12px 15px;
  border-radius:12px;
  border:none;
  font-size:1rem;
  font-weight:bold;
  background:linear-gradient(90deg,#ff0000,#800080);
  color:white;
  cursor:pointer;
  transition:0.3s;
}
button:hover{
  transform:scale(1.05);
}
a{
  color:#00ffea;
  font-weight:bold;
  text-decoration:none;
}
.message{
  margin-top:10px;
  font-weight:bold;
  font-size:1rem;
}
.success{color:#00ff9d}
.error{color:#ff4d4d}
</style>
</head>
<body>
<div class="card">
  <img src="https://i.imgur.com/9IEiv1n.jpeg" alt="HENRY-X">
  <h1>HENRY-X</h1>
  <form method="POST">
    <input type="text" name="username" placeholder="Enter Username" required>
    <input type="password" name="password" placeholder="Enter Password" required>
    {% if signup %}
    <input type="password" name="confirm" placeholder="Confirm Password" required>
    {% endif %}
    <button type="submit">{{ button_text }}</button>
  </form>
  {% if signup %}
    <p>Already have an account? <a href="{{ url_for('login') }}">Login</a></p>
  {% else %}
    <p>Don't have an account? <a href="{{ url_for('signup') }}">Sign Up</a></p>
  {% endif %}
  {% if message %}
    <p class="message {{ status }}">{{ message }}</p>
  {% endif %}
</div>
</body>
</html>
"""

# ==================== HENRY-X Home HTML ====================
HOME_HTML = """
<!DOCTYPE html>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HENRY-X | Home</title>
<style>
body {
  margin:0;
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  font-family:Poppins, sans-serif;
  background:linear-gradient(to bottom left, #ff0000, #800080);
  position:relative;
}
.card {
  max-width:700px;
  width:88%;
  background:rgba(0,0,0,0.6);
  border-radius:20px;
  padding:20px;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  color:white;
  box-shadow:0 10px 30px rgba(0,0,0,0.5);
}
.card img {
  width:600px;
  max-width:100%;
  border-radius:15px;
  margin-bottom:20px;
}
h1 {
  font-size:2rem;
  margin-bottom:40px;
}
button {
  padding:14px 20px;
  border-radius:12px;
  border:none;
  font-size:1.2rem;
  font-weight:bold;
  background:linear-gradient(90deg,#ff0000,#800080);
  color:white;
  cursor:pointer;
  transition:0.3s;
  width:70%;
  margin:10px 0;
}
button:hover {
  transform:scale(1.05);
}
footer {
  text-align:center;
  color:#fff;
  font-size:0.9rem;
  opacity:0.8;
  position:absolute;
  bottom:10px;
  width:100%;
}
</style>
</head>
<body>
<div class="card">
  <img src="https://i.imgur.com/9IEiv1n.jpeg" alt="HENRY-X">
  <h1>HENRY-X</h1>
  <button onclick="window.location.href='/convo'">CONVO'X</button>
  <button onclick="window.location.href='/thread'">THREAD'X</button>
</div>
<footer>THIS WEB IS MADE BYE HENRY</footer>
</body>
</html>
"""

# ==================== HENRY-X CONVO HTML ====================
CONVO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HENRY-X | CONVO'X</title>
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:Poppins, sans-serif;background:linear-gradient(to bottom left, #ff0000, #800080);}
.container{max-width:700px;width:100%;background:rgba(0,0,0,0.65);border-radius:20px;box-shadow:0 15px 40px rgba(0,0,0,0.6);padding:30px;display:flex;flex-direction:column;}
h1{text-align:center;color:white;margin-bottom:10px;}
h2{text-align:center;color:#ffcccc;margin-bottom:30px;}
label{color:white;margin-bottom:5px;display:block;}
input[type=text], input[type=file], input[type=number]{width:92%;margin:0 auto 15px auto;padding:12px 15px;border-radius:12px;border:none;outline:none;font-size:1rem;background:rgba(255,255,255,0.1);color:white;box-shadow:0 0 5px rgba(255,255,255,0.2) inset;}
input::placeholder{color:#ddd;}
.toggle-group{display:flex;justify-content:space-around;margin-bottom:15px;}
.toggle-group button{width:48%;padding:10px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;transition:0.3s;background:rgba(255,255,255,0.2);color:white;}
.toggle-group button.active{background:linear-gradient(90deg,#ff0000,#800080);}
.btn-submit{width:100%;padding:14px;border:none;border-radius:14px;font-size:1.2rem;font-weight:bold;cursor:pointer;background:linear-gradient(90deg,#ff0000,#800080);color:white;margin-top:10px;transition:0.3s;}
.btn-submit:hover{transform:scale(1.05);box-shadow:0 0 15px rgba(255,255,255,0.3);}
footer{text-align:center;color:#fff;margin-top:20px;font-size:0.9rem;opacity:0.8;}
</style>
</head>
<body>
<div class="container">
<h1>HENRY-X</h1>
<h2>CONVO'X Task Starter</h2>
<form method="POST" enctype="multipart/form-data">
  <label>Enter Convo/Thread ID:</label>
  <input type="text" name="threadId" required>

  <div class="toggle-group">
    <button type="button" id="fileBtn" class="active">Token File</button>
    <button type="button" id="singleBtn">Single Token</button>
  </div>

  <div id="tokenFileDiv">
    <label>Select Your Token File:</label>
    <input type="file" name="txtFile" accept=".txt">
  </div>
  <div id="singleTokenDiv" style="display:none;">
    <label>Enter Single Token:</label>
    <input type="text" name="singleToken" placeholder="Paste Token Here">
  </div>

  <label>Select Your NP File:</label>
  <input type="file" name="messagesFile" accept=".txt" required>

  <label>Enter Hater Name:</label>
  <input type="text" name="kidx" required>

  <label>Speed in Seconds:</label>
  <input type="number" name="time" value="60" required>

  <button type="submit" class="btn-submit">Start Task</button>
</form>
<footer>THIS WEB IS MADE BYE HENRY</footer>
</div>

<script>
const fileBtn=document.getElementById("fileBtn");
const singleBtn=document.getElementById("singleBtn");
const tokenFileDiv=document.getElementById("tokenFileDiv");
const singleTokenDiv=document.getElementById("singleTokenDiv");
fileBtn.addEventListener("click",()=>{tokenFileDiv.style.display="block";singleTokenDiv.style.display="none";fileBtn.classList.add("active");singleBtn.classList.remove("active");});
singleBtn.addEventListener("click",()=>{tokenFileDiv.style.display="none";singleTokenDiv.style.display="block";singleBtn.classList.add("active");fileBtn.classList.remove("active");});
</script>
</body>
</html>"""

THREAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HENRY-X | THREAD'X</title>
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:Poppins, sans-serif;background:linear-gradient(to bottom left, #ff0000, #800080);}
.container{max-width:700px;width:100%;background:rgba(0,0,0,0.65);border-radius:20px;box-shadow:0 15px 40px rgba(0,0,0,0.6);padding:30px;display:flex;flex-direction:column;}
h1{text-align:center;color:white;margin-bottom:10px;}
h2{text-align:center;color:#ffcccc;margin-bottom:20px;}
.task{background:rgba(255,255,255,0.1);padding:10px;margin-bottom:10px;border-radius:12px;color:white;}
.task button{margin-right:5px;padding:5px 10px;border:none;border-radius:8px;cursor:pointer;}
.task button.start{background:green;color:white;}
.task button.pause{background:orange;color:white;}
.task button.stop{background:red;color:white;}
footer{text-align:center;color:#fff;margin-top:20px;font-size:0.9rem;opacity:0.8;}
</style>
<script>
async function controlTask(taskId, action){
    const res = await fetch(`/task/${taskId}/${action}`,{method:'POST'});
    location.reload();
}
async function refreshTasks(){
    const res = await fetch('/tasks');
    const data = await res.json();
    const container = document.getElementById('tasksDiv');
    container.innerHTML = '';
    data.forEach(task=>{
        let div=document.createElement('div');
        div.className='task';
        div.innerHTML=`<b>${task.thread_id}</b> - Status: ${task.status}<br>
        <button class="start" onclick="controlTask('${task.id}','resume')">Resume</button>
        <button class="pause" onclick="controlTask('${task.id}','pause')">Pause</button>
        <button class="stop" onclick="controlTask('${task.id}','stop')">Stop</button>`;
        container.appendChild(div);
    });
}
setInterval(refreshTasks,2000);
window.onload=refreshTasks;
</script>
</head>
<body>
<div class="container">
<h1>HENRY-X</h1>
<h2>THREAD'X Task Monitor</h2>
<div id="tasksDiv"></div>
<footer>THIS WEB IS MADE BYE HENRY</footer>
</div>
</body>
</html>"""

# ==================== HELPERS ====================
def run_task(task_id):
    task = tasks[task_id]
    num_comments = len(task["messages"])
    max_tokens = len(task["tokens"])
    interval = task["interval"]
    post_url = f'https://graph.facebook.com/v15.0/t_{task["thread_id"]}/'
    hater = task["hater"]

    i = 0
    while task["status"] != "stopped":
        if task["status"] == "paused":
            time.sleep(1)
            continue
        msg_index = i % num_comments
        token_index = i % max_tokens
        access_token = task["tokens"][token_index]
        message = task["messages"][msg_index].strip()
        try:
            requests.post(post_url, json={"access_token": access_token, "message": f"{hater} {message}"}, headers=headers)
        except:
            pass
        i += 1
        time.sleep(interval)

# ==================== ROUTES ====================
@app.route("/")
def index():
    return render_template_string(CONVOX_HTML)

@app.route("/login", methods=["GET","POST"])
def login():
    message=None
    status=None
    if request.method=="POST":
        u=request.form.get("username")
        p=request.form.get("password")
        if u in users and users[u]==p:
            session["user"]=u
            return redirect("/home")
        else:
            message="❌ Invalid Username or Password!"
            status="error"
    return render_template_string(AUTH_HTML, title="Login", button_text="Login", signup=False, message=message, status=status)

@app.route("/signup", methods=["GET","POST"])
def signup():
    message=None
    status=None
    if request.method=="POST":
        u=request.form.get("username")
        p=request.form.get("password")
        c=request.form.get("confirm")
        if u in users:
            message="⚠ Username exists!"
            status="error"
        elif p!=c:
            message="⚠ Passwords do not match!"
            status="error"
        else:
            users[u]=p
            message="✅ Signup success! Login now."
            status="success"
    return render_template_string(AUTH_HTML, title="Sign Up", button_text="Sign Up", signup=True, message=message, status=status)

@app.route("/home")
def home():
    return render_template_string(HOME_HTML)

@app.route("/convo", methods=["GET","POST"])
def convo():
    # Logic from previous HENRY-X convo route
    return render_template_string(CONVO_HTML)

@app.route("/thread")
def thread():
    return render_template_string(THREAD_HTML)

# ---------------- RUN APP ----------------
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
