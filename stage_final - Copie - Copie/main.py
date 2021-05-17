import tkinter
from tkinter.filedialog import *
from pandas import *
from PIL import ImageTk, Image, ImageDraw, ImageFilter
import numpy
from screeninfo import get_monitors

#selection la map correspendante au chemin
def get_map2():
    global data, tab
    i_deb = debut_data()
    tmp = None
    for i in range (i_deb, data["MediaName"].size) :
        if not(isnull(data["MediaName"][i])):
            if isnull(tmp):
                tmp = data["MediaName"][i]
                tab[tmp] = {}
                tab[tmp]["debut"] = i+1
                tab[tmp]["fin"] = None
        else:
            if not(isnull(tmp)):
                tab[tmp]["fin"] = i
                tmp = None

#retourne l'indice du debut
def debut_data():
    global data
    i = 0
    while isnull(data["GazePointX (MCSpx)"][i]) or isnull(data["GazePointX (MCSpx)"][i]):
        i += 1
    return i

def add_file():
    global filepath, data, i3, ball2, blanc, i2, boutD, boutSup, boutSuiv,boutPrec, boutAff, boutF, vitesse, tab, tableau, spinbox, taille, animation, boutOk, tab_time
    filepath = askopenfilename(title="Ouvrir une fichier",filetypes=[('tsv files','.tsv'),('all files','.*')])
    data = pandas.read_csv(filepath, sep='\t',low_memory=False)
    name.set(data["RecordingName"][2])
    #initialisation
    i3 = 0
    blanc = False
    i3 = debut_data()
    i2 = debut_data()
    time = 0
    taille = int(data["GazePointX (MCSpx)"].size)
    tab = {}
    get_map2()
    tableau = []
    for i in tab:
        tableau.append(i)
    tab_time = {}
    spinbox.destroy()
    spinbox = tkinter.Spinbox(top, values=tableau)
    if boutD is not None:
        boutD.destroy()
        print("boutD")
    if boutSup is not None:
        boutSup.destroy()
        print("sup")
    if boutPrec is not None:
        boutPrec.destroy()
        print("prec")
    if boutSuiv is not None:
        boutSuiv.destroy()
        print("suiv")
    if vitesse is not None:
        vitesse.destroy()
        print("vitesse")
    if boutAff is not None:
        boutAff.destroy()
        print("aff")

    spinbox.place(x = 20 , y = 65)
    boutOk.place(x = 30 , y = 85)


def creatF():
    top2 = tkinter.Toplevel(fenetre)
    top2.title('Utilisateur2')
    top2.geometry("500x500")

def bouton_ok():
    global animation, spinbox, data, tab, spinbox, i3, p, indice, monCanvas, ball2, largeur_fenetre, tableau_carte, i_actuelle,boutD, boutSup, boutSuiv, boutF,boutPrec, vitesse, boutAff, anim_deb, time_deb
    
    boutD = tkinter.Button(top, textvariable =text_bouton_play, width =15, command=play_stop, activebackground="red")
    boutOk = tkinter.Button(top, text='OK', width =3,height = 1, command=bouton_ok)
    boutS = tkinter.Button(top, text='Stop', width =15, command=stop)
    boutSup = tkinter.Button(top, text = 'Supprimer',width = 15, command = bouton)
    boutSuiv = tkinter.Button(top, text='Suivant',width = 15, command = suivant)
    boutPrec = tkinter.Button(top, text='Précedent',width = 15, command = precedent)
    vitesse = tkinter.Scale(top, orient='horizontal', from_=1, to=30, resolution=1, length=150, label='vitesse', variable = value)
    boutAff = tkinter.Button(top, text="HeatMap", width = 15, command = map_heatmap , activebackground="red")
    if animation is not None:
        animation.destroy()

    anim_deb = tab[spinbox.get()]["debut"]
    anim_fin = tab[spinbox.get()]["fin"] - tab[spinbox.get()]["debut"]
    animation = tkinter.Scale(fenetre, orient='horizontal', from_= 0, to=anim_fin, resolution=1, length=900, label='timeline', variable = i3, command = trace_ligne6)
    
    remplire_tableau_indice()
    i_actuelle = tab[spinbox.get()]["debut"]
    monCanvas.delete("all")
    time_deb = int(data["RecordingTimestamp"][tableau_indice[tableau_indice.index(anim_deb)]])
    
    # placement des boutons
    boutD.place(x = 30 , y = 125)
    boutSup.place(x = 30 , y = 150)
    boutSuiv.place(x = 30 , y = 175)
    boutPrec.place(x = 30 , y = 200)
    boutAff.place(x = 30 , y = 225)
    vitesse.place(x = 10 , y = 250)

    indice = int(animation.get())
    remplire_tableau_carte()
    animation.place(x = 0, y = largeur_fenetre)
    modif_image2(spinbox.get())
    get_time_tab()
    timee.set("0")
    if ball2 is not None:
        ball2.destroy()

def demarer_ligne():
    global start, monCanvas, i3, tableau_indice, i_v, animation
    start = True
    i_v = animation.get()
    animation_lines4()

def affiche_lines3():
    global data, monCanvas, division, tab, spinbox
    for i in range (tab[spinbox.get()]["debut"],tab[spinbox.get()]["fin"]-1):
        k = tableau_indice[i]
        l = tableau_indice[i+1]
        monCanvas.create_line(data["GazePointX (MCSpx)"][k]/division,data["GazePointY (MCSpx)"][k]/division,data["GazePointX (MCSpx)"][l]/division,data["GazePointY (MCSpx)"][l]/division, fill = "black", width=2)

def animation_lines4():
    global i3, animation, data, monCanvas, tab, tableau_carte, start, division, i_v, list_ligne
    size_tab = tab[spinbox.get()]["fin"] - tab[spinbox.get()]["debut"]
    if i_v < (tab[spinbox.get()]["fin"]-1) and start:
        k = tableau_indice[i_v]
        l = tableau_indice[i_v + 1]
        i_v+=1
        animation.set(i_v + 1)
        i_actuelle = i_v + 1
        fenetre.after(int((data["GazeEventDuration"][l])/(value.get())),animation_lines4)
    else:
        start = False

def zoneHeatMap(x, y, h):
    s = 0
    for i in range(x - h, x + h):
        for j in range(y - h, y + h):
            s += tableau_heatmap[i][j]
    return s

def map_heatmap():
    for i in range(5, hauteur_fenetre - 5):
        for j in range(5, largeur_fenetre - 5):
            s = zoneHeatMap(i, j, 5)
            if s > 0:
                if s > 15:
                    print(s)
                    monCanvas.create_oval(i, j, i, j, fill = "red", outline = "red")
                else:
                    if s > 10:
                        monCanvas.create_oval(i, j, i, j, fill = "orange", outline = "orange")
                    else:
                        if s > 1:
                            monCanvas.create_oval(i, j, i, j, fill = "yellow", outline = "yellow")
                        else:
                            monCanvas.create_oval(i, j, i, j, fill = "green", outline = "green")


def stop():
    global start, animation, i3
    start = False
    #nb_id = monCanvas.find_all()[len(monCanvas.find_all())-1]
    animation.set(i3)

def modif_image2(var_img):
    global data, i3, monCanvas,  img, ball2, blanc, i2
    img_fichier = "./Cartes/" + var_img[0:(len(var_img)-6)]+".jpg"
    img2 = Image.open(img_fichier)
    im_rgba = img2.copy()
    im_rgba.putalpha(128)
    name_img = "./Cartes/" + var_img[0:(len(var_img)-6)]+ "-trans.png"
    im_rgba.save(name_img)
    img = ImageTk.PhotoImage(Image.open(name_img).resize((int(hauteur/division), int(largeur/division))))
    monCanvas.create_image(0,0, image = img, anchor=tkinter.NW)

def couleur_lines():
    global i2, i3
    if abs(i2 - i3) != 1:
        return "green"
    else:
        return "black"

def appartient(elt, lst):
    for e in lst:
        if e == elt:
            return True
    return False

def trace_ligne6(val):
    global data, monCanvas, tableau_indice, division, list_ligne, i_actuelle, ball,timee, anim_deb, time_deb
    val = str( int(anim_deb) + int(val))
    if (appartient(int(val),tableau_indice)):
        if(int(val) >= i_actuelle):
            i = tableau_indice.index(int(val))
            k = tableau_indice[i]
            l = tableau_indice[i + 1]
            if (True):
                for j in range(i_actuelle+1,int(val)):
                    if (appartient(j, tableau_indice)):
                        k_i = tableau_indice.index(j)
                        k_1 = tableau_indice[k_i]
                        k_2 = tableau_indice[k_i + 1]
                        list_ligne.append(monCanvas.create_line(data["GazePointX (MCSpx)"][k_1]/division,data["GazePointY (MCSpx)"][k_1]/division,data["GazePointX (MCSpx)"][k_2]/division,data["GazePointY (MCSpx)"][k_2]/division))
                        
            list_ligne.append(monCanvas.create_line(data["GazePointX (MCSpx)"][k]/division,data["GazePointY (MCSpx)"][k]/division,data["GazePointX (MCSpx)"][l]/division,data["GazePointY (MCSpx)"][l]/division))
            monCanvas.delete(ball)
            
            ball = monCanvas.create_oval((data["GazePointX (MCSpx)"][l]/division)-5,(data["GazePointY (MCSpx)"][l]/division)-5,(data["GazePointX (MCSpx)"][l]/division)+5,(data["GazePointY (MCSpx)"][l]/division)+5, fill = "red")
            if(len(list_ligne)>10):
                tmp = list_ligne[0]
                del list_ligne[0]
                monCanvas.delete(tmp)
            
            tableau_heatmap[int(data["GazePointX (MCSpx)"][l]/division)][int(data["GazePointY (MCSpx)"][l]/division)] += 1
            timee.set(str(int(data["RecordingTimestamp"][l])-int(time_deb)))
        else:
            for j in range(int(val),i_actuelle):
                l = int(val)
                if list_ligne != [] and appartient(j, tableau_indice):
                    a = list_ligne.pop()
                    monCanvas.delete(a)
                    monCanvas.delete(ball)
                    ball = monCanvas.create_oval((data["GazePointX (MCSpx)"][l]/division)-5,(data["GazePointY (MCSpx)"][l]/division)-5,(data["GazePointX (MCSpx)"][l]/division)+5,(data["GazePointY (MCSpx)"][l]/division)+5, fill = "red")
            timee.set(str(int(data["RecordingTimestamp"][l])-int(time_deb)))
        i_actuelle = int(val)

tab_time = {}

def get_time_tab():
    global data, tab, spinbox
    deb = tab[spinbox.get()]["debut"]
    fin = tab[spinbox.get()]["fin"]
    tmp = 0
    for i in range(deb,fin):
        if appartient(i, tableau_indice):
            tab_time[i] = tmp
        tmp += data["GazeEventDuration"][i]

def get_time(val):
    global data, tab, spinbox
    tmp = 0
    val1 = tab[spinbox.get()]["debut"]
    for i in range(val1, val):
        tmp += data["GazeEventDuration"][i]
    return tmp

def remplire_tableau_indice():
    global data
    i = 0
    while i < data["GazePointX (MCSpx)"].size:
        if not(isnull(data["GazePointX (MCSpx)"][i])) or not(isnull(data["GazePointY (MCSpx)"][i])) :
            tableau_indice.append(i)
        i += 1

def remplire_tableau_carte():
    global data, tableau_carte
    i = 0
    while i < data["GazePointX (MCSpx)"].size:
        if not(isnull(data["GazePointX (MCSpx)"][i])) or not(isnull(data["GazePointY (MCSpx)"][i])) :
            tableau_carte[i] = {"x":data["GazePointX (MCSpx)"][i], "y":data["GazePointY (MCSpx)"][i]}
        i += 1

def bouton():
    global monCanvas
    monCanvas.delete('all')
    monCanvas.create_image(0,0, image = img, anchor=tkinter.NW)

def suivant():
    global i3, ball2, animation
    i3 = animation.get()
    i3 += 1
    animation.set(i3)

def precedent():
    global monCanvas, i3, animation
    i3 = animation.get()
    i3 -= 1
    animation.set(i3)

def modification():
    global ball2
    if (monCanvas.itemcget(ball2, 'state')== tkinter.HIDDEN) :
        monCanvas.itemconfig(ball2, state=tkinter.NORMAL)
    else:
        monCanvas.itemconfig(ball2, state=tkinter.HIDDEN)

def play_stop():
    global text_bouton_play, play, animation, i3, i2
    i3 = animation.get()
    i2 = i3
    if play:
        stop()
        play = False
        text_bouton_play.set("Démarrer")
    else:
        demarer_ligne()
        play =True
        text_bouton_play.set("Arrêter")

division = 2.5

hauteur = 1920
#1920
largeur = 1080
#1080

ratio = max(largeur / get_monitors()[0].height, hauteur / get_monitors()[0].width)

hauteur_fenetre = int(hauteur/division)
largeur_fenetre = int(largeur/division)
taille_img = str(hauteur_fenetre)+"x"+str(largeur_fenetre+100)

list_ligne = []
i_actuelle = 0

#creation de la fenetre tkinter
fenetre = tkinter.Tk()
fenetre.title("Animation")
fenetre.geometry(taille_img)

#creation du canvas
monCanvas = tkinter.Canvas(fenetre, width=hauteur_fenetre, height=largeur_fenetre, bg='ivory', bd=0, highlightthickness=0)
monCanvas.place(x=0,y=0)


#fenetre top level "boite a outils"
top = tkinter.Toplevel(fenetre)
top.title('Boîte à outils')
top.transient(fenetre)
top.geometry("180x350")

#-variable changeante
ball = monCanvas.create_line(0,0,0,0)
text_bouton_play = tkinter.StringVar(fenetre)
timee = tkinter.StringVar(fenetre)
name = tkinter.StringVar(fenetre)
i_a = tkinter.IntVar(fenetre)
taille = tkinter.IntVar(fenetre)
inf = tkinter.IntVar(fenetre)
value = tkinter.DoubleVar(top)

#initialisation des variables

tab = {}
play = False
text_bouton_play.set("Play")
data = None
start = True
blanc = False
p = 0
time = 0.0000
indice = 0
i = 0
i2 = 0
i3 = None
i_v = 0
ball2 = None
value.set(1)

#variable tableau, liste, dictionnaire
tableau = []
tableau_indice = []
tableau_heatmap = [0] * hauteur_fenetre
for i in range(hauteur_fenetre):
    tableau_heatmap[i] = [0] * largeur_fenetre

tableau_carte = {}

#initialisation bouton
animation = None

#Les boutons de la boîte à outils

spinbox = tkinter.Spinbox(top, values=tableau)
texteLabel3 = tkinter.Label(top, textvariable = timee)
texteLabel4 = tkinter.Label(top, textvariable = name)
ms = tkinter.Label(top, text = "ms")

boutD = tkinter.Button(top, textvariable =text_bouton_play, width =15, command=play_stop, activebackground="red")
boutOk = tkinter.Button(top, text= 'OK', width =15, command=bouton_ok)
boutS = tkinter.Button(top, text= 'Stop', width =15, command=stop)
boutSup = tkinter.Button(top, text = 'Supprimer',width = 15, command = bouton)
boutF = tkinter.Button(top, text = 'Utilisateur',width = 15, command = add_file, bg="yellow")
boutSuiv = tkinter.Button(top, text='Suivant',width = 15, command = suivant)
boutPrec = tkinter.Button(top, text='Précedent',width = 15, command = precedent)
boutAff = tkinter.Button(top, text="Tout afficher", width = 15, command = affiche_lines3, activebackground="red")
vitesse = tkinter.Scale(top, orient='horizontal', from_=1, to=30, resolution=1, length=150, label='vitesse', variable = value)
# autreF = tkinter.Button(top, text = 'Utilisateur 2',width = 15, command = add_file_Ut2, bg="blue")

top2 = None

texteLabel3.place( x = 85, y = 8)
ms.place(x = 120, y = 8 )
texteLabel4.place( x = 30, y = 8 )
boutF.place(x = 30 , y = 28)
# autreF.place(x = 8, y = 100)

fenetre.mainloop()
