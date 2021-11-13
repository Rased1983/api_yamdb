from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'role', 'confirmation_code')
    search_fields = ('username', )


admin.site.register(User, UserAdmin)
