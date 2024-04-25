Overview

The Gemini Integration App is a Streamlit-based web application designed to integrate with Google's generative AI technologies. It allows users to upload documents and images, which are then processed and analysed using Google's AI models. The app supports handling PDFs, JPEGs, and PNG files, converting them into suitable formats and generating AI-based content responses.

Features

Document and Image Upload: Users can upload PDFs or image files (JPG, JPEG, PNG) for processing.
AI-Powered Analysis: Utilises Google's generative AI models to analyse the content of the documents or images.
Flexible Input Handling: Supports text input alongside file uploads to tailor the AI response based on user-provided prompts.
Base64 Encoding: Converts images and PDF pages to base64 encoded strings for AI processing.

Requirements

To run this app, you need the following:

Python 3.6 or newer
Streamlit
Google's Generative AI library (google.generativeai)
pdf2image
PIL (Pillow)
base64
io
dotenv for environment variable management

Installation

Clone the repository
               git clone <repository-url>
               cd <repository-directory>

Install dependencies
pip install streamlit pdf2image Pillow python-dotenv google-generativeai

Set up environment variables
Create a .env file in the root directory of the project and add the following line
GOOGLE_API_KEY='your_google_api_key_here'

Usage

To run the application, navigate to the project directory and execute

streamlit run app.py
Open your web browser and go to http://localhost:8501 to interact with the app.