import customtkinter as ctk
import tkinter as tk
import pygame
import os
import time
import math

def on_select(event):
    global choosensong
    global runningsong
    global isplaying
    choosensong = event.widget.get(event.widget.curselection())
    if(choosensong!=runningsong):
        play.pack_forget()
        pause.pack()
        isplaying=True
        pygame.mixer.music.load(choosensong)
        pygame.mixer.music.play()
        runningsong=choosensong

def newfolder():
    global choosensong
    directory=tk.filedialog.askdirectory()
    songs=os.listdir(directory)
    os.chdir(directory)
    songindex=0
    listbox.delete(0,tk.END)
    for i in songs:
        name,ext=os.path.splitext(i)
        if(ext=='.mp3'):
            listbox.insert(tk.END,i)
            songlist.insert(songindex,i)
            songindex+=1
    listbox.bind("<<ListboxSelect>>", on_select)

def volumefnc(value):
    pygame.mixer.music.set_volume(value)


def playbtnclick():
    play.pack_forget()
    pause.pack()
    global runningsong
    global choosensong
    global isplaying
    isplaying=True
    choosensong=listbox.get(tk.ACTIVE)
    if((runningsong!="")and(choosensong==runningsong)):
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.load(choosensong)
        pygame.mixer.music.play()
        runningsong=choosensong

def pausebtnclick():
    pause.pack_forget()
    play.pack()
    pygame.mixer.music.pause()
    isplaying=False

def prevbtnclick():
    choosensong=listbox.get(tk.ACTIVE)
    curindex=songlist.index(choosensong)
    if(isplaying):
        play.pack_forget()
        pause.pack()
    if(curindex==0):
        previndex=len(songlist)-1
    else:
        previndex=curindex-1
    listbox.selection_set(previndex)
    listbox.selection_clear(curindex)
    listbox.activate(previndex)
    choosensong=songlist[previndex]
    pygame.mixer.music.load(choosensong)
    pygame.mixer.music.play()
    runningsong=choosensong

def nextbtnclick():
    choosensong=listbox.get(tk.ACTIVE)
    curindex=songlist.index(choosensong)
    if(isplaying):
        play.pack_forget()
        pause.pack()

    if(curindex==len(songlist)-1):
        nextindex=0
    else:
        nextindex=curindex+1
    listbox.selection_set(nextindex)
    listbox.selection_clear(curindex)
    listbox.activate(nextindex)
    choosensong=songlist[nextindex]
    pygame.mixer.music.load(choosensong)
    pygame.mixer.music.play()
    runningsong=choosensong


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(1)
ctk.set_window_scaling(4)

pygame.mixer.init()
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
interface=ctk.CTk()
interface.title("Music Player")
interface.geometry("200x140")


frame=ctk.CTkFrame(master=interface)
frame.place(relx=0,rely=0,relheight=0.85,relwidth=1)

songlistframe=ctk.CTkFrame(master=frame,width=100)
songlistframe.place(relx=0,rely=0,relheight=1,relwidth=0.3) 

scroll=ctk.CTkScrollbar(master=songlistframe)
scroll.pack(side=ctk.RIGHT,fill=ctk.Y)

listbox=tk.Listbox(master=songlistframe,bg="#202124",fg="cyan",font=ctk.CTkFont(size=25))
listbox.pack(side="left",fill="both",expand=True)

listbox.config(yscrollcommand=scroll.set)
scroll.configure(command=listbox.yview)

runningsong=""
choosensong=""
songlist=[]
isplaying=False

bgimage=tk.PhotoImage(file="images/music.png")
playerframe=tk.Frame(master=frame,bg="cyan")
playerframe.place(relx=0.3,rely=0,relheight=1,relwidth=0.7)
bglabel=tk.Label(master=playerframe,image=bgimage)
bglabel.place(relheight=1,relwidth=1)


btnframe=tk.Frame(master=interface,bg="cyan",borderwidth=1,relief="solid")
btnframe.place(relx=0,rely=0.85,relwidth=1,relheight=0.15)

speakerframe=tk.Frame(master=btnframe,bg="cyan")
speakerframe.place(relx=0.85,rely=0.5,anchor="center")

speakerimg=tk.PhotoImage(file="images/speaker.png")
speakerlabel=tk.Label(master=speakerframe,image=speakerimg,bg="cyan",width=50)
speakerlabel.grid(row=0,column=0)

slidervolume=ctk.CTkSlider(master=speakerframe,command=volumefnc)
slidervolume.grid(row=0,column=1)

playbtn=tk.PhotoImage(file="images/play.png")
pausebtn=tk.PhotoImage(file="images/pause.png")
nextbtn=tk.PhotoImage(file="images/next.png")
prevbtn=tk.PhotoImage(file="images/prev.png")

rdobtnframe=tk.Frame(master=btnframe,bg="cyan")
rdobtnframe.place(relx=0.5,rely=0.5,anchor="center")

prevframe=ctk.CTkFrame(master=rdobtnframe)
prevframe.grid(row=1,column=3,columnspan=2,padx=(45,0),pady=5)

playpauseframe=ctk.CTkFrame(master=rdobtnframe)
playpauseframe.grid(row=1,column=5,columnspan=2,padx=(45,0),pady=5)

nextframe=ctk.CTkFrame(master=rdobtnframe)
nextframe.grid(row=1,column=7,padx=(45,),pady=5)

prev=tk.Button(master=prevframe,command=prevbtnclick,image=prevbtn,borderwidth=0,bg="cyan")
prev.pack()

pause=tk.Button(master=playpauseframe,command=pausebtnclick,image=pausebtn,borderwidth=0,bg="cyan")

play=tk.Button(master=playpauseframe,command=playbtnclick,image=playbtn,borderwidth=0,bg="cyan")
play.pack()

next=tk.Button(master=nextframe,command=nextbtnclick,image=nextbtn,borderwidth=0,bg="cyan")
next.pack()

addfolderbtn=tk.PhotoImage(file="images/addfolder.png")
newfolderbtn=tk.Button(master=btnframe,image=addfolderbtn,command=newfolder,borderwidth=0,bd=2.5,highlightcolor="#FFA500",bg="cyan",fg="cyan")
newfolderbtn.place(relx=0.12,rely=0.35)



interface.mainloop()