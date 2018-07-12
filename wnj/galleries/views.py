import os
from io import BufferedWriter, FileIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wnj.galleries.forms import GalleryAddForm
from wnj.galleries.models import Gallery


@login_required
def gallery(request):
    context = {'images': Gallery.objects.filter(approved=True)}
    return render(request, 'galleries/gallery.html', context)


@login_required
def moments(request):
    context = {'images': Gallery.objects.filter(user=request.user)}
    return render(request, 'galleries/moments.html', context)


@login_required
def add_picture(request):
    if request.method == 'POST':
        form = GalleryAddForm(request.POST, request.FILES)
        if form.is_valid():
            img = _upload_image(request.FILES['image'], request.user.email)
            Gallery.objects.create(user=request.user, image=img)
            return HttpResponseRedirect('/moments/')
        else:
            import pprint; pprint.pprint(form.errors)
            context = {'form': form}
    else:
        context = {'form': GalleryAddForm()}
    return render(request, 'galleries/gallery_add.html', context)


def _upload_image(file_, user_):
    user_path = ''.join([user_.replace('@', '_').replace('.', '_'), '/'])

    if not settings.AWS_STORAGE_BUCKET_NAME:
        media_user_path = os.path.join(settings.MEDIA_ROOT, user_path)
        if not os.path.exists(media_user_path):
            os.makedirs(media_user_path)
        path_picture = os.path.join(settings.MEDIA_ROOT, file_.name)
        with BufferedWriter(FileIO(path_picture, "w")) as destiny:
           for c in file_.chunks():
               destiny.write(c)
    else:
        write_destiny = ''.join([user_path, file_.name])
        fl = default_storage.open(write_destiny, 'w')
        fl.write(file_.read())
        fl.close()
        path_picture = ''.join([settings.MEDIA_ROOT, write_destiny])

    return path_picture
