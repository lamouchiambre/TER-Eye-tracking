import tkinter
from tkinter.filedialog import *
from pandas import *
from PIL import ImageTk, Image, ImageDraw, ImageFilter
import numpy
from screeninfo import get_monitors

def appartient(elt, lst):
    for e in lst:
        if e == elt:
            return True
    return False

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.division = 2.5
        self.play = False
        self.hauteur = 1920
        #1920
        self.largeur = 1080
        #1080
        self.list_ligne = []

        self.ratio = max(self.largeur / get_monitors()[0].height, self.hauteur / get_monitors()[0].width)

        self.hauteur_fenetre = int(self.hauteur/self.division)
        self.largeur_fenetre = int(self.largeur/self.division)
        taille_img = str(self.hauteur_fenetre)+"x"+str(self.largeur_fenetre+100)
        master.geometry(taille_img)
        self.rowconfigure(0, weight=20)
        self.columnconfigure(0, weight=10)
        self.create_widget()

    def demarer_ligne(self):
        self.start = True
        self.i_v = self.animation.get()
        self.animation_lines4()

    def animation_lines4(self):
        size_tab = self.tab[self.spinbox.get()]["fin"] - self.tab[self.spinbox.get()]["debut"]
        if self.i_v < (self.tab[self.spinbox.get()]["fin"]-1) and self.start:
            k = self.tableau_indice[self.i_v]
            l = self.tableau_indice[self.i_v + 1]
            self.i_v+=1
            self.animation.set(self.i_v + 1)
            self.i_actuelle = self.i_v + 1
            self.after(int((self.data["GazeEventDuration"][l])/(5)),self.animation_lines4)
        else:
             self.start = False

    def play_stop(self):
        self.i3 = self.animation.get()
        self.i2 = self.i3
        if self.play:
            self.stop()
            selfplay = False
            # text_bouton_play.set("Démarrer")
        else:
            self.demarer_ligne()
            self.play =True
            # text_bouton_play.set("Arrêter")
    
    def stop(self):
        self.start = False
        #nb_id = monCanvas.find_all()[len(monCanvas.find_all())-1]
        self.animation.set(self.i3)

    def create_widget(self):

        #-variable changeante
        self.timee = tkinter.StringVar(self)

        self.boutF = tkinter.Button(self, text = 'Utilisateur',width = 15, bg="yellow", command = self.add_file)
        self.boutF.grid(row = 0, column = 0)
        self.boutT = tkinter.Button(self, text = 'test',width = 15, bg="yellow")
        self.boutT.grid(row= 0, column = 1)
        self.monCanvas = tkinter.Canvas(self, width=self.hauteur_fenetre, height=self.largeur_fenetre, bg='ivory', bd=0, highlightthickness=0)
        self.monCanvas.grid(row = 1, column = 0, rowspan =5, columnspan = 5)
        self.boutD = tkinter.Button(self, text = "play", width =15, command=self.play_stop, activebackground="red")


        # creation du couton "ok"
        self.boutok = tkinter.Button(self, text= 'OK', width =15, command=self.bouton_ok)
        # self.timee = ""
        self.texteLabel3 = tkinter.Label(self, textvariable = self.timee)
        self.texteLabel3.grid(row = 8, column = 0)
        self.ball = self.monCanvas.create_line(0,0,0,0)


    
    def add_file(self):
        self.filepath = filepath = askopenfilename(title="Ouvrir une fichier",filetypes=[('tsv files','.tsv'),('all files','.*')])
        self.data = pandas.read_csv(filepath, sep='\t',low_memory=False)
        # tab = fichier des maps avec debut et fin
        self.tab = {}
        self.get_map()
        # print(self.tab)

        # tableau = fichier des map de l'utilisateur
        self.tableau = []
        self.tableau_heatmap = [0] * self.hauteur_fenetre
        for i in range(self.hauteur_fenetre):
            self.tableau_heatmap[i] = [0] * self.largeur_fenetre
        for i in self.tab:
            self.tableau.append(i)
        self.spinbox = tkinter.Spinbox(self, values=self.tableau)
        self.spinbox.grid(row = 0, column = 2)

        self.tableau_indice = []
        # self.tableau_indice = []
        self.tab_time = {}
        self.tableau_carte = {}
        #initialisation
        self.boutok.grid(row = 0, column = 3)
        self.i3 = self.debut_data()

    def get_map(self):
        self.i_deb = self.debut_data()
        tmp = None
        for i in range (self.i_deb, self.data["MediaName"].size) :
            if not(isnull(self.data["MediaName"][i])):
                if isnull(tmp):
                    tmp = self.data["MediaName"][i]
                    self.tab[tmp] = {}
                    self.tab[tmp]["debut"] = i+1
                    self.tab[tmp]["fin"] = None
            else:
                if not(isnull(tmp)):
                    self.tab[tmp]["fin"] = i
                    tmp = None
    

    def debut_data(self):
        i = 0
        while isnull(self.data["GazePointX (MCSpx)"][i]) or isnull(self.data["GazePointX (MCSpx)"][i]):
            i += 1
        return i
    
    def bouton_ok(self):
        self.anim_deb = self.tab[self.spinbox.get()]["debut"]
        self.anim_fin = self.tab[self.spinbox.get()]["fin"] - self.tab[self.spinbox.get()]["debut"]
        self.animation = tkinter.Scale(self, orient='horizontal', from_= 0, to=self.anim_fin, resolution=1, length=500, label='timeline', variable = self.i3, command = self.trace_ligne6)
        self.animation.grid(row=6,column=0)

        self.remplire_tableau_indice()
        # print(self.tableau_indice)
        self.i_actuelle = self.tab[self.spinbox.get()]["debut"]
        self.monCanvas.delete("all")
        self.time_deb = int(self.data["RecordingTimestamp"][self.tableau_indice[self.tableau_indice.index(self.anim_deb)]])
        
        self.boutD.grid(row= 7, column = 0)
        
        self.indice = int(self.animation.get())
        self.remplire_tableau_carte()
        # self.animation.place(x = 0, y = self.largeur_fenetre)
        self.modif_image2(self.spinbox.get())
        self.get_time_tab()
        self.timee.set("0")

    def get_time_tab(self):
        deb = self.tab[self.spinbox.get()]["debut"]
        fin = self.tab[self.spinbox.get()]["fin"]
        tmp = 0
        for i in range(deb,fin):
            if appartient(i, self.tableau_indice):
                self.tab_time[i] = tmp
            tmp += self.data["GazeEventDuration"][i]

    def modif_image2(self,var_img):
        img_fichier = "./Cartes/" + var_img[0:(len(var_img)-6)]+".jpg"
        img2 = Image.open(img_fichier)
        im_rgba = img2.copy()
        im_rgba.putalpha(128)
        name_img = "./Cartes/" + var_img[0:(len(var_img)-6)]+ "-trans.png"
        im_rgba.save(name_img)
        self.img = ImageTk.PhotoImage(Image.open(name_img).resize((int(self.hauteur/self.division), int(self.largeur/self.division))))
        self.monCanvas.create_image(0,0, image = self.img, anchor=tkinter.NW)


    def remplire_tableau_carte(self):
        i = 0
        while i < self.data["GazePointX (MCSpx)"].size:
            if not(isnull(self.data["GazePointX (MCSpx)"][i])) or not(isnull(self.data["GazePointY (MCSpx)"][i])) :
                self.tableau_carte[i] = {"x":self.data["GazePointX (MCSpx)"][i], "y":self.data["GazePointY (MCSpx)"][i]}
            i += 1
    def trace_ligne6(self,val):
        val = str( int(self.anim_deb) + int(val))
        if (appartient(int(val),self.tableau_indice)):
                if(int(val) >= self.i_actuelle):
                    i = self.tableau_indice.index(int(val))
                    k = self.tableau_indice[i]
                    l = self.tableau_indice[i + 1]
                    if (True):
                        for j in range(self.i_actuelle+1,int(val)):
                            if (appartient(j, self.tableau_indice)):
                                k_i = self.tableau_indice.index(j)
                                k_1 = self.tableau_indice[k_i]
                                k_2 = self.tableau_indice[k_i + 1]
                                self.list_ligne.append(self.monCanvas.create_line(self.data["GazePointX (MCSpx)"][k_1]/self.division,self.data["GazePointY (MCSpx)"][k_1]/self.division,self.data["GazePointX (MCSpx)"][k_2]/self.division,self.data["GazePointY (MCSpx)"][k_2]/self.division))
                                
                    self.list_ligne.append(self.monCanvas.create_line(self.data["GazePointX (MCSpx)"][k]/self.division,self.data["GazePointY (MCSpx)"][k]/self.division,self.data["GazePointX (MCSpx)"][l]/self.division, self.data["GazePointY (MCSpx)"][l]/self.division))
                    self.monCanvas.delete(self.ball)
                    
                    self.ball = self.monCanvas.create_oval((self.data["GazePointX (MCSpx)"][l]/self.division)-5,(self.data["GazePointY (MCSpx)"][l]/self.division)-5,(self.data["GazePointX (MCSpx)"][l]/self.division)+5,(self.data["GazePointY (MCSpx)"][l]/self.division)+5, fill = "red")
                    if(len(self.list_ligne)>10):
                        tmp = self.list_ligne[0]
                        del self.list_ligne[0]
                        self.monCanvas.delete(tmp)
                    
                    self.tableau_heatmap[int(self.data["GazePointX (MCSpx)"][l]/self.division)][int(self.data["GazePointY (MCSpx)"][l]/self.division)] += 1
                    self.timee.set(str(int(self.data["RecordingTimestamp"][l])-int(self.time_deb)))
                else:
                    for j in range(int(val),self.i_actuelle):
                        l = int(val)
                        if self.list_ligne != [] and appartient(j, self.tableau_indice):
                            a = self.list_ligne.pop()
                            self.monCanvas.delete(a)
                            self.monCanvas.delete(self.ball)
                            self.ball = self.monCanvas.create_oval((self.data["GazePointX (MCSpx)"][l]/self.division)-5,(self.data["GazePointY (MCSpx)"][l]/self.division)-5,(self.data["GazePointX (MCSpx)"][l]/self.division)+5,(self.data["GazePointY (MCSpx)"][l]/self.division)+5, fill = "red")
                    self.timee.set(str(int(self.data["RecordingTimestamp"][l])-int(self.time_deb)))
                self.i_actuelle = int(val)


    def remplire_tableau_indice(self):
        i = 0
        while i < self.data["GazePointX (MCSpx)"].size:
            if not(isnull(self.data["GazePointX (MCSpx)"][i])) or not(isnull(self.data["GazePointY (MCSpx)"][i])) :
                self.tableau_indice.append(i)
            i+= 1

root = tkinter.Tk()
# ritt1 = tkinter.Toplevel(root)
# ritt2 = tkinter.Toplevel(root)


listApp = []
listfen = []
i=0
def new_f():
    global i
    listApp.append(tkinter.Toplevel(root))
    listfen.append(Application(master=listApp[i]))
    # listfen[i]
    for j in range(0, i):
        print(i)
        # listApp[j].mainloop()
    i +=1

bouton = tkinter.Button(root, text = "new fenetre", width =15, command = new_f)
bouton.pack()
root.mainloop()
# app1 = Application(master=ritt1)
# app2 = Application(master=ritt2)

# app1.mainloop()
# app2.mainloop()
