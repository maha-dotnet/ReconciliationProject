
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    SystemARecord,
    SystemBRecord,
    ReconciliationResult
)

from .importer import import_csv
from .comparison import reconcile
from .serializers import ReconciliationResultSerializer


class UploadCSVView(APIView):

    def post(self, request, system):

        if system not in ["A", "B"]:
            return Response(
                {"error": "Invalid system. Use A or B."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES.get("file")
        batch_value = request.data.get("batch_id")

        if not file:
            return Response(
                {"error": "Please upload a CSV file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.lower().endswith(".csv"):
            return Response(
                {"error": "Only CSV files are supported."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if file.size > 10 * 1024 * 1024:
            return Response(
                {"error": "File size must not exceed 10 MB."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            batch_id = uuid.UUID(str(batch_value))

            result = import_csv(
                file=file,
                batch_id=batch_id,
                system=system
            )

            if result["errors"]:
                return Response(
                    {
                        "message": "CSV imported with some errors.",
                        "batch_id": str(batch_id),
                        **result
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message": f"System {system} CSV uploaded successfully.",
                    "batch_id": str(batch_id),
                    **result
                },
                status=status.HTTP_200_OK
            )

        except (ValueError, TypeError, AttributeError) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReconciliationView(APIView):

    def post(self, request):

        try:
            batch_id = uuid.UUID(
                str(request.data.get("batch_id"))
            )

            count_a = SystemARecord.objects.filter(
                batch_id=batch_id
            ).count()

            count_b = SystemBRecord.objects.filter(
                batch_id=batch_id
            ).count()

            if count_a == 0 or count_b == 0:
                return Response(
                    {
                        "error": "Upload both System A and System B files first."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = reconcile(batch_id)

            return Response(
                {
                    "message": "Reconciliation completed successfully.",
                    "batch_id": str(batch_id),
                    "summary": result
                },
                status=status.HTTP_200_OK
            )

        except (ValueError, TypeError, AttributeError) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReconciliationResultsView(APIView):

    def get(self, request):

        batch_value = request.query_params.get("batch_id")
        result_status = request.query_params.get("status")

        if not batch_value:
            return Response(
                {"error": "batch_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            batch_id = uuid.UUID(str(batch_value))

        except (ValueError, TypeError, AttributeError):
            return Response(
                {"error": "Invalid batch_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = ReconciliationResult.objects.filter(
            batch_id=batch_id
        ).order_by("transaction_id")

        if result_status:
            valid_statuses = [
                choice[0]
                for choice in ReconciliationResult.STATUS_CHOICES
            ]

            if result_status not in valid_statuses:
                return Response(
                    {"error": "Invalid reconciliation status."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            results = results.filter(
                reconciliation_status=result_status
            )

        serializer = ReconciliationResultSerializer(
            results,
            many=True
        )

        return Response(
            {
                "count": results.count(),
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


class DashboardSummaryView(APIView):

    def get(self, request):

        batch_value = request.query_params.get("batch_id")

        if not batch_value:
            return Response(
                {"error": "batch_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            batch_id = uuid.UUID(str(batch_value))

        except (ValueError, TypeError, AttributeError):
            return Response(
                {"error": "Invalid batch_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = ReconciliationResult.objects.filter(
            batch_id=batch_id
        )

        return Response(
            {
                "batch_id": str(batch_id),
                "total_records": results.count(),
                "matched": results.filter(
                    reconciliation_status="MATCHED"
                ).count(),
                "mismatched": results.filter(
                    reconciliation_status="MISMATCHED"
                ).count(),
                "missing_in_a": results.filter(
                    reconciliation_status="MISSING_IN_A"
                ).count(),
                "missing_in_b": results.filter(
                    reconciliation_status="MISSING_IN_B"
                ).count()
            },
            status=status.HTTP_200_OK
        )
