
import os
import io
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import base64
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Missing Google API key.")

def input_pdf_setup(uploaded_file):
    """Converts the first page of a PDF to a JPEG image in base64 format."""
    try:
        # Convert from PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        if not images:
            raise ValueError("No images found in the PDF.")
        first_page = images[0]

        # Convert the first page image to a JPEG byte array
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode the image to base64
        pdf_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
        return pdf_part
    except Exception as e:
        st.error(f"Failed to convert PDF to image: {str(e)}")
        return None

def get_gemini_response(model_type, input_data, prompt):
    """Generate content based on the model type and input data."""
    try:
        # Initialize the generative model
        model = genai.GenerativeModel(model_type)
        response = model.generate_content([prompt, input_data])
        return response.text
    except Exception as e:
        st.error(f"Failed to generate content: {str(e)}")
        return "Error in generating response."

def main():
    st.set_page_config(page_title="Gemini Integration App")
    st.header("Images and Docs Reading (Gemini API)")

    input_text = st.text_area("Enter your prompt:", key="input")
    uploaded_file = st.file_uploader("Upload your document (PDF or image)...", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file:
        file_type = uploaded_file.type
        st.write(f"Detected file type: {file_type}")  # Show the detected file type

    input_type = st.selectbox("Select the input type:", ("Text", "PDF", "Image"))
    submit_button = st.button("Generate Response")

    if submit_button and uploaded_file:
        try:  # This try covers the whole if condition for PDF and Image processing
            if input_type == "PDF" and 'pdf' in file_type:
                pdf_content = input_pdf_setup(uploaded_file)
                if pdf_content:
                    response = get_gemini_response("gemini-pro-vision", pdf_content, input_text)
                    st.subheader("Response")
                    st.write(response)
            elif input_type == "Image" and any(ext in file_type for ext in ['jpg', 'jpeg', 'png']):
                image = Image.open(uploaded_file)
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format)
                img_byte_arr = img_byte_arr.getvalue()
                image_data = {
                    "mime_type": f"image/{image.format.lower()}",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
                response = get_gemini_response("gemini-pro-vision", image_data, input_text)
                st.subheader("Response")
                st.write(response)
            else:
                st.error("Unsupported file type or mismatch between selected input type and actual file type.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
