# Goodreads CSV to Markdown Converter

This script converts your Goodreads data export (`data.csv`) into Markdown files suitable for personal note-taking systems and integration with static site generators like [Hugo](https://gohugo.io/).

It's how I migrated from Goodreads to [gianluca.ai/books](https://gianluca.ai/books).

Note: I knew how to do this, but it's mundane gruntwork. I just wrote a basic spec and then had OpenAI's `o1-preview` generate the script. A few rounds of tweaking and it was doing what I wanted. It also wrote large chunks of this README in a similar way. I consider this kind of hacky once-off scripting an ideal use case for LLM code generation. 

## Overview

Export your Goodreads books from [https://www.goodreads.com/review/import/](https://www.goodreads.com/review/import/). Name the resulting file `data.csv`

- **Input**: `data.csv` (Goodreads data export)
- **Outputs**:
  - `reviews.md`: Contains books you've read, rated, and/or reviewed.
  - `list.md`: Contains books you've shelved as wanting to read but haven't read yet.

Both output files are sorted chronologically, with the most recent additions or modifications at the top.

## Features

- **No External Dependencies**: The script uses only Python's standard libraries.
- **Date Parsing**: Handles various date formats and uses `Date Read` or `Date Added` for sorting.
- **HTML to Markdown Conversion**: Converts basic HTML in reviews to Markdown for better compatibility with Markdown processors like Hugo.
- **Customizable Output**: Easily modify the script to adjust formatting or add additional fields.

## Prerequisites

- **Python 3.x** installed on your system.

## Getting Started

### 1. Export Your Goodreads Data

- **Log in to Goodreads** and navigate to [Export Library](https://www.goodreads.com/review/import).
- Click on **Export Library** to download your data in CSV format.
- Save the downloaded file as `data.csv` in the project directory.

### 2. Prepare the Project Directory

Ensure your project directory has the following structure:

```
.
├── data.csv
├── script.py
```

Place the provided `script.py` file in the same directory as your `data.csv`.

### 3. Run the Script

Open a terminal window, navigate to your project directory, and execute:

```bash
python script.py
```

### 4. View the Output

After running the script, you should see two new files in your directory:

- `reviews.md`
- `list.md`

## Output Formats

### reviews.md

- **Grouping**: Books are grouped by year using level 2 headings (`##`), based on the `Date Read` field. If `Date Read` is unavailable, `Date Added` is used.
- **Book Entries**: Each book is listed under its respective year with detailed information.
- **Formatting**:

  ```markdown
  ## 2024

  ### Book Title (Original Publication Year)

  Author Name

  - Completed: YYYY-MM-DD
  - My Rating: /5  

  Review text in Markdown format.

  ---
  ```

- **Reviews**: Any HTML content in your reviews is converted to Markdown for better readability and compatibility.

### list.md

- **To-Read List**: A simple markdown list of books you want to read.
- **Formatting**:

  ```markdown
  - [[YYYY-MM-DD]] Book Title (Year Published) - Author Name
  ```

## Customization

Feel free to modify `script.py` to adjust the formatting or include additional data fields from the CSV.

### Adjust Date Formats

The script supports multiple date formats. If your dates are in a different format, you can update the `date_formats` tuple in the `parse_date` function.

```python
date_formats = ("%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y")
```
