# 🩺 AI Doctor Chatbot

This AI Doctor Chatbot is an M.Tech project developed to provide preliminary health information, symptom analysis, and basic lab report interpretations leveraging Google's Gemini AI models. It features a user-friendly web interface built with Streamlit and includes a basic user authentication system.

-----

## ✨ Key Features

  * **Chat with DocBot:** An intelligent chatbot primarily focused on medical and health-related queries. It maintains conversation context and augments responses with specific medical knowledge, refusing to answer non-medical questions.
  * **Symptom Checker:** Input your symptoms to receive suggestions for possible medical conditions based on a curated medical knowledge base.
  * **Lab Report Analyzer:** Paste raw text from your lab reports to get an overview of the results, identify anomalies compared to normal ranges, and receive AI-driven explanations.
  * **User Authentication:** A basic sign-up and login system to manage user sessions, demonstrating protected access to the main application features.
  * **Chat History Management:** Ability to start new conversations and save current chat sessions locally for later review.

## ⚙️ Technologies Used and Their Application Areas

| Technology             | Application Area                                                                                                                              |
| :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Streamlit** | Building the interactive and responsive web application user interface.                                                                       |
| **Google Gemini API** | Powers the core AI functionalities: general conversational AI (`chatbot.py`), symptom extraction (`symptom_checker.py`), and report explanations (`report_parser.py`). |
| **`python-dotenv`** | Securely loading environment variables (specifically your `GEMINI_API_KEY`) from a `.env` file, preventing hardcoding sensitive information. |
| **`re` module (Regex)**| Used extensively in `report_parser.py` for efficient and robust text parsing of lab test values from unstructured reports.                     |
| **`sqlite3`** | Local database management in `auth.py` for storing user signup and login details (usernames and hashed passwords).                            |
| **`bcrypt`** | Crucial for security in `auth.py`, used for robust password hashing to protect user credentials stored in the `users.db`.                     |
| **`pandas`** | Utilized in `report_parser.py` for structuring and displaying parsed lab report data in a clear, tabular format (DataFrame) within Streamlit. |

## 📁 Project Structure

```
ai_doctor_chatbot/
├── .env                       # Stores your GEMINI_API_KEY (create this file)
├── main.py                    # Main application entry point, handles UI, navigation, and integrates modules
├── requirements.txt           # Lists all Python dependencies
├── users.db                   # SQLite database for user authentication (created on first run)
├── chat_logs/                 # Directory to store saved chat history text files
├── app/                       # Python package for core application logic
│   ├── __init__.py            # Makes 'app' a Python package (empty file)
│   ├── auth.py                # Handles user registration and login (SQLite & bcrypt)
│   ├── chatbot.py             # DocBot's core logic: Gemini interaction, knowledge augmentation, medical query classification
│   ├── report_parser.py       # Parses lab reports, analyzes values, and generates AI explanations
│   └── symptom_checker.py     # Extracts symptoms and suggests conditions
└── README.md                  # This file!
```

## 🚀 Setup and Installation

Follow these steps to get the AI Doctor Chatbot running on your local machine:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-github-username/ai-doctor-chatbot.git # Replace with your actual repo URL if public
    cd ai_doctor_chatbot
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

      * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Google Gemini API Key:**

      * Obtain a Gemini API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).
      * Create a file named `.env` in the root directory of your `ai_doctor_chatbot` project (next to `main.py`).
      * Add your API key to this file in the following format:
        ```
        GEMINI_API_KEY='your_gemini_api_key_here'
        ```
        **Make sure there are no spaces around the `=` sign and the key is enclosed in single quotes.**

## ▶️ How to Run the App

Once you've completed the setup:

1.  **Ensure your virtual environment is active.**
2.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```
    Your default web browser should automatically open the application. If not, open your browser and navigate to `http://localhost:8501`.

## 🖥️ Usage

1.  **Login/Sign Up:**
      * If you're a new user, navigate to the "Sign Up" tab to create an account.
      * Existing users can log in using their credentials on the "Login" tab.
2.  **Navigate Tabs:** After logging in, explore the different functionalities using the tabs:
      * **Chat with DocBot:** Ask medical questions. Try asking a non-medical question to see the new medical-only filtering in action\!
      * **Symptom Checker:** Enter your symptoms for a possible diagnosis.
      * **Lab Report Analyzer:** Paste text from a lab report for analysis and explanation.
      * **Chat History:** View your previously saved conversations.
      * **About & Disclaimers:** Read important information about the app and its limitations.

-----

## ⚠️ Disclaimers & Important Information

  * **NOT Medical Advice:** This application provides general health information and AI-generated insights. It is **not intended to be, and should not be used as, medical advice, diagnosis, or treatment.** Always consult with a qualified healthcare provider for any health concerns or before making any decisions related to your health or treatment.
  * **No Doctor-Patient Relationship:** Use of this application does not create a doctor-patient relationship between you and the developers or the AI.
  * **Limitations of AI:** The AI models used rely on patterns and data they were trained on. They do not possess consciousness, empathy, or the ability to conduct physical examinations or consider your full, unique medical history, which are all essential for proper medical diagnosis and care. This tool's analysis is based on general knowledge and cannot account for individual variations, medical history, or other factors a human doctor would consider.
  * **Data Privacy:** This application processes the input you provide temporarily to generate responses. **No personal health information (PHI) is stored or shared by this application on any external servers.** When you save chat logs or process lab reports, this data is saved to your *local machine* (e.g., `users.db` for login, `chat_logs/` for chat history). However, **you should always avoid entering any sensitive or personally identifiable medical information into any AI tool.** The implemented login system is simplified and is **NOT designed for production environments or for handling sensitive user data without significant security hardening.**

By using this application, you acknowledge and agree to these disclaimers.

-----

## 👨‍💻 Meet the Developer

**Uday Kiran Sangeesa** M.Tech Student, GITAM University

-----

**Connect with me:**

  * **GitHub:** [UdayKiran-dotcom](https://github.com/UdayKiran-dotcom)
  * **LinkedIn:** [Uday Kiran Sangeesa](https://www.linkedin.com/in/uday-kiran4/)

-----