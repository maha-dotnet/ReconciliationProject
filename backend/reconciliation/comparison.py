
from django.db import transaction

from .models import (
    SystemARecord,
    SystemBRecord,
    ReconciliationResult
)


@transaction.atomic
def reconcile(batch_id):

    records_a = {
        record.transaction_id: record
        for record in SystemARecord.objects.filter(
            batch_id=batch_id
        )
    }

    records_b = {
        record.transaction_id: record
        for record in SystemBRecord.objects.filter(
            batch_id=batch_id
        )
    }

    transaction_ids = set(records_a) | set(records_b)

    ReconciliationResult.objects.filter(
        batch_id=batch_id
    ).delete()

    results = []

    for transaction_id in transaction_ids:

        record_a = records_a.get(transaction_id)
        record_b = records_b.get(transaction_id)

        differences = {}

        if record_a is None:

            result_status = ReconciliationResult.MISSING_IN_A

        elif record_b is None:

            result_status = ReconciliationResult.MISSING_IN_B

        else:

            if record_a.amount != record_b.amount:
                differences["amount"] = {
                    "system_a": str(record_a.amount),
                    "system_b": str(record_b.amount)
                }

            if record_a.transaction_date != record_b.transaction_date:
                differences["transaction_date"] = {
                    "system_a": str(record_a.transaction_date),
                    "system_b": str(record_b.transaction_date)
                }

            if record_a.status != record_b.status:
                differences["status"] = {
                    "system_a": record_a.status,
                    "system_b": record_b.status
                }

            result_status = (
                ReconciliationResult.MISMATCHED
                if differences
                else ReconciliationResult.MATCHED
            )

        results.append(
            ReconciliationResult(
                batch_id=batch_id,
                transaction_id=transaction_id,
                system_a=record_a,
                system_b=record_b,
                reconciliation_status=result_status,
                differences=differences
            )
        )

    ReconciliationResult.objects.bulk_create(results)

    return {
        "total_records": len(results),
        "matched": sum(
            r.reconciliation_status == "MATCHED" for r in results
        ),
        "mismatched": sum(
            r.reconciliation_status == "MISMATCHED" for r in results
        ),
        "missing_in_a": sum(
            r.reconciliation_status == "MISSING_IN_A" for r in results
        ),
        "missing_in_b": sum(
            r.reconciliation_status == "MISSING_IN_B" for r in results
        )
    }
