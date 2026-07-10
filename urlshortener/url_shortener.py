import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
import os

# Use os.path for cross-platform path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "history.json")

API_URL = "https://tinyurl.com/api-create.php?url={url}"


def load_history() -> list[dict]:
    """Load URL shortening history from JSON."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[dict]) -> None:
    """Save history to JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def shorten_url(long_url: str) -> str:
    """Shorten a URL using the TinyURL free API."""
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url

    api_request = API_URL.format(url=urllib.parse.quote(long_url, safe=""))

    try:
        with urllib.request.urlopen(api_request, timeout=15) as response:
            short_url = response.read().decode("utf-8").strip()
    except urllib.error.URLError as e:
        raise ConnectionError(f"API request failed: {e}") from e

    if not short_url.startswith("http"):
        raise ValueError(f"Invalid response from API: {short_url}")

    return short_url


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard (Windows)."""
    try:
        subprocess.run("clip", input=text, text=True, check=True, shell=True)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def add_to_history(history: list[dict], long_url: str, short_url: str) -> None:
    """Add a shortened URL entry to history."""
    entry = {
        "id": len(history) + 1,
        "original_url": long_url,
        "short_url": short_url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    history.insert(0, entry)
    save_history(history)


def shorten_and_save(history: list[dict]) -> None:
    """Shorten a URL, save to history, and copy to clipboard."""
    print("\n--- Shorten URL ---")
    long_url = input("Enter URL to shorten: ").strip()

    if not long_url:
        print("URL cannot be empty.")
        return

    try:
        short_url = shorten_url(long_url)
    except (ConnectionError, ValueError) as e:
        print(f"Error: {e}")
        return

    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url

    add_to_history(history, long_url, short_url)

    print(f"\nOriginal : {long_url}")
    print(f"Shortened: {short_url}")

    if copy_to_clipboard(short_url):
        print("Copied to clipboard!")
    else:
        print("Could not copy to clipboard. Copy the URL manually.")


def view_history(history: list[dict]) -> None:
    """Display saved URL history."""
    print("\n--- URL History ---")

    if not history:
        print("No URLs shortened yet.")
        return

    for entry in history:
        print(
            f"\n[{entry['id']}] {entry['created_at']}\n"
            f"  Original : {entry['original_url']}\n"
            f"  Short    : {entry['short_url']}"
        )


def copy_from_history(history: list[dict]) -> None:
    """Copy a shortened URL from history to clipboard."""
    if not history:
        print("No history available.")
        return

    view_history(history)
    try:
        entry_id = int(input("\nEnter ID to copy: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    entry = next((e for e in history if e["id"] == entry_id), None)
    if not entry:
        print("Entry not found.")
        return

    if copy_to_clipboard(entry["short_url"]):
        print(f"Copied: {entry['short_url']}")
    else:
        print(f"Copy manually: {entry['short_url']}")


def main() -> None:
    history = load_history()

    while True:
        print("\n========== URL SHORTENER ==========")
        print("1. Shorten URL")
        print("2. View History")
        print("3. Copy from History")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            shorten_and_save(history)
        elif choice == "2":
            view_history(history)
        elif choice == "3":
            copy_from_history(history)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()