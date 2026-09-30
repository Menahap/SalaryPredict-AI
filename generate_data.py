import pandas as pd
import numpy as np
import random

def generate_data():
    np.random.seed(42)
    random.seed(42)
    
    num_samples = 500
    
    data = []
    for _ in range(num_samples):
        age = random.randint(22, 60)
        
        # Education Level: 0=High School, 1=Bachelors, 2=Masters, 3=PhD
        education = random.choices([0, 1, 2, 3], weights=[0.1, 0.5, 0.3, 0.1])[0]
        
        # Job Level: 1=Junior, 2=Mid, 3=Senior, 4=Manager, 5=Director
        job_level = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.3, 0.2, 0.15, 0.05])[0]
        
        # Experience should roughly make sense with age
        max_exp = max(0, age - 22)
        years_exp = random.uniform(0, max_exp) if max_exp > 0 else 0
        
        prev_exp = random.uniform(0, max(0, years_exp - 2))
        curr_exp = years_exp - prev_exp
        
        working_hours = random.uniform(35, 50)
        
        # Base salary
        base_salary = 20000
        salary = (
            base_salary 
            + (education * 10000) 
            + (job_level * 15000) 
            + (years_exp * 2000) 
            + (prev_exp * 1000)
            + (working_hours * 100)
        )
        
        # Add some noise
        noise = np.random.normal(0, 5000)
        salary += noise
        
        data.append({
            'Age': int(age),
            'Years of Experience': round(years_exp, 1),
            'Education Level': education,
            'Job Level': job_level,
            'Working Hours': round(working_hours, 1),
            'Previous Experience': round(prev_exp, 1),
            'Salary': round(salary, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv('salary_data.csv', index=False)
    print("Dataset 'salary_data.csv' created successfully with 500 records.")

if __name__ == '__main__':
    generate_data()
