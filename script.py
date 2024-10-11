import csv
from collections import OrderedDict
from datetime import datetime
import re
import html


def parse_date(date_str):
    """Parse date string into a datetime object."""
    if not date_str:
        return None
    date_formats = ("%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y")
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def html_to_markdown(html_content):
    """Convert basic HTML content into Markdown format."""
    # Unescape HTML entities
    text = html.unescape(html_content)

    # Replace <br>, <br/> and </p> with double newlines
    text = re.sub(r"(<br\s*/?>)|(<\/p>)", "\n\n", text, flags=re.IGNORECASE)

    # Remove <p> tags
    text = re.sub(r"<p>", "\n\n", text, flags=re.IGNORECASE)

    # Replace headings <h1>-<h6> with Markdown equivalents (with diff of 1)
    for i in range(6, 0, -1):
        text = re.sub(
            rf"<h{i}>(.*?)<\/h{i}>", rf'{"#"*(i+1)} \1', text, flags=re.IGNORECASE
        )

    # Replace <b>, <strong> tags with Markdown bold
    text = re.sub(r"<\/?(b|strong)>", "**", text, flags=re.IGNORECASE)

    # Replace <i>, <em> tags with Markdown italics
    text = re.sub(r"<\/?(i|em)>", "*", text, flags=re.IGNORECASE)

    # Replace <u> tags with underscores
    text = re.sub(r"<\/?u>", "_", text, flags=re.IGNORECASE)

    # Convert hyperlinks to Markdown format
    text = re.sub(r'<a href="(.*?)">(.*?)<\/a>', r"[\2](\1)", text, flags=re.IGNORECASE)

    # Remove any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Replace multiple newlines with a single newline
    # text = re.sub(r"\n+", "\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


# Lists to hold read books and to-read books
read_books = []
to_read_books = []

# Read the CSV data
with open("data.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        exclusive_shelf = row["Exclusive Shelf"].strip().lower()
        if exclusive_shelf == "read":
            # Parse dates
            date_read = parse_date(row["Date Read"]) or parse_date(row["Date Added"])
            if not date_read:
                continue  # Skip if no valid date
            # Collect book data
            read_books.append(
                {
                    "date_read": date_read,
                    "year": date_read.year,
                    "title": row["Title"] or "Unknown Title",
                    "original_publication_year": row["Original Publication Year"]
                    or "Unknown",
                    "author": row["Author"] or "Unknown Author",
                    "my_rating": row["My Rating"] or "Unrated",
                    "number_of_pages": row["Number of Pages"] or "Unknown",
                    "read_count": row["Read Count"] or "1",
                    "review": html_to_markdown(row["My Review"]),
                }
            )
        elif exclusive_shelf == "to-read":
            # Parse date added
            date_added = parse_date(row["Date Added"])
            if not date_added:
                continue  # Skip if no valid date
            # Collect book data
            to_read_books.append(
                {
                    "date_added": date_added,
                    "title": row["Title"] or "Unknown Title",
                    "year_published": row["Year Published"] or "Unknown",
                    "author": row["Author"] or "Unknown Author",
                }
            )

# Sort read books by date_read, most recent first
read_books.sort(key=lambda x: x["date_read"], reverse=True)

# Group read books by year
books_by_year = OrderedDict()
for book in read_books:
    year = book["year"]
    books_by_year.setdefault(year, []).append(book)

# Write reviews.md
with open("reviews.md", "w", encoding="utf-8") as f:
    for year, books in books_by_year.items():
        f.write(f"## {year}\n\n")
        for book in books:
            f.write(f"### {book['title']} ({book['original_publication_year']})\n\n")
            f.write(f"{book['author']}\n\n")
            f.write(f"- Completed: {book['date_read'].strftime('%Y-%m-%d')}\n")
            f.write(f"- My Rating: {book['my_rating']}\n")
            f.write(f"- Number of Pages: {book['number_of_pages']}\n")
            f.write(f"- Reads: {book['read_count']}\n\n")
            f.write(f"{book['review']}\n\n")
            f.write("---\n\n")

# Sort to-read books by date_added, most recent first
to_read_books.sort(key=lambda x: x["date_added"], reverse=True)

# Write list.md
with open("list.md", "w", encoding="utf-8") as f:
    for book in to_read_books:
        f.write(
            f"- [[{book['date_added'].strftime('%Y-%m-%d')}]] {book['title']} ({book['year_published']}) - {book['author']}\n"
        )
