
import uuid

from datetime import date
from decimal import Decimal

from django.test import TestCase

from .models import (
    SystemARecord,
    SystemBRecord,
    ReconciliationResult
)

from .comparison import reconcile


class ReconciliationTests(TestCase):

    def setUp(self):

        self.batch_id = uuid.uuid4()

        SystemARecord.objects.create(
            batch_id=self.batch_id,
            transaction_id="TXN001",
            amount=Decimal("1000.00"),
            transaction_date=date(2026, 11, 17),
            status="SUCCESS"
        )

        SystemBRecord.objects.create(
            batch_id=self.batch_id,
            transaction_id="TXN001",
            amount=Decimal("1000.00"),
            transaction_date=date(2026, 11, 17),
            status="SUCCESS"
        )

        SystemARecord.objects.create(
            batch_id=self.batch_id,
            transaction_id="TXN002",
            amount=Decimal("2000.00"),
            transaction_date=date(2026, 11, 17),
            status="SUCCESS"
        )

        SystemBRecord.objects.create(
            batch_id=self.batch_id,
            transaction_id="TXN002",
            amount=Decimal("2500.00"),
            transaction_date=date(2026, 11, 17),
            status="SUCCESS"
        )

    def test_reconciliation(self):

        result = reconcile(self.batch_id)

        self.assertEqual(result["total_records"], 2)
        self.assertEqual(result["matched"], 1)
        self.assertEqual(result["mismatched"], 1)

    def test_mismatch_amount(self):

        reconcile(self.batch_id)

        record = ReconciliationResult.objects.get(
            batch_id=self.batch_id,
            transaction_id="TXN002"
        )

        self.assertEqual(
            record.reconciliation_status,
            "MISMATCHED"
        )

        self.assertIn("amount", record.differences)
