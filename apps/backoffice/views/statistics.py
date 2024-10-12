from dataclasses import asdict
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone

from apps.finance.services import get_statistics


@staff_member_required
def statistics_view(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        try:
            if start_date_str:
                start_date = timezone.make_aware(timezone.datetime.fromisoformat(start_date_str))
            if end_date_str:
                end_date = timezone.make_aware(timezone.datetime.fromisoformat(end_date_str))
        except ValueError:
            pass

    return render(request, 'statistics.html', asdict(get_statistics(start_date, end_date)))
