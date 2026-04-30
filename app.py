from flask import Flask, render_template, request
import joblib
import os
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Load trained model
model_path = os.path.join(os.getcwd(), "model.pkl")
model = joblib.load(model_path) if os.path.exists(model_path) else None

# Global list to store session history
history_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard_home():
    return render_template("dashboard.html", history=history_data)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not model:
            return "Model file not found! Run model.py first."

        open_price = float(request.form["open_price"])
        predicted_price = model.predict([[open_price]])[0]
        difference = predicted_price - open_price
        percent_change = (difference / open_price) * 100 if open_price != 0 else 0

        # Determine Trend
        if difference > 0:
            trend = f"Market Trend: HIGH 📈"
            change_str = f"+{difference:.2f}"
            gauge_color = "#22c55e"
            gauge_value = min(100, 50 + abs(percent_change) * 10)
        else:
            trend = f"Market Trend: LOW 📉"
            change_str = f"{difference:.2f}"
            gauge_color = "#ef4444"
            gauge_value = max(0, 50 - abs(percent_change) * 10)

        # Update History
        history_entry = {
            "input": f"{open_price:.2f}",
            "prediction": f"{predicted_price:.2f}",
            "change": change_str,
            "trend": "High" if difference > 0 else "Low"
        }
        history_data.insert(0, history_entry)
        if len(history_data) > 5: history_data.pop()

        # Visuals: Bar Chart
        bar_fig = go.Figure(data=[go.Bar(
            x=["Today Open", "Predicted Next"], 
            y=[open_price, predicted_price],
            marker=dict(color=["#6366f1", "#a855f7"])
        )])
        bar_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350)
        bar_chart = pio.to_html(bar_fig, full_html=False)

        # Visuals: Gauge Chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number", value=gauge_value,
            title={'text': "Market Sentiment"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': gauge_color}}
        ))
        gauge_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=350)
        gauge_chart = pio.to_html(gauge_fig, full_html=False)

        return render_template(
            "dashboard.html",
            prediction_text=f"₹{predicted_price:.2f}",
            trend_text=trend,
            bar_chart=bar_chart,
            gauge_chart=gauge_chart,
            history=history_data
        )

    except Exception as e:
        return render_template("dashboard.html", prediction_text=f"Error: {str(e)}", history=history_data)

if __name__ == "__main__":
    print("Starting Flask App...")   # 👈 ye add karo
    app.run(host="0.0.0.0", port=5000)