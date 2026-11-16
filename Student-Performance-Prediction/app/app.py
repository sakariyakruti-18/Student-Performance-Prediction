
import streamlit as st
import pandas as pd
import joblib
import sqlite3

from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# 2. PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "prediction_history.db"


# --------------------------------------------------
# 3. LOAD SAVED MACHINE LEARNING FILES
# --------------------------------------------------

@st.cache_resource
def load_ml_files():

    model = joblib.load(BASE_DIR / "best_student_model.pkl")

    preprocessor = joblib.load(
        BASE_DIR / "student_preprocessor.pkl"
    )

    label_encoder = joblib.load(
        BASE_DIR / "student_label_encoder.pkl"
    )

    return model, preprocessor, label_encoder


model, preprocessor, label_encoder = load_ml_files()


# --------------------------------------------------
# 4. PREDICTION HISTORY DATABASE
# --------------------------------------------------

def create_history_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            age INTEGER,
            attendance REAL,
            study_hours REAL,
            previous_marks REAL,
            assignment_score REAL,
            internal_marks REAL,
            quiz_average REAL,
            practical_score REAL,
            learning_hours REAL,

            class_participation TEXT,
            assignment_submission TEXT,
            internet_access TEXT,
            extracurricular_activities TEXT,

            predicted_category TEXT,
            prediction_date TEXT

        )
    """)

    conn.commit()
    conn.close()


def save_prediction(student_data, predicted_category):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    student = student_data.iloc[0]

    cursor.execute("""
        INSERT INTO prediction_history (

            age,
            attendance,
            study_hours,
            previous_marks,
            assignment_score,
            internal_marks,
            quiz_average,
            practical_score,
            learning_hours,

            class_participation,
            assignment_submission,
            internet_access,
            extracurricular_activities,

            predicted_category,
            prediction_date

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        int(student["Age"]),
        float(student["Attendance"]),
        float(student["Study_Hours"]),
        float(student["Previous_Marks"]),
        float(student["Assignment_Score"]),
        float(student["Internal_Marks"]),
        float(student["Quiz_Average"]),
        float(student["Practical_Score"]),
        float(student["Learning_Hours"]),

        student["Class_Participation"],
        student["Assignment_Submission"],
        student["Internet_Access"],
        student["Extracurricular_Activities"],

        predicted_category,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


def get_prediction_history():

    conn = sqlite3.connect(DB_PATH)

    history = pd.read_sql_query(
        "SELECT * FROM prediction_history ORDER BY id DESC",
        conn
    )

    conn.close()

    return history


def clear_prediction_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM prediction_history")

    conn.commit()
    conn.close()


# Create database table
create_history_table()


# --------------------------------------------------
# 5. APPLICATION TITLE
# --------------------------------------------------

st.title("🎓 AI-Based Student Performance Prediction")

st.write(
    "Enter the student's academic details below "
    "to predict their performance category."
)

st.divider()


# --------------------------------------------------
# 6. STUDENT INPUT FORM
# --------------------------------------------------

st.subheader("📋 Student Academic Information")

with st.form("student_form"):

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=21
        )

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

        study_hours = st.number_input(
            "Daily Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=4.0
        )

        previous_marks = st.number_input(
            "Previous Marks",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

        assignment_score = st.number_input(
            "Assignment Score",
            min_value=0.0,
            max_value=100.0,
            value=80.0
        )

        internal_marks = st.number_input(
            "Internal Marks",
            min_value=0.0,
            max_value=100.0,
            value=78.0
        )

        quiz_average = st.number_input(
            "Quiz Average",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

    with col2:

        practical_score = st.number_input(
            "Practical Score",
            min_value=0.0,
            max_value=100.0,
            value=80.0
        )

        learning_hours = st.number_input(
            "Additional Learning Hours",
            min_value=0.0,
            max_value=24.0,
            value=2.0
        )

        class_participation = st.selectbox(
            "Class Participation",
            ["Low", "Medium", "High"]
        )

        assignment_submission = st.selectbox(
            "Assignment Submission",
            ["Not Submitted", "Late", "On Time"]
        )

        internet_access = st.selectbox(
            "Internet Access",
            ["Yes", "No"]
        )

        extracurricular_activities = st.selectbox(
            "Extracurricular Activities",
            ["Yes", "No"]
        )

    submitted = st.form_submit_button(
        "🔍 Predict Performance",
        use_container_width=True
    )


# --------------------------------------------------
# 7. PREDICTION
# --------------------------------------------------

if submitted:

    student_data = pd.DataFrame([{

        "Age": age,
        "Attendance": attendance,
        "Study_Hours": study_hours,
        "Previous_Marks": previous_marks,
        "Assignment_Score": assignment_score,
        "Internal_Marks": internal_marks,
        "Quiz_Average": quiz_average,
        "Practical_Score": practical_score,
        "Learning_Hours": learning_hours,
        "Class_Participation": class_participation,
        "Assignment_Submission": assignment_submission,
        "Internet_Access": internet_access,
        "Extracurricular_Activities": extracurricular_activities

    }])

    # Apply saved preprocessing pipeline
    processed_data = preprocessor.transform(student_data)

    # Predict category
    prediction = model.predict(processed_data)

    # Decode prediction
    predicted_category = label_encoder.inverse_transform(
        prediction.astype(int)
    )[0]

    # Save prediction to database
    save_prediction(student_data, predicted_category)

    # Save latest prediction in session
    st.session_state["latest_prediction"] = predicted_category
    st.session_state["latest_student_data"] = student_data


    # --------------------------------------------------
    # 8. DISPLAY PREDICTION RESULT
    # --------------------------------------------------

    st.divider()

    st.subheader("📊 Student Performance Prediction")

    if predicted_category == "At Risk":

        st.error("Predicted Category: At Risk")

        st.write(
            "The student may need additional academic support."
        )

    elif predicted_category == "Average":

        st.warning("Predicted Category: Average")

        st.write(
            "The student is currently performing at an average level."
        )

    elif predicted_category == "Good":

        st.success("Predicted Category: Good")

        st.write(
            "The student is demonstrating good academic performance."
        )

    elif predicted_category == "Excellent":

        st.success("Predicted Category: Excellent")

        st.write(
            "The student is demonstrating excellent academic performance."
        )

    # Display entered information
    with st.expander("View Student Information"):

        st.dataframe(
            student_data,
            use_container_width=True
        )

    st.caption(
        "Prediction generated using the trained SVM machine learning model. "
        "This result is an estimate, not a definitive assessment."
    )


# --------------------------------------------------
# 9. BATCH CSV PREDICTION
# --------------------------------------------------

st.divider()

st.header("📂 Batch Student Performance Prediction")

st.write(
    "Upload a CSV file containing multiple student records "
    "to predict their performance categories together."
)

# Required input columns
REQUIRED_COLUMNS = [
    "Age",
    "Attendance",
    "Study_Hours",
    "Previous_Marks",
    "Assignment_Score",
    "Internal_Marks",
    "Quiz_Average",
    "Practical_Score",
    "Learning_Hours",
    "Class_Participation",
    "Assignment_Submission",
    "Internet_Access",
    "Extracurricular_Activities"
]

# CSV file uploader
uploaded_file = st.file_uploader(
    "Upload Student CSV File",
    type=["csv"],
    key="batch_csv_uploader"
)

if uploaded_file is not None:

    try:

        batch_df = pd.read_csv(uploaded_file)

        st.subheader("📋 Uploaded Dataset")

        st.write("Total student records:", len(batch_df))

        st.dataframe(
            batch_df.head(10),
            use_container_width=True
        )

        # Check required columns
        missing_columns = [
            col for col in REQUIRED_COLUMNS
            if col not in batch_df.columns
        ]

        if missing_columns:

            st.error(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )

        elif batch_df.empty:

            st.warning("The uploaded CSV file is empty.")

        else:

            if st.button(
                "🚀 Predict All Students",
                use_container_width=True,
                key="batch_predict_button"
            ):

                # Preserve Student_ID if available
                if "Student_ID" in batch_df.columns:
                    student_ids = batch_df["Student_ID"].copy()
                else:
                    student_ids = pd.Series(
                        [
                            f"Student {i + 1}"
                            for i in range(len(batch_df))
                        ]
                    )

                # Select only required input features
                X_batch = batch_df[REQUIRED_COLUMNS].copy()

                # Apply saved preprocessing
                X_batch_processed = preprocessor.transform(X_batch)

                # Predict all student categories
                batch_predictions = model.predict(
                    X_batch_processed
                )

                # Convert encoded predictions to category names
                predicted_categories = label_encoder.inverse_transform(
                    batch_predictions.astype(int)
                )

                # Create results DataFrame
                batch_results = pd.DataFrame({
                    "Student_ID": student_ids,
                    "Predicted_Category": predicted_categories
                })

                # Add prediction results to uploaded data
                final_results = batch_df.copy()

                final_results["Predicted_Category"] = (
                    predicted_categories
                )

                # Save each batch prediction to SQLite history
                for index, category in enumerate(predicted_categories):

                    student_record = X_batch.iloc[[index]]

                    save_prediction(
                        student_record,
                        category
                    )

                # Display results
                st.success(
                    f"Successfully predicted {len(batch_results)} students!"
                )

                st.subheader("📊 Batch Prediction Results")

                st.dataframe(
                    batch_results,
                    use_container_width=True,
                    hide_index=True
                )

                # Category summary
                st.subheader("📈 Performance Category Summary")

                category_counts = (
                    batch_results["Predicted_Category"]
                    .value_counts()
                    .reindex(
                        label_encoder.classes_,
                        fill_value=0
                    )
                )

                summary_df = category_counts.reset_index()

                summary_df.columns = [
                    "Performance Category",
                    "Number of Students"
                ]

                st.dataframe(
                    summary_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.bar_chart(
                    summary_df.set_index("Performance Category")
                )

                # Download results
                csv_output = final_results.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="⬇️ Download Batch Prediction Results",
                    data=csv_output,
                    file_name="student_batch_prediction_results.csv",
                    mime="text/csv"
                )

    except Exception as e:

        st.error(
            f"Unable to process the uploaded CSV file: {e}"
        )

# --------------------------------------------------
# 10. PREDICTION HISTORY
# --------------------------------------------------

st.divider()

st.header("📚 Student Prediction History")

history_df = get_prediction_history()

if not history_df.empty:

    # Display total predictions
    st.metric(
        "Total Predictions",
        len(history_df)
    )

    # Display history table
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    # Download history
    csv_data = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Prediction History",
        data=csv_data,
        file_name="student_prediction_history.csv",
        mime="text/csv"
    )

    # Clear history
    with st.expander("⚠️ Manage Prediction History"):

        st.warning(
            "Clearing history permanently deletes all saved prediction records."
        )

        confirm_clear = st.checkbox(
            "I confirm that I want to delete all prediction history."
        )

        if st.button(
            "🗑️ Clear Prediction History",
            disabled=not confirm_clear
        ):

            clear_prediction_history()

            st.success("Prediction history cleared successfully!")

            st.rerun()

else:

    st.info(
        "No prediction history available. "
        "Make your first student prediction to see records here."
    )


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Based Student Performance Prediction | "
    "Machine Learning Model: Support Vector Machine (SVM)"
)
