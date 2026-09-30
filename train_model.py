import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle
import json

def train_model():
    try:
        # 1. Load dataset
        df = pd.read_csv('salary_data.csv')
        
        # 2. Select features and target
        X = df[['Age', 'Years of Experience', 'Education Level', 'Job Level', 'Working Hours', 'Previous Experience']]
        y = df['Salary']
        
        # 3. Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 4. Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # 5. Evaluate model
        y_pred = model.predict(X_test)
        
        metrics = {
            'R2_Score': r2_score(y_test, y_pred),
            'MAE': mean_absolute_error(y_test, y_pred),
            'MSE': mean_squared_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
        }
        
        print("Model Training Results:")
        for k, v in metrics.items():
            print(f"{k}: {v:.4f}")
            
        # 6. Save model and metrics
        with open('salary_model.pkl', 'wb') as f:
            pickle.dump(model, f)
            
        with open('model_metrics.json', 'w') as f:
            json.dump(metrics, f)
            
        print("\nModel saved as 'salary_model.pkl'")
        print("Metrics saved as 'model_metrics.json'")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")

if __name__ == '__main__':
    train_model()
