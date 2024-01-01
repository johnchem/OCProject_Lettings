import pytest
from django.urls import reverse, resolve

# Create your tests here.
@pytest.mark.django_db    
class TestUrlLettings:
    def test_letting_detail_url(self):
        path = reverse('letting', kwargs={'letting_id':1})
        
        assert path == "/1"
        assert resolve(path).view_name == "infos"