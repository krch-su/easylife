# your_app/management/commands/populate_historical_data.py

import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from apps.finance.models import Transaction
from apps.users.models import User


class Command(BaseCommand):
    help = "Populate the database with fake historical transactions."

    def handle(self, *args, **kwargs):
        num_transactions = 100  # Number of transactions to generate

        # Get all users
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("No users found. Please create some users first."))
            return

        # Define the time range for the transactions
        start_date = datetime.now() - timedelta(days=60)
        end_date = datetime.now()

        # Function to generate a random datetime between start_date and end_date
        def random_date(start, end):
            delta = end - start
            random_seconds = random.randint(0, int(delta.total_seconds()))
            return start + timedelta(seconds=random_seconds)

        for _ in range(num_transactions):
            # Choose a random user
            user = random.choice(users)

            # Generate a new random date and time for each transaction
            transaction_date = random_date(start_date, end_date)
            transaction_date = make_aware(transaction_date)  # Ensure the date is timezone-aware

            # Print the generated random date for debugging
            self.stdout.write(self.style.NOTICE(f"Generated date: {transaction_date}"))

            # Create random transaction data
            transaction_type = random.choice([1, 2])  # Adjust types as per your model
            amount = round(random.uniform(10.00, 1000.00), 2)  # Random amount between 10 and 1000

            # Create a new transaction
            Transaction.objects.create(
                user=user,
                type=transaction_type,
                amount=amount,
                date=transaction_date  # Assign the unique random date
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_transactions} random transactions."))
