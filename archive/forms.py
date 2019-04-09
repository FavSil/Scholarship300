from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.
from decimal import *

from django import forms


class ApplyScholarshipForm(forms.Form):
    """Form to apply Scholarships."""
    applicant_summary = forms.CharField(
            help_text="Enter a short summary of why you should be awarded this scholarship"
    )

    gpa = forms.DecimalField(max_value = 4,min_value = 0, max_digits= 3 , decimal_places = 2,
            help_text = "Enter your GPA."
    )

#
    def clean_gpa(self):
        data = self.cleaned_data['gpa']

        # Check gpa a float.
        if data > int(4):
            raise ValidationError(_('Invalid gpa - must be less than 4.0'))
        # Check date is in range archival allowed to change (+4 weeks)
        if data < int(0) :
            raise ValidationError(_('Invalid gpa - must be a positive integer'))

        # Remember to always return the cleaned data.
        return data
