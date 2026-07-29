import joblib

def load_model_pipeline(model_name='rf_model.pkl'):
    """Load a saved pipeline from models/ folder. Default: Random Forest."""
    return joblib.load(f'models/{model_name}')