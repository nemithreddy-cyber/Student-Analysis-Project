"""
Script to generate reproducible 100-record demo student dataset (data/students.csv).
First 5 records match the exact PDF requirement.
"""
import os
import numpy as np
import pandas as pd

def generate_demo_dataset(output_path="data/students.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Exact initial 5 records specified in project requirements (plus Previous/Current Marks for trend analysis)
    first_five = [
        {"Student_ID": "ST001", "Attendance": 86.0, "Study_Hours": 3.5, "Assignment_Marks": 17.0, "Internal_Marks": 18.0, "Final_Marks": 78.0, "Previous_Marks": 70.0, "Current_Marks": 78.0},
        {"Student_ID": "ST002", "Attendance": 92.0, "Study_Hours": 5.0, "Assignment_Marks": 19.0, "Internal_Marks": 20.0, "Final_Marks": 88.0, "Previous_Marks": 82.0, "Current_Marks": 88.0},
        {"Student_ID": "ST003", "Attendance": 74.0, "Study_Hours": 2.5, "Assignment_Marks": 14.0, "Internal_Marks": 15.0, "Final_Marks": 65.0, "Previous_Marks": 68.0, "Current_Marks": 65.0},
        {"Student_ID": "ST004", "Attendance": 81.0, "Study_Hours": 4.0, "Assignment_Marks": 16.0, "Internal_Marks": 17.0, "Final_Marks": 72.0, "Previous_Marks": 64.0, "Current_Marks": 72.0},
        {"Student_ID": "ST005", "Attendance": 68.0, "Study_Hours": 2.0, "Assignment_Marks": 12.0, "Internal_Marks": 13.0, "Final_Marks": 58.0, "Previous_Marks": 52.0, "Current_Marks": 58.0},
    ]
    
    np.random.seed(42)
    num_remaining = 95
    
    # Generate realistic study hours between 1.0 and 8.0
    study_hours = np.round(np.random.uniform(1.0, 7.5, size=num_remaining) + np.random.beta(2, 2, size=num_remaining)*0.8, 1)
    study_hours = np.clip(study_hours, 1.0, 8.0)
    
    # Attendance between 50% and 100%, slightly correlated with study hours
    attendance = np.round(55 + 4.5 * study_hours + np.random.normal(0, 6, size=num_remaining), 1)
    attendance = np.clip(attendance, 50.0, 100.0)
    
    # Assignment marks (5 - 20)
    assignment = np.round(6 + 1.6 * study_hours + np.random.normal(0, 1.5, size=num_remaining), 1)
    assignment = np.clip(assignment, 5.0, 20.0)
    
    # Internal marks (5 - 20)
    internal = np.round(5 + 1.7 * study_hours + 0.1 * attendance + np.random.normal(0, 1.5, size=num_remaining), 1)
    internal = np.clip(internal, 5.0, 20.0)
    
    # Final marks (35 - 100), composite with variation
    final_raw = 15 + 4.5 * study_hours + 0.25 * attendance + 1.1 * assignment + 1.2 * internal + np.random.normal(0, 5.5, size=num_remaining)
    final_marks = np.round(final_raw, 1)
    final_marks = np.clip(final_marks, 35.0, 98.0)
    
    # Previous marks for comparison / trend analysis
    previous_marks = np.clip(np.round(final_marks - np.random.normal(3.0, 4.0, size=num_remaining), 1), 30.0, 95.0)
    
    remaining_records = []
    for i in range(num_remaining):
        sid = f"ST{i+6:03d}"
        remaining_records.append({
            "Student_ID": sid,
            "Attendance": float(attendance[i]),
            "Study_Hours": float(study_hours[i]),
            "Assignment_Marks": float(assignment[i]),
            "Internal_Marks": float(internal[i]),
            "Final_Marks": float(final_marks[i]),
            "Previous_Marks": float(previous_marks[i]),
            "Current_Marks": float(final_marks[i])
        })
        
    all_records = first_five + remaining_records
    df = pd.DataFrame(all_records)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated demo dataset with {len(df)} records at '{output_path}'.")
    return df

if __name__ == "__main__":
    generate_demo_dataset()
