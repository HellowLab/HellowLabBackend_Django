from django.contrib.sites.models import Site
site = Site.objects.get(id=1)  # Assuming your site's ID is 1
site.domain = 'HellowLab.com'  # Replace 'example.com' with the desired domain
site.save()