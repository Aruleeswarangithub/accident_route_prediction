from flask import Flask, request, render_template
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load dataset
df = pd.read_csv('routes.csv')

# Home page route to show the form
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route to handle the form submission and search for route details
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the form
    source = request.form['source']
    destination = request.form['destination']
    
    # Search for the route in the dataset
    route = df[(df['source'] == source) & (df['destination'] == destination)]
    
    if not route.empty:
        # If route found, display details
        route_details = route.iloc[0]
        safety_level = route_details['safety_level']
        distance_km = route_details['distance_km']
        blackspot_count = route_details['blackspot_count']
        night_time = route_details['night_time']
        poor_streetlight = route_details['poor_streetlight']
        via = route_details['via']
        accident_prone_area = route_details['accident_prone_area']
        
        return render_template('index.html', 
                               safety_level=safety_level,
                               distance_km=distance_km,
                               blackspot_count=blackspot_count,
                               night_time=night_time,
                               poor_streetlight=poor_streetlight,
                               via=via,
                               accident_prone_area=accident_prone_area)
    else:
        # If no route found
        return render_template('index.html', error="No route found for the given source and destination.")

if __name__ == '__main__':
    app.run(debug=True)
