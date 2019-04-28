from tkinter import *
from time import time,sleep
from os import path
from multiprocessing import Pool,cpu_count
from random import random,randint
import gc
from enum import Enum
class colour:
  red=0
  blue=1
  green=2
  none=-1
  def randomcol():
    return [colour.red,colour.blue,colour.green][randint(0,2)]
  def gethex(col):
    return ["#ff0000","#0000ff","#00ff00"][col]#{colour.red:"#ff0000",colour.blue:"#0000ff",colour.green:"#00ff00"}[col]
class GUI:
  def __init__(self,width,height,dispw,disph,threads,ruleset):
    self.delay=0
    self.width,self.height,self.dispw,self.disph,self.threads=width,height,dispw,disph,threads
    self.ruleset=self.setruleset(ruleset)
    #print(self.ruleset)
    self.frame=tgol_frame(width,height,threads,self.ruleset)
    self.dontstop=True
    self.window=Tk()
    self.canvas=Canvas(self.window,width=dispw,height=disph,background="white")
    self.canvas.grid(row=0,column=0,rowspan=20)
    self.canvas.bind("<Button-1>",lambda event:self.changedot(event))
    self.canvas.bind("<B1-Motion>",lambda event:self.writepoint(event))
    self.canvas.bind("<B3-Motion>",lambda event:self.erasepoint(event))
    self.beginbutton=Button(self.window,width=15,text="confirm seed",command=lambda :self.setseed())
    self.beginbutton.grid(row=0,column=1)
    """self.speedlabel=Label(self.window,text="Speed:")
    self.speedlabel.grid(row=1,column=1)
    self.speedscroll=Scale(self.window,from_=1, to =100,orient="horizontal",command=lambda value:self.delayset(int(value)))
    self.speedscroll.grid(row=2,column=1)
    self.speedscroll.set(100)
    self.clearbutton=Button(self.window,text="clear",command=lambda:self.clear())
    self.clearbutton.grid(row=3, column=1)
    self.filename=Entry(self.window)
    self.filename.grid(row=4, column=1)
    self.savebut=Button(self.window,text="Save",command= lambda:self.savegame())
    self.savebut.grid(row=5, column=1)
    self.loadbut=Button(self.window,text="Load",command=lambda:self.loadgame())
    self.loadbut.grid(row=6, column=1)
    self.errorlabel=Label(self.window, text="")
    self.errorlabel.grid(row=7, column=1)"""
    self.sizelabel=Label(self.window,text="Size of grid:")
    self.sizelabel.grid(column=1,row=8)
    self.size=Scale(self.window,from_=2, to=dispw,orient="horizontal")
    self.size.bind("<ButtonRelease-1>",lambda value:self.changesize())
    self.size.grid(column=1,row=9)
    self.sizey=Scale(self.window,from_=1, to=50, orient="horizontal")
    #self.sizey.bind("<ButtonRelease-1>",lambda value:self.changesize())
    self.sizey.grid(column=1, row=10)
    self.size.set(width)
    #self.sizey.set(height)
    self.randombut=Button(self.window,text="Random",command= lambda :self.makerandom())
    self.randombut.grid(column=1,row=11)
    self.ruleset=Entry(self.window)
    self.ruleset.grid(row=12,column=1)
    self.rulesetset=Button(self.window, text="Set ruleset",command= lambda :self.frame.setruleset(self.setruleset(self.ruleset.get())))
    self.ruleset.insert(0,ruleset)
    self.rulesetset.grid(row=13,column=1)
    #self.window.mainloop()
  #def test(self):
  #  print("ajfh")
  def setruleset(self,ruleset):
    #print([set([int(x) for x in i[1:]]) for i in ruleset.split("/")])
    return [set([int(x) for x in i[1:]]) for i in ruleset.split("/")]
    
  def makerandom(self):
    self.frame.setstructure([[[random()>0.8,colour.randomcol()] for x in range(self.width)] for y in range(self.height)])
    self.drawframe()
  def changesize(self):
    self.width,self.height=self.size.get(),self.size.get()
    #pixelwidth=self.dispw/self.width if self.dispw/self.width<self.disph/self.height else self.dispw/self.width<self.disph/self.height
    #self.canvas.config(width=self.width*pixelwidth,height=self.height*pixelwidth)
    self.frame=tgol_frame(self.width,self.height,self.threads,self.setruleset(self.ruleset.get()))
    self.drawframe()
  def loadgame(self):
    if path.exists(self.filename.get()+".cnwy"):
      file=open(self.filename.get()+".cnwy","r")
      data=[[int(x) for x in i] for i in file.read().strip().split("\n")]
      self.size.set(len(data[0]))#self.width
      self.sizey.set(len(data))
      self.height=len(data)
      self.width=len(data[0])
      self.frame.setstructure(data)
      self.drawframe()
    else:
      self.errorlabel.config(text="that file doesn't exist")
  def savegame(self):
    if self.filename.get()!="":
      file=open(self.filename.get()+".cnwy","w+")
      file.write("\n".join(["".join([str(x) for x in i]) for i in self.frame.getstructure()]))
      file.close()
    else:
      self.errorlabel.config(text="please enter\na valid filename")
  def clear(self):
    self.frame.clearframe()
    self.drawframe()
  def delayset(self,value):
    self.delay=(1/value)-1/100
  def stop(self):
    self.dontstop=False
    self.beginbutton.config(text="Resume",command=lambda :self.setseed())
  def coordstogrid(self,x,y):
    return int(x//(self.dispw/self.width)),int(y//(self.disph/self.height))
  def changedot(self,event):
    x,y=self.coordstogrid(event.x%(self.dispw-1),event.y%(self.disph-1))
    self.frame.togglepoint(x,y)
    self.drawframe()
  def writepoint(self,event):
    x,y=self.coordstogrid(event.x%(self.dispw-1),event.y%(self.disph-1))
    self.frame.onpoint(x,y)
    self.drawframe()
  def erasepoint(self,event):
    x,y=self.coordstogrid(event.x%(self.dispw-1),event.y%(self.disph-1))
    self.frame.offpoint(x,y)
    self.drawframe()
  def drawframe(self):
    structure=self.frame.getstructure()
    oldstructure=self.frame.getoldstructure()
    self.canvas.delete("all")
    for y in range(self.height):
      for x in range(self.width):
        a=structure[y][x]
        if structure[y][x][0]:
          self.canvas.create_rectangle(x*(self.dispw/self.width),y*(self.disph/self.height),(x+1)*(self.dispw/self.width),(y+1)*(self.disph/self.height),width=0,fill=colour.gethex(structure[y][x][1]))#*a+"white"*(not a))#"#"+"".join([str(hex(int(1024+random()*256)))[-2:] for i in range(3)]))
  def setseed(self):
    self.beginbutton.config(text="Pause",command=lambda:self.stop())
    self.dontstop=True
    frameskip=0
    chunksize=self.height//(self.threads) if self.height//(self.threads)!=0 else self.sizey.get()
    with Pool(processes=self.threads) as p:
      while self.dontstop:
        nowtime=time()
        ttime=time()
        self.frame.advance_frame(p,chunksize)
        print("calculation time: "+str(time()-ttime))
        self.updater()
        if frameskip%self.sizey.get()==0:
          ttime=time()
          self.drawframe()
          print("framedraw: "+str(time()-ttime))
  
        frameskip+=1
        while nowtime>time()-self.delay:
          self.updater()
  def updater(self):
    self.window.update()
  def mainlooper(self):
    self.window.mainloop()
class tgol_frame:
  def __init__(self,width,height,threads,ruleset):
    self.tocheck=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    self.threads=threads
    self.setstructure([[[0,colour.none] for z in range(width)] for i in range(height)])
    self.setruleset(ruleset)
  def setruleset(self,ruleset):
    self.born,self.survives=ruleset[0],ruleset[1]
    #print("reached")
  def setstructure(self,newstructure):
    self.height=len(newstructure)
    self.width=len(newstructure[0])
    self.oldstructure=[[[0,colour.none] for z in range(self.width)] for i in range(self.height)]
    self.structure=newstructure
    #self.divisions=[int((x/self.threads)*self.width*self.height) for x in range(self.threads)]+[self.width*self.height]
  def getstructure(self):
    return self.structure
  def getoldstructure(self):
    return self.oldstructure
  def clearframe(self):
    self.structure=[[[0,colour.none] for z in range(self.width)] for i in range(self.height)]
  def togglepoint(self,x,y):
    self.structure[y][x][0]=1-self.structure[y][x][0]
  def onpoint(self,x,y):
    self.structure[y][x][0]=1
  def offpoint(self,x,y):
    self.structure[y][x][0]=0
  def advance_frame(self,pool,chsize):
    #tframe=[[0 for z in range(self.width)] for i in range(self.height)]
    #t=time()
    self.oldstructure=self.structure
    #tframe=[list(map(self.isalivenext,[[y,x]for x in range(self.width)]))  for y in range(self.height)]
    #tframe=pool.map(self.isalivenext,[[y,x] for y in range(self.height) for x in range(self.width)],(self.height*self.width)//(self.threads))
    tframe=pool.map(self.isrowalive,range(self.height),chsize)
    #tframe=pool.map(lambda x:list(map(self.isalivenext,[[y,x] for y in range(self.height)])),[x for x in range(self.width)])
    #tframe=pool.map(self.isbatchalive,[[[y,x] for x in range(self.width) for y in range(self.height)][self.divisions[i]:self.divisions[i+1]] for i in range(self.threads)])
    #tframe=[i for x in tframe for i in x]
    #tframe=[i for x in pool.map(self.isbatchalive,[[[y,x] for x in range(self.width) for y in range(self.height)][self.divisions[i]:self.divisions[i+1]] for i in range(self.threads)]) for i in x]#[i*self.width:i*self.width+self.height] for i in range(self.height)]
    #tframe=[tframe[i*self.width:i*self.width+self.height] for i in range(self.height)]
    #print(time()-t)
    self.structure=tframe
  #def isbatchalive(self,batch):
  #  return list(map(self.isalivenext,batch))
  def isrowalive(self,y):
    return list(map(self.isalivenext,[[y,x] for x in range(self.width)]))
  def isalivenext(self,coords):
    sumn=self.neighbourvalue(coords)
    centre=self.structure[coords[0]][coords[1]]        
    if centre[0] and sumn in self.survives:
      return centre#tframe[coords[1]][coords[0]]=1
    elif not centre[0] and sumn in self.born:
      return [1,self.neighbourmodecolour(coords)]#tframe[coords[1]][coords[0]]=1
    else:
      return [0,colour.none]#tframe[coords[1]][coords[0]]=0
    return 
  def neighbourvalue(self,coords):
    summ=0
    for i in self.tocheck:
      summ+=self.structure[(coords[0]+i[0])%self.height][(coords[1]+i[1])%self.width][0]
    return summ
  def neighbourmodecolour(self,coords):
    counts=[0,0,0]
    for i in self.tocheck:
      data=self.structure[(coords[0]+i[0])%self.height][(coords[1]+i[1])%self.width]
      counts[data[1]]+=data[0]
    red,blue,green=counts[0],counts[1],counts[2]
    if blue>= red:
      if green>=blue:
        return colour.green
      return colour.blue
    elif red>=green:
      return colour.red
    return colour.green
#print(cpu_count())
gui=GUI(100,100,800,800,cpu_count(),"B3/S23")
#gui.mainlooper()
#print(colour.gethex(colour.blue))
