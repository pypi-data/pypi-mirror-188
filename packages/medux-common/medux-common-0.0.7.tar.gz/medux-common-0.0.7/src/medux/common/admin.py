from django.contrib import admin

from .models import Vendor, Tenant


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return super().has_add_permission(request) and not Vendor.objects.exists()


admin.site.register(Tenant)
