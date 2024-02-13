import logging
from django.shortcuts import render
from django.http import Http404
from lettings.models import Letting


# Create your views here.

# Aenean leo magna, vestibulum et tincidunt fermentum, consectetur quis velit.
# Sed non placerat massa. Integer est nunc, pulvinar a
# tempor et, bibendum id arcu. Vestibulum ante ipsum primis infaucibus
# orci luctus et ultrices posuere cubilia curae; Cras eget scelerisque
def index(request):
    """Display all the lettins instance in the database

    :param lettings_list: All instance of :class:`lettings.Lettings`.
    :type lettings_list: list(:class:`lettings.Lettings`)
    :param template: `lettings/index.html`

    :return: the httpResponse filled with appropriate data
    :rtype: HttpResponse

    :raises exc Http404: Send page 404 if Letting is not found :exc:`Letting.DoesNotExist`
    :raises ext Exception: If any other issue append during the retreving of the letting
    """
    try:
        lettings_list = Letting.objects.all()
        context = {'lettings_list': lettings_list}

    except Exception as e:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.exception(f"User {user_identity} get an exception {e}")

    return render(request, 'lettings/index.html', context)


# Cras ultricies dignissim purus, vitae hendrerit ex varius non. In accumsan
# porta nisl id eleifend. Praesent dignissim, odio eu consequat pretium,
# purus urna vulputate arcu, vitae efficitur lacus justo nec purus.
# Aenean finibus faucibus lectus at porta. Maecenas auctor, est ut luctus congue,
# dui enim mattis enim, ac condimentum velit libero in magna. Suspendisse potenti.
# In tempus a nisi sed laoreet. Suspendisse porta dui eget sem accumsan interdum.
# Ut quis urna pellentesque justo mattis ullamcorper ac non tellus.
# In tristique mauris eu velit fermentum, tempus pharetra est luctus.
# Vivamus consequat aliquam libero, eget bibendum lorem. Sed non dolor risus.
# Mauris condimentum auctor elementum. Donec quis nisi ligula. Integer vehicula
# tincidunt enim, ac lacinia augue pulvinar sit amet.
def letting(request, letting_id):
    """Display the letting instance selected by user throught its letting_id

    :param string title: The title of :class:`lettings.Letting`
    :param address: The address :class:`lettings.Address`
    :param address: linked to the instance :class:`lettings.Letting`
    :type address: :class:`lettings.Address`
    :param template: `lettings/letting.html`

    :return: the httpResponse filled with appropriate data
    :rtype: HttpResponse

    :raises exc Http404: Send page 404 if Letting is not found :exc:`Letting.DoesNotExist`
    :raises exc Exception: If any other issue append during the retreving of the letting
    """
    try:
        letting = Letting.objects.get(id=letting_id)
        context = {
            'title': letting.title,
            'address': letting.address,
        }

    except Letting.DoesNotExist:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.error(f"User {user_identity} get page 404 : {request.path}")
        raise Http404

    except Exception as e:
        user_identity = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.exception(f"User {user_identity} get an exception {e}")

    return render(request, 'lettings/letting.html', context)
