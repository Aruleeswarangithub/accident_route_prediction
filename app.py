from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('routes.csv')

# Function to calculate safety percentage
def calculate_safety(route):
    score = 100

    # Deduct points based on blackspot count, night-time travel, and poor streetlight
    score -= route['blackspot_count'] * 5
    score -= route['night_time'] * 10
    score -= route['poor_streetlight'] * 10

    # Minimum 40% safety guaranteed
    return max(score, 40)

# Route for form input
@app.route('/')
def home():
    return render_template('index.html')

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    source = request.form['source'].strip()
    destination = request.form['destination'].strip()

    # Filter matching routes
    matching_routes = df[
        (df['source'].str.lower() == source.lower()) & 
        (df['destination'].str.lower() == destination.lower())
    ]

    if matching_routes.empty:
        return render_template('index.html', error="No routes found between the selected locations.")

    # Add safety score
    matching_routes = matching_routes.copy()
    matching_routes['safety_percentage'] = matching_routes.apply(calculate_safety, axis=1)

    # Sort by safety
    sorted_routes = matching_routes.sort_values(by='safety_percentage', ascending=False)

    # Send to UI
    routes = sorted_routes.to_dict(orient='records')
    return render_template('index.html', routes=routes, source=source, destination=destination)

if __name__ == '__main__':
    app.run(debug=True)
