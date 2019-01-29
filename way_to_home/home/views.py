"""  Generate index html page """

from django.http import HttpResponse
from django.template import loader
from django.conf import settings


def index(request):  # pylint: disable=unused-argument
    """Send index.html page on GET request"""
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'key': settings.GOOGLE_API_KEY}), content_type='text/html')
