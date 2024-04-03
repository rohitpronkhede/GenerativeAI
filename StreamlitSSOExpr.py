import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Define Google OAuth2.0 configuration
GOOGLE_CLIENT_ID = "XXXXX"
GOOGLE_CLIENT_SECRET = "XXXXX"
SCOPES = ['openid', 'email', 'profile']
REDIRECT_URI = 'http://localhost:8501'

CLIENT_SECRET_PATH = r'XXXXX'

def get_authorization_url():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_PATH,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return authorization_url

def main():
    st.title("Google SSO and Chat Interface with Streamlit")

    code = st.query_params.get('code')
    if code is None:
        # Google Sign-In button
        if st.button("Sign in with Google"):
            authorization_url = get_authorization_url()
            st.markdown(f"[Sign in with Google]({authorization_url})")
    else:
        # Handle redirection from Google after successful sign-in
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_PATH,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        st.success("You have successfully signed in with Google!")

        # Display user info
        st.subheader("User Information")
        st.write("Name:", credentials.id_token['name'])
        st.write("Email:", credentials.id_token['email'])

        # Chat interface
        st.subheader("Chat Interface")
        # Add your chat interface here

if __name__ == "__main__":
    main()
