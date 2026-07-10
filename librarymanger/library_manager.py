from database import SessionLocal
from services.book_service import BookService
from services.issue_service import IssueService
from services.report_service import ReportService


def add_book(session) -> None:
    print("\n--- Add Book ---")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()

    try:
        copies = int(input("Number of copies: ").strip())
    except ValueError:
        print("Enter a valid number of copies (1 or more).")
        return

    book, error = BookService(session).add_book(title, author, isbn, copies)
    if error:
        print(error)
        return
    print(f"Book added: [{book.id}] {book.title} ({book.total_copies} copies)")


def issue_book(session) -> None:
    print("\n--- Issue Book ---")
    book_query = input("Book ID / ISBN / Title: ").strip()
    borrower_name = input("Borrower name: ").strip()
    borrower_id = input("Borrower ID: ").strip()

    record, error = IssueService(session).issue_book(
        book_query, borrower_name, borrower_id
    )
    if error:
        print(error)
        return

    book = BookService(session).find_book(record.book_id)
    print(f"Issued: {record.book_title} to {record.borrower_name} [{record.issue_id}]")
    if book:
        print(f"Available copies left: {book.available_copies}")


def return_book(session) -> None:
    print("\n--- Return Book ---")
    issue_id = input("Issue ID (or press Enter to search by borrower): ").strip()

    service = IssueService(session)
    if issue_id:
        record, error, _ = service.return_book(issue_id=issue_id)
    else:
        borrower_id = input("Borrower ID: ").strip()
        record, error, matches = service.return_book(borrower_id=borrower_id)

        if matches:
            print("Multiple active issues:")
            for i, m in enumerate(matches, 1):
                print(f"  {i}. [{m.issue_id}] {m.book_title}")
            try:
                choice = int(input("Select issue number: ").strip())
            except ValueError:
                print("Invalid selection.")
                return
            record, error, _ = service.return_book(
                borrower_id=borrower_id,
                selection_index=choice,
            )

    if error:
        print(error)
        return

    book = BookService(session).find_book(record.book_id)
    print(f"Returned: {record.book_title} from {record.borrower_name}")
    if book:
        print(f"Available copies now: {book.available_copies}")


def search_books(session) -> None:
    print("\n--- Search Books ---")
    query = input("Search (title / author / ISBN): ").strip()

    if not query:
        print("Enter a search term.")
        return

    results = BookService(session).search_books(query)
    if not results:
        print("No books found.")
        return

    print(f"\nFound {len(results)} book(s):")
    for book in results:
        print(
            f"  [{book.id}] {book.title}\n"
            f"       Author  : {book.author}\n"
            f"       ISBN    : {book.isbn}\n"
            f"       Available: {book.available_copies}/{book.total_copies}"
        )


def count_available(session) -> None:
    print("\n--- Available Books Count ---")
    service = BookService(session)
    summary = service.get_availability_summary()

    if not summary:
        print("No books in the library.")
        return

    print(f"Total book titles : {summary.total_titles}")
    print(f"Total copies      : {summary.total_copies}")
    print(f"Available copies  : {summary.available_copies}")
    print(f"Issued copies     : {summary.issued_copies}")
    print("\nPer book:")
    for book in service.get_all_books():
        status = "Available" if book.available_copies > 0 else "Not Available"
        print(
            f"  [{book.id}] {book.title[:30]:30} "
            f"{book.available_copies}/{book.total_copies}  {status}"
        )


def view_all_books(session) -> None:
    print("\n--- All Books ---")
    books = BookService(session).get_all_books()

    if not books:
        print("No books in the library.")
        return

    for book in books:
        print(
            f"  [{book.id}] {book.title} by {book.author}\n"
            f"       ISBN: {book.isbn} | "
            f"Available: {book.available_copies}/{book.total_copies}"
        )


def view_issued_books(session) -> None:
    print("\n--- Currently Issued ---")
    active = IssueService(session).get_active_issues()

    if not active:
        print("No books currently issued.")
        return

    for record in active:
        print(
            f"  [{record.issue_id}] {record.book_title}\n"
            f"       Borrower: {record.borrower_name} ({record.borrower_id})\n"
            f"       Issued  : {record.issue_date.isoformat()}"
        )


def generate_reports(session) -> None:
    print("\n--- Generate Reports ---")
    result = ReportService(session).generate_reports()

    if not result:
        print("No data to report. Add books first.")
        return

    xlsx_path, pdf_path = result
    print("Reports generated successfully:")
    print(f"  XLSX: {xlsx_path}")
    print(f"  PDF : {pdf_path}")


def main() -> None:
    session = SessionLocal()

    try:
        while True:
            print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
            print("1. Add Book")
            print("2. Issue Book")
            print("3. Return Book")
            print("4. Search Books")
            print("5. Count Available Books")
            print("6. View All Books")
            print("7. View Issued Books")
            print("8. Generate Reports (XLSX & PDF)")
            print("9. Exit")
            choice = input("Choose an option (1-9): ").strip()

            actions = {
                "1": add_book,
                "2": issue_book,
                "3": return_book,
                "4": search_books,
                "5": count_available,
                "6": view_all_books,
                "7": view_issued_books,
                "8": generate_reports,
            }

            if choice == "9":
                print("Goodbye!")
                break
            elif choice in actions:
                actions[choice](session)
            else:
                print("Invalid option. Try again.")
    finally:
        session.close()


if __name__ == "__main__":
    main()