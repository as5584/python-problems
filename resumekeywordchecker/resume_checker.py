import re
import os

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_FILE = os.path.join(SCRIPT_DIR, "resume.txt")
JOB_FILE = os.path.join(SCRIPT_DIR, "job_description.txt")


def read_text(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def extract_keywords(text: str) -> set[str]:
   
    words = re.findall(r"[A-Za-z0-9+#]+", text)
    return {word.lower() for word in words if len(word) > 1}


def check_match(resume_text: str, job_text: str) -> dict:
     resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_text)
    matched = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    extra = resume_keywords - job_keywords
    total_job = len(job_keywords)
    match_count = len(matched)
    percentage = round((match_count / total_job) * 100, 1) if total_job > 0 else 0.0

    return {
        "resume_keywords": sorted(resume_keywords),
        "job_keywords": sorted(job_keywords),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "extra": sorted(extra),
        "match_count": match_count,
        "total_job": total_job,
        "percentage": percentage,
    }


def print_report(result: dict) -> None:
    print("=" * 45)
    print("       RESUME KEYWORD CHECKER REPORT")
    print("=" * 45)
    print(f"\nResume Keywords : {', '.join(result['resume_keywords'])}")
    print(f"Job Keywords    : {', '.join(result['job_keywords'])}")
    print(f"\nMatched ({result['match_count']}/{result['total_job']}) : {', '.join(result['matched']) or 'None'}")
    print(f"Missing         : {', '.join(result['missing']) or 'None'}")
    print(f"Extra in Resume : {', '.join(result['extra']) or 'None'}")
    print(f"\nMatch           : {result['percentage']}%")
    print("=" * 45)


def save_report(result: dict, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("RESUME KEYWORD CHECKER REPORT\n\n")
        f.write(f"Resume Keywords: {', '.join(result['resume_keywords'])}\n")
        f.write(f"Job Keywords: {', '.join(result['job_keywords'])}\n\n")
        f.write(f"Matched: {', '.join(result['matched']) or 'None'}\n")
        f.write(f"Missing: {', '.join(result['missing']) or 'None'}\n")
        f.write(f"Extra in Resume: {', '.join(result['extra']) or 'None'}\n")
        f.write(f"\nMatch: {result['percentage']}%\n")


def main() -> None:
    resume_text = read_text(RESUME_FILE)
    job_text = read_text(JOB_FILE)

    result = check_match(resume_text, job_text)
    print_report(result)

    report_file = os.path.join(SCRIPT_DIR, "match_report.txt")
    save_report(result, report_file)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()