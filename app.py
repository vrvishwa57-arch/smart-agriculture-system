from flask import Flask, render_template, request
import joblib
import requests

app = Flask(__name__)

model = joblib.load("model.pkl")

# Profit data
profit_data = {
    "rice": (2000, 2.5),
    "wheat": (1800, 3.0),
    "maize": (1700, 2.8),
    "cotton": (5000, 1.2)
}

# 🌦️ Weather Function
def get_weather(city):
    api_key = "8b8d25d5c599bd9c91e6724892d8e311"   

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    data = requests.get(url).json()

    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    return temperature, humidity


@app.route('/')
def home():
     return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        city = request.form['city']

        # 🌦️ Get real weather
        temperature, humidity = get_weather(city)

        values = [
            float(request.form['N']),
            float(request.form['P']),
            float(request.form['K']),
            temperature,
            humidity,
            float(request.form['ph']),
            float(request.form['rainfall'])
        ]

        result = model.predict([values])[0]

        # 💰 Profit calculation
        if result in profit_data:
            price, yield_val = profit_data[result]
            profit = price * yield_val
        else:
            profit = "N/A"

        return render_template(
            "index.html",
            result=result,
            profit=profit,
            temp=temperature,
            hum=humidity
        )

    except Exception as e:
        return render_template("index.html", result="Error: " + str(e))


# 🤖 Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.form['message'].lower()

    if "crop" in msg:
        reply = "Enter details above to get crop recommendation."
    elif "water" in msg:
        reply = "Water crops when soil moisture is low."
    elif "fertilizer" in msg:
        reply = "Use fertilizers based on NPK values."
    else:
        reply = "I can help with farming advice!"

    return {"response": reply}


if __name__ == "__main__":
    app.run(debug=True)