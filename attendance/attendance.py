import csv
import os
from datetime import datetime
DATA_FILE = "attendance_data.csv"
def load_data():
    students = []
    records = []  
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            current_date = None
            current_att = {}
            
            for row in reader:
                date = row['Date']
                student = row['Student']
                status = row['Status']
                
                if date != current_date and current_date is not None:
                    records.append({"date": current_date, "attendance": current_att.copy()})
                    current_att = {}
                
                current_date = date
                current_att[student] = status
                
                if student not in students:
                    students.append(student)
            
            if current_date:
                records.append({"date": current_date, "attendance": current_att})
    
    return students, records

def save_data(students, records):
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Student", "Status"])
        for record in records:
            date = record["date"]
            for student, status in record["attendance"].items():
                writer.writerow([date, student, status])

def add_student(students, records):
    name = input("Enter student name: ").strip()
    if name and name not in students:
        students.append(name)
        print(f"Added student: {name}")
        save_data(students, records)  
    else:
        print("Student already exists or invalid name.")

def record_attendance(students, records):
    if not students:
        print("No students added yet!")
        return
    
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    attendance_today = {}
    print(f"\nMark attendance for {date} (P = Present, A = Absent)")
    for student in students:
        while True:
            mark = input(f"{student}: ").strip().upper()
            if mark in ['P', 'A']:
                attendance_today[student] = mark
                break
            else:
                print("Enter P or A only.")
    
    records.append({
        "date": date,
        "attendance": attendance_today
    })
    save_data(students, records)
    print(f"Attendance recorded for {date}")

def calculate_percentage(attendance_list):
    if not attendance_list:
        return 0.0
    present = sum(1 for a in attendance_list if a == 'P')
    return (present / len(attendance_list)) * 100

def view_attendance(students, records):
    if not students:
        print("No students.")
        return
    
    print("\n=== Attendance Summary ===")
    for student in students:
        student_att = [record["attendance"].get(student, 'A') for record in records]
        total = len(student_att)
        perc = calculate_percentage(student_att)
        print(f"{student}: {perc:.1f}% ({sum(1 for x in student_att if x=='P')}/{total})")

def find_low_attendance(students, records):
    print("\n=== Students below 75% ===")
    found = False
    for student in students:
        student_att = [record["attendance"].get(student, 'A') for record in records]
        perc = calculate_percentage(student_att)
        if perc < 75 and len(student_att) > 0:
            print(f"{student}: {perc:.1f}%")
            found = True
    if not found:
        print("No students below 75% or no records yet.")

def export_report(students, records):
    if not records:
        print("No attendance records to export!")
        return
    
    filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Student", "Total Days", "Present", "Percentage"])
        
        for student in students:
            student_att = [record["attendance"].get(student, 'A') for record in records]
            total = len(student_att)
            present = sum(1 for x in student_att if x == 'P')
            perc = calculate_percentage(student_att)
            writer.writerow([student, total, present, f"{perc:.1f}"])
    
    print(f"Report exported to {filename}")

def main():
    students, records = load_data()
    print("=== Simple Attendance Management System (Single CSV) ===")
    
    while True:
        print("\nOptions:")
        print("1. Add Student")
        print("2. Record Attendance")
        print("3. View Attendance")
        print("4. Find Low Attendance (<75%)")
        print("5. Export Report (CSV)")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == '1':
            add_student(students, records)
        elif choice == '2':
            record_attendance(students, records)
        elif choice == '3':
            view_attendance(students, records)
        elif choice == '4':
            find_low_attendance(students, records)
        elif choice == '5':
            export_report(students, records)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()