import hashlib
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import HashForm
from .models import Hash

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def home(request):
    form = HashForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text']
        value = digest(text)
        Hash.objects.get_or_create(hash=value, defaults={'text': text})
        return redirect('detail', value=value)
    return render(request, 'school/home.html', {'form': form})

def detail(request, value):
    return render(request, 'school/detail.html', {'entry': get_object_or_404(Hash, hash=value)})

@require_POST
def quickhash(request):
    text = request.POST.get('text', '')
    if len(text) > 10000:
        return JsonResponse({'error': 'Maximum 10,000 characters.'}, status=400)
    return JsonResponse({'hash': digest(text)})
