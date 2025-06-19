import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

# Load dataset
df = pd.read_csv("Application_Data.csv")

print("Missing values before cleaning:\n", df.isnull().sum())


# Selecting relevant columns
selected_columns = ["Applicant_Age", "Years_of_Working", "Total_Bad_Debt", "Total_Good_Debt",
                    "Owned_Realty", "Owned_Car", "Income_Type", "Status"]
df = df[selected_columns]

# One-hot encoding categorical variables
# Machine learning models can't work with categorical data, so we convert them into numeric values using One-Hot Encoding.
df = pd.get_dummies(df, columns=["Owned_Car", "Owned_Realty", "Income_Type"], drop_first=True)

# Splitting features and target variable
X = df.drop(columns=["Status"])
y = df["Status"]

# Standardizing the data
# Standardizes numerical features (mean = 0, standard deviation = 1).
# Helps models perform better and train faster.


scaler = StandardScaler()
X = scaler.fit_transform(X)

#f there are more approved applications (1s) than rejected (0s)
# Handling imbalanced data using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)  #SMOTE generates synthetic samples for the minority class (if needed).

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Logistic Regression Model
log_model = LogisticRegression()
log_model.fit(X_train, y_train)

# Predictions
y_pred_log = log_model.predict(X_test)

# Model Evaluation
print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred_log) * 100)
print("\nClassification Report:\n", classification_report(y_test, y_pred_log))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_log))
print("AUC-ROC Score:", roc_auc_score(y_test, y_pred_log))

# Save the trained model
joblib.dump(log_model, "credit_card_approval_model.pkl") #.pkl - Pickle file,
joblib.dump(scaler,"scaler.pkl")



# Load and test the saved model
loaded_model = joblib.load("credit_card_approval_model.pkl")
sample_input = X_test[0].reshape(1, -1)  # Example input
prediction = loaded_model.predict(sample_input)
print("Prediction:", prediction)
