#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from research_crew_ollama.crew import ResearchCrewOllama

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

app = Flask(__name__)

def run_research(topic):
    """
    Run the crew with a specific topic.
    """
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    
    try:
        ResearchCrewOllama().crew().kickoff(inputs=inputs)
        return True
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_research', methods=['POST'])
def start_research():
    topic = request.form.get('topic', 'AI Agents in 2024-2025')
    success = run_research(topic)
    
    if success:
        try:
            with open('output/report.md', 'r') as f:
                report = f.read()
        except:
            report = "Report file not found. Check the output directory."
    else:
        report = "An error occurred during research."
        
    return jsonify({'status': 'success' if success else 'error', 'report': report})

def run():
    """
    Run the web application.
    """
    app.run(debug=True)

def train(topic):
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": topic,
    }
    try:
        ResearchCrewOllama().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def test(topic):
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": topic,
        "current_year": str(datetime.now().year)
    }
    try:
        ResearchCrewOllama().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
