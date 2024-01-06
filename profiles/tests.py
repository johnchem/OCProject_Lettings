import re
import pytest
from bs4 import BeautifulSoup
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, resolve

from profiles.models import Profile
from django.contrib.auth.models import User

@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db_profile_test.json')

class TestProfilesUrl:
    """
    Test for the Profiles application urls

    :function: test_profiles_index_url
    :function: test_profiles_detail_url
    """
    def test_profiles_index_url(self):
        path = reverse("profiles_index")
        assert path == "/profiles/"
        assert resolve(path).view_name == "profiles_index"

    def test_profiles_detail_url(self):
        path = reverse("profile", kwargs={'username':"AirWow"})
        assert path == "/profiles/AirWow/"
        assert resolve(path).view_name == "profile"

@pytest.mark.django_db
class TestProfilesModels:
    """
    Test for the Profiles application's model
    
    :function: test_create_user
    :function: test_create_profiles
    :function: test_delete_user
    """
    def test_create_user(self, client):
        """
        Test for the creation of a new user.
        the data of the instance are checked against 
        the initial data
        """
        password = "Abc1234!"
        username = "Paulo1234"
        first_name = "paul"
        last_name = "test"
        email = "paul@test.com"
        user = User.objects.create(
            password = password,
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        assert user.username == username
        assert user.first_name == first_name
        assert user.last_name == last_name

    def test_create_profiles(self, client, capsys):
        """
        Test the creation of a new profile
        A new user is created then feed for the creation 
        of the new profile.
        the instance informantion are evaluated against the 
        initial data for the user and the profile
        """
        password = "Abc1234!"
        username = "Paulo1234"
        first_name = "paul"
        last_name = "test"
        email = "paul@test.com"
        user = User.objects.create(
            password = password,
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email
        )

        favorite_city = "Las Vegas"
        profile = Profile.objects.create(
            user = user,
            favorite_city = favorite_city
        )
        print(profile)
        captured = capsys.readouterr()
        assert captured.out == username+"\n"
        assert profile.favorite_city == favorite_city
        assert profile.user.username == username

    def test_delete_user(self, client):
        """
        Test the deletion of a user,
        this must lead to the deletion of the linked profile
        """
        profile = Profile.objects.get(id=1)
        user = profile.user
        del_info = user.delete()
        with pytest.raises(ObjectDoesNotExist) as exc_info:
            Profile.objects.get(id=1)

        assert del_info[0] == 2
        assert exc_info.value.args[0] == "Profile matching query does not exist."

@pytest.mark.django_db
class TestProfilesView:
    """
    Test for the Profiles application's view
    
    :function: test_profiles_index_view
    :function: test_profiles_detail_view
    """
    def test_profiles_index_view(self, client):
        """
        Test the elements displayed by the view 
        with the name of the letting elements in the database
        The database is pre-load with the data in fixtures/db_profile_test.json
        """
        expected_list = [
            'HeadlinesGazer',
            'DavWin',
            'AirWow',
            '4meRomance',
            ]
        path = reverse('profiles_index')
        resp = client.get(path)
        soup = BeautifulSoup(resp.content, features="html.parser")
        list_letting = [x.string for x in soup.find_all("a", href=re.compile("/profiles/\w+"))]
        
        assert len(list_letting) == 4
        for x in list_letting:
            assert x in expected_list

    def test_profiles_detail_view(self, client):
        expected_data = [
            'First name : Ada',
            'Last name : Paul',
            'Email : flocation.vam4@glendenningflowerdesign.com',
            'Favorite city : Budapest'
            ]
        
        path = reverse('profile', kwargs={'username':"AirWow"})
        resp = client.get(path)
        soup = BeautifulSoup(resp.content, features="html.parser")
        card = soup.find("div", "card-body")
        result = [x.get_text() for x in card.find_all("p")]
        
        for data, expected in zip(result, expected_data):
            assert data == expected
    
    def test_letting_not_found(self, client):
        """
        Test to get the detail of a profile who doesn't 
        exist. Expect to receive a page 404 
        """
        path = reverse('profile', kwargs={'username':"NotExistUser"})
        resp = client.get(path)
        assert resp.status_code == 404