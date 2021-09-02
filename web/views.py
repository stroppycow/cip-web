from django.http import HttpResponse
from django.template import loader

def consulter_index_profession(request):
    template = loader.get_template('web/index_profession.html')
    return HttpResponse(template.render({}, request))