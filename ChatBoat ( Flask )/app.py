from flask import Flask, request, jsonify, render_template
from mira_sdk import MiraClient, Flow
import re
import json

client = MiraClient(config={"API_KEY": "your Mira api key"})  # Initialize Mira Client

def format_to_html(text):
    # Convert headings (### Heading → <h3>Heading</h3>)
    text = re.sub(r"### (.*?)\n", r"<h3>\1</h3>", text)
    text = re.sub(r"## (.*?)\n", r"<h2>\1</h2>", text)
    text = re.sub(r"# (.*?)\n", r"<h1>\1</h1>", text)

    # Convert bold text (**bold** → <b>bold</b>)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Convert bullet points (- Item → <li>Item</li>)
    text = text.replace("\n- ", "\n<li>").replace("\n  - ", "\n  <li>")
    text = re.sub(r"<li>(.*?)(?=\n<li>|\n\n|$)", r"<li>\1</li>", text)
    text = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)

    # Format sections for the frontend cards
    text = re.sub(r"<h2>Energy Generation Forecast:</h2>", r'<div class="forecast-card"><div class="card-title">⚡ Energy Generation Forecast</div><div class="card-content">', text)
    text = re.sub(r"<h2>Load Balancing Strategies:</h2>", r'</div></div><div class="strategy-card"><div class="card-title">⚖️ Load Balancing Strategies</div><div class="card-content">', text)
    text = re.sub(r"<h2>Battery Health Optimization:</h2>", r'</div></div><div class="battery-card"><div class="card-title">🔋 Battery Health Optimization</div><div class="card-content">', text)
    text = re.sub(r"<h2>Smart Energy Management:</h2>", r'</div></div><div class="strategy-card"><div class="card-title">🏡 Smart Energy Management</div><div class="card-content">', text)
    
    # Close the last card
    text = text + "</div></div>"

    return text

app = Flask(__name__)

def get_energy_management(input_dict):
    # Load the energy forecasting flow from the YAML file
    flow = Flow(source="energy_forecasting.yaml")
    response = client.flow.test(flow, input_dict)
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/collect_energy_data", methods=["POST"])
def collect_energy_data():
    # Get the user input
    data = request.json
    user_input = data.get("user_message", "")
    
    # Extract selected energy sources if available
    selected_sources = data.get("energy_sources", [])
    if not selected_sources:
        # Try to extract from the message
        if "solar" in user_input.lower():
            selected_sources.append("Solar Panels")
        if "wind" in user_input.lower():
            selected_sources.append("Wind Turbine")
        if "battery" in user_input.lower() or "storage" in user_input.lower():
            selected_sources.append("Battery Storage")
    
    # Extract weather if available
    weather = data.get("weather", "sunny")
    for condition in ["sunny", "cloudy", "rainy", "windy", "storm"]:
        if condition in user_input.lower():
            weather = condition
            break
    
    # Extract location if available
    location = data.get("location", "Manipur")
    # You could implement more sophisticated location extraction here
    
    # Prepare input for the flow
    input_dict = {
        "location": location,
        "weather": weather,
        "energySources": ", ".join(selected_sources) if selected_sources else "Solar Panels, Battery Storage",
        "batteryStatus": data.get("battery_status", "Battery at 85% capacity, optimal health")
    }
    
    # Get energy management response
    response = get_energy_management(input_dict)
    formatted_response = format_to_html(response["result"])
    
    return jsonify({
        "bot": formatted_response,
        "energy_data": {
            "location": location,
            "weather": weather,
            "sources": selected_sources,
            "battery_status": input_dict["batteryStatus"]
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
