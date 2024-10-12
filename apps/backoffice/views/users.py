from django.contrib import admin


class UserView(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'created_at',
        'is_staff',
    )

    fields = (
        'username',
        'is_staff',
    )
