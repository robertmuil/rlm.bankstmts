import datetime
import os
import re
import logging

logger = logging.getLogger(__name__)

# Specify the directory where the PDF files are located
directory = "/Users/robert_muil/for-personal/finances/nationwide personal"


def get_date(filename):
    """Extract the date from the filename using regular expressions."""

    date_match = re.search(r"\d{2}-?[A-Za-z]{3}-?\d{4}", filename)
    if date_match:
        return date_match.group()
    else:
        return None


# Iterate over each file in the directory
def list_date_files(directory, filename_suffix=".pdf"):
    """List all files in the directory with a date in the filename."""

    for filename in os.listdir(directory):
        logger.debug(f"Checking {filename}")
        if filename.endswith(filename_suffix):
            datestr = get_date(filename)
            if datestr:
                yield filename, datestr


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    print("hi")
    for filename, datestr in list_date_files(directory):
        # Convert the date to ISO format
        date_iso = datetime.datetime.strptime(datestr, "%d%b%Y").strftime("%Y-%m-%d")

        # Construct the new filename with the date in ISO format
        new_filename = f"{date_iso}_{filename}"

        print(f"Renaming {filename} to {new_filename}")

        # Rename the file
        os.rename(
            os.path.join(directory, filename), os.path.join(directory, new_filename)
        )
