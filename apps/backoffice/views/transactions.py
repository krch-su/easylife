from django.contrib import admin


class TransactionView(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'type',
        'amount',
        'date'
    )

