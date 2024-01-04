import pytest
from django.urls import reverse, resolve
from lettings.models import Letting, Address


class TestLettingsUrl:
    """
    Test for the letting application's urls

    :function: test_letitng_index_url
    :function: test_letting_detail_url
    """
    def test_letting_index_url(self):
        path = reverse('lettings_index')
        assert path == "/lettings/"
        assert resolve(path).view_name == "lettings_index"

    def test_letting_detail_url(self):
        path = reverse('letting', kwargs={'letting_id':1})
        assert path == "/lettings/1/"
        assert resolve(path).view_name == "letting"

@pytest.mark.django_db
class TestLettingsModels:
    def test_create_address(self, client):
        """
        test the creation of a new address with correct data
        """
        pass

    def test_create_letting(self, client):
        """
        test the creation of a new letting with correct data
        """
        pass

    def test_validator_address(self, client):
        """
        test the error message when incorrect data are provided
        **data : **
            number [int] : 0> int > 9999
            state [str] : length = 2
            zip_code [int] : 0> int > 9999
            country_iso_code [str] : length = 3
        """
        pass

    def test_delete_letting(self, client):
        """
        Test the deletion of a letting, this must also delete the linked address
        """
        pass

class TestLettingsView:
    pass

