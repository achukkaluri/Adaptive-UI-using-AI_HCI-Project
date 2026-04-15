
"""Generating random questions based on difficulty and using a trained model to predict difficulty level, updating the score with
user feedback. Displaying questions, checking answers, and automatically transitioning to the next question,
ending after five rounds with the final score displayed."""

import random
import tkinter as tk
from tkinter import messagebox
from sklearn.naive_bayes import GaussianNB

# Defining a function for generating random questions based on difficulty levels
def generate_question(level):
    if level == "easy":
        # Generating easy questions with addition
        a, b = random.randint(1, 10), random.randint(1, 10)
        return {"q": f"{a} + {b} = ?", "a": str(a + b), "level": "easy"}
    elif level == "medium":
        # Generating medium questions with subtraction
        a, b = random.randint(5, 20), random.randint(1, 10)
        return {"q": f"{a} - {b} = ?", "a": str(a - b), "level": "medium"}
    elif level == "hard":
        # Generating hard questions with multiplication
        a, b = random.randint(2, 12), random.randint(2, 12)
        return {"q": f"{a} * {b} = ?", "a": str(a * b), "level": "hard"}

# Creating predefined questions for each difficulty level
questions = {
    "easy": [generate_question("easy") for _ in range(5)],
    "medium": [generate_question("medium") for _ in range(5)],
    "hard": [generate_question("hard") for _ in range(5)],
}

# Preparing training data for the AI model to predict difficulty level based on performance
X = [
    [0, 0], [0, 1],
    [1, 0], [1, 1],
    [2, 0], [2, 1],
    [3, 0], [3, 1]
]
y = ["easy", "easy", "medium", "medium", "medium", "hard", "hard", "hard"]

# Training the Naive Bayes model to predict the difficulty level
model = GaussianNB()
model.fit(X, y)

# Defining the main application class for the adaptive quiz
class AdaptiveQuizApp:
    def __init__(self, root):
        # Initializing the window and setting up initial variables
        self.root = root
        self.root.title("AI-Driven Adaptive Quiz")
        self.score = 0
        self.last_result = 1
        self.rounds = 0
        self.current_question = None

        # Creating and displaying the welcome label
        self.question_label = tk.Label(root, text="Welcome to the AI-Driven Adaptive Quiz", font=("Arial", 16))
        self.question_label.pack(pady=20)

        # Creating the answer entry box
        self.answer_entry = tk.Entry(root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        # Creating the submit button for answering questions
        self.submit_button = tk.Button(root, text="Submit Answer", font=("Arial", 14), command=self.check_answer)
        self.submit_button.pack(pady=20)

        # Creating and displaying the score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Starting the quiz by showing the first question
        self.next_question()

    def next_question(self):
        # Stopping the quiz after 5 rounds
        if self.rounds >= 5:
            self.end_quiz()
            return

        # Predicting the difficulty of the next question based on previous performance
        difficulty = model.predict([[self.score, self.last_result]])[0]

        # Selecting a random question from the predicted difficulty level
        self.current_question = random.choice(questions[difficulty])

        # Displaying the question and difficulty level
        self.question_label.config(text=f"Q: {self.current_question['q']} (Level: {self.current_question['level'].capitalize()})")

        # Enabling the submit button for the next question
        self.submit_button.config(state=tk.NORMAL)

    def check_answer(self):
        # Getting the user's answer
        user_answer = self.answer_entry.get().strip()

        # Checking if the user's answer is correct
        if user_answer == self.current_question["a"]:
            # Displaying a message for a correct answer
            messagebox.showinfo("Correct!", "Your answer is correct!")
            self.score += 1
            self.last_result = 1
        else:
            # Displaying a message for an incorrect answer
            messagebox.showerror("Incorrect!", "Your answer is wrong!")
            self.last_result = 0

        # Updating the score and disabling the submit button
        self.score_label.config(text=f"Score: {self.score}")
        self.submit_button.config(state=tk.DISABLED)

        # Clearing the answer entry for the next question
        self.answer_entry.delete(0, tk.END)

        # Moving to the next question after a short delay
        self.rounds += 1
        self.root.after(1000, self.next_question)

    def end_quiz(self):
        # Disabling further interaction and showing the final score
        messagebox.showinfo("Quiz Ended", f"Quiz Ended! Your final score is: {self.score}/5")

        # Closing the window automatically after the user clicks OK
        self.root.quit()

# Creating the main window and running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdaptiveQuizApp(root)
    root.mainloop()
