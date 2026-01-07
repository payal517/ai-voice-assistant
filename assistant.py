import speech_recognition as sr
import json
import datetime
import os
import time
import threading
import win32com.client  # Windows TTS

# ================== Initialize Windows TTS ==================
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Volume = 100
speaker.Rate = 0

def speak(text):
    """Speak aloud and print text."""
    print("Assistant:", text)
    speaker.Speak(text)

# ================== File Setup ==================
DATA_FILE = "data.json"

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)

# ================== Reminder Functionality ==================
def set_reminder(reminder_text, delay):
    """Run reminder in a separate thread after delay (in seconds)."""
    def reminder():
        time.sleep(delay)
        speak(f"Reminder: {reminder_text}")
    
    t = threading.Thread(target=reminder, daemon=True)
    t.start()

# ================== Voice Input ==================
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        print("\n🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("🗣️ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error, please check your connection.")
        return ""

# ================== Data Management ==================
def add_item(items, text):
    text = text.strip()
    if not text:
        speak("Please say what to add.")
        return items
    new_item = {
        "item": text,
        "status": "pending",
        "time_added": str(datetime.datetime.now())
    }
    items.append(new_item)
    save_items(items)
    speak(f"Added '{text}'. You now have {len(items)} items total.")
    return items

def show_items(items):
    if not items:
        speak("No items found.")
        return
    speak(f"You have {len(items)} items.")
    for i, it in enumerate(items, start=1):
        print(f"{i}. {it['item']} - {it['status']} (Added: {it['time_added']})")

def mark_done(items, name):
    for it in items:
        if name in it["item"].lower():
            it["status"] = "done"
            save_items(items)
            speak(f"'{it['item']}' marked as done.")
            return items
    speak("Couldn't find that item.")
    return items

def delete_item(items, name):
    for it in items:
        if name in it["item"].lower():
            items.remove(it)
            save_items(items)
            speak(f"'{it['item']}' deleted. You now have {len(items)} items left.")
            return items
    speak("No matching item found.")
    return items

def clear_all():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        speak("All items have been cleared.")
    else:
        speak("No items to clear.")
    return []

def summary(items):
    total = len(items)
    done = len([it for it in items if it["status"] == "done"])
    pending = total - done
    speak(f"You have {total} items, {done} completed and {pending} pending.")

# ================== Command Execution ==================
def execute_command(command, items):
    """Return True to continue, False to exit."""
    speak(f"You said: {command}")
    
    if "add" in command:
        text = command.replace("add", "").strip()
        items = add_item(items, text)
    
    elif "show" in command:
        show_items(items)
    
    elif "mark done" in command or "complete" in command:
        name = command.replace("mark done", "").replace("complete", "").strip()
        items = mark_done(items, name)
    
    elif "delete" in command or "remove" in command:
        name = command.replace("delete", "").replace("remove", "").strip()
        items = delete_item(items, name)
    
    elif "clear all" in command:
        items = clear_all()
    
    elif "summary" in command or "status" in command:
        summary(items)
    
    elif "remind me" in command:
        try:
            parts = command.split(" in ")
            reminder_text = parts[0].replace("remind me to", "").strip()
            time_part = parts[1]
            delay = 0
            if "minute" in time_part:
                num = int(time_part.split("minute")[0].strip())
                delay = num * 60
            elif "second" in time_part:
                num = int(time_part.split("second")[0].strip())
                delay = num
            elif "hour" in time_part:
                num = int(time_part.split("hour")[0].strip())
                delay = num * 3600
            else:
                delay = 60
            
            speak(f"Reminder set for {reminder_text} in {time_part}.")
            set_reminder(reminder_text, delay)
        except Exception:
            speak("Sorry, I couldn't understand the reminder format. Please try again.")
    
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
    
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a nice day.")
        time.sleep(1.5)
        return False
    
    else:
        speak("Command not recognized. Please try again.")
    
    return True

# ================== Threaded Listening Loop ==================
def main():
    speak("Voice Assistant Started. Say a command anytime.")
    items = load_items()
    while True:
        command = listen()
        if command:
            # Running execution in a thread allows the system to remain responsive
            threading.Thread(target=execute_command, args=(command, items), daemon=True).start()

# ================== Run ==================
if __name__ == "__main__":
    main()