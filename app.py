from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Fake storage for booked slots
booked_slots = {}

def categorize_postcode(postcode):
    cleaned = postcode.replace(" ", "").upper()
    if cleaned.startswith("SW147"):
        return "West"
    elif cleaned.startswith("SW148"):
        return "East"
    return "Out of Area"

@app.route("/", methods=["GET", "POST"])
def index():
    zone = None
    if request.method == "POST":
        name = request.form.get("name", "")
        phone = request.form.get("phone", "")
        postcode = request.form.get("postcode", "")
        service = request.form.get("service", "")
        date = request.form.get("date", "")
        time = request.form.get("time", "")

        zone = categorize_postcode(postcode)

        if not booked_slots.get(date):
            booked_slots[date] = []

        if time not in booked_slots[date]:
            booked_slots[date].append(time)
            return render_template("success.html", name=name, date=date, time=time)

    today = datetime.today()
    days = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    times = [f"{hour:02d}:00" for hour in range(9, 21)]
    return render_template("index.html", days=days, times=times, booked=booked_slots)

if __name__ == "__main__":
    app.run(debug=True)
