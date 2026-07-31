from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Account

fake = Faker()

db: Session = SessionLocal()

BATCH_SIZE = 1000
TOTAL = 10000

accounts = []

for i in range(TOTAL):
    account = Account(
        owner_name=fake.name(),
        account_type="chequing" if i % 2 == 0 else "savings",
        balance=fake.random_int(min=0, max=100000),
        frozen=False,
        owner_id=fake.random_int(min=1, max=2),
    )

    accounts.append(account)

    if (
        len(accounts) == BATCH_SIZE
    ):  # SQLAlchemy inserts all 1000 in one operation. More efficient than db.add(account)
        db.bulk_save_objects(accounts)
        db.commit()
        accounts = []  # resets account array

if accounts:  # adds the final accounts
    db.bulk_save_objects(accounts)
    db.commit()

db.close()

print(f"Inserted {TOTAL:,} accounts.")
