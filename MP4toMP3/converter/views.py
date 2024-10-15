import json
import os
from pytube import YouTube
import ffmpeg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import User, MP3File

def index(request):
    mp3s = MP3File.objects.all().order_by('-uploaded_at')[:5]

    return render(request, "converter/index.html", {
        "mp3s": mp3s,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "converter/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "converter/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "converter/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "converter/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "converter/register.html")

def browse_mp3(request):
    query = request.GET.get('q')
    mp3s = MP3File.objects.all().order_by('-uploaded_at')

    if query:
        mp3s = mp3s.filter(
            Q(title__icontains=query)
        )

    paginator = Paginator(mp3s, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "converter/browse.html", {
        "mp3s": mp3s,
        "page_obj": page_obj,
        "query": query
    })

def profile(request, username):
    user = get_object_or_404(User, username=username)

    mp3s = MP3File.objects.filter(user=user).order_by('-uploaded_at')

    paginator = Paginator(mp3s, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "converter/profile.html", {
        "mp3s": mp3s,
        "mp3_user": user,
        "page_obj": page_obj
    })

def convert_to_mp3(mp4_url, user_filename=None):
    try:
        youtube = YouTube(mp4_url)
        stream = youtube.streams.get_audio_only()

        output_folder = os.path.join(settings.MEDIA_ROOT, 'converter')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


        mp4_filename = f"{user_filename or youtube.title}.mp4".replace(" ", "")
        mp4_file_path = stream.download(output_path=output_folder, filename=mp4_filename)

        mp3_file_path = mp4_file_path.replace(".mp4", ".mp3")
        if os.path.exists(mp3_file_path):
            temp = remove_last(mp3_file_path, 4)
            temp_name = remove_last(mp4_filename, 4)
            file_count = 0
            for file in os.listdir(output_folder):
                if file.startswith(temp_name):
                    file_count += 1
            mp3_file_path = temp + str(file_count - 1) + ".mp3"

        ffmpeg.input(mp4_file_path).output(mp3_file_path).run()
                 
        os.remove(mp4_file_path)
        return mp3_file_path

    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
    

def convert(request):
    if request.method == "POST":
        mp4_url = request.POST.get("mp4_url")
        user_filename = request.POST.get("filename").strip()
        mp3_file_path = convert_to_mp3(mp4_url, user_filename)

        if mp3_file_path:
            mp3_file_url = request.build_absolute_uri(settings.MEDIA_URL + 'converter/' + os.path.basename(mp3_file_path))
            file_size = os.path.getsize(mp3_file_path)
            request.session['file_size'] = file_size

            if request.user.is_authenticated:
                return redirect('post_mp3', mp3_file_url=mp3_file_url)
            else:
                return JsonResponse({"mp3_file_url": mp3_file_url, "file_size": file_size})
                
            
        return JsonResponse({"error": "Failed to convert the video. Please try again"})
    
    return render(request, "converter/convert.html")

# Save mp3 to database if user decides to post the mp3 file
@login_required
def post_mp3(request, mp3_file_url):
    if request.method == "POST" and request.user.is_authenticated:
        mp3_title = request.POST.get("mp3_title")
        file_size = request.session.get('file_size') / (1024 * 1024)
        file_size = round(file_size, 2)
        del request.session['file_size']
        if mp3_title == "None":
            name = os.path.basename(os.path.normpath(mp3_file_url))
            mp3_title = f"{name}"

        mp3_file = MP3File(user=request.user, file_path=mp3_file_url, title=mp3_title, file_size=file_size, posted=True)
        mp3_file.save()

        

        return redirect("index")
    
    else:
        mp3_title = request.POST.get("mp3_title")
        return render(request, "converter/prompt_post.html", {
                "mp3_file_url": mp3_file_url,
                "mp3_title": mp3_title
        })

def remove_last(string, number):
    result = ''

    for i in range(len(string)-number):
        result += string[i]
    return result

def delete_file(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mp3_file_url = data.get('mp3_file_url')

        file_path = os.path.join(settings.MEDIA_ROOT, 'converter', os.path.basename(mp3_file_url))
        if os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({"message": "File deleted successfully"})
        
        return JsonResponse({"error": "File not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)