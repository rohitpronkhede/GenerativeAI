import streamlit as st
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rohit@123",
    database="trendytech"
)
cursor = conn.cursor()

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
            st.success("Logged in successfully!")
            faqs()  # Redirect to FAQs page after successful login
        else:
            st.error("Invalid username or password")

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

# Streamlit UI for FAQs page
def faqs():
    st.title("FAQs - Logistics")
    with open("logistics_faqs.txt", "r") as file:
        faqs_content = file.read()
    st.write(faqs_content)

# Main function to run the Streamlit app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Signup"])

    if page == "Login":
        login()
    elif page == "Signup":
        signup()

if __name__ == "__main__":
    main()

