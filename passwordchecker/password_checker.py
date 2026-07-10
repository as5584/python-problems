
import re
import string


def check_password(password: str) -> dict:
    checks = {
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_numbers": bool(re.search(r"\d", password)),
        "has_symbols": bool(re.search(r"[^\w\s]", password)),
        "min_length": len(password) >= 8,
    }

    score = sum(checks.values())
    percentage = round((score / 5) * 100)

    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Medium",
        4: "Strong",
        5: "Very Strong",
    }

    return {
        "password": password,
        "checks": checks,
        "score": score,
        "max_score": 5,
        "percentage": percentage,
        "strength": labels[score],
    }


def print_report(result: dict) -> None:
    """Print password strength report."""
    labels = {
        "has_uppercase": "Uppercase letters (A-Z)",
        "has_lowercase": "Lowercase letters (a-z)",
        "has_numbers": "Numbers (0-9)",
        "has_symbols": "Symbols (!@#$...)",
        "min_length": "At least 8 characters",
    }

    print("\n" + "=" * 45)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 45)
    print(f"\nPassword: {'*' * len(result['password'])}")

    print("\nCriteria:")
    for key, label in labels.items():
        status = "PASS" if result["checks"][key] else "FAIL"
        print(f"  [{status}] {label}")

    print(f"\nScore     : {result['score']}/{result['max_score']}")
    print(f"Match     : {result['percentage']}%")
    print(f"Strength  : {result['strength']}")
    print("=" * 45)


def main() -> None:
    print("========== PASSWORD STRENGTH CHECKER ==========")
    print("Press Enter to exit.\n")

    while True:
        password = input("Enter password to check: ")

        if not password:
            print("Goodbye!")
            break

        result = check_password(password)
        print_report(result)


if __name__ == "__main__":
    main()