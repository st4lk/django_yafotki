# coding: utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .storage import YFStorage

@csrf_exempt
@require_POST
def upload_photos(request):
    if not request.FILES.getlist("file") or not len(request.FILES.getlist("file")):
        return HttpResponse("No file", status=400)

    uploaded_file = request.FILES.getlist("file")[0]
    url = YFStorage().save('image', uploaded_file)

    return HttpResponse('<img src="%s">' % url, mimetype="text/html")
