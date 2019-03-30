from django.shortcuts import render

# Create your views here.

from .models import Scholarship, Donor, ScholarshipInstance, Type


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_scholarships = Scholarship.objects.all().count()
    num_instances = ScholarshipInstance.objects.all().count()
    # Available copies of scholarships
    num_instances_available = ScholarshipInstance.objects.filter(status__exact='a').count()
    num_donors = Donor.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_scholarships': num_scholarships, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_donors': num_donors,
                 'num_visits': num_visits},
    )


from django.views import generic


class ScholarshipListView(generic.ListView):
    """Generic class-based view for a list of scholarships."""
    model = Scholarship
    paginate_by = 10


class ScholarshipDetailView(generic.DetailView):
    """Generic class-based detail view for a scholarship."""
    model = Scholarship


class DonorListView(generic.ListView):
    """Generic class-based list view for a list of donors."""
    model = Donor
    paginate_by = 10


class DonorDetailView(generic.DetailView):
    """Generic class-based detail view for an donor."""
    model = Donor


from django.contrib.auth.mixins import LoginRequiredMixin

##in testing will not work propperly!!!
class AwardedScholarshipsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing scholarships on awared to current user."""
    model = ScholarshipInstance
    template_name = 'archive/scholarshipinstance_list_applied_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ScholarshipInstance.objects.filter(applicant=self.request.user).filter(status__exact='d').order_by('deadline')

from django.contrib.auth.mixins import PermissionRequiredMixin


class AwardedScholarshipsAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all scholarships awarded. Only visible to users with can_mark_applied permission."""
    model = ScholarshipInstance
    permission_required = 'archive.can_mark_applied'
    template_name = 'archive/scholarshipinstance_list_applied_all.html'
    paginate_by = 10

    def get_queryset(self):
        return ScholarshipInstance.objects.filter(status__exact='o').order_by('deadline')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

# from .forms import ScholarshipForm
from archive.forms import ApplyScholarshipForm


@permission_required('archive.can_mark_applied')
def apply_scholarship_archival(request, pk):
    """View function for renewing a specific ScholarshipInstance by archival."""
    scholarship_instance = get_object_or_404(ScholarshipInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ApplyScholarshipForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model deadline field)
            #scholarship_instance.deadline = form.cleaned_data['renewal_date']
            scholarship_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-applied'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ApplyScholarshipForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'scholarship_instance': scholarship_instance,
    }

    return render(request, 'archive/scholarship_apply_archival.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Donor


class DonorCreate(PermissionRequiredMixin, CreateView):
    model = Donor
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'archive.can_mark_applied'


class DonorUpdate(PermissionRequiredMixin, UpdateView):
    model = Donor
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'archive.can_mark_applied'


class DonorDelete(PermissionRequiredMixin, DeleteView):
    model = Donor
    success_url = reverse_lazy('donors')
    permission_required = 'archive.can_mark_applied'


# Classes created for the forms DOES NOT WORK
class ScholarshipCreate(PermissionRequiredMixin, CreateView):
    model = Scholarship
    fields = '__all__'
    permission_required = 'archive.can_mark_applied'


class ScholarshipUpdate(PermissionRequiredMixin, UpdateView):
    model = Scholarship
    fields = '__all__'
    permission_required = 'archive.can_mark_applied'


class ScholarshipDelete(PermissionRequiredMixin, DeleteView):
    model = Scholarship
    success_url = reverse_lazy('scholarships')
    permission_required = 'archive.can_mark_applied'
