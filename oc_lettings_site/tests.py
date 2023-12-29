from django.http import HttpResponseServerError, Http404
from django.test import SimpleTestCase, override_settings
from django.urls import path

def page_not_found_view(request):
    raise Http404

def server_error_view(request):
    raise HttpResponseServerError(request, status = 500)

urlpatterns = [
    path("404/", page_not_found_view),
    path("500/", server_error_view),
]

handler404 = "oc_lettings_site.views.page_not_found"
handler500 = "oc_lettings_site.views.server_error"

@override_settings(ROOT_URLCONF="oc_lettings_site.urls")
class CustomErrorHandlerTests(SimpleTestCase):
    def test_handler_renders_404_response(self):
        response = self.client.get("404/")
        # Make assertions on the response here. For example:
        print(response)
        self.assertContains(response, "We’re sorry, but the requested page could not be found.", status_code=404)

    def test_handler_renders_500_response(self):
        response = self.client.get("/500/")
        print(response)
        # Make assertions on the response here. For example:
        self.assertContains(response, "There’s been an error.", status_code=500)