from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from account.models import User
from machinery1.forms import *
from machinery1.models import *
from machinery1.permission import *
User = get_user_model()

"""
def home_view(request):

    published_jobs = Machine.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_unavailabled=False)
    total_candidates = User.objects.filter(role='machinery').count()
    total_companies = User.objects.filter(role='machinery').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists=[]
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'job_lists':job_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_unavailabled=True)),
    'page_obj': page_obj
    }
    print('ok')
    return render(request, 'machinery1/index.html', context)
    
"""    

@cache_page(60 * 15)
def machine_list_view(request):
   
    machine_list = Machine.objects.filter(is_published=True,is_unavailabled=False).order_by('-timestamp')
    paginator = Paginator(machine_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'machinery1/machine-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_machine_view(request):
    """
    Provide the ability to create job post
    """
    form = MachineForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    vtypes = Vtype.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your vehicle! Please wait for review.')
            return redirect(reverse("machinery1:single-machine", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'vtypes': vtypes
    }
    return render(request, 'machinery1/post-machine.html', context)


def single_machine_view(request, id):
    """
    Provide the ability to view job details
    """
    if cache.get(id):
        machine = cache.get(id)
    else:
        machine = get_object_or_404(Machine, id=id)
        cache.set(id,machine , 60 * 15)
    related_machine_list = machine.tags.similar_objects()

    paginator = Paginator(related_machine_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'machine': machine,
        'page_obj': page_obj,
        'total': len(related_machine_list)

    }
    return render(request, 'machinery1/machine-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_machine_view(request, id):

    form = MachineApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    client = Client.objects.filter(user=user, machine=id)

    if not client:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this Vehicle!')
                return redirect(reverse("machinery1:single-machine", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("machinery1:single-machine", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Vehicle!')

        return redirect(reverse("machiney1:single-machine", kwargs={
            'id': id
        }))

"""
@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    machines = []
    savedmachines = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)

"""



@login_required(login_url=reverse_lazy('account:login'))


def machineadmin_list_view(request):
   
    machines = []
    savedmachines = []
    appliedmachines = []
    total_clients = {}
    if request.user.role == 'employer':

        machines = Machine.objects.filter(user=request.user.id)
        for machine in machines:
            count = Client.objects.filter(machine=machine.id).count()
            total_clients[machine.id] = count
     
    context = {
		'machines': machines,
        #'savedmachines': savedmachines,
        #'appliedmachines':appliedmachines,
        'total_clients': total_clients
    }

    return render(request, 'machinery1/my-machines.html', context)








"""

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')
"""

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_unavailable_machine_view(request, id):
    machine = get_object_or_404(Machine, id=id, user=request.user.id)

    if machine:
        try:
            machine.is_unavailabled = True
            machine.save()
            messages.success(request, 'Your Vehicle was marked Unavailable!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('machinery1:machineadmin')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_clients_view(request, id):

    all_clients = Client.objects.filter(machine=id)

    context = {

        'all_clients': all_clients
    }

    return render(request, 'machinery1/all-clients.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)

"""
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))

"""
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def machine_edit_view(request, id=id):
    """
    Handle Job Update

    """

    machine = get_object_or_404(Machine, id=id, user=request.user.id)
    types = Vtype.objects.all()
    form = MachineEditForm(request.POST or None, instance=machine)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Vehicle Post Was Successfully Updated!')
        return redirect(reverse("machinery1:single-machine", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'vtypes': vtypes
    }

    return render(request, 'machinery1/machine-edit.html', context)
    
    
"""  
def apply_job_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))
"""
"""
@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):

    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)

"""
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_machine_view(request, id):

    machine = get_object_or_404(Machine, id=id, user=request.user.id)

    if machine:

        machine.delete()
        messages.success(request, 'Your Vehicle was successfully deleted!')

    return redirect('machinery1:machineadmin')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_unavailable_machine_view(request, id):
    machine = get_object_or_404(Machine, id=id, user=request.user.id)

    if machine:
        try:
            machine.is_unavailabled = True
            machine.save()
            messages.success(request, 'Your Vehicle was marked Unavailable!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('machinery1:machineadmin')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_clients_view(request, id):

    all_clients = Client.objects.filter(machine=id)

    context = {

        'all_clients': all_clients
    }

    return render(request, 'machinery1/all-clients.html', context)



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_machine_view(request, id):

    form = MachineApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    client = Applicant.objects.filter(user=user, machine=id)

    if not client:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this Vehicle!')
                return redirect(reverse("machinery1:single-machine", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("machinery1:single-machine", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Vehicle!')

        return redirect(reverse("machinery1:single-machine", kwargs={
            'id': id
        }))






@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    machine = get_object_or_404(BookmarkMachine, id=id, user=request.user.id)

    if machine:

        machine.delete()
        messages.success(request, 'Saved Machine was successfully deleted!')

    return redirect('machinery1:machineadmin')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def client_details_view(request, id):

    client = get_object_or_404(User, id=id)

    context = {

        'client': client
    }

    return render(request, 'machinery1/client-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def machine_bookmark_view(request, id):

    form = MachineBookmarkForm(request.POST or None)
    user = get_object_or_404(User, id=request.user.id)
    client = BookmarkMachine.objects.filter(user=request.user.id, machine=id)

    if not client:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this Vehicle!')
                return redirect(reverse("machinery1:single-machine", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("machinery1:single-machine", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Vehicle!')

        return redirect(reverse("machinery1:single-machine", kwargs={
            'id': id
        }))

"""
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    #Handle Job Update
    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)


def single_job_view(request, id):
    #Provide the ability to view job details
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id,job , 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)
"""
