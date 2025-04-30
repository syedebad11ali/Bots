import speech_recognition as sr
import pyttsx3
import random as ra 
import time as t

engine=pyttsx3.init()

def speak(text):
    print(f"James Johns: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient voice")
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print("Listening....")
        audio=recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You Said {command}")
            return command.lower()
        except sr.UnknownValueError :
            speak("I didn't catch that, please try again.")
            return listen()
        except sr.RequestError:
            speak("Speach srevice error. Try agian later")
            return None
class Game:
    def start(self):
        raise NotImplementedError("Start must be implemented by subclasses.")

class RockPaperScissor(Game):
    def start(self):
        print("Rock, Paper, Scissors Game Started!")
        option=["rock","paper","scissor"]
        while True:
            speak("Chosee rock,paper,scissor.Say stop to exit")
            user_voice=listen()
            if user_voice.lower() == None:
                continue
            if "stop" in user_voice.lower():
                break
            if user_voice.lower() not in option:
                speak("Invalid Choice, try again")
            ai_voice=ra.choice(option)
            speak(f"I choice {ai_voice}")
            if user_voice.lower() == ai_voice.lower():
                speak("It's a Draw")
            elif (user_voice.lower() == "paper" and ai_voice.lower() == "scissor") or (user_voice.lower() == "scissor" and ai_voice.lower() == "rock") or(user_voice.lower() == "rock" and ai_voice.lower() == "paper"):
                speak("You lose!")
            else:
                speak("Congrats, You won!")

    
class Game:
    def start(self):
        raise NotImplementedError("Subclasses must implement the start method.")

class TicTacToeGame(Game):
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def print_board(self):
        print("\n")
        for row in self.board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def start(self):
        while True:
            self.print_board()
            print(f"Player {self.current_player}'s turn")

            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
            except ValueError:
                print("Please enter valid numbers.")
                continue

            if 0 <= row <= 2 and 0 <= col <= 2:
                if self.board[row][col] == " ":
                    self.board[row][col] = self.current_player
                    if self.check_winner(self.current_player):
                        self.print_board()
                        print(f"Player {self.current_player} wins!")
                        break
                    elif self.is_draw():
                        self.print_board()
                        print("It's a draw!")
                        break
                    self.current_player = "O" if self.current_player == "X" else "X"
                else:
                    print("Cell already taken. Try again.")
            else:
                print("Invalid move. Try again.")

class Numbergame(Game):
    def word_to_num(self, word):
        mapping = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "twentyone": 21, "twentytwo": 22, "twentythree": 23, "twentyfour": 24, "twentyfive": 25
        }
        return mapping.get(word.lower().replace(" ", ""), None)

    def start(self):
        speak("Welcome To Number Guessing Game")
        Number= ra.randint(1,25)
        speak("I've picked an number from 1 to 25 try to guess it ")
        attempt=5
        while attempt >0:
            speak(f"You Have {attempt} attempt left")
            guess=listen()
            if guess == None:
                continue
            try:
                if guess.isdigit():
                    guess=int(guess)
                else:
                    guess= self.word_to_num(guess)
                if guess is None or not (1 <= guess <= 25):
                    speak("Say a number between 1 and 25")
                    continue
                if guess == Number :
                    speak(f"You guessed coreectly the number was {Number}")
                    return
                elif guess<Number:
                    speak("Too low")
                else:
                    speak("Too high")
                    attempt -= 1
            except :
                speak("Say a  valid number")
        speak(f"Out of attempt! The number was {Number}")
class Gamestore:
    def __init__(self):
        self.Game={
            "rock":RockPaperScissor(),
            "tic tac toe": TicTacToeGame(),
            "tic-tac-toe": TicTacToeGame(),
            "number":Numbergame()
        }
    def run(self):
        speak("Hi, I am James Johns in short JJ! Welcome to the voice game store ")
        while True:
            speak("Speak Rock, Tic Tac Toe,Number to play. say exit to stop")
            command =listen()
            if command == None:
                continue
            if "stop" in command.lower():
                speak("Have a Nice day")
                break
            # if command.lower() in self.Game:
            #     speak(f"Starting {command}...")
            #     self.Game[command.lower()].start()  # Start the chosen game
            for key in self.Game:
                self.Game[key].start()
                return
            else:

                speak("Game isn't available at the moment try again later")
                # speak("Sorry, I didn't catch that. Please try again.")
if __name__ =="__main__":
    Gamestore().run()
