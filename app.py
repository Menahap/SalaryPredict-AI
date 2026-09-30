from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import json
import os

app = Flask(__name__)

# Load model and metrics once
MODEL_PATH = 'salary_model.pkl'
DATA_PATH = 'salary_data.csv'
METRICS_PATH = 'model_metrics.json'

model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if not model:
            return render_template('predict.html', error="Model not found. Please train the model first.")
            
        try:
            # Get input data
            age = int(request.form.get('age', 0))
            years_exp = float(request.form.get('years_exp', 0))
            education = int(request.form.get('education', 0))
            job_level = int(request.form.get('job_level', 1))
            working_hours = float(request.form.get('working_hours', 40))
            prev_exp = float(request.form.get('prev_exp', 0))
            
            # Predict
            features = np.array([[age, years_exp, education, job_level, working_hours, prev_exp]])
            prediction = model.predict(features)[0]
            
            # Format prediction
            predicted_salary = f"₹ {prediction:,.2f}"
            
            return render_template('predict.html', prediction=predicted_salary)
            
        except ValueError:
            return render_template('predict.html', error="Invalid input. Please enter numbers.")
        except Exception as e:
            return render_template('predict.html', error=f"An error occurred: {str(e)}")
            
    return render_template('predict.html')

@app.route('/dashboard')
def dashboard():
    if not os.path.exists(DATA_PATH):
        return render_template('dashboard.html', error="Dataset not found. Please generate the data first.")
        
    try:
        # Load data
        df = pd.read_csv(DATA_PATH)
        
        # Calculate stats
        stats = {
            'total_employees': len(df),
            'avg_salary': df['Salary'].mean(),
            'min_salary': df['Salary'].min(),
            'max_salary': df['Salary'].max()
        }
        
        # Load metrics
        metrics = {}
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, 'r') as f:
                metrics = json.load(f)
                
        # Data for charts
        # Convert data to lists for JSON serialization to pass to JS
        chart_data = {
            'exp': df['Years of Experience'].tolist(),
            'age': df['Age'].tolist(),
            'salary': df['Salary'].tolist(),
            'education': df['Education Level'].tolist()
        }
        
        # For actual vs predicted, we need the model
        if model:
            X = df[['Age', 'Years of Experience', 'Education Level', 'Job Level', 'Working Hours', 'Previous Experience']]
            chart_data['predicted'] = model.predict(X).tolist()
        else:
            chart_data['predicted'] = []
            
        return render_template('dashboard.html', stats=stats, metrics=metrics, chart_data=chart_data)
        
    except Exception as e:
        return render_template('dashboard.html', error=f"An error occurred loading dashboard data: {str(e)}")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
