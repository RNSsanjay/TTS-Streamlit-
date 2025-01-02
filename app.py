import streamlit as st
from gtts import gTTS
from io import BytesIO
import PyPDF2
import docx

# App Title
st.title("Text-to-Speech from Document or Text")
st.write("Upload a document (txt, pdf, docx) or type your text, and convert it to speech.")

# File Upload Section
uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

# Text Input by User
text_input = st.text_area("Or, type the text you want to convert to speech:")

# Language Selection
language = st.selectbox("Choose the language:", ["en", "es", "fr", "de", "it", "hi"])

# Voice Speed Control
voice_speed = st.selectbox("Choose the voice speed:", ["Normal", "Slow", "Fast"])

# Voice Modulation Options (Simulated with speed adjustments in gTTS)
voice_type = st.selectbox(
    "Choose the voice type:",
    ["Default (Neutral)", "Fast (Female-like)", "Slow (Male-like)"]
)

# Function to extract text from txt file
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from docx file
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Generate Button
if st.button("Generate Speech"):
    if uploaded_file is not None or text_input.strip():
        try:
            # Extract text based on file type or use the user input text
            if uploaded_file is not None:
                if uploaded_file.type == "text/plain":
                    extracted_text = extract_text_from_txt(uploaded_file)
                elif uploaded_file.type == "application/pdf":
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    extracted_text = extract_text_from_docx(uploaded_file)
                else:
                    st.warning("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
                    extracted_text = None
            else:
                extracted_text = text_input

            # Check if any text was extracted
            if extracted_text:
                # Convert text to speech based on selected speed and voice type
                slow_speed = voice_speed == "Slow"
                fast_speed = voice_speed == "Fast"
                
                if voice_type == "Fast (Female-like)" and fast_speed:
                    tts = gTTS(text=extracted_text, lang=language, slow=False)
                elif voice_type == "Slow (Male-like)" and slow_speed:
                    tts = gTTS(text=extracted_text, lang=language, slow=True)
                else:
                    tts = gTTS(text=extracted_text, lang=language, slow=slow_speed)

                # Save to BytesIO for streaming
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                # Audio Playback
                st.audio(audio_buffer, format="audio/mp3")

                # Download Button
                st.download_button(
                    label="Download Audio",
                    data=audio_buffer,
                    file_name="speech.mp3",
                    mime="audio/mp3",
                )

        except Exception as e:
            st.error(f"Error generating speech: {e}")
    else:
        st.warning("Please upload a document or enter some text.")

# Footer
st.markdown(
    """
    **Note**: This application uses Google Text-to-Speech (gTTS) for speech synthesis. 
    """
)
