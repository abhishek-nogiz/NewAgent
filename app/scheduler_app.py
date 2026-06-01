from flask import Flask, render_template, request, redirect
import json
import os

from app.scheduler_runner import start_scheduler
from app.scheduler_config import CATEGORY_MAP, COUNTRIES

app = Flask(__name__)


@app.route("/")
def home():

    with open("app/config.json", "r") as f:
        config = json.load(f)

    return render_template(
        "index.html",
        config=config,
        categories=CATEGORY_MAP.keys(),
        countries=COUNTRIES
    )


@app.route("/save", methods=["POST"])
def save():

    category_name = request.form["category"]

    data = {
        "country": request.form["country"],
        "category_name": category_name,
        "category_code": CATEGORY_MAP[category_name],
        "interval_minutes": int(
            request.form["interval_minutes"]
        )
    }

    with open("app/config.json", "w") as f:
        json.dump(data, f, indent=4)

    # DO NOT start scheduler again here
    # Instead reload/update jobs inside scheduler_runner if needed

    return redirect("/")


import os

if __name__ == "__main__":

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )