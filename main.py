# main.py

import streamlit as st
import asyncio # Kept for consistency if other async operations are added in the future
import pandas as pd
import datetime
import os
import logging
import sys # Make sure sys is imported for logging.StreamHandler

# Configure logging for the entire application (best practice)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout) # Log to console
                        # logging.FileHandler("app_log.log") # Optional: Log to a file
                    ])

# Import functions from respective modules (UPDATED IMPORTS)
from app.chatbot import doctor_chatbot_response, start_new_chat_session
from app.symptom_checker import symptom_checker_tab
from app.report_parser import report_parser_tab
from app.auth import add_user, verify_user, init_db # Import authentication functions

# Initialize the database on app startup
init_db()

# Set page config
st.set_page_config(page_title="AI Doctor Chatbot - M.Tech Project", layout="centered", initial_sidebar_state="auto")

# App title
st.title("🩺 AI Doctor Chatbot")
st.markdown(
    "This AI chatbot provides preliminary health information and analysis. "
    "*It is NOT a replacement for professional medical advice.*"
)

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# --- Login/Signup Section ---
if not st.session_state.logged_in:
    st.header("Welcome!")
    login_tab, signup_tab, about_tab_unauth = st.tabs(["Login", "Sign Up", "About & Disclaimers"])

    with login_tab:
        st.subheader("Login to your account")
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            login_button = st.form_submit_button("Login")

            if login_button:
                if verify_user(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(f"Welcome back, {login_username}!")
                    logging.info(f"User '{login_username}' logged in successfully.")
                    st.rerun() # Rerun to switch to the main app interface
                else:
                    st.error("Invalid username or password.")
                    logging.warning(f"Failed login attempt for username: {login_username}.")

    with signup_tab:
        st.subheader("Create a new account")
        with st.form("signup_form"):
            new_username = st.text_input("New Username", key="new_user")
            new_password = st.text_input("New Password", type="password", key="new_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
            signup_button = st.form_submit_button("Sign Up")

            if signup_button:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    result = add_user(new_username, new_password)
                    if result is True:
                        st.success("Account created successfully! You can now login.")
                        logging.info(f"New user '{new_username}' signed up successfully.")
                    elif result is False:
                        st.error("Username already exists. Please choose a different one.")
                    else: # result is None from an error
                        st.error("An error occurred during sign up. Please try again.")

    with about_tab_unauth:
        st.subheader("About AI Doctor Chatbot")
        st.markdown(
            """
            This AI Doctor Chatbot is designed to provide preliminary health information, symptom analysis,
            and basic lab report interpretations. **It is NOT a replacement for professional medical advice.**
            Always consult a qualified healthcare provider for any health concerns.

            **Features:**
            * **Chat with DocBot:** General health queries.
            * **Symptom Checker:** Suggests conditions based on symptoms.
            * **Report Analyzer:** Interprets lab results.

            **Disclaimer:** Please read the disclaimer section carefully.
            """
        )
        # --- DEVELOPER DETAILS ADDED HERE FOR UNAUTHENTICATED TAB ---
        st.markdown(
            """
            ---
            ### Meet the Developer

            **Uday Kiran Sangeesa** M.Tech Student, GITAM University

            ---

            **Connect with me:**
            * **GitHub:** [UdayKiran-dotcom](https://github.com/UdayKiran-dotcom)
            * **LinkedIn:** [Uday Kiran Sangeesa](https://www.linkedin.com/in/uday-kiran4/)
            """
        )
        # --- END DEVELOPER DETAILS ---
        st.subheader("Disclaimers")
        st.info(
            """
            * **NOT Medical Advice:** This application provides general health information and AI-generated insights. It is not intended to be, and should not be used as, medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for any health concerns or before making any decisions related to your health or treatment.
            * **No Doctor-Patient Relationship:** Use of this application does not create a doctor-patient relationship between you and the developers or the AI.
            * **Limitations of AI:** The AI models used rely on patterns and data they were trained on. They do not possess consciousness, empathy, or the ability to conduct physical examinations or consider your full, unique medical history, which are all essential for proper medical diagnosis and care. This tool's analysis is based on general knowledge and cannot account for individual variations, medical history, or other factors a human doctor would consider.
            * **Data Privacy:** This application processes the input you provide temporarily to generate responses. No personal health information (PHI) is stored or shared by this application on any external servers. When you save logs/reports, they are saved to your *local machine*. However, **you should always avoid entering any sensitive or personally identifiable medical information into any AI tool.**

            By using this application, you acknowledge and agree to these disclaimers.
            """
        )

# --- Main Application Section (after login) ---
else:
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        logging.info(f"User '{st.session_state.username}' logged out.")
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.chat_session = None # Clear chat session on logout
        st.rerun()

    app_tab, symptom_tab, report_tab, history_tab, about_tab = st.tabs([
        "🤖 Chat with DocBot", "🤒 Symptom Checker", "🔬 Lab Report Analyzer", "📜 Chat History", "ℹ️ About & Disclaimers"
    ])

    with app_tab:
        st.header("Chat with DocBot")
        st.markdown("Ask DocBot general health questions or get information.")

        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
            start_new_chat_session() # Start a new session when app loads for the first time
            logging.info("Chat history and new chat session initialized.")

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Ask DocBot..."):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("DocBot is thinking..."):
                # Get DocBot's response
                full_response = doctor_chatbot_response(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        st.markdown("---")
        if st.button("Start New Conversation"):
            start_new_chat_session()
            st.session_state.messages = [] # Clear chat history
            st.success("New conversation started! Chat history cleared.")
            logging.info("User started a new conversation.")
            st.rerun() # Rerun to update the UI immediately

        if st.button("Save Chat History"):
            if st.session_state.messages:
                # Ensure chat_logs directory exists
                log_dir = "chat_logs"
                os.makedirs(log_dir, exist_ok=True)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(log_dir, f"chat_log_{timestamp}.txt")
                
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"AI Doctor Chatbot - Chat Log\nDate: {timestamp.replace('_', ' ')}\n\n")
                        for msg in st.session_state.messages:
                            role_prefix = "🧑 You: " if msg["role"] == "user" else "🤖 DocBot: "
                            f.write(f"{role_prefix}{msg['content']}\n\n")
                        f.write("--- End of Chat Log ---")
                    st.success(f"Chat history saved to {filename}")
                    logging.info(f"Chat history saved to {filename}.")
                except Exception as e:
                    st.error(f"Failed to save chat history: {e}")
                    logging.exception(f"Failed to save chat history to {filename}: {e}")
            else:
                st.info("No chat history to save.")
                logging.info("Attempted to save empty chat history.")


    with symptom_tab:
        symptom_checker_tab() # Call the function from symptom_checker.py

    with report_tab:
        report_parser_tab() # Call the function from report_parser.py

    with history_tab:
        st.header("📜 Chat History Logs")
        st.markdown("You can find saved chat logs in the `chat_logs/` directory of your application.")
        
        log_dir = "chat_logs"
        if os.path.exists(log_dir) and os.path.isdir(log_dir):
            log_files = sorted([f for f in os.listdir(log_dir) if f.startswith("chat_log_") and f.endswith(".txt")], reverse=True)
            if log_files:
                selected_log = st.selectbox("Select a chat log to view:", log_files)
                if selected_log:
                    try:
                        with open(os.path.join(log_dir, selected_log), "r", encoding="utf-8") as f:
                            log_content = f.read()
                        st.text_area(f"Content of {selected_log}", log_content, height=400)
                        logging.info(f"Viewed chat log: {selected_log}")
                    except Exception as e:
                        st.error(f"Error reading log file: {e}")
                        logging.exception(f"Error reading chat log file {selected_log}: {e}")
            else:
                st.info("No saved chat logs found yet.")
                logging.info("No saved chat logs found.")
        else:
            st.info("The 'chat_logs' directory does not exist. No logs available.")
            logging.warning("chat_logs directory not found.")


    with about_tab:
        st.header("ℹ️ About AI Doctor Chatbot")
        st.markdown(
            """
            This AI Doctor Chatbot is an M.Tech project developed to provide preliminary health information,
            symptom analysis, and basic lab report interpretations using Google's Gemini AI models.
            It features a user-friendly web interface built with Streamlit and includes a basic authentication system.

            **Key Features:**
            * **Chat with DocBot:** A general health chatbot that can answer your queries and maintain conversation context, augmented with specific medical knowledge.
            * **Symptom Checker:** Input your symptoms to get possible conditions based on a curated medical knowledge base.
            * **Report Analyzer:** Paste your lab report text to get an overview of your results and identify potential anomalies based on standard ranges, with AI-driven explanations.
            * **User Authentication:** Basic sign-up and login functionality to manage user sessions (for demonstration purposes).

            **Technologies Used:**
            * **Streamlit:** For building the interactive web application.
            * **Google Gemini API:** Powering the conversational AI, symptom extraction, and report explanations.
            * **Python-Dotenv:** For secure loading of environment variables (like API keys).
            * **SQLite3:** For a simple, local user authentication database.
            * **Bcrypt:** For secure password hashing.
            * **Pandas:** For tabular data manipulation and display (e.g., in the report analyzer).
            """
        )
        # --- DEVELOPER DETAILS ADDED HERE FOR AUTHENTICATED TAB ---
        st.markdown(
            """
            ---
            ### Meet the Developer

            **Uday Kiran Sangeesa** M.Tech Student, GITAM University

            ---

            **Connect with me:**
            * **GitHub:** [UdayKiran-dotcom](https://github.com/UdayKiran-dotcom)
            * **LinkedIn:** [Uday Kiran Sangeesa](https://www.linkedin.com/in/uday-kiran4/)
            """
        )
        # --- END DEVELOPER DETAILS ---
        st.subheader("Disclaimers")
        st.info(
            """
            * **NOT Medical Advice:** This application provides general health information and AI-generated insights. It is not intended to be, and should not be used as, medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for any health concerns or before making any decisions related to your health or treatment.
            * **No Doctor-Patient Relationship:** Use of this application does not create a doctor-patient relationship between you and the developers or the AI.
            * **Limitations of AI:** The AI models used rely on patterns and data they were trained on. They do not possess consciousness, empathy, or the ability to conduct physical examinations or consider your full, unique medical history, which are all essential for proper medical diagnosis and care. This tool's analysis is based on general knowledge and cannot account for individual variations, medical history, or other factors a human doctor would consider.
            * **Data Privacy:** This application processes the input you provide temporarily to generate responses. No personal health information (PHI) is stored or shared by this application on any external servers. When you save logs/reports, they are saved to your *local machine*. However, **you should always avoid entering any sensitive or personally identifiable medical information into any AI tool.**

            By using this application, you acknowledge and agree to these disclaimers.
            """
        )


# Footer for the entire app - remains visible across all tabs
st.markdown(
    "<hr><small>⚠ This tool is for informational purposes only. "
    "Always consult a licensed doctor for any medical issues.</small>",
    unsafe_allow_html=True
)