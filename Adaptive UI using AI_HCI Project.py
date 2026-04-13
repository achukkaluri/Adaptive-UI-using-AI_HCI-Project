
"""Generating random questions based on difficulty levels and predicting the difficulty of the next question using a machine learning model trained on user 
performance data. Adapting the quiz in real-time by adjusting question difficulty according to previous answers and updating the score accordingly.
"""

# Importing necessary libraries for random number generation and machine learning
import random
from sklearn.naive_bayes import GaussianNB

# Defining a function to generate random questions based on difficulty levels
def generate_question(level):
    # Generating easy questions with addition
    if level == "easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
        return {"q": f"{a} + {b} = ?", "a": str(a + b)}
    
    # Generating medium questions with subtraction
    elif level == "medium":
        a, b = random.randint(5, 20), random.randint(1, 10)
        return {"q": f"{a} - {b} = ?", "a": str(a - b)}
    
    # Generating hard questions with multiplication
    elif level == "hard":
        a, b = random.randint(2, 12), random.randint(2, 12)
        return {"q": f"{a} * {b} = ?", "a": str(a * b)}

# Creating a dictionary to store questions for each difficulty level
questions = {
    "easy": [generate_question("easy") for _ in range(5)],  
    "medium": [generate_question("medium") for _ in range(5)],  
    "hard": [generate_question("hard") for _ in range(5)]  
}

# Preparing training data for the AI model to predict the difficulty level
X = [
    [0, 0], [0, 1], 
    [1, 0], [1, 1],  
    [2, 0], [2, 1], 
    [3, 0], [3, 1]   
]
y = ["easy", "easy", "medium", "medium", "medium", "hard", "hard", "hard"]  

# Training the Naive Bayes model to predict the difficulty level based on user performance
model = GaussianNB()
model.fit(X, y)

# Defining the function for the adaptive quiz
def adaptive_quiz():
    score = 0 
    last_result = 1 
    print("Welcome to the AI-Driven Adaptive Quiz\n")

    # Running 5 rounds of questions
    for i in range(5):
        # Predicting the difficulty level based on the user's score and last result
        difficulty = model.predict([[score, last_result]])[0]
        
        # Selecting a random question from the predicted difficulty level
        question = random.choice(questions[difficulty])
        
        # Asking the user the question
        answer = input(f"Q{i+1} ({difficulty.upper()}): {question['q']} ")

        # Checking the user's answer
        if answer.strip() == question["a"]:
            print("Correct!")
            score += 1  
            last_result = 1  
        else:
            print("Wrong!")
            last_result = 0  

    # Displaying the final score and message
    print(f"\nFinal Score: {score}/5")
    print("The quiz used AI to adapt question difficulty based on your performance.")

# Running the adaptive quiz if the script is executed directly
if __name__ == "__main__":
    adaptive_quiz()