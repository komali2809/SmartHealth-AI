# SmartHealth AI 🩺

### Explainable, Region-Aware Health & Wellness Intelligence Platform

SmartHealth AI is a machine-learning-powered health and wellness platform that combines **symptom pattern analysis, explainability, nutrition intelligence, regional food recommendations, traditional wellness knowledge, personalized meal planning, safety filtering, and user history** in a single application.

> **Important:** SmartHealth AI is an educational and decision-support prototype. Its predictions are model-generated possibilities based on the available dataset and are **not medical diagnoses or medical advice**. Users should consult qualified healthcare professionals for medical concerns.

---

## 🚀 Project Overview

Many basic health applications only provide a disease prediction from selected symptoms.

SmartHealth AI goes beyond a simple prediction model by combining multiple intelligence layers:

```text
User Symptoms
      ↓
Symptom Preprocessing
      ↓
ML-Based Pattern Analysis
      ↓
Top Possible Condition Patterns
      ↓
Explainability
      ↓
Nutrition & Wellness Intelligence
      ↓
Regional Food Recommendations
      ↓
Allergy & Safety Filtering
      ↓
Personalized Meal Planning
      ↓
History & Progress Tracking
```

The goal is to demonstrate how machine learning, structured knowledge, personalization, and safety-aware filtering can be combined into a practical software product.

---

## ✨ Key Features

### 1. 🧠 Symptom Analysis

Users can select multiple symptoms and receive:

* Primary model-generated condition pattern
* Top possible condition patterns
* Probability estimates from the trained model
* Selected symptom summary
* Explainability information
* Safety guidance

The system does **not** present the prediction as a medical diagnosis.

---

### 2. 🔍 Explainable Predictions

Instead of only displaying a prediction, SmartHealth AI provides information about the symptom patterns associated with the model's output.

This makes the result easier to understand and demonstrates an explainable-AI workflow.

---

### 3. 🥗 Nutrition Intelligence

The platform provides nutrition-related recommendations based on available condition and food information.

The nutrition module can consider:

* Food categories
* Nutritional characteristics
* User preferences
* Dietary restrictions
* Allergies
* Regional availability

Nutrition values and recommendations are treated as estimates/information rather than medical prescriptions.

---

### 4. 🌎 Region-Aware Food Recommendations

Food recommendations can be filtered according to the user's:

* Country
* State/region
* Dietary preferences
* Available food options

This makes the recommendation system more personalized than a generic food list.

---

### 5. 🌿 Traditional Wellness Knowledge

SmartHealth AI contains separate knowledge modules for:

* Ayurveda
* Homeopathy

These sections are provided for **traditional and educational information**.

The platform does not claim that traditional remedies cure diseases or replace evidence-based medical treatment.

---

### 6. 🤖 Knowledge Retrieval / RAG Layer

The project includes a knowledge-retrieval architecture for retrieving relevant information from structured wellness and safety knowledge sources.

The retrieval layer can be used to provide context for:

* Nutrition information
* Traditional wellness information
* Safety guidance
* Food recommendations

This separates knowledge retrieval from the ML prediction layer.

---

### 7. ⚠️ Allergy & Safety Filtering

The application includes safety-oriented filtering to reduce inappropriate food recommendations.

The system can consider:

* User allergies
* Dietary restrictions
* Food compatibility
* Safety information

Safety information is presented conservatively and does not replace professional medical advice.

---

### 8. 🍱 Personalized Meal Planning

Users can generate meal plans using available food and nutrition information.

The meal-planning module can incorporate:

* Food preferences
* Regional foods
* Dietary restrictions
* Allergy filtering
* Nutrition information

Generated plans are informational and should not be treated as prescribed diets.

---

### 9. 📊 Dashboard

The dashboard provides an overview of the user's activity and available health/wellness information.

It connects different parts of the platform into a single interface.

---

### 10. 🕒 History Tracking

Previous symptom analyses and meal plans can be stored in the application database.

This allows users to review previous activity instead of treating every session as completely independent.

---

### 11. 📈 Progress Tracking

The progress section provides a way to review historical activity and observe changes in recorded information over time.

---

### 12. 👤 User Profile

The platform can store basic user information required for personalization, such as:

* Name
* Age
* Gender
* Country
* State/region

Only information required by the application should be provided by the user.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │    User Interface   │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ Symptom        │ │ Nutrition &    │ │ Wellness       │
        │ Analysis       │ │ Meal Planning  │ │ Knowledge      │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ ML Model       │ │ Safety /       │ │ RAG / Knowledge│
        │                │ │ Allergy Filter │ │ Retrieval      │
        └───────┬────────┘ └───────┬────────┘ └────────────────┘
                │                  │
                └──────────┬───────┘
                           ▼
                  ┌─────────────────┐
                  │ SQLite Database │
                  │ History/Profile │
                  └─────────────────┘
```

---

## 🧰 Technology Stack

### Frontend / Application

* Python
* Streamlit

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Database

* SQLite

### AI / Intelligence

* Machine Learning
* Explainable prediction workflow
* Knowledge retrieval / RAG architecture
* Rule-based safety filtering

### Development

* VS Code
* Git
* GitHub
* Python Virtual Environment

---

## 📁 Project Structure

```text
SmartHealth-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── model/
│   ├── train_model.py
│   ├── disease_model.pkl
│   └── model_metadata.json
│
├── data/
│   ├── symptoms_disease_dataset_40.csv
│   ├── disease_diet_plan_40.csv
│   ├── regional_foods.csv
│   ├── ayurvedic_knowledge.csv
│   └── homeopathy_knowledge.csv
│
├── database/
│   └── database.py
│
├── modules/
│   ├── symptom_analyzer.py
│   ├── preprocessing.py
│   ├── explainability.py
│   ├── nutrition.py
│   ├── regional_recommendations.py
│   ├── ayurveda.py
│   ├── homeopathy.py
│   ├── meal_planner.py
│   ├── safety.py
│   └── rag_engine.py
│
├── pages/
│   ├── dashboard.py
│   ├── symptom_analysis.py
│   ├── nutrition.py
│   ├── wellness.py
│   ├── meal_plan.py
│   ├── progress.py
│   ├── history.py
│   ├── model_performance.py
│   └── profile.py
│
└── knowledge/
    ├── nutrition/
    ├── ayurveda/
    ├── homeopathy/
    └── safety/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/komali2809/SmartHealth-AI.git
```

### 2. Open the project

```bash
cd SmartHealth-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing

SmartHealth AI can be tested directly through the Streamlit interface.

### Symptom Analysis

1. Open Symptom Analysis.
2. Enter the required profile information.
3. Select symptoms.
4. Run the analysis.
5. Review the generated condition patterns.
6. Review explainability and safety information.

### Meal Planning

1. Open Meal Plan.
2. Provide the required information.
3. Generate a meal plan.
4. Verify that allergy/diet restrictions are considered.

### History

1. Perform a symptom analysis.
2. Save the result.
3. Open History.
4. Verify that the analysis appears with its recorded timestamp.

### Progress

1. Generate multiple records.
2. Open Progress.
3. Review the recorded activity.

---

## 🔐 Privacy & Security

SmartHealth AI is designed to minimize unnecessary exposure of user information.

Security considerations include:

* Local SQLite storage during development
* No API keys committed to Git
* `.env` excluded through `.gitignore`
* Database files excluded from Git
* Python virtual environment excluded from Git
* Separation of application modules
* Safety filtering before presenting recommendations

Example `.gitignore` entries:

```text
.env
*.db
database/*.db
.venv/
__pycache__/
*.pyc
```

For production deployment, additional controls such as authentication, encrypted storage, HTTPS, access control, secure secrets management, database security, logging policies, and data-retention controls would be required.

---

## ⚠️ Model & Dataset Limitations

The current prototype uses a relatively small symptom dataset containing approximately 40 condition classes.

Because the dataset is limited, the model should **not** be interpreted as clinically accurate or medically validated.

The model output represents:

> A machine-learning-generated symptom pattern based on the available training data.

It should not be used to diagnose, treat, or rule out a medical condition.

A production medical system would require substantially larger and clinically validated datasets, rigorous evaluation, external validation, bias analysis, clinical review, and appropriate regulatory compliance.

---

## 🧠 Engineering Highlights

This project demonstrates the integration of multiple software and AI concepts:

* Machine-learning classification
* Feature preprocessing
* Explainable prediction
* Structured knowledge retrieval
* RAG architecture
* Rule-based safety filtering
* Recommendation systems
* Personalization
* Regional filtering
* Meal planning
* SQLite persistence
* Multi-page Streamlit architecture
* Modular Python development
* Git/GitHub version control

Rather than implementing only a disease classifier, the project combines th
