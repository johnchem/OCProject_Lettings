import random
import pytest
import re
from bs4 import BeautifulSoup
from django.http import Http404
from django.urls import include, path, reverse, resolve
from django.core.management import call_command
from django.shortcuts import render

@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db_test_site.json')

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
        soup = BeautifulSoup(response.content, features="html.parser")

        re_msg = re.compile("We’re sorry, but the requested page could not be found.")
        
        assert response.status_code == 404
        assert soup.body.find(string=re_msg)
        
    def test_handler_render_500_response(self, client):
        """Test the page received after raising an error 500"""
        response = client.get("/500/")
        soup = BeautifulSoup(response.content, features="html.parser")

        re_msg = re.compile("There’s been an error.")

        assert response.status_code == 500
        assert soup.body.find("p", string=re_msg)

### Test the urls ###
class TestSiteUrl:
    def test_root_url(self):
        path = reverse('index')
        assert path == "/"
        assert resolve(path).view_name == "index"

### Test the views ###
@pytest.mark.django_db
class TestSiteView:
    def test_index_view(self, client):
        url = reverse("index")
        resp = client.get(url)
        soup = BeautifulSoup(resp.content, features="html.parser")

        title = "Welcome to Holiday Homes"
        re_button_profile = re.compile("Profiles")
        re_button_letting = re.compile("Letting")

        assert resp.status_code == 200
        assert title in soup.body.h1.contents 
        assert len(soup.find_all("a", string=re_button_profile)) == 2
        assert len(soup.find_all("a", string=re_button_letting)) == 2

    def test_admin_view(self, client):
        resp = client.get("/admin/")
        redirect_url = resp["Location"].split('?')[0]

        assert resp.status_code == 302
        assert redirect_url == reverse("admin:login")

    def test_connected_admin_view(self, admin_client):
        resp = admin_client.get("/admin/")
        
        assert resp.status_code == 200
        assert resp.request["PATH_INFO"] == "/admin/"
        assert resp.template_name == "admin/index.html"

@pytest.mark.django_db
class TestIntegration:
    """
    Integration test for the platform

    :function: test_navigation_customer
    """
    def test_navigation_customer(self, client):
        """
        integration test simulating a user navigating through the site

        the user start from the landing page, go to the profile page.
        he goes to a profil pick at random. Then he moves to the lettings page.
        So he pickes again at random a lettings and goes to the page.
        finally he goes back to the home page.
        """
        # connection on the landing page
        url = reverse("index")
        resp = client.get(url)
        assert resp.status_code == 200
        
        # get profile_index url from Profile button
        soup = BeautifulSoup(resp.content, features="html.parser")
        button_profile = soup.find("a", string=re.compile("Profiles"))
        url_button_profiles = button_profile.attrs["href"]
        assert resolve(url_button_profiles).view_name == "profiles_index"

        # access to profiles index
        resp = client.get(url_button_profiles)
        assert resp.status_code == 200

        # check the profile view and select a random profile
        soup = BeautifulSoup(resp.content, features="html.parser")
        list_profiles = [(x.a.string, x.a.attrs["href"]) for x in soup.div("li")]
        profil_username, profil_url = random.choice(list_profiles)
        assert len(list_profiles) == 4
        assert resolve(profil_url).view_name == "profile"

        # go to the profil page
        resp = client.get(profil_url)
        assert resp.status_code == 200
        
        # check the data
        soup = BeautifulSoup(resp.content, features="html.parser")
        username = soup.h1.string
        assert username == profil_username

        # get lettings_index url from Lettings button
        button_lettings = soup.find("a", string=re.compile("Lettings"))
        url_button_lettings = button_lettings.attrs["href"]
        assert resolve(url_button_lettings).view_name == "lettings_index"

        # access to lettings index
        resp = client.get(url_button_lettings)
        assert resp.status_code == 200

        # check the lettings view and select a random letting
        soup = BeautifulSoup(resp.content, features="html.parser")
        list_lettings = [(x.a.string, x.a.attrs["href"]) for x in soup.div("li")]
        letting_title, letting_url = random.choice(list_lettings)
        assert len(list_lettings) == 6
        assert resolve(letting_url).view_name == "letting"

        # go to the letting page
        resp = client.get(letting_url)
        assert resp.status_code == 200
        
        # check the data
        soup = BeautifulSoup(resp.content, features="html.parser")
        title = soup.h1.string
        assert title == letting_title

        # get home url from home button
        button_home = soup.find("a", string=re.compile("Home"))
        url_button_home = button_home.attrs["href"]
        assert resolve(url_button_home).view_name == "index"

        # access to lettings index
        resp = client.get(url_button_home)
        assert resp.status_code == 200