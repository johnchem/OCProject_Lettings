from django.http import HttpResponseServerError, Http404
from django.test import SimpleTestCase, override_settings
from django.urls import path

def page_not_found_view(request):
    """
    Testing view raising the error 404
    """
    raise Http404

def server_error_view(request):
    """
    Testing view raising the error 500
    """
    raise HttpResponseServerError(request, status = 500)

# url for testing purpose
urlpatterns = [
    path("404/", page_not_found_view),
    path("500/", server_error_view),
]

handler404 = "oc_lettings_site.views.page_not_found"
handler500 = "oc_lettings_site.views.server_error"

@override_settings(ROOT_URLCONF="oc_lettings_site.urls")
class CustomErrorHandlerTests(SimpleTestCase):
    """
    Class intended to test the error handling

    :function: test_handler_render_404_response()
        Call the url 404/ and expect a response with a code 400 and a defined message
    :function: test_handler_render_500_response()
        Call the url 500/ and and expect a response with a code 500 and a defined message
    """
    def test_handler_render_404_response(self):
        """Test the page received after raising an error 404"""
        response = self.client.get("404/")
        self.assertContains(response, "We’re sorry, but the requested page could not be found.", status_code=404)

    def test_handler_render_500_response(self):
        """Test the page received after raising an error 500"""
        response = self.client.get("/500/")
        self.assertContains(response, "There’s been an error.", status_code=500)