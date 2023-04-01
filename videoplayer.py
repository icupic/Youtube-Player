import vlc
import sys
from tkinter import *
import pafy
import datetime




class Screen(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.parent = parent
        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def init_play(self, _source):
        # Function to start player from given source
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)
        self.player.set_hwnd(self.winfo_id())
        self.player.play()
        self.player.audio_set_mute(False)
        updateTime()
 
  
    def pause(self):
        self.player.pause()
        if self.player.is_playing()==1:
           playPause.config(image=pauseImg)
        else:
           playPause.config(image=playImg)
        
    def mute(self):
        self.player.audio_toggle_mute()
        if self.player.audio_get_mute():
            mute.config(image=unmutePic)
        else:
            mute.config(image=mutePic)
            
    def exitEverything(self):
        if "cancel" in globals():
            root.after_cancel(cancel)
        root.destroy()
        self.player.release()
        sys.exit()
        
    def set__volume(self, val):
        self.player.audio_set_volume(val)
        
    def getVideoTime(self):
        millis = self.player.get_time()
        seconds=int((millis/1000)%60)+1
        if(seconds == 60):
            seconds = 0
        minutes=int((millis/(1000*60))%60)
        hours=int((millis/(1000*60*60))%24)
        time = datetime.time(hours, minutes, seconds)
        trenutnoVrijeme["text"]=time



def openUrlWindow():
    urlWindow = Tk()
    urlWindow.title("Enter youtube URL")
    e1 = Entry(urlWindow)
    b3 = Button(urlWindow, text="GET", command= lambda: getUrl(e1, urlWindow))
    e1.pack()
    b3.pack()
    
def getUrl(e1, window):
    url = e1.get()
    if url !="":
        global best
        pafy.set_api_key("apikey")
        video = pafy.new(url)
        root.title(video.title)
        best = video.getbest()
        player.init_play(best.url)
        duzinaVidea["text"]= video.duration
        inforAboutVideo(video)
        window.destroy()
        

def volume_control(val):
     player.set__volume(int(val))

def inforAboutVideo(video):
        author.configure(text="Author: " + video.author)
        published.config(text="Published: " + video.published)
        viewcount.config(text="Viewcount: " + str(video.viewcount))
        likes.config(text="Likes: " + str(video.likes))
        dislikes.config(text="Dislikes: " + str(video.dislikes))

def downloadVideo():
    player.pause()
    best.download()
    player.pause()
  

def updateTime():
    global cancel
    player.getVideoTime()
    if duzinaVidea["text"] != trenutnoVrijeme["text"]:
        cancel = root.after(1000, updateTime)
  


#konfiguracija glavnog Tk window
root = Tk()
root.config(width=1000, bg="black")
titleImage = PhotoImage(file = "images/youtube.png")
root.iconphoto(False, titleImage)
root.title("Youtube Media Player")

#konfiguracija video player-a
player = Screen(root)
player.config(width=1000, height=500)
player.pack(fill=X)
root.protocol('WM_DELETE_WINDOW', player.exitEverything)
#meni
toolbar = Menu(root, bg="black", fg="white" )
root.config(menu=toolbar)
submenu = Menu(toolbar, tearoff=0)
toolbar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Add youtube url", command=openUrlWindow)
submenu.add_command(label="Exit", command=player.exitEverything)

#trenutno vrijeme i duzina videa
infoOVremenu = Frame(root, bg="black")
trenutnoVrijeme = Label(infoOVremenu, text="00:00:00", fg="white", font=("Arial", 16), bg="black")
duzinaVidea = Label(infoOVremenu, text="00:00:00", fg="white", font=("Arial", 16), bg="black")
trenutnoVrijeme.pack(side=LEFT)
duzinaVidea.pack(side=RIGHT)
infoOVremenu.pack(fill=X)



#kontrolni panel video player-a
controlsFrame = Frame(root, bg="black")

#kontrola jacine zvuka
volume_slider = Scale(controlsFrame, from_=0, to=200, orient = HORIZONTAL, command=volume_control, bg="red", fg="white", length=100, troughcolor="white", borderwidth=2)
volume_slider.set(100)
volume_slider.pack(side=LEFT)

#play i pause dugme
playImg = PhotoImage(file='images/play.png')
pauseImg = PhotoImage(file='images/pause.png')
playPause= Button(controlsFrame, image=playImg,  command=player.pause, bg="black", borderwidth=0, padx=50, pady=50)
playPause.pack(side=LEFT)

#mute i unmute dugme
unmutePic = PhotoImage(file='images/audio.png')
mutePic=PhotoImage(file='images/mute.png')
mute = Button(controlsFrame, text="Toggle mute", command=player.mute, image=unmutePic, bg="black", borderwidth=0)
mute.pack(side=LEFT)
controlsFrame.pack()

#download dugme

download = Button(controlsFrame, text="Download", command=downloadVideo,bg="red", fg="white" ,font=("Arial", 15))
download.pack(side=LEFT)

#informacije o video
infoOVideo = Frame(root, bg="black")
author = Label(infoOVideo, text="Author: ", fg="white",  font=("Arial", 15), bg="black")
author.pack(side=LEFT, padx=5, pady=5,fill=X)
published = Label(infoOVideo, text="Published: ", fg="white",  font=("Arial", 15), bg="black")
published.pack(side=LEFT, padx=5, pady=5,fill=X)
viewcount = Label(infoOVideo, text="Viewcount: " ,  fg="white",  font=("Arial", 15), bg="black")
viewcount.pack(side=LEFT, padx=5, pady=5,fill=X)
likes = Label(infoOVideo, text="Likes: " ,  fg="white",  font=("Arial", 15), bg="black")
likes.pack(side=LEFT, padx=5, pady=5,fill=X)
dislikes = Label(infoOVideo, text="Dislikes: ",  fg="white",  font=("Arial", 15), bg="black")
dislikes.pack(side=LEFT, padx=5, pady=5,fill=X)
infoOVideo.pack(fill=X)

root.mainloop()