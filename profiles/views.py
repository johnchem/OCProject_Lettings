import logging
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from profiles.models import Profile

# Create your views here.


# Sed placerat quam in pulvinar commodo. Nullam laoreet consectetur ex, sed consequat libero
# pulvinar eget. Fusc faucibus, urna quis auctor pharetra, massa dolor cursus neque, quis
# dictum lacus d
def index(request):
    """
    Display all the profile instances in the database

    **Context :**

    ``profiles_list``
        All instance of :model:`profiles.Profile`.

    **Template :**

    :template:`profiles/index.html`
    """
    try:
        profiles_list = Profile.objects.all()
        context = {'profiles_list': profiles_list}

    except Exception as e:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.exception(f"User {user_identity} get an exception {e}")

    return render(request, 'profiles/index.html', context)


# Aliquam sed metus eget nisi tincidunt ornare accumsan eget lac
# laoreet neque quis, pellentesque dui. Nullam facilisis pharetra vulputate. Sed tincidunt,
# dolor id facilisis fringilla, eros leo tristique lacus, it. Nam aliquam dignissim congue.
# Pellentesque habitant morbi tristique senectus et netus et males
def profile(request, username):
    """
    Display the profile instance selected by user throught its username

    **Context :**

    ``profile``
        an instance of :model:`profiles.Profile`

    **Template :**

    :template:`profiles/profile.html`
    """
    try:
        profile = Profile.objects.get(user__username=username)
        context = {'profile': profile}

    except Profile.DoesNotExist:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.error(f"User {user_identity} get page 404 : {request.path}")
        raise Http404
    
    except Exception as e:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.exception(f"User {user_identity} get an exception {e}")

    return render(request, 'profiles/profile.html', context)