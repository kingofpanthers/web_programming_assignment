from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentEditForm, StudentFilterForm
WEEK = 6

def home(request):
    students = Student.objects.prefetch_related('modules').all()
    form = StudentFilterForm(request.GET)
    if WEEK >= 6 and form.is_valid():
        data = form.cleaned_data
        for key in ['firstName', 'lastName']:
            if data[key]:
                students = students.filter(**{key + '__icontains': data[key]})
        if data['min_age'] is not None:
            students = students.filter(age__gt=data['min_age'])
        if data['max_age'] is not None:
            students = students.filter(age__lt=data['max_age'])
        if data['module']:
            students = students.filter(modules=data['module'])
        if data['module_name']:
            students = students.filter(modules__name__icontains=data['module_name'])
        students = students.distinct()
    page = Paginator(
        students, 20 if WEEK >= 5 else max(students.count(), 1)
    ).get_page(request.GET.get('page'))
    # Keep the current filters when moving to another page.
    params = request.GET.copy()
    params.pop('page', None)
    return render(
        request,
        'school/home.html',
        {
            'page_obj': page,
            'filter_form': form,
            'query_string': params.urlencode(),
            'week': WEEK,
        },
    )

def detail(request, pk):
    return render(
        request,
        'school/detail.html',
        {'student': get_object_or_404(Student, pk=pk), 'week': WEEK},
    )

def edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentEditForm(
        request.POST if request.method == 'POST' else None,
        request.FILES or None,
        instance=student,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detail', pk=student.pk)
    return render(request, 'school/edit.html', {'form': form, 'student': student})
