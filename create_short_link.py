import sqlite3
import sys
import string
import random
from urllib.parse import urlparse

if len(sys.argv) < 2:
    print("Usage: python main.py <url>")
    sys.exit()

url = sys.argv[1]

parsed = urlparse(url)

if (
    parsed.scheme not in ("http", "https")
    or not parsed.netloc
):
    print("Invalid URL")
    sys.exit()

characters = string.ascii_lowercase + string.digits
length = random.randint(1, 3)

random_string = ''.join(
    random.choices(characters, k=length)
)

con = sqlite3.connect("url.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS pair(
    original TEXT,
    shorted TEXT UNIQUE
)
""")

data = (url, random_string)

try:
    cur.execute("INSERT INTO pair VALUES (?, ?)", data)
    con.commit()
    print("Short URL: http://localhost/" + random_string)

except sqlite3.IntegrityError:
    print("Duplicate detected")

con.close()