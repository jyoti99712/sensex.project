import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# CSV load
data = pd.read_csv("sensex.csv")

# Features aur target
X = data[['High','Low','Close','Volume']]
y = data['Open']

# Model train
model = LinearRegression()
model.fit(X,y)

# Model save
joblib.dump(model,"open_model.pkl")

print("Model trained successfully")

# Example prediction
sample = [[62500,62000,62300,200000]]

prediction = model.predict(sample)

print("Predicted Open Price:", prediction[0])


import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample dataset (Open vs Close price)
data = {
    "Open": [100, 200, 300, 400, 500],
    "Close": [110, 210, 310, 410, 510]
}

df = pd.DataFrame(data)

# Features & Target
X = df[["Open"]]
y = df["Close"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model as .pkl file
joblib.dump(model, "model.pkl")

print("✅ model.pkl created successfully!")