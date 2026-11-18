
import uuid

from django.db import models


class SystemARecord(models.Model):
    batch_id = models.UUIDField(db_index=True)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateField()
    status = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch_id", "transaction_id"],
                name="unique_system_a_transaction"
            )
        ]

    def __str__(self):
        return self.transaction_id


class SystemBRecord(models.Model):
    batch_id = models.UUIDField(db_index=True)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateField()
    status = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch_id", "transaction_id"],
                name="unique_system_b_transaction"
            )
        ]

    def __str__(self):
        return self.transaction_id


class ReconciliationResult(models.Model):

    MATCHED = "MATCHED"
    MISMATCHED = "MISMATCHED"
    MISSING_IN_A = "MISSING_IN_A"
    MISSING_IN_B = "MISSING_IN_B"

    STATUS_CHOICES = [
        (MATCHED, "Matched"),
        (MISMATCHED, "Mismatched"),
        (MISSING_IN_A, "Missing in System A"),
        (MISSING_IN_B, "Missing in System B"),
    ]

    batch_id = models.UUIDField(db_index=True)
    transaction_id = models.CharField(max_length=100)

    system_a = models.ForeignKey(
        SystemARecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    system_b = models.ForeignKey(
        SystemBRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reconciliation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    differences = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch_id", "transaction_id"],
                name="unique_reconciliation_result"
            )
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.reconciliation_status}"
