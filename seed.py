import psycopg2
from faker import Faker
from random import randint
from datetime import datetime
import time

fake = Faker()

conn = psycopg2.connect("dbname=stream-api user=postgres password=password host=localhost")
cursor = conn.cursor()

start = time.time()
batch_size = 10000
total = 1_000_000

print("Inserting data...")

for i in range(0, total, batch_size):
    batch = [
        (
            randint(1, 500),                  # sk
            fake.first_name(),               # fname
            fake.last_name(),                # lname
            fake.date_of_birth(minimum_age=18, maximum_age=90),
            fake.zipcode()
        )
        for _ in range(batch_size)
    ]

    args_str = ",".join(cursor.mogrify("(%s, %s, %s, %s, %s)", row).decode("utf-8") for row in batch)
    cursor.execute("INSERT INTO people (sk, fname, lname, dob, zipcode) VALUES " + args_str)
    conn.commit()
    batch_num = (i // batch_size) + 1
    total_batches = total // batch_size
    print(f"[{batch_num}/{total_batches}] Inserted {i + batch_size} rows...")

end = time.time()
print(f"Finished in {end - start:.2f} seconds.")

cursor.close()
conn.close()