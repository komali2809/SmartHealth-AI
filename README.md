# SmartHealth AI 🧠🥗

**Explainable, Region-Aware Health & Wellness Intelligence Platform**

SmartHealth AI is an AI/ML-based health and wellness platform that combines symptom-pattern analysis, explainability, nutrition intelligence, regional food recommendations, allergy filtering, personalized meal planning, traditional wellness information, knowledge retrieval, and user history in a single application.

> **Important:** SmartHealth AI is an educational and wellness-support system. Its model outputs are model-generated possibilities based on the training data and are **not medical diagnoses or medical advice**.

---

## 🚀 Problem

Health-related information is often scattered across different applications:

* Symptom analysis is separated from nutrition planning.
* Food recommendations may not consider region or dietary preferences.
* Allergy restrictions are often handled manually.
* Traditional wellness information is difficult to organize and retrieve.
* Users have limited history and progress tracking across these activities.

SmartHealth AI combines these capabilities into one modular platform.

---

## 💡 Solution

The platform provides a connected workflow:

```text
User Profile
     ↓
Symptom Analysis
     ↓
Top Model-Generated Possibilities
     ↓
Explainability
     ↓
Nutrition Profile
     ↓
Regional Food Recommendations
     ↓
Allergy & Diet Filtering
     ↓
Personalized Meal Plan
     ↓
History & Progress
```

The application also provides separate knowledge-based wellness sections for Ayurveda and homeopathy.

---

## ✨ Key Features

### 🧠 1. Symptom Analysis

Users select symptoms from the application's symptom vocabulary.

The machine-learning model provides:

* Primary model output
* Top possible condition patterns
* Probability values where supported
* Selected symptom summary

The output is explicitly presented as a **model-generated possibility**, not a diagnosis.

---

### 🔍 2. Model Explainability

The application displays feature-importance information for selected symptoms when supported by the trained model.

This helps users understand which selected input features contributed to the model's output.

---

### 🥗 3. Nutrition Intelligence

The platform calculates:

* BMI
* BMI category
* BMR
* Estimated TDEE

It also provides condition-aware food recommendations using nutritional attributes.

---

### 🌎 4. Region-Aware Food Recommendations

Food recommendations can be filtered using:

* Country
* State
* Region
* Diet type
* Calories
* Protein
* Allergies

This allows the recommendation system to consider food availability and dietary preferences.

---

### 🚨 5. Allergy Safety Filtering

The platform identifies foods containing specified allergens and removes them from recommended food results.

Supported allergen categories include examples such as:

* Peanut
* Milk
* Egg
* Fish
* Shellfish
* Gluten
* Soy
* Tree nuts
* Coconut

---

### 🍽️ 6. Personalized Meal Planning

The system generates meal plans containing:

* Breakfast
* Lunch
* Snack
* Dinner

Meal plans are generated using available food data, nutritional requirements, diet preferences, and allergy restrictions.

---

### 🌿 7. Traditional Wellness Knowledge

Separate knowledge modules provide informational references for:

* Ayurveda
* Homeopathy

These sections are presented as **traditional/educational information** and are not represented as proven medical treatments.

---

### 📚 8. Knowledge Retrieval

SmartHealth AI includes a local knowledge-retrieval layer that searches project knowledge documents and returns relevant information.

The current implementation uses lightweight local retrieval rather than claiming clinical-grade semantic retrieval.

---

### 🗃️ 9. User History

SQLite is used to store application history such as:

* Symptom analyses
* Selected symptoms
* Model output
* Meal plans
* Nutrition-related meal information
* Creation timestamps

Timestamps are stored using Indian Standard Time (IST).

---

### 📊 10. Progress Dashboard

The application provides:

* Analysis history
* Prediction summaries
* Recent activity
* Progress information

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   Symptom Analysis       Nutrition Engine      Wellness
          │                    │                    │
          ▼                    ▼                    ▼
    ML Model             Food Engine        Knowledge Base
          │                    │                    │
          └──────────────┬─────┴────────────────────┘
                         │
                         ▼
                Allergy/Safety Layer
                         │
                         ▼
                  Meal Plan Engine
                         │
                         ▼
                    SQLite DB
                         │
                         ▼
                 History / Progress
```

---

## 🛠️ Technology Stack

### Frontend / Application

* Python
* Streamlit

### Machine Learning

* Scikit-learn
* Decision Tree Classifier
* NumPy
* Pandas
* Joblib

### Data & Storage

* CSV datasets
* SQLite

### Knowledge & Retrieval

* Local Markdown/Text knowledge base
* Lightweight retrieval engine

### Development

* VS Code
* Git
* GitHub

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
│   ├── disease_model.pkl
│   ├── model_metadata.json
│   └── evaluate_model.py
│
├── data/
│   ├── symptoms_disease_dataset_40.csv
│   ├── disease_diet_plan_40.csv
│   ├── regional_foods.csv
│   ├── ayurvedic_knowledge.csv
│   └── homeopathy_knowledge.csv
│
├── database/
│   ├── database.py
│   └── smarthealth.db
│
├── modules/
│   ├── symptom_analyzer.py
│   ├── preprocessing.py
│   ├── explainability.py
│   ├── nutrition.py
│   ├── regional_recommendations.py
│   ├── condition_nutrition.py
│   ├── allergy_filter.py
│   ├── ayurveda.py
│   ├── homeopathy.py
│   ├── meal_planner.py
│   ├── safety.py
│   ├── rag_engine.py
│   └── history.py
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

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartHealth-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it on Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🔐 Privacy & Security

The project follows basic privacy practices:

* API keys are not stored directly in source code.
* `.env` files are excluded from Git.
* SQLite database files are excluded from Git.
* Python cache files are excluded from Git.
* User history is stored locally by the application.
* Health-related outputs contain safety disclaimers.

Sensitive information should not be entered into a publicly deployed version unless appropriate privacy and security controls have been implemented.

---

## ⚠️ Model & Dataset Limitations

The current prototype dataset contains a small number of records relative to the number of condition classes.

Therefore:

* Conventional train/test metrics are not sufficient to establish clinical performance.
* The model should not be interpreted as a medically validated diagnostic system.
* Predictions depend entirely on the available training data.
* Real-world clinical use would require substantially larger and clinically validated datasets.
* External medical validation would be required before any diagnostic application.

---

## 🧪 Testing

The application was manually tested through the Streamlit interface.

Major workflows tested include:

* Symptom selection and analysis
* Multiple model-generated outputs
* Explainability
* Nutrition calculations
* Regional food filtering
* Allergy filtering
* Meal-plan generation
* Database history
* Progress display
* Ayurveda knowledge search
* Homeopathy knowledge search
* Dashboard
* Profile

---

## 🔮 Future Improvements

Possible future improvements include:

* Larger and higher-quality datasets
* Cross-validation and stronger model evaluation
* Embedding-based semantic retrieval
* Improved personalized nutrition optimization
* Secure authentication
* Encrypted sensitive data storage
* Role-based access control
* Stronger privacy controls
* Evidence-linked knowledge sources
* Clinician-reviewed datasets and validation
* More advanced recommendation models

---

## 👩‍💻 Project

**SmartHealth AI**

**Domain:** Artificial Intelligence / Machine Learning / Health & Wellness Technology

**Core Technologies:** Python, Streamlit, Scikit-learn, Pandas, NumPy, SQLite, RAG/Knowledge Retrieval

---

## ⚕️ Safety Notice

SmartHealth AI is intended for educational and wellness-support purposes.

Its symptom-analysis results are **model-generated possibilities**, not medical diagnoses.

Ayurvedic and homeopathic information is presented for traditional and educational reference and should not be treated as proven medical treatment.

For severe, persistent, or rapidly worsening symptoms, users should seek appropriate professional medical care.
