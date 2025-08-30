from flask import Flask, request, render_template_string
import pickle
import pandas as pd

# Load model and column names
model = pickle.load(open('model.pkl', 'rb'))
model_columns = pickle.load(open('model_columns.pkl', 'rb'))  # loaded instead of redefining

app = Flask(__name__)

# Inline HTML
html = '''


<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Customer Response Prediction</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f4f9fc;
      color: #333;
      padding: 40px;
    }
    h1 {
      color: #2a5d84;
      margin-bottom: 5px;
    }
    h2 {
      color: #4a4a4a;
      font-size: 18px;
      margin-top: 30px;
      margin-bottom: 10px;
    }
    form {
      background: #fff;
      padding: 25px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      max-width: 500px;
    }
    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
    }
    input[type="number"] {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    input[type="submit"] {
      background-color: #2a5d84;
      color: white;
      padding: 12px 18px;
      margin-top: 25px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #1f4c6b;
    }
    h3 {
      margin-top: 30px;
      color: #2a5d84;
    }
  </style>
</head>
<body>
  <h1>Customer Response Prediction Tool</h1>
  <form method="post">
    <h2>📊 Basic Customer Details</h2>
    <label for="age">Customer Age</label>
    <input type="number" name="age" required>

    <label for="balance">Account Balance (in ₹)</label>
    <input type="number" name="balance" required>

    <label for="day">Last Contact Day (1–31)</label>
    <input type="number" name="day" required>

    <h2>📞 Campaign Interaction</h2>
    <label for="duration">Contact Duration (in seconds)</label>
    <input type="number" name="duration" required>

    <label for="campaign">Number of Contacts During Campaign</label>
    <input type="number" name="campaign" required>

    <label for="pdays">Days Passed Since Last Contact</label>
    <input type="number" name="pdays" required>

    <label for="previous">Previous Contact Count</label>
    <input type="number" name="previous" required>

    <input type="submit" value="Predict">
  </form>

  {% if result %}
    <h3>🧠 Prediction Outcome: {{ result }}</h3>
  {% endif %}
</body>
</html>


'''

@app.route('/', methods=['GET', 'POST'])
def predict():
    result = None
    if request.method == 'POST':
        # Basic numeric inputs
        user_input = {
            'age': float(request.form['age']),
            'balance': float(request.form['balance']),
            'day': float(request.form['day']),
            'duration': float(request.form['duration']),
            'campaign': float(request.form['campaign']),
            'pdays': float(request.form['pdays']),
            'previous': float(request.form['previous'])
        }

        # Initialize input DataFrame
        df = pd.DataFrame([user_input])

        # Add missing columns from training
        for col in model_columns:
            if col not in df.columns:
                df[col] = 0

        # Align columns
        df = df[model_columns]

        # Predict
        pred = model.predict(df)[0]
        result = 'Yes' if pred == 1 else 'No'

    return render_template_string(html, result=result)

if __name__ == '__main__':
    app.run(debug=True)