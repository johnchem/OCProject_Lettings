from django.contrib import admin

from lettings.models import Letting
from lettings.models import Address
from profiles.models import Profile

# add the 3 models to the admin site
admin.site.register(Letting)
admin.site.register(Address)
admin.site.register(Profile)
