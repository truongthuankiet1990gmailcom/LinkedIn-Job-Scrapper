#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting LinkedIn Job Market Analyzer..."
echo ""
echo "The application will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py