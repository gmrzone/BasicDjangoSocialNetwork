from django.http import HttpResponseBadRequest

def ajax_only(func):
    def wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()
    return wrapper