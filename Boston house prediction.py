import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
# Load your uploaded dataset
df = pd.read_csv("Boston-house-price-data.csv")

# Quick view of the dataset
print(df.head())
print(df.info())
print(df.describe())
# Check for missing values
print(df.isnull().sum())

# Optionally drop or fill missing values
df = df.dropna()  # Or use df.fillna(method='ffill') if needed
X = df.drop("MEDV", axis=1)  # All features
y = df["MEDV"]               # Target variable (Price)


# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# Ridge Regression
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train_scaled, y_train)


# Predict and evaluate
lr_preds = lr_model.predict(X_test_scaled)
ridge_preds = ridge_model.predict(X_test_scaled)

print("Linear Regression:")
print("MSE:", mean_squared_error(y_test, lr_preds))
print("R2:", r2_score(y_test, lr_preds))

print("\nRidge Regression:")
print("MSE:", mean_squared_error(y_test, ridge_preds))
print("R2:", r2_score(y_test, ridge_preds))


# Correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

# Actual vs Predicted (for Ridge)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, ridge_preds, color='blue', label='Ridge Predictions')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red')
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted House Prices")
plt.legend()
plt.show()
