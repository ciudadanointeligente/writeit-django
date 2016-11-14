

def get_api_url_for_person(person):
    from django.contrib.sites.models import Site
    from rest_framework.reverse import reverse
    from urlparse import urljoin
    current_site = Site.objects.get_current()
    api_url = urljoin('http://' + current_site.domain, reverse('person-detail', kwargs={'pk': person.id}))
    if api_url.endswith('/'):
        api_url = api_url[:-1]
    return api_url
