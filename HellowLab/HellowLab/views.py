from django.shortcuts import render
from django.utils import timezone

def privacy_policy(request):
    current_year = timezone.now().year
    return render(request, 'HellowLab/privacy_policy.html', {'current_year': current_year})
