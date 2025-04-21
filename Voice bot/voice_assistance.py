import speech_recognition as sr
import pyttsx3
import re
import random as ra
import os
import winsound

Recognizeer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def Email(email):
    regex = r"^\S+@\S+\.\S+$"
    return re.match(regex, email) is not None

def ID():
    return f"ID{ra.randint(1000, 9999)}"

def Voice(prompt, retry=3):
    for a in range(retry):
        speak(prompt)
        winsound.Beep(1000, 500)  # Play a beep before listening
        with sr.Microphone() as source:
            print("Listening......")
            audio = Recognizeer.listen(source)
        try:
            text = Recognizeer.recognize_google(audio)
            print(f"You Said {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("System Down")
            return None
    speak("You Have Attempted Many Times Today")
    return None

def valid_email():
    for i in range(3):
        email = Voice("Please say your email, for example john at gmail dot com")
        if email:
            email = (
                email.replace(" period ", ".")
                     .replace(" com ", ".com")
                     .replace(" at ", "@")
                     .replace(" dot ", ".")
                     .replace(" underscore ", "_")
                     .replace(" dash ", "-")
                     .replace(" ", "")
            ).strip().lower()
            if Email(email):
                return email
            else:
                speak("Invalid Email")
    return None

def valid_role():
    for i in range(3):
        role = Voice("Are you registering as a student or teacher?")
        if role:
            if "student" in role:
                return "student"
            elif "teacher" in role:
                return "teacher"
            else:
                speak("Please say either student or teacher.")
    speak("Failed to recognize your role.")
    return None

def confirm_input(input_type, user_input):
    confirm = Voice(f"Did you say your {input_type} is {user_input}?")
    if not confirm or "yes" not in confirm:
        speak("Let's try again.")
        return False
    return True

def Registor():
    speak("Hi, I Am James, Your Registration Assistant")

    name = Voice("What is your name?")
    if not name:
        return
    if not confirm_input("name", name):
        return

    age = Voice("What is your age?")
    if not age:
        return
    if not confirm_input("age", age):
        return

    New_email = valid_email()
    if not New_email:
        speak("Registration failed due to invalid email")
        return
    if not confirm_input("email", New_email):
        return

    role = valid_role()
    if not role:
        speak("Registration failed due to invalid role")
        return
    if not confirm_input("role", role):
        return

    unique_id = ID()

    if role == "student":
        course = Voice("Which course do you want to join?")
        if not course:
            return
        if not confirm_input("course", course):
            return

        # Save to Student.txt
        if not os.path.exists("Student.txt"):
            with open("Student.txt", "w") as f:
                f.write("Id,Name,Age,Email,Course\n")
        with open("Student.txt", "a") as f:
            f.write(f"{unique_id},{name},{age},{New_email},{course}\n")

    else:  # teacher
        course = Voice("Which subject do you want to teach?")
        if not course:
            return
        if not confirm_input("subject", course):
            return

        # Save to Teacher.txt
        if not os.path.exists("Teacher.txt"):
            with open("Teacher.txt", "w") as f:
                f.write("Id,Name,Age,Email,Subject\n")
        with open("Teacher.txt", "a") as f:
            f.write(f"{unique_id},{name},{age},{New_email},{course}\n")

    # Final Registration Summary
    speak("Registration Completed Successfully. Here are your details.")
    print(f"\n--- Registration Summary ---")
    print(f"ID      : {unique_id}")
    print(f"Name    : {name.title()}")
    print(f"Age     : {age}")
    print(f"Email   : {New_email}")
    print(f"Role    : {role}")
    print(f"{'Course' if role == 'student' else 'Subject'}: {course}")
    print(f"------------------------------")

def main():
    speak("Welcome, Let's start the registration")
    Registor()

if __name__ == "__main__":
    main()
