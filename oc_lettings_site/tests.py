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
from django.shortcuts import render
import pytest
import re
from bs4 import BeautifulSoup
from django.http import HttpResponseServerError, Http404, HttpResponse
from django.test import SimpleTestCase, override_settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import include, path
from django.urls import reverse, resolve
from django.test import Client

@pytest.fixture()
def client():
    client = Client()
    return client

def page_not_found_view(request):
    """
    Testing view raising the error 404
    """
    raise Http404

def server_error_view(request):
    """
    Testing view raising the error 500
    """
    try:
        # Votre logique susceptible de générer une exception
        # Par exemple :
        result = 1 / 0  # Division par zéro intentionnelle pour provoquer une erreur
    except ZeroDivisionError:
        return render(request, 'oc_lettings_site/index.html', status=500)


# url for testing purpose
urlpatterns = [
    path("404/", page_not_found_view),
    path("500/", server_error_view),
    path("", include('oc_lettings_site.urls'))
]

handler404 = "oc_lettings_site.views.page_not_found"
handler500 = "oc_lettings_site.views.server_error"

@pytest.mark.urls('oc_lettings_site.tests')
@pytest.mark.django_db()
class TestCustomErrorHandler:
    """
    Class intended to test the error handling

    :function: test_handler_render_404_response()
        Call the url 404/ and expect a response with a code 400 and a defined message
    :function: test_handler_render_500_response()
        Call the url 500/ and and expect a response with a code 500 and a defined message
    """
    def test_handler_render_404_response(self, client):
        """Test the page received after raising an error 404"""
        response = client.get("404/")
        soup = BeautifulSoup(response.content)

        msg = "We’re sorry, but the requested page could not be found."
        
        assert response.status_code == 404
        assert soup.body.find(string=msg)
        
    def test_handler_render_500_response(self, client):
        """Test the page received after raising an error 500"""
        response = client.get("/500/")
        soup = BeautifulSoup(response.content)

        msg = "There’s been an error."

        assert response.status_code == 500
        assert soup.body.find(string=msg)

### Test the urls ###
@pytest.mark.urls('oc_lettings_site.tests')
@pytest.mark.django_db()
class TestSiteUrl:
    def test_root_url(self):
        path = reverse('index')
        assert path == "/"
        assert resolve(path).view_name == "index"


### Test the views ###
@pytest.mark.urls('oc_lettings_site.tests')
@pytest.mark.django_db()
class TestSiteView:
    def test_index_view(client):
        url = reverse("index")
        resp = client.get(url)
        soup = BeautifulSoup(resp.content)

        title = "Welcome to Holiday Homes"
        re_button_profile = re.compile("Profiles")
        re_button_letting = re.compile("Letting")

        assert resp.status_code == 200
        assert title in soup.body.h1.contents 
        assert len(soup.find_all("a", string=re_button_profile)) == 2
        assert len(soup.find_all("a", string=re_button_letting)) == 2

    def test_admin_view(client):
        resp = client.get("/admin/")
        assert resp.status_code == 302
        assert False