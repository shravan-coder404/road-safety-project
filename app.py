from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample data generation (In real project, you'd load from files)
def generate_sample_data():
    """Generate sample accident and traffic data for demonstration"""
    
    # Sample locations in Bengaluru (you can change to your city)
    locations = [
        {"lat": 12.9716, "lng": 77.5946, "name": "MG Road"},
        {"lat": 12.9352, "lng": 77.6245, "name": "Koramangala"},
        {"lat": 12.9698, "lng": 77.7500, "name": "Whitefield"},
        {"lat": 12.9279, "lng": 77.6271, "name": "BTM Layout"},
        {"lat": 12.9141, "lng": 77.6097, "name": "Jayanagar"},
        {"lat": 12.9762, "lng": 77.6033, "name": "Cunningham Road"},
        {"lat": 12.9591, "lng": 77.7040, "name": "Marathahalli"},
        {"lat": 12.9343, "lng": 77.6101, "name": "JP Nagar"},
        {"lat": 12.9180, "lng": 77.6298, "name": "Bannerghatta Road"},
        {"lat": 12.9719, "lng": 77.6412, "name": "Indiranagar"}
    ]
    
    accident_data = []
    for i, loc in enumerate(locations):
        # Generate random accident data for each location
        accidents = random.randint(5, 50)
        severity = random.uniform(1, 10)
        traffic_volume = random.randint(100, 1000)
        weather_impact = random.uniform(0.5, 2.0)
        
        # Calculate risk score
        risk_score = calculate_risk_score(accidents, severity, traffic_volume, weather_impact)
        
        accident_data.append({
            "id": i,
            "location": loc["name"],
            "lat": loc["lat"],
            "lng": loc["lng"],
            "accidents": accidents,
            "severity": round(severity, 2),
            "traffic_volume": traffic_volume,
            "weather_impact": round(weather_impact, 2),
            "risk_score": round(risk_score, 2),
            "risk_level": get_risk_level(risk_score)
        })
    
    return accident_data

def calculate_risk_score(accidents, severity, traffic_volume, weather_impact):
    """Calculate risk score based on multiple factors"""
    # Weighted formula for risk calculation
    base_score = (accidents * 0.4) + (severity * 0.3) + (traffic_volume * 0.002)
    weather_adjusted = base_score * weather_impact
    
    # Normalize to 0-100 scale
    normalized_score = min(100, max(0, weather_adjusted))
    return normalized_score

def get_risk_level(risk_score):
    """Convert risk score to categorical level"""
    if risk_score >= 75:
        return "Very High"
    elif risk_score >= 50:
        return "High" 
    elif risk_score >= 25:
        return "Medium"
    else:
        return "Low"

# Generate sample data when app starts
sample_data = generate_sample_data()

@app.route('/')
def index():
    """Main page with the interactive map"""
    return render_template('index.html')

@app.route('/api/risk-data')
def get_risk_data():
    """API endpoint to get risk data for the map"""
    # Filter data based on query parameters
    min_risk = float(request.args.get('min_risk', 0))
    max_risk = float(request.args.get('max_risk', 100))
    
    filtered_data = [
        item for item in sample_data 
        if min_risk <= item['risk_score'] <= max_risk
    ]
    
    return jsonify(filtered_data)

@app.route('/api/statistics')
def get_statistics():
    """API endpoint to get overall statistics"""
    total_accidents = sum(item['accidents'] for item in sample_data)
    avg_risk = sum(item['risk_score'] for item in sample_data) / len(sample_data)
    high_risk_areas = len([item for item in sample_data if item['risk_score'] >= 50])
    
    stats = {
        "total_locations": len(sample_data),
        "total_accidents": total_accidents,
        "average_risk": round(avg_risk, 2),
        "high_risk_areas": high_risk_areas,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(stats)

@app.route('/api/location-details/<int:location_id>')
def get_location_details(location_id):
    """Get detailed information for a specific location"""
    location = next((item for item in sample_data if item['id'] == location_id), None)
    
    if location:
        # Add some additional details for the popup
        details = location.copy()
        details['recommendations'] = get_safety_recommendations(location['risk_score'])
        return jsonify(details)
    else:
        return jsonify({"error": "Location not found"}), 404

def get_safety_recommendations(risk_score):
    """Get safety recommendations based on risk score"""
    if risk_score >= 75:
        return [
            "Install additional traffic lights",
            "Deploy traffic police during peak hours",
            "Add speed cameras",
            "Improve road lighting",
            "Consider traffic diversions"
        ]
    elif risk_score >= 50:
        return [
            "Add warning signs",
            "Improve road markings",
            "Regular police patrolling",
            "Monitor during bad weather"
        ]
    elif risk_score >= 25:
        return [
            "Monitor traffic patterns",
            "Maintain road conditions",
            "Public awareness campaigns"
        ]
    else:
        return [
            "Continue regular monitoring",
            "Maintain current safety measures"
        ]

if __name__ == '__main__':
    print("🚀 Starting Road Safety Risk Analyzer...")
    print("📊 Generated sample data for demonstration")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000)
