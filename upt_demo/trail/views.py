from django.shortcuts import render, get_object_or_404
from .models import Trail

# Create your views here.


def trail_main_view(request, id):
    #queryset = Trail.objects.all() # list of objects
    queryset = get_object_or_404(Trail, id=id)
    # current_user = request.user.username
    context = {
        "object": queryset,
        }
    print(context)
    return render(request, "trail/trail_main.html", context)



