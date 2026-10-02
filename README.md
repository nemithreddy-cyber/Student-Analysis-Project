# Student Academic Performance and Statistical Analysis System

> **A Practical Descriptive-Statistics Dashboard for Student Data**  
> **Subject**: Probability Theory and Statistical Analysis  
> **Primary Module**: Module I – Introduction to Statistics  

---

## 📌 Project Overview
The **Student Academic Performance and Statistical Analysis System** is an interactive, data-driven analytics dashboard designed to process student academic records into statistical summaries, frequency tables, graphical distributions, Chebyshev bounds, skewness classifications, and scatter association insights.

Instead of keeping student records as raw spreadsheets, this application dynamically computes Module I descriptive statistics, provides visual charts, and generates automatic academic interpretations.

---

## 🎯 Key Objectives
1. **Data Collection & Import**: Automatically load a demonstration dataset of 100 students or import custom user datasets via CSV or Excel formats.
2. **Data Cleaning & Validation**: Validate dataset schemas, data types, missing values, duplicate records, and academic range constraints.
3. **Descriptive Statistics Engine**: Dynamically calculate central tendency (Mean, Median, Mode) and variability (Range, Sample Variance $s^2$, Sample Standard Deviation $s$).
4. **Grouped Frequency Analysis**: Generate continuous class intervals, absolute frequencies, cumulative frequencies ($CF$), and relative percentages.
5. **Distribution Visualizations**: Interactive Plotly histograms, Less-Than Ogive cumulative frequency curves, and Stem-and-Leaf text plots.
6. **Chebyshev's Inequality Evaluator**: Compute theoretical lower bounds ($1 - 1/k^2$) for any $k > 1$ and compare against actual empirical observed data proportions.
7. **Skewness Analysis**: Determine Fisher-Pearson skewness coefficients and classify distributions (Positive skew, Negative skew, Approximately symmetric).
8. **Scatter Plot Relationship Explorer**: Examine paired quantitative associations (e.g. `Study_Hours` vs `Final_Marks`, `Attendance` vs `Final_Marks`) with regression trendlines and academic disclaimers.
9. **Final Statistical Report**: Consolidated report generator for exporting statistical findings and datasets.

---

## 🛠️ Technology Stack
- **Language**: Python 3.x
- **Dashboard Framework**: Streamlit
- **Data Processing**: Pandas & NumPy
- **Statistical Computations**: SciPy (`scipy.stats`)
- **Interactive Visualization**: Plotly Express & Graph Objects
- **Spreadsheet Parsing**: OpenPyXL (Excel `.xlsx` support)
- **Unit Testing**: PyTest

---

## 📁 Repository Directory Structure

```
Student_Statistical_Analysis/
├── app.py                     # Main Streamlit Dashboard Application
├── requirements.txt           # Python Dependencies Manifest
├── README.md                  # Project Documentation & User Guide
├── config/
│   └── settings.py            # Project Settings & Validation Rules
├── data/
│   └── students.csv           # 100-Record Demonstration Dataset
├── scripts/
│   └── generate_demo_data.py  # Reproducible Demo Data Generator Script
├── modules/
│   ├── __init__.py
│   ├── data_processing.py     # Data Loading & Sanitization
│   ├── validation.py          # Data Validation & Range Checks
│   ├── descriptive_stats.py   # Mean, Median, Mode, Variance, Std Dev
│   ├── frequency_analysis.py  # Grouped Frequency & Cumulative Tables
│   ├── chebyshev.py           # Chebyshev Inequality & Bounds
│   ├── skewness.py            # Fisher-Pearson Skewness Logic
│   ├── distribution.py        # Distribution Helper
│   ├── scatter_analysis.py    # Quantitative Association & Regression
│   ├── interpretations.py     # Automatic Academic Interpretations
│   └── report_generator.py    # Consolidated Summary Text Report
├── visualization/
│   ├── __init__.py
│   ├── histograms.py          # Interactive Plotly Histograms
│   ├── ogive.py               # Monotonic Less-Than Ogives
│   ├── stem_leaf.py           # ASCII Stem-and-Leaf Generator
│   └── scatter.py             # Scatter Plots & Trend Lines
└── tests/
    ├── __init__.py
    ├── test_validation.py     # Validation Unit Tests
    ├── test_statistics.py     # Descriptive Stats Unit Tests
    ├── test_frequency.py      # Frequency & Ogive Unit Tests
    ├── test_chebyshev.py      # Chebyshev Bound Unit Tests
    └── test_skewness.py       # Skewness Classification Unit Tests
```

---

## 🚀 Installation & Running Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Demo Dataset (Optional / Built-in)
```bash
python scripts/generate_demo_data.py
```

### 3. Launch Streamlit Dashboard
```bash
streamlit run app.py
```
Access the application in your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Unit Tests
To verify all statistical formulas, validation rules, and monotonic ogive properties:
```bash
pytest
```

---

## 📊 Statistical Methodology & Formulas

### 1. Sample Mean
$$\bar{x} = \frac{\sum_{i=1}^n x_i}{n}$$

### 2. Sample Variance & Standard Deviation
$$s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1} \quad (\text{using } \text{ddof}=1)$$
$$s = \sqrt{s^2}$$

### 3. Chebyshev's Inequality
$$\text{Theoretical Guarantee} = P(|X - \bar{x}| < k \cdot s) \ge 1 - \frac{1}{k^2} \quad (\text{for } k > 1)$$

### 4. Skewness
$$g_1 = \frac{\frac{1}{n} \sum (x_i - \bar{x})^3}{s^3}$$

---

## ⚠️ Academic Disclaimer & Limitations
1. **Association vs. Causation**: Scatter plots and correlation metrics illustrate co-occurrence in the dataset and do **NOT** establish direct causation.
2. **Measurement Error**: Self-reported variables such as study hours may contain reporting noise or bias.
3. **Descriptive Scope**: Module I focuses purely on descriptive statistics and does not perform inferential hypothesis testing or multi-variable regression.

---

## 🔮 Future Scope
- Extension to Probability Theory and Random Variable Distributions (Binomial, Poisson, Normal, Uniform, Gamma, Beta).
- Sampling Distributions, Confidence Intervals, and Inferential $t$-tests / ANOVA.
- Inferential Pearson / Spearman Correlation and Multiple Regression Modeling.
