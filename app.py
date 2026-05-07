import csv
from flask import Flask, redirect, request

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

    try:
        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([category, amount, date, note])
    except FileNotFoundError:
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([category, amount, date, note])

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
        if row[0] == id:
            new_rows.append([id, category, amount, date, note])
        else:
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
