from django.contrib import admin


class NotificationView(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'type',
        'context',
        'created_at',
        'sent_at'
    )
