# DocBot: A Streamlit-Powered AI Medical Assistant

## Table of Contents

- [Abstract](#abstract)
- [1. Introduction](#1-introduction)
  - [1.1 AI’s Role in Modern Healthcare](#11-ais-role-in-modern-healthcare)
  - [1.2 Why Accessible Medical Information Matters](#12-why-accessible-medical-information-matters)
  - [1.3 What DocBot Aims to Achieve](#13-what-docbot-aims-to-achieve)
- [2. System Architecture](#2-system-architecture)
  - [2.1 Streamlit Interface](#21-streamlit-interface)
  - [2.2 Conversational AI Engine](#22-conversational-ai-engine)
  - [2.3 Medical Knowledge Base](#23-medical-knowledge-base)
  - [2.4 Security and User Management](#24-security-and-user-management)
- [3. Methodology](#3-methodology)
  - [3.1 Data Preparation and Processing](#31-data-preparation-and-processing)
  - [3.2 NLP with Gemini](#32-nlp-with-gemini)
  - [3.3 Lightweight Scoring Algorithm](#33-lightweight-scoring-algorithm)
  - [3.4 Knowledge Base Design](#34-knowledge-base-design)
- [4. Implementation](#4-implementation)
  - [4.1 Application Orchestration](#41-application-orchestration)
  - [4.2 AI Interaction Workflow](#42-ai-interaction-workflow)
  - [4.3 Report Parsing and Explanation](#43-report-parsing-and-explanation)
  - [4.4 Full Interaction Flow](#44-full-interaction-flow)
- [5. Key Functionalities](#5-key-functionalities)
  - [5.1 Symptom Checker](#51-symptom-checker)
  - [5.2 Conversational Medical Assistance](#52-conversational-medical-assistance)
  - [5.3 Report Analysis](#53-report-analysis)
  - [5.4 Informational Recommendations](#54-informational-recommendations)
- [6. Evaluation](#6-evaluation)
  - [6.1 Information Accuracy](#61-information-accuracy)
  - [6.2 User Engagement](#62-user-engagement)
  - [6.3 System Performance](#63-system-performance)
  - [6.4 Comparison to Other Tools](#64-comparison-to-other-tools)
- [7. Ethical and Practical Considerations](#7-ethical-and-practical-considerations)
  - [7.1 Data Privacy](#71-data-privacy)
  - [7.2 Transparent AI](#72-transparent-ai)
  - [7.3 Limitations](#73-limitations)
- [8. Future Enhancements](#8-future-enhancements)
  - [8.1 EHR Integration](#81-ehr-integration)
  - [8.2 Multilingual Support](#82-multilingual-support)
  - [8.3 Telemedicine Features](#83-telemedicine-features)
- [9. Conclusion](#9-conclusion)
  - [9.1 Summary](#91-summary)
  - [9.2 Impact on Accessibility](#92-impact-on-accessibility)
  - [9.3 Future Research](#93-future-research)

## Abstract
DocBot is an AI-driven medical assistant built with Streamlit and powered by Google’s Gemini API. It’s designed to make health information accessible to everyone, offering a secure, friendly, and intuitive platform for understanding symptoms, lab reports, and medical questions. With a sleek interface featuring a chatbot, symptom checker, and lab report parser, DocBot combines conversational AI with a structured medical knowledge base to deliver clear, reliable insights. This paper explores how DocBot works, its potential to improve healthcare access—especially in underserved communities—and the ethical considerations that guide its development.

## 1. Introduction

### 1.1 AI’s Role in Modern Healthcare
Artificial Intelligence is reshaping healthcare, helping doctors diagnose conditions, personalizing treatments, and empowering patients with tools to better understand their health. Large Language Models (LLMs) like Google’s Gemini are particularly exciting because they can hold natural, meaningful conversations about complex topics. This makes them perfect for creating tools that feel human and approachable, even when diving into medical details.

### 1.2 Why Accessible Medical Information Matters
Not everyone has easy access to reliable medical advice, especially in rural areas or underserved communities. Many people struggle to make sense of symptoms or lab results without a doctor’s help. AI tools like DocBot can change that by providing clear, personalized health insights, helping users feel more confident about their care and encouraging informed decisions.

### 1.3 What DocBot Aims to Achieve
DocBot was created with a few key goals:
- Deliver accurate, easy-to-understand health information through a conversational AI.
- Provide tools to analyze symptoms and lab reports using a trusted medical knowledge base.
- Build a secure, user-friendly platform that respects privacy and feels intuitive for all users.

## 2. System Architecture

### 2.1 Streamlit Interface
DocBot is built on Streamlit, a platform that lets us create clean, interactive apps quickly. The interface is divided into three tabs—Chatbot, Symptom Checker, and Lab Report Parser—each designed for a specific task but tied together in a seamless, user-friendly experience.

### 2.2 Conversational AI Engine
The chatbot runs on Google’s Gemini (gemini-2.0-flash), which processes user questions by first checking if they’re medical-related. If they are, it pulls in relevant details from our knowledge base before crafting a response. This logic, coded in `app/chatbot.py`, ensures answers are accurate and tailored to the user’s needs.

### 2.3 Medical Knowledge Base
DocBot draws on two structured datasets:
- **Symptom-Disease Mapping**: A dictionary (MEDICAL_KNOWLEDGE_BASE) that links symptoms to possible conditions.
- **Lab Test Reference Ranges**: A dataset (NORMAL_RANGES) with standard values for lab tests, used to interpret results.
These are stored as Python dictionaries, making them transparent and easy to update as new information becomes available.

### 2.4 Security and User Management
Privacy is a top priority for DocBot. We use:
- SQLite with bcrypt for secure password storage (`app/auth.py`).
- Local-only data handling to keep sensitive information off external servers.
- Secure chat history storage in a local directory, so users can revisit past conversations safely.

## 3. Methodology

### 3.1 Data Preparation and Processing
DocBot relies on carefully curated datasets for medical conditions and lab values. User input is cleaned up using regular expressions and keyword matching to structure it for comparison with these datasets, ensuring we’re working with accurate and relevant information.

### 3.2 NLP with Gemini
Gemini powers DocBot’s natural language processing, handling tasks like:
- Extracting symptoms from free-form text (via `extract_symptoms`).
- Determining if a question is medical-related (`_is_medical_query`).
- Generating clear, context-aware responses using carefully designed prompts to keep answers accurate and helpful.

### 3.3 Lightweight Scoring Algorithm
For the symptom checker, DocBot calculates a match score by comparing user-reported symptoms to conditions in the knowledge base (`suggest_conditions`). This simple but effective approach ranks possible conditions based on how closely they align with the input.

### 3.4 Knowledge Base Design
The knowledge bases are coded directly in Python for clarity and ease of maintenance. This setup makes updates straightforward and allows for future scalability, like transitioning to a dynamic database (e.g., PostgreSQL) if needed.

## 4. Implementation

### 4.1 Application Orchestration
The main app (`main.py`) ties everything together, handling:
- User authentication through `auth.py`.
- Interface rendering with Streamlit’s `st.tabs`.
- State management using `st.session_state` to keep interactions smooth and consistent.

### 4.2 AI Interaction Workflow
In `chatbot.py`, Gemini is initialized once and processes user input by:
- Classifying the question and pulling in relevant knowledge base data.
- Generating a conversational response displayed in a friendly, chat-like format.

### 4.3 Report Parsing and Explanation
Lab reports are processed by:
1. Using regex to extract test names, values, and units from user input.
2. Comparing results to `NORMAL_RANGES`.
3. Displaying anomalies in a clear `st.dataframe`.
4. Generating a plain-language explanation via Gemini (`get_gemini_explanation`) to help users understand their results.

### 4.4 Full Interaction Flow
Here’s how it works:
1. Users log in or sign up.
2. They navigate to the Chatbot, Symptom Checker, or Report Parser tab.
3. They input data and get real-time feedback powered by Gemini and the knowledge base.
4. Every response includes a disclaimer reminding users that DocBot is for informational purposes only.

## 5. Key Functionalities

### 5.1 Symptom Checker
Users describe their symptoms, and Gemini extracts key details to match against conditions in the knowledge base. Possible conditions are ranked by how closely they match, giving users a starting point for further exploration.

### 5.2 Conversational Medical Assistance
The chatbot filters for medical questions and uses Gemini to provide clear, context-aware answers. It draws on session history and embedded prompts to keep conversations relevant and helpful.

### 5.3 Report Analysis
Lab reports are broken down into a table, with anomalies highlighted. Gemini explains any unusual results in simple terms, making complex medical data easier to grasp for non-experts.

### 5.4 Informational Recommendations
DocBot offers practical health insights—like explaining what high cholesterol might mean and suggesting next steps—without crossing into prescriptive advice. All recommendations are clearly labeled as informational.

## 6. Evaluation

### 6.1 Information Accuracy
DocBot’s reliability hinges on Gemini’s performance and the quality of our knowledge bases. We’ve validated the system with unit tests (`test_report_parser.py`, `test_auth.py`) to ensure outputs are consistent and accurate.

### 6.2 User Engagement
Early feedback has been encouraging, with users praising:
- The intuitive multi-tab interface.
- The clarity of lab result visualizations.
- The educational value of AI-generated explanations.

### 6.3 System Performance
Thanks to Gemini’s fast processing and Streamlit’s efficient rendering, DocBot delivers quick responses, making it practical for real-time use.

### 6.4 Comparison to Other Tools
Unlike basic symptom checkers or standalone chatbots, DocBot’s integrated approach—combining symptom analysis, report parsing, and conversational AI—offers a more comprehensive and user-friendly experience.

## 7. Ethical and Practical Considerations

### 7.1 Data Privacy
- All data stays local, minimizing the risk of exposure.
- Authentication is secure, using bcrypt and SQLite for transparency and safety.

### 7.2 Transparent AI
Every AI response comes with a disclaimer, and users can inspect the knowledge base in the source code. We want users to trust and understand how DocBot works.

### 7.3 Limitations
- **Not a Doctor**: DocBot is for education, not diagnosis.
- **Static Knowledge**: The knowledge base may not cover rare or newly discovered conditions.
- **Potential Bias**: Like any AI, DocBot could inherit biases from its training data or knowledge sources.

## 8. Future Enhancements

### 8.1 EHR Integration
Connecting DocBot to electronic health records via secure APIs (like HL7 FHIR) could personalize insights and reduce manual data entry.

### 8.2 Multilingual Support
Leveraging Gemini’s language capabilities, we could expand DocBot to support non-English users, making it even more accessible globally.

### 8.3 Telemedicine Features
Future updates might include:
- Live chats with doctors.
- Appointment scheduling tools.
- Non-prescriptive medication information.

## 9. Conclusion

### 9.1 Summary
DocBot shows how combining conversational AI, a curated knowledge base, and an interactive interface can create a powerful tool for health education. Its modular design supports symptom analysis, lab report interpretation, and general medical inquiries, all in one place.

### 9.2 Impact on Accessibility
By delivering reliable, user-friendly medical information, DocBot helps bridge the gap for people who lack easy access to healthcare professionals, empowering them to take charge of their health.

### 9.3 Future Research
Next steps include:
- Validating DocBot with real-world, anonymized medical data.
- Studying user behavior to better meet their needs.
- Expanding the knowledge base for broader coverage.
- Exploring Retrieval-Augmented Generation (RAG) to provide dynamic, evidence-backed responses.