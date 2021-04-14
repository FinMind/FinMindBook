from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"Hello": "World"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
