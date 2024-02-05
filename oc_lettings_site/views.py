from django.shortcuts import render
from urllib.parse import quote

from django.http import (
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token

ERROR_404_TEMPLATE_NAME = "oc_lettings_site/404.html"
ERROR_500_TEMPLATE_NAME = "oc_lettings_site/500.html"


# Lorem ipsum dolor sit amet, consectetur adipiscing elit.
# Quisque molestie quam lobortis leo consectetur ullamcorper non id est. Praesent dictum,
# nulla eget feugiat sagittis, sem mi convallis eros,
# vitae dapibus nisi lorem dapibus sem. Maecenas pharetra purus ipsum, eget consequat ipsum
# lobortis quis. Phasellus eleifend ex auctor venenatis tempus.
# Aliquam vitae erat ac orci placerat luctus. Nullam elementum urna nisi,
# pellentesque iaculis enim cursus in. Praesent volutpat porttitor magna,
# non finibus neque cursus id.
def index(request):
    """Display the main page of the site

    :param context: the context is not read in this view
    :type context: None

    :param template:`oc_lettings_site/index.html`

    :return: the httpResponse filled with appropriate data 
    :rtype: HttpResponse

    """
    return render(request, "oc_lettings_site/index.html")


def page_not_found(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    """
    404 handler.

    :param request_path: The path of the requested URL (e.g., '/app/pages/bad_page/'). It's quoted to prevent a content injection attack.
    :param template: `oc_lettings_site/404.html`
    :param exception: The message from the exception which triggered the 404 (if one was supplied), or the exception class name

    :return HttpResponseNotFound: raise exception error_404 and display the page with the template defined. 

    """
    exception_repr = exception.__class__.__name__
    # Try to get an "interesting" exception message, if any (and not the ugly
    # Resolver404 dictionary)
    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message
    context = {
        'request_path': quote(request.path),
        'exception': exception_repr,
    }
    template = loader.get_template(template_name)
    body = template.render(context, request)
    content_type = None             # Django will use 'text/html'.
    return HttpResponseNotFound(body, content_type=content_type)


@requires_csrf_token
def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    """
    500 error handler.

    :param context: the context is not read
    :type context: None

    :param template: `oc_lettings_site/500.html`

    :return HttpResponseServerError: raise exception error_500 and display the page with the template defined.

    """
    template = loader.get_template(template_name)
    return HttpResponseServerError(template.render())
