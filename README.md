# ai-voice-assistant
🎙️ AI Voice Assistant using Python

An AI-based voice assistant developed in Python that allows users to interact with the system using voice commands.
The assistant can manage tasks, set reminders, and respond to basic queries like date and time using speech recognition and text-to-speech technology.

This project is created for academic and learning purposes.

📌 Features

Voice command input using microphone

Add, view, delete, and complete tasks

Set voice-based reminders

Text-to-Speech responses using Windows SAPI

Get current date and time

Persistent task storage using JSON

Multithreading for background reminders

🛠️ Technologies Used

Python

SpeechRecognition library

Windows SAPI (win32com) for Text-to-Speech

JSON for data storage

Multithreading

💻 System Requirements

Windows Operating System

Python 3.8 or higher

Working microphone

Internet connection

⚠️ This project works only on Windows due to the use of Windows SAPI.

📂 Project Structure
ai-voice-assistant/
│
├── assistant.py
├── requirements.txt
├── README.md
└── report/
    └── AI_Voice_Assistant_Report.pdf

⚙️ How to Run the Project

Download or clone the repository

Install required libraries:

pip install -r requirements.txt


Run the assistant:

python assistant.py

🎧 Example Voice Commands

“Add buy groceries.”

“Show items”

“Mark done groceries.”

“Delete groceries”

“Remind me to drink water in 5 minutes.”

“What is the time?”

“What is today’s date?”

“Summary”

“Exit”
