from django.core.exceptions import ObjectDoesNotExist, ValidationError
import pytest
from django.core.management import call_command
from django.urls import reverse, resolve
from lettings.models import Letting, Address
from lettings.fixtures.test_validators import data_validator_address


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db_test.json')

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
        number = 11
        street = "West 53 Street"
        city = "Manhattan"
        state = "NY"
        zip_code = 10019
        country_iso_code = "USA"
        address = Address.objects.create(
            number = number,
            street = street,
            city = city,
            state = state,
            zip_code = zip_code,
            country_iso_code = country_iso_code,
        )
        assert address.street == street
        assert address.state == state
        assert address.zip_code == zip_code

    def test_create_letting(self, client):
        """
        test the creation of a new letting with correct data
        """
        address_ref = Address.objects.create(
            number = 11,
            street = "West 53 Street",
            city = "Manhattan",
            state = "NY",
            zip_code = 10019,
            country_iso_code = "USA",
        )
        title = "Museum of Modern Art"
        address = address_ref.pk

        letting = Letting.objects.create(
            title = title,
            address = address_ref
        )
        assert letting.title == title
        assert letting.address.street == "West 53 Street"

    @pytest.mark.parametrize(
            "address_data,error_message",
            data_validator_address,
            ids=["number", "state","zip_code","iso_code"]
            )
    def test_validator_address(self,address_data,error_message):
        """
        test the error message when incorrect data are provided
        **data : **
            number [int] : 0> int > 9999
            state [str] : length = 2
            zip_code [int] : 0> int > 9999
            country_iso_code [str] : length = 3
        """
        address = Address.objects.create(**address_data)
        with pytest.raises(ValidationError) as exc_info:
            address.full_clean()
        assert exc_info.type is ValidationError
        assert exc_info.value.messages[0] == error_message

    @pytest.mark.django_db(transaction=True)
    def test_delete_address(self, client):
        """
        Test the deletion of a letting, this must also delete the linked address
        """
        letting = Letting.objects.get(id=1)
        address = letting.address
        del_info = address.delete()
        with pytest.raises(ObjectDoesNotExist) as exc_info:
            Letting.objects.get(id=1)

        assert del_info[0] == 2
        assert exc_info.value.args[0] == "Letting matching query does not exist."

class TestLettingsView:
    pass

