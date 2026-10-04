"""
train_model.py
- Loads house_data.csv
- Trains Linear Regression, Decision Tree, Random Forest
- Saves each model to models/ with consistent names:
    linear_model.pkl, dt_model.pkl, rf_model.pkl
- Saves evaluation metrics to models/evaluation.json
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib, json, os

os.makedirs('models', exist_ok=True)

df = pd.read_csv('house_data.csv')
X = df[['sqft', 'bedrooms', 'bathrooms', 'age_of_house', 'location']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_features = ['sqft', 'bedrooms', 'bathrooms', 'age_of_house']
cat_features = ['location']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
])

models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

filenames = {
    'Linear Regression': 'linear_model.pkl',
    'Decision Tree': 'dt_model.pkl',
    'Random Forest': 'rf_model.pkl'
}

evaluation = {}

for name, model in models.items():
    pipe = Pipeline([('preprocessor', preprocessor), ('regressor', model)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    evaluation[name] = {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'R2_Score': round(r2, 4)
    }
    joblib.dump(pipe, f'models/{filenames[name]}')

with open('models/evaluation.json', 'w') as f:
    json.dump(evaluation, f, indent=2)

print("✅ All models trained and saved.")
print("Evaluation metrics:", json.dumps(evaluation, indent=2))
