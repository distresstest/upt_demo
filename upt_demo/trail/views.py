from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Trail

# Create your views here.


@login_required(login_url='/login/')
def trail_main_view(request, id=1):
    #queryset = Trail.objects.all() # list of objects
    queryset = get_object_or_404(Trail, id=id)
    # current_user = request.user.username
    context = {
        "object": queryset,
        }
    print(context)
    return render(request, "trail/trail_main.html", context)



