from django.contrib import admin
# Register your models here.
from .models import Donor, Type, Scholarship, ScholarshipInstance, GPA, Student

"""Minimal registration of Models.
admin.site.register(Scholarship)
admin.site.register(Donor)
admin.site.register(ScholarshipInstance)
admin.site.register(Type)
admin.site.register(GPA)
"""

admin.site.register(Type)
admin.site.register(GPA)
admin.site.register(Student)


class ScholarshipsInline(admin.TabularInline):
    """Defines format of inline scholarship insertion (used in DonorAdmin)"""
    model = Scholarship


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    """Administration object for Donor models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of scholarships in donor view (inlines)
    """
    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [ScholarshipsInline]


class ScholarshipsInstanceInline(admin.TabularInline):
    """Defines format of inline scholarship instance insertion (used in ScholarshipAdmin)"""
    model = ScholarshipInstance


class ScholarshipAdmin(admin.ModelAdmin):
    """Administration object for Scholarship models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of scholarship instances in scholarship view (inlines)
    """
    list_display = ('name', 'donor', 'display_type')
    inlines = [ScholarshipsInstanceInline]


admin.site.register(Scholarship, ScholarshipAdmin)


@admin.register(ScholarshipInstance)
class ScholarshipInstanceAdmin(admin.ModelAdmin):
    """Administration object for ScholarshipInstance models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('scholarship', 'status', 'applicant', 'deadline', 'id')
    list_filter = ('status', 'deadline')

    fieldsets = (
        (None, {
            'fields': ('scholarship', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'deadline', 'applicant')
        }),
    )
