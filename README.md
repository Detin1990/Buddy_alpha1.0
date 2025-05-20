# Buddy v1.0 (Redacted Public Release)

Buddy is a lightweight local agent designed for task execution, orchestration, and simulation workflows. It listens for instructions from a local Flask server, executes them, and returns output — acting as a foundation for more complex workflows.

---

## ✂️ What Happened to the Cool Stuff?

> There used to be some cool stuff here, but it has been redacted for ethical concerns 😔  
> Certain features interacted with online services in ways that might raise eyebrows. Those features have been surgically removed from this release to keep everything squeaky clean.

If you're reading this, you're likely reviewing the project for collaboration, contribution, or portfolio purposes. What remains is the **core logic**, architecture, and philosophy behind a broader autonomous system called **Testbed**.

---

## 🧠 Core Components

- `exec_handler.py` – executes system instructions from the queue  
- `tag_listener.py`, `tag_grabber.py` – extracts or tracks relevant tags from input/output  
- `log_server.py` – simple Flask API for instruction polling and result capture  
- `/buddy_extension/` – previously housed extension logic (**now redacted**)  
- `requirements.txt` – minimal dependencies (mostly just Flask)

---

## 🚀 Setup & Usage

### 1. Clone the Repo

```bash
git clone https://github.com/Detin1990/Buddy_alpha1.0.git
cd Buddy_alpha1.0
```

### 2. Install Dependencies

```bash
pip install flask
```

### 3. Run the Flask Server

```bash
python log_server.py
```

### 4. Start the Buddy Agent

```bash
python exec_handler.py
```

Buddy will begin polling for tasks and executing them locally.

---

## 🧪 Example Workflow

1. You send a task (like `echo Hello World`) to the server  
2. Buddy retrieves the task  
3. It runs the task and logs the output  
4. Server receives and stores the result  

You now have a basic decision-execution loop that can be extended or sandboxed to suit your goals.

---

## ⚠️ Legal & Ethical Disclaimer

This version intentionally omits any features that could violate Terms of Service of external platforms.  
**Major derivative works require written approval** from the original author.  
Feel free to learn, remix, and experiment — but respect the original intent and limits.

---

Stay ethical. Stay clever. Build cool shit.

— Buddy Dev Team (a.k.a. me, a tired wizard with a terminal)

> *The quieter you become, the more you are able to hear*
