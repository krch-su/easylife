from django.contrib import admin
from django.urls import path, include

from .views import transactions, users
from .views.statistics import statistics_view
from ..finance.models import Transaction
from ..users.models import User


class Backoffice(admin.AdminSite):
    site_header = "Backoffice"
    site_title = "Backoffice"

    def get_urls(self):
        _urls = super().get_urls()
        my_urls = [
            path("statistics/", statistics_view, name="statistics"),
        ]
        return my_urls + _urls

    def get_app_list(self, request, *args, **kwargs):
        app_list = super().get_app_list(request, kwargs)
        app_list += [
            {
                "name": "Statistics",
                "app_label": "statistics",
                "add_url": "/admin/statistics",
                "models": [
                    {
                        "name": "statistics",
                        "view_only": True,
                        "admin_url": "/admin/statistics/",
                    }
                ],
            }
        ]
        return app_list


backoffice = Backoffice(name='backoffice')

backoffice.register(User, users.UserView)
backoffice.register(Transaction, transactions.TransactionView)
# backoffice.admin_view(statistics_view)


urls = backoffice.urls

