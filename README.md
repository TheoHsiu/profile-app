# profile-app
Simple profile app created using Python and KivyMD

The app runs on Python 3.8.8, Kivy, and KivyMD. I used Visual Studio Code 1.84.2 on Windows 10. 
- Install Python at https://www.python.org/downloads/
- From Terminal, install Kivy and KivyMD with pip:
	"pip install kivy"
	"pip install https://github.com/kivymd/KivyMD/archive/master.zip"
- Run profile_app.py with "python profile_app.py"

Know issues:
1) "Tell us aboout yourself" display shows long texts with "..."
2) Name title is slightly higher than titles in other edit screens
3) Phone only accepts US phone numbers
4) Opening a folder with a lot of image files can be slow due to Kivy's current limitation
