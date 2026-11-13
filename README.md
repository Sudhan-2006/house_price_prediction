# House Price Prediction Project

A Django-based web application for predicting house prices using machine learning models. The project includes a user-facing prediction interface, history tracking, CSV upload support, admin dashboard, and automated model evaluation.

## Overview

This application uses a dataset of house attributes such as square footage, bedrooms, bathrooms, property age, and location to estimate property values. It trains multiple regression models and saves the best-performing pipeline for prediction.

## Features

- User authentication and role-based access
- House price prediction form
- Prediction history for each user
- CSV bulk prediction export
- PDF report generation for the latest prediction
- Admin dashboard with usage statistics and user insights
- Model training and evaluation pipeline

## Tech Stack

- Python
- Django
- pandas
- scikit-learn
- NumPy
- reportlab
- SQLite (default database)

## Project Structure

```text
house_price_project/
├── accounts/                # Authentication and landing page logic
├── house_price_project/      # Django project configuration
├── models/                  # Trained ML models and evaluation metrics
├── predictor/               # Prediction app and dashboards
├── templates/               # HTML templates
├── house_data.csv           # House dataset used for training/prediction
├── manage.py                # Django entry point
├── train_model.py           # Model training script
├── requirements.txt         # Python dependencies
├── db.sqlite3               # Local SQLite database
└── README.md                # Project documentation
```

## Setup

1. Clone or open the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Training the Model

Run the training script to create the machine learning models and evaluation file:

```bash
python train_model.py
```

This will generate the following files under the `models/` directory:

- `linear_model.pkl`
- `dt_model.pkl`
- `rf_model.pkl`
- `evaluation.json`

## Running the Application

Apply database migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Default Admin Access

If you create a superuser, you can access the admin panel and analytics dashboard:

```bash
python manage.py createsuperuser
```

## Notes

- The project is configured to use SQLite by default.
- The model uses a Random Forest regressor for production prediction.
- The application stores historical predictions per user in the database.

## License

This project is intended for educational and demonstration purposes.
