from moviepy.editor import *

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Video


@csrf_exempt
def video_upload(request):
    if not request.method == 'POST':
        return HttpResponse("POST method is required ", status=405)
    video = request.FILES.get('video')
    if not video:
        return HttpResponse("Video is Required. send video in key 'video' ", status=400)

    video_extension = video.name.split('.')[-1]
    if video_extension not in ['mp4', 'mkv']:
        return HttpResponse("only .mp4 and .mkv file is supported ", status=400)
    try:
        movie = VideoFileClip(video.temporary_file_path())
        duration_sec = movie.duration
    except:
        # not a video file
        return HttpResponse("valid video file is required", status=400)

    if duration_sec > 10 * 60:  # 10 mins is 600000ms
        return HttpResponse("max 10 mins video can be uploaded ", status=400)

    if video.size >= 1073741824:  # 1GB validation
        return HttpResponse("max 1 GB video can be uploaded ", status=400)

    obj = Video()
    obj.video = video
    obj.save()
    return HttpResponse("Upload Success")


def video_list(request):
    query = Video.objects.all()
    data = []
    for i in query:
        d = {
            'id': i.id,
            'video': i.video.url,
            "created_at": i.created_at
        }
        data.append(d)
    return JsonResponse(data, safe=False)


@csrf_exempt
def calculate(request):
    if not request.method == 'POST':
        return HttpResponse("POST method is required ", status=405)

    try:
        video_size = request.POST['video_size_mb']
        video_length = request.POST['video_length_sec']
        video_type = request.POST['video_type']
    except KeyError:
        return HttpResponse("video_size_mb,video_length_sec and video_type is required", status=400)

    try:
        video_size = int(video_size)
        video_length = int(video_length)
    except:
        return HttpResponse("video_size_mb,video_length_sec are required to be numbers", status=400)

    if video_type not in ['mp4', 'mkv']:
        return HttpResponse("only .mp4 and .mkv file is supported ", status=400)

    charge = 0
    if video_size < 500:
        charge = charge + 5
    else:
        charge = charge + 12.5

    if video_length < 378:  # 6 mins 18 sec rule
        charge = charge + 12.5
    else:
        charge = charge + 20
    return HttpResponse(charge)
