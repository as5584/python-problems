import random
import tkinter as tk
from tkinter import messagebox
import os

# Questions
questions = [
    {"question": "1. What is the correct file extension for Python files?", 
     "options": [".py", ".pt", ".pyt", ".p"], "answer": ".py"},
    {"question": "2. How do you create a variable with the numeric value 5?", 
     "options": ["x = int(5)", "x = 5", "int x = 5", "x <- 5"], "answer": "x = 5"},
    {"question": "3. Which of the following is a correct syntax to output 'Hello World' in Python?", 
     "options": ["echo 'Hello World'", "print('Hello World')", "p('Hello World')", "printf('Hello World')"], 
     "answer": "print('Hello World')"},
    {"question": "4. What is the correct way to create a function in Python?", 
     "options": ["function myFunction():", "create myFunction():", "def myFunction():", "myFunction():"], 
     "answer": "def myFunction():"},
    {"question": "5. Which method can be used to remove any whitespace from both the beginning and the end of a string?", 
     "options": ["strip()", "trim()", "stripped()", "len()"], "answer": "strip()"},
    {"question": "6. Which of the following statements is used to create an empty set?", 
     "options": ["set = {}", "set = []", "set = set()", "set = ()"], "answer": "set = set()"},
    {"question": "7. Which operator is used to multiply numbers in Python?", 
     "options": ["%", "*", "#", "&"], "answer": "*"},
    {"question": "8. How do you insert COMMENTS in Python code?", 
     "options": ["/* This is a comment */", "// This is a comment", "# This is a comment", "-- This is a comment"], 
     "answer": "# This is a comment"},
    {"question": "9. What is the correct way to write a list in Python?", 
     "options": ["{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)", "<1, 2, 3>"], "answer": "[1, 2, 3]"},
    {"question": "10. What is a correct syntax to return the first character in a string?", 
     "options": ["x = sub('Hello', 0, 1)", "x = 'Hello'.sub(0, 1)", "x = 'Hello'[0]", 
                 "x = substring('Hello', 0, 1)"], "answer": "x = 'Hello'[0]"}
]

score = 0
current_question_index = 0
timer_id = None
time_left = 30  # seconds per question

def shuffle_questions(qs):
    random.shuffle(qs)

def start_timer():
    global timer_id, time_left
    cancel_timer()  # Clear any previous timer
    
    time_left = 30
    update_timer_display()

def update_timer_display():
    global timer_id, time_left
    
    if time_left > 0:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"⏱ Time Left: {time_left} seconds")
        time_left -= 1
        timer_id = root.after(1000, update_timer_display)
    else:
        timer_label.config(text="⏰ Time's up!")
        mark_question_failed()

def cancel_timer():
    global timer_id
    if timer_id is not None:
        try:
            root.after_cancel(timer_id)
        except:
            pass
        timer_id = None

def submit():
    global current_question_index, score
    cancel_timer()
    
    selected = var.get()
    if not selected:
        messagebox.showwarning("Selection Required", "Please choose an option!")
        start_timer()  # Restart timer if no selection
        return

    correct = questions[current_question_index]['answer']
    
    if selected == correct:
        score += 1
        feedback_label.config(text="✅ Correct! Well done.", fg="green")
    else:
        feedback_label.config(text=f"❌ Wrong. Correct answer: {correct}", fg="red")

    current_question_index += 1
    if current_question_index < len(questions):
        root.after(1500, next_question)  # Small delay for user to see feedback
    else:
        root.after(1500, show_final_score)

def mark_question_failed():
    global current_question_index
    cancel_timer()
    correct = questions[current_question_index]['answer']
    feedback_label.config(text=f"⏰ Time's up! Correct answer: {correct}", fg="red")
    
    current_question_index += 1
    if current_question_index < len(questions):
        root.after(2000, next_question)
    else:
        root.after(2000, show_final_score)

def next_question():
    global current_question_index
    cancel_timer()
    
    var.set("")
    feedback_label.config(text="")
    
    if current_question_index < len(questions):
        q = questions[current_question_index]
        question_label.config(text=q['question'])
        
        for i, option in enumerate(q['options']):
            option_buttons[i].config(text=option, value=option)
        
        start_timer()          # Start fresh timer for new question
    else:
        show_final_score()

def show_final_score():
    cancel_timer()
    for widget in [question_label, *option_buttons, submit_button, timer_label]:
        try:
            widget.pack_forget()
        except:
            pass
    
    percentage = (score / len(questions)) * 100
    feedback_label.config(text=f"Quiz Completed!\nYour Score: {score}/{len(questions)} ({percentage:.1f}%)", 
                         fg="blue", font=("Arial", 12, "bold"))
    
    messagebox.showinfo("Quiz Finished", f"Final Score: {score}/{len(questions)} ({percentage:.1f}%)")
    update_high_score(score)

def update_high_score(current_score):
    high_score = 0
    try:
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as f:
                high_score = int(f.read().strip())
    except:
        pass

    if current_score > high_score:
        with open("high_score.txt", "w") as f:
            f.write(str(current_score))
        messagebox.showinfo("🎉 New High Score!", f"Congratulations! New High Score: {current_score}/{len(questions)}")
    else:
        messagebox.showinfo("Score", f"Your Score: {current_score}/{len(questions)}\nHigh Score: {high_score}/{len(questions)}")

# ====================== GUI Setup ======================
root = tk.Tk()
root.title("Python Quiz")
root.geometry("650x550")
root.resizable(False, False)

question_label = tk.Label(root, text="", font=("Arial", 13, "bold"), wraplength=600, justify="left")
question_label.pack(pady=20)

var = tk.StringVar()
option_buttons = []
for _ in range(4):
    rb = tk.Radiobutton(root, text="", variable=var, value="", font=("Arial", 11), anchor="w", padx=10)
    rb.pack(anchor=tk.W, padx=40, pady=6)
    option_buttons.append(rb)

submit_button = tk.Button(root, text="Submit Answer", command=submit, font=("Arial", 12), bg="#4CAF50", fg="white", height=2, width=20)
submit_button.pack(pady=25)

feedback_label = tk.Label(root, text="", font=("Arial", 11), wraplength=600)
feedback_label.pack(pady=10)

timer_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="#d32f2f")
timer_label.pack(pady=10)

# Start the quiz
messagebox.showinfo("Welcome", "Welcome to Python Quiz!\n30 seconds per question.\nGood Luck!")
shuffle_questions(questions)
next_question()

root.mainloop()