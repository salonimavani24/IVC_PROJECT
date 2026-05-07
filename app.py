import csv
import os
from flask import Flask, redirect, request, render_template

app = Flask(__name__)
FILE_NAME = "expenses.csv"

@app.route("/add", methods=["POST"])
def add():
    category = request.form.get("category", "")
    amount = request.form.get("amount", "")
    date = request.form.get("date", "")
    note = request.form.get("note", "")

    if not amount.isdigit():
        return "Invalid amount"

    rows = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as f:
            rows = list(csv.reader(f))

    id = len(rows) if rows else 1

    if not rows:
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category", "amount", "date", "note"])
            writer.writerow([id, category, amount, date, note])
    else:
        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([id, category, amount, date, note])

    return redirect("/")

@app.route("/edit/<id>", methods=["POST"])
def edit(id):
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    note = request.form["note"]

    with open(FILE_NAME, "r", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return redirect("/")

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] == str(id):
            new_rows.append([id, category, amount, date, note])
        else:
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/")

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expense Tracker</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: #333;
            }
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 40px;
                max-width: 600px;
                text-align: center;
                backdrop-filter: blur(10px);
            }
            h1 {
                color: #4a5568;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .links {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .link {
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                font-weight: bold;
                font-size: 1.1em;
            }
            .link:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
            .info {
                margin-top: 30px;
                color: #718096;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💰 Expense Tracker</h1>
            <div class="links">
                <a href="/insights" class="link">📊 View Insights Dashboard</a>
                <p class="info">Use /add or /edit/&lt;id&gt; to manage expenses.</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/insights")
def insights():

    try:
        with open(FILE_NAME, 'r') as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        rows = []

    expenses = rows[1:] if rows else []

    total = 0
    category_totals = {}

    for row in expenses:
        category = row[1]
        amount = int(row[2])
        total += amount
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += amount

    highest_category = max(category_totals, key=category_totals.get) if category_totals else "N/A"

    if total < 2000:
        message = "Excellent spending habits 🌟"
    elif total < 5000:
        message = "Good budgeting 👍"
    else:
        message = "High spending detected 💸"

    return render_template(
        "insights.html",
        total=total,
        count=len(expenses),
        highest=highest_category,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
