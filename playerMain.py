from tkinter import *
from tkinter import filedialog
import pygame

root = Tk() # Main window
root.minsize(400, 400) # size of window
label = Label(root, text = "Music PLayer") # text label
label.pack() 
listbox = Listbox(root)  # text box to show list of songs
listbox.pack()

pygame.mixer.init()

fileName = ""
playlist = [] # to store list of songs
index = 0 # global index to handle playlist
pauseFlag = 1 # global flag to check pause
initPlay = 0

def playSong(event):
    global pauseFlag
    if pauseFlag == 1:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(type)

def pauseSong(event):
    global pauseFlag
    pygame.mixer.music.pause()
    pauseFlag=1

def stopSong(event):
    pygame.mixer.music.stop()

def nextSong(event):
    global index, playlist, pauseFlag
    pauseFlag = 0
    index += 1
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()

def prevSong(event):
    global index, playlist, pauseFlag
    pauseFlag = 0
    index -= 1
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()

def browseSong(event):
    global index, playlist, fileName, initPlay
    root.filename = filedialog.askopenfilename(initialdir="/home/toor/Downloads", title="Select file", filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
    fileName = root.filename
    playlist.append(fileName)
    songName=fileName.split("/")
    listbox.insert(END, songName[-1])
    if index == 0 and initPlay == 0:
        pygame.mixer.music.load(playlist[index])
        initPlay = 1
        pygame.mixer.music.play()

playButton = Button(root, text = "Play")
playButton.pack()
pauseButton = Button(root, text="Pause")
pauseButton.pack()
stopButton = Button(root, text="stop")
stopButton.pack()
nextButton = Button(root, text="Next")
nextButton.pack()
prevButton = Button(root, text="Previous")
prevButton.pack()
browseButton = Button(root, text = "Browse")
browseButton.pack()

playButton.bind("<Button-1>", playSong)
pauseButton.bind("<Button-1>", pauseSong)
stopButton.bind("<Button-1>", stopSong)
nextButton.bind("<Button-1>", nextSong)
prevButton.bind("<Button-1>", prevSong)
browseButton.bind("<Button-1>", browseSong)

root.mainloop()
