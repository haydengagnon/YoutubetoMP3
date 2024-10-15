# Youtube to MP3 Converter Web Application
  This web app allows users to convert youtube to mp3 files. Authorized users are able to download and post their mp3 files while unauthorized users are only able to download their mp3 files.

# Distinctiveness and Complexity:
  While this project's layout shares some similarities with the social media web app, I believe that the rest of the content and functionality steers far enough away from the social media app to be considered its own distinct app. In each post I had to handle users being able to download mp3 files as well as playing them so they can listen before they decide to download the file. This is the first project I had to use python's file management capabilities. I had to save the mp4 file to the server, have that converted into an mp3 using the ffmpeg library, then delete the mp4 as it isn't needed anymore, and then it would branch with what happens from there depending on if the user is signed in or not. If the user wasn't signed in then the mp3 file would start downloading as soon as the conversion is done and a timer would start using javascript based on the size of the file. Once the timer runs out it deletes the mp3 file as it won't be needed anymore since a user that isn't signed in can't post their mp3. If a user is signed in the file stays downloaded on the server so that if the user decides to post it, other users will be able to download it later. After a user posts an mp3, other users are able to download those files as well as being able to listen to a preview of the file. I had to make a dynamic sliders using javascript that tracks how far into the mp3 file the user is while listening as well as allowing the user to drag the slider to different parts of the song to change where they are. Because all of these things are something that I haven't used in any of the other projects and required me to learn new things on my own I feel that the distinctiveness and complexity of this project are satisfactory for this capstone project.

# File Contents
## views.py
### index(request)
  The index view is simple, it has button that will send the user to convert a youtube video to mp3 and displays the five most recent mp3 posts.

### login_view(request)
  The login view is a standard login page, it allows existing users to login using their username and password then redirects them to the home page.

### logout_view(request)
  Simply logs the user out and returns them to the home page.

### register(request)
  Standard registration page that allows a user to make a new account for posting mp3 files on the web app.

### browse_mp3(request)
  Displays and paginates all mp3 posts as well as having a search bar that allows users to search for specific mp3 titles.

### profile(request, username)
  Displays all mp3 files posted by a specific user

### convert_to_mp3(mp4_url, user_filename=None)
  The function that converts the youtube url into an mp3 file. Uses pytube and ffmpeg libraries to achieve this. This function takes in a url and filename from a form that is filled out by the user. If the user leaves the filename blank it fills in the filename with the title of the youtube video. It starts by taking in the url using YouTube from pytube and then grabs the audio stream from the youtube video. After that it sets the output folder to the media folder within the server file tree. Then the filename and file path are set. Next the mp3 filepath is set by replacing the ".mp4" with ".mp3". The function then checks if the file already exists and if the file does already exist it will rename the file to the same name with n at the end of it, where n is the amount of files with that name that already exist. For example if there is a FeelSomething.mp3, FeelSomething1.mp3, and FeelSomething2.mp3, if the user names their file FeelSomething.mp3 it will change the name to FeelSomething3.mp3. After the name is set for the file I use ffmpeg to input the mp4 file and output the mp3 file. After this the mp4 file is removed and the function returns the mp3 file path.

### convert(request)
  This is the page where a user submits their youtube video to be converted. The url and filename are inputted by the user to be used in the convert_to_mp3 function. After this, as long as the file path exists, the file url and size are assigned values and sent to the post_mp3 page if the user is signed in or sent to a jsonresponse of the user is not signed in. A signed in user will be able to download and/or post their mp3 while a user who isn't signed in will have the file downloaded to their computer as soon as the conversion is done.

### post_mp3(request, mp3_file_url)
  Post mp3 is what allows users to post their mp3 to the app if they are signed in. When a user decides to post their mp3 it saves its data to the MP3File database model. Thiis data is the user who posted the mp3, the file path, the title, the file size, and that the mp3 has been posted. After posting the user is redirected to the home page.

### remove_last(string, number)
  The remove_last function is a function that I created to remove the last n letters from a string. I used this to remove the .mp3 and .mp4 extensions while looping through the titles of the mp3 if it was a duplicate title.

### delete_file(request)
  This is a function used to delete a file. I used this in my convert view and it's called through my JavaScript when unauthorized users convert their youtube url to an mp3 it deletes the file after it's downloaded.

## urls.py
  Contains my urlpatterns for the converter app as well as adding the path for my media files to my project.

## models.py
  Contains the standard User model as well as an MP3File to contain information about posted mp3 files.

## admin.py
  Has Users and MP3Files listed so that an admin can acess both of these databases if needed.

## register.html
  Contains the form registering a new user account.

## prompt_post.html
  The page that authorized users are directed to that allows them to download and/or post their mp3 after converting it.

## profile.html
  Displays the user and all mp3 files that they have posted.

## login.html
  Contains the form that allows users to login to their account using their username and password.

## layout.html
  loads all of the static files for the project as well as having the navbar for every page.

## index.html
  Has a large button to direct users to the correct place for converting a youtube url into an mp3 as well as containing the five most recent posted mp3 files.

## convert.html
  Contains the form that allows users to convert their youtube url into an mp3 file. The form has a place for the user to put in the url as well as place for naming their file. If they choose not to name the file it takes the title of the youtube video as its name.

## browse.html
  The browse page has a search bar where users are able to search for mp3 files by title at the top of it. Below the search bar users can browse all posted mp3 files in reverse chronological order. These are paginated with five mp3 files per page.

## style.css
  This is my stylesheet that I used to make my app look presentable and easy on a users eyes as well as making it easier to navigate the page.

## index.js
  My javascript file starts out by waiting until the DOM content is loaded. The first portion of my index.js is for the convert form when a user submits that what url and title they want to use for conversion. If the user is signed in it sends them to the post_mp3 page but if the user isn't signed in it will download their file once the conversion is complete, followed by the deletion of the file to save some storage space on the server. The deletion of the file is based on a timer that is set depending on the size of the file. 1Mb = 1 second on the timer, which gives almost all internet connections ample time to complete the download before the file is deleted from the server.
  The next function is for the download button and it works by creating a link with download path to .mp3 file, then clicking the link to start the download, and finally the link is removed before the end of the function.
  The last function in my index.js is for the play/pause button on each mp3 post. These buttons allow the user to play the audio of each file as well as moving to any point in the audio using a slider. The play and pause button are made entirely using css and clicking the button causes the css to change depending on whether or not the audio is playing or not. These buttons also keep track of the currently playing mp3 and will pause an mp3 and reset its slider if a new mp3 audio starts playing. This script also allows the slider to move as the audio is played as well as displaying a timer that displays the current time / total time.

# How to run the Converter App
1. Download python https://www.python.org/downloads/
2. Download pip https://pip.pypa.io/en/stable/installation/
3. Install Django by running "pip install Django"
4. Download Source Code
5. Unzip Source Code
6. In any terminal change your directory to project folder (MP4toMP3)
7. After getting to that folder run: python manage.py runserver
8. Open any web browser and go to localhost (127.0.0.1)
