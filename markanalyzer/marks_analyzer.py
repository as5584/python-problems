import csv

with open('students.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    
    students = []
    for row in reader:
        roll = int(row[0])
        name = row[1]
        math = int(row[2])
        science = int(row[3])
        english = int(row[4])
        students.append([roll, name, math, science, english])

print("Student Report:")


total_avg = 0
for student in students:
    avg = (student[2] + student[3] + student[4]) / 3
    print(f"Roll No: {student[0]}, Name: {student[1]}, Avg: {avg:.2f}")
    total_avg = total_avg + avg

class_average = total_avg / len(students)
print(f"\nClass Average: {class_average:.2f}")

topper = students[0]
for student in students:
    if (student[2] + student[3] + student[4]) > (topper[2] + topper[3] + topper[4]):
        topper = student

print(f"\nTopper: {topper[1]} (Roll No: {topper[0]})")

# Step 4: List students who failed (below 40 in any subject)
print("\nFailed Students:")
failed = False
for student in students:
    if student[2] < 40 or student[3] < 40 or student[4] < 40:
        print(f"{student[1]} (Roll No: {student[0]})")
        failed = True
if not failed:
    print("No one failed!")

with open('report.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RollNo', 'Name', 'Department', 'Average', 'Status'])
    
    for student in students:
        avg = (student[2] + student[3] + student[4]) / 3
        status = "Pass" if avg >= 40 else "Fail"
        writer.writerow([student[0], student[1], student[2], round(avg, 2), status])

print("\nReport saved to report.csv")