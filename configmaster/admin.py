from django.contrib import admin
from configmaster.models import DeviceType, DeviceGroup
from configmaster.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("label", "name", "hostname", "group", "device_type", "enabled")
    list_filter = ("group", "device_type")
    search_fields = ("name", "hostname")

    fieldsets = (
        ("Basic info", {
            'fields': ('name', 'label', 'group', 'device_type')
        }),
        ("Flags", {
            'fields': ('enabled', 'sync')
        }),
        ('Config management data', {
            'description': "Will get overwritten during the next run.",
            'fields': ('data_model', 'data_firmware', 'data_serial'),
        })
    )


    def get_readonly_fields(self, request, obj=None):
        fields = super(DeviceAdmin, self).get_readonly_fields(request, obj)

        if obj:
            if obj.sync:
                return "label", "name", "hostname", "group"

        return fields


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceType)
admin.site.register(DeviceGroup)
