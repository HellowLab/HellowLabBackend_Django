from django.contrib.sites.models import Site
site = Site.objects.get(id=1)  # Get the current site, using ID 1

site.name = 'HellowLab'  
site.domain = 'HellowLab.com' 
site.save()