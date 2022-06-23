import pygwin
from tinytag import TinyTag
from pathlib import Path
import sys
import os

frozen = getattr(sys,"frozen",False)

temp = str(Path(sys._MEIPASS))+"\\" if frozen else ""

pygwin.mixer.ffmpeg = temp+"ffmpeg.exe"

path = sys.argv[1] if frozen else "OMFG - Yeah.mp3"

tag = TinyTag.get(path)

if tag.title == None:
    title = os.path.splitext(os.path.basename(path))[0]
else:
    title = tag.title+" - "+tag.artist

win = pygwin.create(title,(300,150),icon=temp+"icon.png")
win.tray.stop()
base = pygwin.ui.base(win)

l = pygwin.ui.label(title,30,(20,20,20),font=pygwin.font.font(temp+"font.ttf"))
base.put(l,(150-l.surface.size[0]/2,10))

p = pygwin.ui.slider(200,fg=(50,200,50),bg=(25,50,25))
base.put(p,(5,50))

v = pygwin.ui.slider(200,fg=(200,200,50),bg=(75,75,25))
v.set(52)
base.put(v,(5,90))

def play():
    if b.text == "⏸":
        sound.pause()
        b.text = "▶"
    else:
        sound.resume()
        b.text = "⏸"

b = pygwin.ui.button("⏸",play,
    font=pygwin.font.font(temp+"font.ttf"),
    width=70,height=70,fontSize=50)
base.put(b,(220,60))

pos = 0

sound = pygwin.mixer.music(path)
sound.play(loops=-1)

run = True
while run:
    for event in pygwin.getEvents():
        if event.type == pygwin.QUIT:
            run = False
    base.draw()

    if not p.s:
        p.set((((pos+sound.pos/1000))/tag.duration)*94+6)
    else:
        pos = (p.get()-6)/94*tag.duration
        sound.play(-1,pos)
    sound.volume = (v.get()-6)/94

    win.update()
