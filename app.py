from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__, template_folder = "templates")
app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        response = make_response({"message": "Wrong email or password!"}, 400)
        response.headers.add_header("Content-Type", "application/json")
        return response
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        response = make_response({"message": "Wrong email or password!"}, 400)
        response.headers.add_header("Content-Type", "application/json")
        return response
    else:
        return render_template("signup.html")