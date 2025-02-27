import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from datetime import datetime
import plotly.express as px

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set page configuration
st.set_page_config(page_title="Healthcare Assistant", page_icon="⚕️", layout="wide")

# Hide Streamlit branding
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Initialize chatbot model
chatbot = pipeline("text-generation", model="distilgpt2")

# Predefined health tips
health_tips = [
    "Stay hydrated by drinking at least 8 glasses of water daily. 💧",
    "Incorporate a mix of cardio and strength exercises into your routine. 🏃‍♀️🏋️‍♂️",
    "Prioritize sleep! Aim for 7-8 hours every night. 😴",
    "Include more greens and lean protein in your diet. 🥗🍗",
    "Take short breaks when working long hours to reduce stress. 🧘‍♂️",
    "Wash your hands frequently to prevent infections. 🧼",
]

# Predefined FAQs
faq_responses = {
    "What is a healthy diet?": "A healthy diet includes fruits, vegetables, whole grains, lean proteins, and limited sugar and saturated fats.",
    "How can I boost my immunity?": "Eat a balanced diet, exercise regularly, stay hydrated, and get enough sleep. Vitamins like C and D can also help.",
    "How much exercise is enough?": "It’s recommended to have at least 150 minutes of moderate aerobic activity per week.",
}

# Generate chatbot response with disclaimer
def healthcare_chatbot(user_input):
    if user_input.lower() in faq_responses:
        return faq_responses[user_input.lower()]
    try:
        response = chatbot(user_input, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"] + "\n\n⚠️ *Disclaimer: AI-generated responses may not always be accurate. Consult a medical professional for serious concerns.*"
    except Exception:
        return "Sorry, I couldn't process your request. Could you try asking in a different way?"

# Page layout
def main():
    st.title("💡 Healthcare Assistant Chatbot")
    st.markdown("""
        Welcome to your all-in-one health assistant. Here’s what I can do:
        - 🩺 Chatbot for quick health advice.
        - 📋 Daily health tips to improve your lifestyle.
        - 📅 Appointment scheduling with reminders.
        - 🤔 FAQ section for common queries.
    """)

    # Sidebar navigation
    st.sidebar.header("🔧 Tools")
    page = st.sidebar.radio("Navigate to:", ["🤖 Chatbot", "📋 Health Tips", "📅 Appointment Scheduler", "❓ FAQs", "📊 Health Data"])

    if page == "🤖 Chatbot":
        st.subheader("How can I assist you today?")
        user_input = st.text_input("Enter your question or message:")
        if st.button("Submit", key="chat_submit"):
            if user_input:
                st.write("**You:**", user_input)
                with st.spinner("Processing..."):
                    response = healthcare_chatbot(user_input)
                st.write("**Healthcare Assistant:**", response)
            else:
                st.warning("Please enter a message to get a response.")

    elif page == "📋 Health Tips":
        st.subheader("Daily Health Tips")
        st.write(random.choice(health_tips))
        if st.button("Show Another Tip", key="tip_refresh"):
            st.write(random.choice(health_tips))

    elif page == "📅 Appointment Scheduler":
        st.subheader("Schedule an Appointment")
        name = st.text_input("Your Name")
        date = st.date_input("Choose a date", min_value=datetime.now().date())
        time = st.time_input("Choose a time")
        if st.button("Book Appointment", key="appointment_submit"):
            if name:
                st.success(f"Appointment booked for {name} on {date.strftime('%A, %d %B %Y')} at {time}!")
            else:
                st.warning("Please enter your name to book an appointment.")

    elif page == "❓ FAQs":
        st.subheader("Frequently Asked Questions")
        question = st.selectbox("Select a question:", list(faq_responses.keys()))
        if st.button("Get Answer", key="faq_submit"):
            st.write("**Question:**", question)
            st.write("**Answer:**", faq_responses[question])

    elif page == "📊 Health Data":
        st.subheader("Health Data Visualization")
        data = {
            "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "Hours of Exercise": [1, 0.5, 1.5, 1, 2],
        }
        fig = px.bar(data, x="Day", y="Hours of Exercise", title="Weekly Exercise Tracker", color="Hours of Exercise", height=400)
        st.plotly_chart(fig)
        
    # Footer Section
    st.markdown("""
    ---
    🚀 Developed by [Akshay Sirpuram](https://in.linkedin.com/in/akshay-sirpuram)  
    🌟 GitHub: [AkshaySirpuram](http://github.com/AkshaySirpuram)  
    📧 Contact: sakshayrao1265@gmail.com
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
