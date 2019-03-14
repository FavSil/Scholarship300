from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Type(models.Model):
    """Model representing a scholarship type (e.g. Athletic, Merit)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a scholarship type (e.g. Athletic, Merit.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class GPA(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    grade = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.grade


class Scholarship(models.Model):
    """Model representing a scholarship (but not a specific copy of a scholarship)."""
    name = models.CharField(max_length=200)
    donor = models.ForeignKey('Donor', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the scholarship")
    value = models.CharField('Value', max_length=13,
                            help_text='Ammount distributed')
    type = models.ManyToManyField(Type, help_text="Select a type for this scholarship")
    # ManyToManyField used because a type can contain many scholarships and a Scholarship can cover many types.
    # Type class has already been defined so we can specify the object above.
    gpa = models.ForeignKey('GPA', on_delete=models.SET_NULL, null=True)

    def display_type(self):
        """Creates a string for the Type. This is required to display type in Admin."""
        return ', '.join([type.name for type in self.type.all()[:3]])

    display_type.short_description = 'Type'

    def get_absolute_url(self):
        """Returns the url to access a particular scholarship instance."""
        return reverse('scholarship-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


import uuid  # Required for unique scholarship instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a applicant


class ScholarshipInstance(models.Model):
    """Model representing a specific copy of a scholarship (i.e. that can be applied from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular scholarship across whole library")
    scholarship = models.ForeignKey('Scholarship', on_delete=models.SET_NULL, null=True)
    #    imprint = models.CharField(max_length=200)
    deadline = models.DateField(null=True, blank=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.deadline and date.today() > self.deadline:
            return True
        return False

    APPLICANT_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=APPLICANT_STATUS,
        blank=True,
        default='d',
        help_text='Scholarship availability')

    class Meta:
        ordering = ['deadline']
        permissions = (("can_mark_returned", "Set scholarship as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.scholarship.name)


class Donor(models.Model):
    """Model representing an donor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular donor instance."""
        return reverse('donor-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
