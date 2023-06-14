from django.http import HttpResponse as HttpResponseBase
from django.http import HttpResponseRedirect

from django.template import loader
from typing import Any


class HTTPResponseHXRedirect(HttpResponseRedirect):
    '''HTMX를 사용해 페이지를 redirect 하기 위한 클래스'''
    def __init__(self, redirect_to: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(redirect_to, *args, **kwargs)
        self["HX-Redirect"] = self["Location"]
    
    status_code = 200


class HttpResponse(HttpResponseBase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        trigger = kwargs.pop('trigger', None)
        super().__init__(*args, **kwargs)
        self.headers["HX-Trigger"] = trigger


def render(request, template_name, context=None, content_type=None, status=None, using=None, **kwargs: Any):
    content = loader.render_to_string(template_name, context, request, using=using)
    trigger = kwargs.pop('trigger', None)
    response = HttpResponse(content, content_type, status, trigger=trigger)
    return response
