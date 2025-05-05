# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv('routes.csv')

# Encode categorical columns
le_safety = LabelEncoder()
df['safety_level_encoded'] = le_safety.fit_transform(df['safety_level'])

# Drop non-essential columns
df = df.drop(['source', 'destination', 'via', 'accident_prone_area', 'safety_level'], axis=1)

# Define features and target variable
X = df.drop('safety_level_encoded', axis=1)
y = df['safety_level_encoded']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'accident_predictor_model.pkl')
joblib.dump(le_safety, 'safety_label_encoder.pkl')

print("Model training complete and saved.")
