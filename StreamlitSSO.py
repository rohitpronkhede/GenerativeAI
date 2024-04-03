import streamlit as st
import mysql.connector
from requests_oauthlib import OAuth2Session

# Initialize session state
if "signed_in" not in st.session_state:
    st.session_state.signed_in = False

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rohit@123",
    database="trendytech"
)
cursor = conn.cursor()

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = "XXXXX"
GOOGLE_CLIENT_SECRET = "XXXXX"
GOOGLE_REDIRECT_URI = "http://localhost:8501"
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Function to handle Google OAuth2 login
def google_login():
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI, scope=["openid", "email", "profile"])
    authorization_url, _ = google.authorization_url(GOOGLE_AUTHORIZATION_URL)
    st.write(f"[Login with Google]({authorization_url})")

# Function to handle Google OAuth2 callback
def google_callback():
    # Handle the callback after Google OAuth2 authentication
    pass  # Implement your logic here

# Streamlit UI for login page
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        # Check if username and password exist in the database
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            st.session_state.signed_in = True
            st.success("Logged in successfully!")
            chatbot()  # Redirect to Chatbot page after successful login
        else:
            st.error("Invalid username or password. Please proceed with Signup first!")

# Streamlit UI for signup page
def signup():
    st.title("Signup")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Signup"):
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            st.error("Username already exists. Please choose another one.")
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            st.success("Signup successful! Please login.")
            login()  # Redirect to login page after signup

# Streamlit UI for chatbot page
def chatbot():
    st.title("Chatbot")
    st.write("Welcome to the chatbot interface!")

    # Generate a unique key for the user input widget
    user_input_key = "user_input"

    # Chatbot logic
    user_input = st.text_input("You:", key=user_input_key)
    if st.button("Send"):
        # Placeholder chatbot response logic
        chatbot_response = get_chatbot_response(user_input)
        st.text_area("Chatbot:", value=chatbot_response)

# Placeholder chatbot response logic
def get_chatbot_response(user_input):
    # Simple if-else condition for demonstration
    if "hello" in user_input.lower():
        return "Hello! How can I assist you today?"
    else:
        return "I'm a simple chatbot. How can I help you?"

# Main function to run the Streamlit app
def main():
    st.sidebar.title("Navigation")
    if not st.session_state.signed_in:
        page = st.sidebar.radio("Go to", ["Login", "Signup", "SSO with Google"])
        if page == "Login":
            login()
        elif page == "Signup":
            signup()
        elif page == "SSO with Google":
            google_login()  # Render Google login button
    else:
        chatbot()

if __name__ == "__main__":
    main()
