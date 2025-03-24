from flask import Flask


app = Flask(__name__)

@app.route("/ping")
def ping():

    return "server is working123"

@app.route("/home")
def home():
   return "Welcome to the home page"


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)