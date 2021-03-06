#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
#   Copyright (C) 2013-2016 Continum AG
#

from django.contrib import admin
from django import forms
import adminactions.actions as actions

from configmaster.models import DeviceType, DeviceGroup, Report, Credential, \
    Task, ConnectionSetting, \
    Repository
from configmaster.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "label", "name", "hostname", "group",
        "device_type", "enabled", "version_info")

    list_filter = (
        "group", "device_type", "do_not_use_scp",
        "enabled", "known_by_nagios")

    search_fields = ("name", "hostname")
    readonly_fields = ("known_by_nagios", "version_info")

    fieldsets = (
        ("Basic info", {
            'fields': ('name', 'label', 'hostname', 'group', 'device_type')
        }),
        ("Settings", {
            'fields': ('enabled', 'sync', 'credential',
                       'accept_new_hostkey', 'do_not_use_scp')
        }),
        ('Info', {
            'fields': ('known_by_nagios', 'version_info'),
        })
    )

    def get_readonly_fields(self, request, obj=None):
        fields = super(DeviceAdmin, self).get_readonly_fields(request, obj)

        if obj:
            if obj.sync:
                return fields + ("label", "name", "hostname", "group")

        return fields


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = (
        "device", "date", "task", "result", "output", "long_output")
    list_display = ("date", "device", "task", "result", "output")
    list_filter = ("result",)


class CredentialAdminForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = '__all__'

    new_password = forms.CharField(
        required=False,
        label="Set password",
        help_text="Set new password for this entry. "
                  "Leave empty to keep existing password.",
        widget=forms.TextInput(
            attrs={'class': 'vTextField'}))


class CredentialAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('description', 'type',),
        }),
        ('Plaintext login', {
            'fields': ('username', 'new_password'),
        }),
        ("SSH login", {
            'fields': ('path',)
        })
    )

    form = CredentialAdminForm

    list_display = ("description", "type", "username", "path")
    list_filter = ("type",)

    def save_model(self, request, obj, form, change):
        new_password = form.cleaned_data['new_password']

        # Ignore passwords consisting only of whitespace
        # (prevent accidental overwrite).

        if len(new_password.strip()):
            obj.password = new_password

        obj.save()


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceType)
admin.site.register(DeviceGroup)
admin.site.register(Task)
admin.site.register(Repository)
admin.site.register(ConnectionSetting)
admin.site.register(Credential, CredentialAdmin)
admin.site.register(Report, ReportAdmin)

actions.add_to_site(admin.site)
