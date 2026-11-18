
import csv
import io

from datetime import datetime
from decimal import Decimal, InvalidOperation

from .models import SystemARecord, SystemBRecord


REQUIRED_COLUMNS = {
    "transaction_id",
    "amount",
    "transaction_date",
    "status"
}


def import_csv(file, batch_id, system):

    try:
        content = file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no headers.")

        reader.fieldnames = [
            name.strip().lower() for name in reader.fieldnames
        ]

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"Missing columns: {', '.join(sorted(missing_columns))}"
            )

        model = (
            SystemARecord if system == "A"
            else SystemBRecord
        )

        imported = 0
        errors = []

        for row_number, row in enumerate(reader, start=2):
            try:
                transaction_id = (row.get("transaction_id") or "").strip()

                if not transaction_id:
                    raise ValueError("Transaction ID is required.")

                amount = Decimal(
                    (row.get("amount") or "").strip()
                )

                if not amount.is_finite():
                    raise ValueError("Amount must be finite.")

                date_value = datetime.strptime(
                    (row.get("transaction_date") or "").strip(),
                    "%Y-%m-%d"
                ).date()

                status = (row.get("status") or "").strip()

                if not status:
                    raise ValueError("Status is required.")

                model.objects.update_or_create(
                    batch_id=batch_id,
                    transaction_id=transaction_id,
                    defaults={
                        "amount": amount,
                        "transaction_date": date_value,
                        "status": status
                    }
                )

                imported += 1

            except (ValueError, InvalidOperation) as error:
                errors.append({
                    "row": row_number,
                    "error": str(error)
                })

        return {
            "imported": imported,
            "errors": errors
        }

    except UnicodeDecodeError:
        raise ValueError("CSV file must use UTF-8 encoding.")
