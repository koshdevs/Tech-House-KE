from django.shortcuts import render


def csrf_failure(request, *args, **kwargs):
    
    
    return render(request, 'csrf_failure.html')