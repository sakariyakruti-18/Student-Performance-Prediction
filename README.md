# 🎓 AI-Based Student Performance Prediction

An Artificial Intelligence and Machine Learning project that predicts students' academic performance categories using student-related academic data and machine learning techniques.

## 📌 Project Overview

Student academic performance is an important factor in understanding learning outcomes and identifying students who may require additional academic support.

This project aims to develop an AI-based Student Performance Prediction system that analyzes student-related data and predicts their performance category using Machine Learning algorithms.

The system uses historical student data, data preprocessing, feature extraction, and trained machine learning models to generate predictions.

## 🎯 Project Objectives

- Analyze student academic performance using historical data.
- Apply data preprocessing techniques to prepare the dataset.
- Implement Machine Learning algorithms for performance prediction.
- Predict students' academic performance categories.
- Evaluate and compare the performance of different ML models.
- Develop an interactive application for generating predictions.
- Maintain prediction history for further reference.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Jupyter Notebook | Model development and experimentation |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Streamlit | Web application |
| SQLite | Prediction history database |
| Joblib / Pickle | Model serialization |

## 📂 Project Structure

```text
Student-Performance-Prediction/
│
├── app/
│   └── app.py
│
├── dataset/
│   └── student_performance_dataset.csv
│
├── notebooks/
│   └── Student_Performance_Prediction.ipynb
│
├── models/
│   ├── best_student_model.pkl
│   ├── student_label_encoder.pkl
│   └── student_preprocessor.pkl
│
├── database/
│   └── prediction_history.db
│
├── documentation/
│   ├── AI_Student_Performance_Prediction_IEEE.docx
│   └── AI_Student_Performance_Prediction_IEEE.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Project Workflow

1. **Dataset Collection:** Obtain student-related academic data.
2. **Exploratory Data Analysis:** Understand the dataset and identify patterns.
3. **Data Preprocessing:** Handle missing values, encode categorical variables, and prepare features.
4. **Feature Preparation:** Transform the dataset into a suitable format for machine learning.
5. **Model Implementation:** Train and evaluate machine learning models.
6. **Model Evaluation:** Compare model performance using evaluation metrics.
7. **Model Selection:** Select the best-performing model.
8. **Prediction Application:** Integrate the trained model into a Streamlit application.
9. **Prediction History:** Store prediction records using SQLite.

## 🤖 Machine Learning

The project uses supervised Machine Learning techniques to predict student performance categories.

The workflow includes:

- Model training
- Model testing
- Performance evaluation
- Model comparison
- Best model selection
- Performance category prediction

## 📊 Model Evaluation

The machine learning models are evaluated using appropriate performance metrics.

Evaluation outputs include:

- Accuracy comparison
- Confusion matrix
- Classification report
- Model evaluation table

*Actual evaluation results will be added after final model validation.*

## 🚀 Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/sakariyakruti-18E/Student-Performance-Prediction.git
```

### 2. Navigate to the project directory

```bash
cd Student-Performance-Prediction
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app/app.py
```

## 📈 Expected Outcome

The system predicts a student's academic performance category based on the input features and provides an interactive interface for generating predictions.

It aims to support academic performance analysis and help identify students who may benefit from additional learning support.

## 🔮 Future Enhancements

- Integrate additional student academic and behavioral features.
- Experiment with more machine learning algorithms.
- Improve prediction performance through hyperparameter tuning.
- Add interactive dashboards and advanced visualizations.
- Enhance prediction history and reporting.
- Deploy the application online.

## 👩‍💻 Project Information

**Project Title:** AI-Based Student Performance Prediction

**Domain:** Artificial Intelligence and Machine Learning

**Programming Language:** Python

**Application Framework:** Streamlit

**Project Type:** Academic / Research Project

## 📄 Documentation

The project includes IEEE-style research documentation.

Further details about the methodology, implementation, experimental results, and findings will be provided in the research paper.

## 📜 License

This project is developed for academic and educational purposes.

---

⭐ If you find this project interesting, consider giving this repository a star!
