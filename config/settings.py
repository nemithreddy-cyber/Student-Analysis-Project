"""
Configuration settings for Student Academic Performance and Statistical Analysis System.
"""
import os

PROJECT_TITLE = "Student Academic Performance and Statistical Analysis System"
PROJECT_SUBTITLE = "A Practical Descriptive-Statistics Dashboard for Student Data"
SUBJECT = "Probability Theory and Statistical Analysis"
PRIMARY_MODULE = "Module I – Introduction to Statistics"

REQUIRED_COLUMNS = [
    "Student_ID",
    "Attendance",
    "Study_Hours",
    "Assignment_Marks",
    "Internal_Marks",
    "Final_Marks"
]

OPTIONAL_COLUMNS = [
    "Age",
    "Year",
    "Semester",
    "Department",
    "Section"
]

NUMERIC_COLUMNS = [
    "Attendance",
    "Study_Hours",
    "Assignment_Marks",
    "Internal_Marks",
    "Final_Marks",
    "Previous_Marks",
    "Current_Marks"
]

VALIDATION_RULES = {
    "Attendance": {"min": 0.0, "max": 100.0, "label": "Attendance (%)"},
    "Study_Hours": {"min": 0.0, "max": 24.0, "label": "Daily Study Hours"},
    "Assignment_Marks": {"min": 0.0, "max": 20.0, "label": "Assignment Marks (out of 20)"},
    "Internal_Marks": {"min": 0.0, "max": 20.0, "label": "Internal Marks (out of 20)"},
    "Final_Marks": {"min": 0.0, "max": 100.0, "label": "Final Examination Marks (out of 100)"},
    "Previous_Marks": {"min": 0.0, "max": 100.0, "label": "Previous Marks (out of 100)"},
    "Current_Marks": {"min": 0.0, "max": 100.0, "label": "Current Marks (out of 100)"}
}

DEFAULT_CHEBYSHEV_K = 2.0
PREVIEW_ROW_OPTIONS = [5, 10, 25, 50, 100]

TEAM_MEMBERS = [
    {"name": "Team Lead / Data Specialist", "role": "Data Collection, Questionnaire & Cleaning"},
    {"name": "Statistical Analyst", "role": "Statistical Calculations & Mathematical Validation"},
    {"name": "Visualization Engineer", "role": "Histograms, Ogives, Stem-and-Leaf & Scatter Plots"},
    {"name": "Dashboard Developer", "role": "Streamlit UI Integration & User Experience"},
    {"name": "Project Coordinator", "role": "System Integration, Testing, Report & Presentation"}
]

DEMO_DATASET_PATH = os.path.join("data", "students.csv")
