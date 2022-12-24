import pytesseract as eyes
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle
import cv2
import webbrowser as wb
from pdf2image import convert_from_path as cp
import time

#Définition des variables
testcmd = False 
testl = False 
testutil = False
tcmd = ""
tlien = ""
ilien = ""
list_lien = []
histo = []

trajet = os.getcwd()

#Définitions des images utilisées
lien_font_page = "{}\Data\Font.png".format(trajet)
lien_font_page2 = "{}\Data\Font2.png".format(trajet)

#Définition des élément autres utilisés
lien_ico = "{}\Data\ico.ico".format(trajet)

#Définition des Utilitaires 
def ecrire(doc, titre_doc):
    lien = "{}".format(titre_doc)
    with open(lien, 'ab') as recap:
        donnees = pickle.Pickler(recap)
        donnees.dump(doc)
    return doc

def lire(doc, titre_cible):
    lien = "{}".format(titre_cible)
    with open(lien, 'rb') as sta:
        donnees = pickle.Unpickler(sta)
        doc = donnees.load()
    return doc

def Trad_temps(temps_cible):
    """Méthode qui traduit le temps brut (secondes) au format 'HH:MM:SS'"""
    q,s=divmod(temps_cible,60)
    h,m=divmod(q,60)
    return "%d heures,%d minutes et %d secondes" %(h,m,s)

#Creer la fenetre d'init
window1 = Tk()

#Personnaliser la fenetre
window1.title("Initialisation du Programme d'OCR")
window1.iconbitmap(lien_ico)
window1.geometry("1500x650")
window1.minsize(400,400)
window1.configure(background='#224466')

#Reparamètrage à partir des dimensions de l'image (Fond d'écran)
img = PhotoImage(file=lien_font_page)
w = img.width()
h = img.height()
window1.geometry('%dx%d+0+0' % (w,h))
window1.maxsize(w,h)

#Création du Canvas
can_init = Canvas(window1, width=w, height=h, bg='black')
can_init.create_image(0,0, anchor=NW, image=img)
can_init.place(x=0, y=0, relwidth=1, relheight=1)

#Test des lien et initialisation du programme
tcmd = ""
tlien = ""
try: 
    tcmd = lire(tcmd,'tlien_tes')
    tlien = lire(tlien,'tlien_repo')
except FileNotFoundError or OSError:
    tcmd = ""
    tlien = ""
if tlien != "":
    eyes.pytesseract.tesseract_cmd = tcmd
    showinfo(title="Confirmation",message="Vos liens sont récupérés, Bon retour")
    window1.destroy()
else:#Si les liens ne sont pas paramétrés
    verif_ouverture = askyesno(title="Message",message="Voulais vous ouvrir la page web pour télécharger Tesseract?")
    if verif_ouverture == True:    
        wb.open_new_tab(r"https://digi.bib.uni-mannheim.de/tesseract/")
        wb.open_new_tab(r"https://blog.alivate.com.au/poppler-windows/")
    else:
        showinfo(title="Information",message="Vous pouvez ré-ouvrir les liens en fermant et ouvrant à nouveau ce programme")
    label1 = Label(can_init,text="Bienvenue sur l'initailisation de programme d'OCR", font=("Courrier",35), width=40, bg='#224466', fg='deepskyblue2')
    label1.pack(pady=10, fill=X, side=TOP)
    can_init.create_window(w/2,100, window=label1)

    label_tes = Label(can_init,text="Veuillez selectionnez votre lien du Dossier Tesseract",
    font=("Ink free", 25), bg='#224466', fg='deepskyblue2')
    label_tes.pack(pady=10, fill=X)
    can_init.create_window(w/2,150, window=label_tes)

    def initial_tes():#Initialisation du lien Tesseract
        tcmd = ""
        try: 
            tcmd = lire(tcmd,'tlien_tes')
        except FileNotFoundError or OSError:
            tcmd = ""
        if tcmd == "":  
            tcmd = askdirectory(title="Recherche du dossier Tesseract")
            if tcmd != "":
                lien_fake = '{}/tesseract.exe'.format(tcmd)
                teslien = os.path.exists(lien_fake)
                if teslien == True: #Lorsque le lien est bon, le passage à l'autre page
                    showinfo(title="Confirmation",message="Votre lien est bon")
                    showinfo(title="Confirmation",message="Vous avez configuré le lien de votre Repository pour 'Tesseract' que: '{}'".format(tcmd))
                    eyes.pytesseract.tesseract_cmd = lien_fake
                    lien_fake = ecrire(lien_fake,'tlien_tes')
                    but2.configure(state='normal')
                else:
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    try:
                        os.remove('tlien_tes')
                    except FileNotFoundError:
                        pass
                    return
            else:
                showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                try:
                    os.remove('tlien_tes')
                except FileNotFoundError:
                    pass
                return
        else:
            showinfo(title="Attention",message="Votre lien de votre fichier est déjà entrer '{}'".format(tcmd))
            verif_ouverture = askyesno(title="Message",message="Votre lien étant valide, voulez-vous garder le lien?")
            if verif_ouverture == True:    
                but2.configure(state='normal')
            else:
                showinfo(title="Information",message="Votre lien à été supprimer")
                try:
                    os.remove('tlien_tes')
                except FileNotFoundError:
                    pass
                return

    #Partie d'initialisation de Tesseract 
    but_tesseract = Button(can_init, text="Entrez le lien du Dossier de Tesseract", command= initial_tes,font=("Courrier", 25), fg='#224466', bg='deepskyblue2')
    but_tesseract.pack(pady=10)
    can_init.create_window(w/2,250, window=but_tesseract)

    #Si erreur dans l'entré du Tesseract
    def sup_tes():
        try:
            os.remove('tlien_tes')
        except FileNotFoundError:
            showinfo(title="Attention",message="Votre lien n'existait pas") 
        showinfo(title="Information",message="Votre lien à été supprimé")

    but_tesseract_sup = Button(can_init, text="Effacer le lien du fichier Tesseract", command= sup_tes,font=("Courrier", 15), fg='#224466', bg='deepskyblue2')
    but_tesseract_sup.pack(pady=10)
    can_init.create_window(w-450,350, window=but_tesseract_sup)

    def initial_lien():#Paramètrage du lien du repo
        tlien = ""
        try: 
            tlien = lire(tlien,'tlien_repo')
        except FileNotFoundError or OSError:
            tlien = ""
        if tlien == "":  
            tlien = askdirectory(title="Recherche du dossier de 'Poppler'")
            if tlien != "":
                lien_fake = '{}/pdfimages.exe'.format(tlien)
                teslien = os.path.exists(lien_fake)
                if teslien == True: #Lorsque le lien est bon, le passage à l'autre page
                    showinfo(title="Confirmation",message="Votre lien est bon")
                    showinfo(title="Confirmation",message="Vous avez configuré le lien de votre Repository 'Poppler': '{}'".format(tlien))
                    tlien = ecrire(tlien,'tlien_repo')
                    window1.destroy()
                else:
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    try:
                        os.remove('tlien_repo')
                    except FileNotFoundError:
                        pass
                    return
            else:
                showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                try:
                    os.remove('tlien_repo')
                except FileNotFoundError:
                    pass
                return
        else:
            showinfo(title="Attention",message="Votre lien de votre fichier est déjà entrer '{}'".format(tcmd))
            verif_ouverture = askyesno(title="Message",message="Votre lien étant valide, voulez-vous garder le lien?")
            if verif_ouverture == True:    
                window1.destroy()
            else:
                showinfo(title="Information",message="Votre lien à été supprimer")
                try:
                    os.remove('tlien_tes')
                except FileNotFoundError:
                    pass
                return

    #Bouton1 d'initialisation
    label_ocr = Label(can_init, text="Veuillez entrez votre lien du Dossier contenant 'Poppler'",
    font=("Ink free", 25), bg='#224466', fg='deepskyblue2')
    label_ocr.pack(pady=10)
    can_init.create_window(w/2,550, window=label_ocr)

    but2 = Button(can_init, text="Entrez le lien du Dossier contenant 'Poppler'",font=("Courrier", 25), command= initial_lien,
                  state='disabled',disabledforeground='deepskyblue2',bg='deepskyblue2',activeforeground='#224466')
    but2.pack(pady=10, fill=X, side=RIGHT)
    can_init.create_window(w/2,650, window=but2)

    window1.mainloop()

#Creer la fenetre principal
window = Tk()
lien_icone = tlien

testuniq = False
try: 
    tlien = lire(tlien,'tlien_repo')
except FileNotFoundError or OSError:
    testuniq = True

if testuniq == True:
    showerror(title="Attention", message="Vous n'avez pas paramètrer vos liens, veuillez reprendre svp")
    window.destroy()
else:
    #Personnaliser la fenetre
    window.title("Programme d'OCR Version 3")
    window.geometry("1500x650")
    window.minsize(400,400)
    window.iconbitmap(lien_ico)
    menu = Menu(window, font=("Courrier", 15), bg='#224466', fg='deepskyblue2')
    window.config(menu=menu, background='#224466')

    #Reparamètrage à partir des dimensions de l'image (Fond d'écran)
    img2 = PhotoImage(file=lien_font_page2)
    w = img2.width()
    h = img2.height()
    window.geometry('%dx%d+0+0' % (w,h))
    window.maxsize(w,h)

    #Création du Canvas
    can_princip = Canvas(window, width=w, height=h, bg='black')
    can_princip.create_image(0,0, anchor=NW, image=img2)
    can_princip.place(x=0, y=0, relwidth=1, relheight=1)

    #Ajout des menus cascade
    zoneMenu = Frame(window, borderwidth=3, bg='#224466')
    zoneMenu.pack(fill=X)

    menufichier = Menubutton(zoneMenu, text="Fichier", width='20', borderwidth=2, activebackground='#224466',relief = RAISED)
    menufichier.grid(row=0,column=0)
    menup = Menubutton(zoneMenu, text="Paramètres", width='20', borderwidth=2,activebackground='#224466',relief = RAISED)
    menup.grid(row=0,column=1)

    #Parètrage en menu déroulant
    menuD1 = Menu(menufichier)
    menuD2 = Menu(menup)

    #Ajout des fonction du menu 1
    def histo():
        try:
            os.startfile("histo")
        except FileNotFoundError or OSError:
            showerror(title="Erreur", message= "Vous n'avez pas encore d'historique")

    def aide():
        try:
            os.startfile("aide.pdf")
        except FileNotFoundError or OSError:
            showerror(title="Erreur", message= "Erreur, le fichier est inexistant")

    def Marche():
        try:
            os.startfile("Marche_a_suivre.pdf")
        except FileNotFoundError or OSError:
            showerror(title="Erreur", message= "Erreur, le fichier est inexistant")
        
    def fic():
        lienp = os.getcwd()
        try:
            os.startfile(lienp)
        except FileNotFoundError or OSError:
            showerror(title="Erreur", message= "Erreur, le fichier '{}' ne s'ouvre pas".format(lienp))

    def tableau():
        try:
            os.startfile("result")
        except FileNotFoundError or OSError:
            showerror(title="Erreur", message= "Vous n'avez pas encore de Tableau déjà traiter")

    menuD1.add_command(label="Historique", command=histo)
    menuD1.add_separator()
    menuD1.add_command(label="Emplacement Fichier", command=fic)
    menuD1.add_separator()
    menuD1.add_command(label="Tableau", command=tableau)
    menuD1.add_separator()
    menuD1.add_command(label="Marche à suivre", command=Marche)
    menuD1.add_command(label="Aide", command=aide)
    menuD1.add_separator()
    menuD1.add_command(label="Quitter", command= window.destroy)
    menufichier.configure(menu=menuD1)

    #Ajout des fonctions du menu 2
    def Sup_lien():
        testutil = os.path.exists('tlien_repo')
        if testutil == True:
            testfin = askyesno(title="Attention",message="êtes-vous sur de vouloir supprimer vos lien?")
            if testfin == True:
                try:
                    os.remove('tlien_repo')
                except FileNotFoundError or OSError:
                    showinfo(title="Attention",message="Vos liens n'ont pas été supprimer")
                    return    
                try:
                    os.remove('tlien_tes')
                except FileNotFoundError or OSError:
                    showinfo(title="Attention",message="Votre lien '{}' n'à pas été supprimer".format(tcmd))
                    return
                try:
                    os.remove('histo')
                except FileNotFoundError or OSError:
                    showinfo(title="Attention",message="Vous n'avez pas encore d'historique")
                    return
                try:
                    os.remove('result')
                except FileNotFoundError or OSError:
                    showinfo(title="Attention",message="Voous n'avez pas encore de Résultat")
                    return
                showinfo(title="Confirmation",message="Vos liens ont été supprimer avec succès")
                window.destroy()
                return
            else:
                showinfo(title="Attention",message="Vos liens n'ont pas été supprimer")
                return
        else:
            showinfo(title="Attention",message="Vos liens n'ont pas été supprimer")
            return

    menuD2.add_command(label="Suppression des liens paramètrées", command=Sup_lien)
    menup.configure(menu=menuD2)

    #Indication pour l'utilisateur: Haut de Page
    label_title = Label(can_princip, text="Bienvenue sur le programme de l'OCR", font=("Courrier", 45), bg='#224466', fg='deepskyblue2')
    label_title.pack(pady=10)
    can_princip.create_window(w/2,50, window=label_title)

    label_title2 = Label(can_princip, text="Veuillez Saisir le lien de l'image à traiter :", font=("Ink free", 25), bg='#224466', fg='deepskyblue2')
    label_title2.pack(pady=10)
    can_princip.create_window(w/2,150, window=label_title2)

    #Fonction du bouton pour trouver le fichier à traiter
    def lien_a_traiter():#Paramètrage du lien du fichier à traiter
        tlien_traiter = ""
        info_trait.configure(state='normal')
        try: 
            tlien_traiter = lire(tlien_traiter,'tlien_traiter_repo')
        except FileNotFoundError or OSError:
            tlien_traiter = ""
        if tlien_traiter == "":  
            tlien_traiter = askopenfilename(title="Recherche du Fichier à Traiter",filetypes=[("Fichier en PDF",".pdf"),("Fichier en .PNG",".png")])
            if tlien_traiter != "":
                teslien = os.path.exists(tlien_traiter)
                if teslien == True: #Lorsque le lien est bon, le passage à l'autre page
                    showinfo(title="Confirmation",message="Votre lien est bon")
                    tlien_traiter = ecrire(tlien_traiter,'tlien_traiter_repo')
                    info_trait.delete(0,END)
                    info_trait.insert(0, tlien_traiter)
                    info_trait.configure(state='disabled')
                    but.configure(state="normal")
                    but_ex.configure(state="normal")
                else:
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    try:
                        os.remove('tlien_traiter_repo')
                    except FileNotFoundError:
                        showinfo(title="Attention",message="Votre lien n'a pas été supprimé")
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    info = "Votre lien de votre fichier n'est pas correct"
                    info_trait.delete(0,END)
                    info_trait.insert(0, info)
                    info_trait.configure(state='disabled')
                    return
            else:
                showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                try:
                    os.remove('tlien_traiter_repo')
                except FileNotFoundError:
                    showinfo(title="Attention",message="Votre lien n'a pas été supprimé")
                showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                info = "Votre lien de votre fichier n'est pas correct"
                info_trait.delete(0,END)
                info_trait.insert(0, info)
                info_trait.configure(state='disabled')
                return
        else:
            verif_ouverture = askyesno(title="Message",message="Votre lien de votre fichier est déjà entrer sous l'adresse: ' {} ',voulez-vous réutiliser le lien?".format(tlien_traiter))
            if verif_ouverture == True:    
                showinfo(title="Confirmation",message="Votre lien est bon")
                info_trait.delete(0,END)
                info_trait.insert(0, tlien_traiter)
                info_trait.configure(state='disabled')
                but.configure(state="normal")
                but_ex.configure(state="normal")
            else:
                showinfo(title="Information",message="Votre lien à été supprimé")
                try:
                    os.remove('tlien_traiter_repo')
                except FileNotFoundError:
                    showinfo(title="Attention",message="Votre lien n'a pas été supprimé")
                info = "Votre lien à été supprimé"
                info_trait.delete(0,END)
                info_trait.insert(0, info)
                info_trait.configure(state='disabled')
                return

    #Boutton de parametrage de fichier à traiter
    but_trait = Button(can_princip, text="Trouver le fichier à traiter", font=("Courrier", 25),
    bg='deepskyblue2', fg='#224466', command=lien_a_traiter)
    but_trait.pack(pady=10)
    can_princip.create_window(w/2,250, window=but_trait)

    #Info sur le fichier à traiter
    info_trait = Entry(can_princip, textvariable=lien_a_traiter, font=("Courrier", 25),
    disabledbackground='deepskyblue2',bg='#224466', fg='deepskyblue2', relief=FLAT,state='disabled')
    info_trait.pack(pady=10)
    can_princip.create_window(w/2,350,width=800, window=info_trait)

    #Fonction du bouton "Normal"
    def ocr_core():
        rep.configure(state='normal')
        result_text = []
        list_symbole = ['<','>','-','_','&',"~","#",'/','^']
        cong = r'--psm 6 --oem 1' #the best for now --psm 6 or 4 --oem 1 et meilleur configue pour trouver les mots separements --psm 11 --oem 1
        tlien_traiter = ""
        try: 
            tlien_traiter = lire(tlien_traiter,'tlien_traiter_repo')
        except FileNotFoundError or OSError:
            tlien_traiter = ""
            showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
            return
        histo = ""
        img = tlien_traiter
        testutil = False
        testutil = os.path.exists(img)
        if testutil == True:#Si le lien est bon
            #Début du traitement
            if ".png" in tlien_traiter:
                img = cv2.imread(img)
                img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
                text = eyes.image_to_string(img,lang='spa+fra',config=cong)
                #for x,y in enumerate(text.splitlines()):
                #    if x!=0:    
                #        y = y.split()
                #        if len(y)==12:
                #            x,y,w,h = int(y[6]),int(y[7]),int(y[8]),int(y[9])
                #            cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),1)
                #Detection de chaine de caractère
                #cv2.imshow("Image traite",img)#Ouvrir l'image traiter
                if text == "":
                    lien = "Votre lien ne contient pas de texte"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state='disabled')
                    os.remove('histo')
                    return
                else:
                    try:
                        os.remove('histo')
                    except FileNotFoundError or OSError:
                        pass
                    with open('result', 'w+') as result:
                        result.writelines(text)
                    verif_ouverture3 = askyesno(title="Message",message="Voulez-vous ouvrir le resultat?")
                    if verif_ouverture3 == True:    
                        os.startfile('result')
                    else:
                        showinfo(title="Information",message="Vous pouvez ré-ouvrir le tableau dans le menu en haut de la page")
                    lien = "Votre lien est bon, Merci"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state='disabled')
                    histo = tlien_traiter
                    with open('histo', 'w+') as historique:
                        historique.write(histo)
                    return
            else:#Pour une image en PDF
                starting = time.time()
                pdf_path = img
                page_sup_conpt = 0
                try:
                    pdf_path != ""
                except ValueError:
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    return
                page_test = os.path.exists('out{}.png'.format(page_sup_conpt))
                if page_test != True:
                    for page_sup_conpt in range(0,1000000):
                        pages_testing = os.path.exists('out{}.png'.format(page_sup_conpt))
                        if pages_testing == True:
                            os.remove('out{}.png'.format(page_sup_conpt))
                        else:
                            break
                        page_sup_conpt += 1                   
                #Continuation de la fonction de traitement du PDF
                pages = cp(pdf_path,poppler_path=tlien)
                page_counter = 0
                for page_counter,page in enumerate(pages):#Convertir les pages en png
                    img_name = 'out{}.png'.format(page_counter)
                    page.save(img_name)
                    page_counter += 1
                page_t_t = 0
                result = []
                for page_t_t in range(0,page_counter):#On traite tout le texte dans les pages
                    text_to_trait = eyes.image_to_string('out{}.png'.format(page_t_t),config=cong)
                    trait = '\nPage {}:'.format(page_t_t)
                    result.append(trait.capitalize())
                    result.append(text_to_trait)
                    result.append("\n\n")
                    page_t_t += 1
                text = result
                pages_to_del = 0
                for pages_to_del in range(0,page_counter):#On supprime le resultat des conversions
                    pages_test = os.path.exists('out{}.png'.format(pages_to_del))
                    if pages_test == True:
                        os.remove('out{}.png'.format(pages_to_del))
                        pages_to_del += 1
                    pages_to_del += 1
                finished = time.time()
                final = finished-starting
                final = Trad_temps(final)
                showinfo(title="Information",message="Votre lien comporte {} pages, le traitement à duré {} à traiter".format(page_t_t,final))
                if text == "":
                    rep.configure(state="normal")
                    lien = "Votre lien ne contient pas de texte"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state="disabled")
                    os.remove('histo')
                    return
                else:
                    try:
                        os.remove('histo')
                    except FileNotFoundError or OSError:
                        pass
                    with open('result', 'w+') as result:
                        for line in text:
                            try:
                                result.write(line)
                            except UnicodeEncodeError:
                                line.replace("\\","/")   
                    verif_ouverture2 = askyesno(title="Message",message="Voulez-vous ouvrir le resultat?")
                    if verif_ouverture2 == True:    
                        os.startfile('result')
                    else:
                        showinfo(title="Information",message="Vous pouvez ré-ouvrir le tableau dans le menu en haut de la page")
                    lien = "Votre lien est bon, Merci"
                    rep.configure(state="normal")
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state="disabled")
                    histo = tlien_traiter
                    with open('histo', 'w+') as historique:
                        historique.write(histo)
                    return        
        else:
            lien = "Votre lien est invalide"
            rep.delete(0, END)
            rep.insert(0, lien)
            os.remove('histo')
            return

    #Définition de la fonction du bouton "Supprimez ..."
    def Sup():
        testutil = os.path.exists('result')
        if testutil == True:
            os.remove('result')
            showinfo(title="Attention",message="Votre lien de votre fichier est supprimer")
        else:
            showinfo(title="Attention",message="Votre lien de votre fichier n'est pas supprimer")
            return

    #Affichage: Bas de page
    but = Button(can_princip, text="Débuter l'OCR en mode 'Normal'", font=("Courrier", 30),disabledforeground='deepskyblue2',
    bg='deepskyblue2', fg='#224466', command=ocr_core,state='disabled')
    but.pack(pady=10)
    can_princip.create_window(w/2,450, window=but)

    #Fonction du bouton "Expert"
    def ocr_core_expert():
        rep.configure(state='normal')
        result_text = []
        list_symbole = ['<','>','-','_','&',"~","#",'/','^']
        cong = r'--psm 6 --oem 1' #the best for now --psm 6 or 4 --oem 1 et meilleur configue pour trouver les mots separements --psm 11 --oem 1
        tlien_traiter = ""
        try: 
            tlien_traiter = lire(tlien_traiter,'tlien_traiter_repo')
        except FileNotFoundError or OSError:
            tlien_traiter = ""
            showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
            return
        histo = ""
        img = tlien_traiter
        testutil = False
        testutil = os.path.exists(img)
        if testutil == True:#Si le lien est bon
            #Début du traitement
            if ".png" in tlien_traiter:
                img = cv2.imread(img)
                img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
                #Detection de chaine de caractère
                boxes = eyes.image_to_data(img,lang='spa+fra',config=cong)
                for x,y in enumerate(boxes.splitlines()):
                    if x!=0:    
                        y = y.split()
                        if len(y)==12:
                            if y[11] in list_symbole:
                                pass
                            result_text.append(y[11])
                            result_text.append(" ")
                            if ":" in y[11] or "." in y[11]:
                                result_text.append("\n")
                text = result_text
                if text == "":
                    lien = "Votre lien ne contient pas de texte"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state='disabled')
                    os.remove('histo')
                    return
                else:
                    try:
                        os.remove('histo')
                    except FileNotFoundError or OSError:
                        pass
                    with open('result', 'w+') as result:
                        result.writelines(text)
                    verif_ouverture3 = askyesno(title="Message",message="Voulez-vous ouvrir le resultat?")
                    if verif_ouverture3 == True:    
                        os.startfile('result')
                    else:
                        showinfo(title="Information",message="Vous pouvez ré-ouvrir le tableau dans le menu en haut de la page")
                    lien = "Votre lien est bon, Merci"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state='disabled')
                    histo = tlien_traiter
                    with open('histo', 'w+') as historique:
                        historique.write(histo)
                    return
            else:#Pour une image en PDF
                starting = time.time()
                pdf_path = img
                page_sup_conpt = 0
                try:
                    pdf_path != ""
                except ValueError:
                    showinfo(title="Attention",message="Votre lien de votre fichier n'est pas correct")
                    return
                page_test = os.path.exists('out{}.png'.format(page_sup_conpt))
                if page_test != True:
                    for page_sup_conpt in range(0,1000000):
                        pages_testing = os.path.exists('out{}.png'.format(page_sup_conpt))
                        if pages_testing == True:
                            os.remove('out{}.png'.format(page_sup_conpt))
                        else:
                            break
                        page_sup_conpt += 1                   
                #Continuation de la fonction de traitement du PDF
                pages = cp(pdf_path,poppler_path=tlien)
                page_counter = 0
                for page_counter,page in enumerate(pages):#Convertir les pages en png
                    img_name = 'out{}.png'.format(page_counter)
                    page.save(img_name)
                    page_counter += 1
                page_t_t = 0
                result = []
                for page_t_t in range(0,page_counter):#On traite tout le texte dans les pages
                    text_to_trait = eyes.image_to_data('out{}.png'.format(page_t_t),config=cong)
                    for x,y in enumerate(text_to_trait.splitlines()):
                        if x!=0:    
                            y = y.split()
                            if len(y)==12:
                                if y[11] in list_symbole:
                                    pass
                                result_text.append(y[11])
                                result_text.append(" ")
                                if ":" in y[11] or "." in y[11]:
                                    result_text.append("\n")
                    result_text.append("\n\n\n")
                    text_to_trait = result_text
                    trait = '\nPage {}:'.format(page_t_t)
                    result.append(trait.capitalize())
                    result.append(text_to_trait)
                    result.append("\n\n")
                    page_t_t += 1
                text = result
                pages_to_del = 0
                for pages_to_del in range(0,page_counter):#On supprime le resultat des conversions
                    pages_test = os.path.exists('out{}.png'.format(pages_to_del))
                    if pages_test == True:
                        os.remove('out{}.png'.format(pages_to_del))
                        pages_to_del += 1
                    pages_to_del += 1
                finished = time.time()
                final = finished-starting
                final = Trad_temps(final)
                showinfo(title="Information",message="Votre lien comporte {} pages, le traitement à duré {} à traiter".format(page_t_t,final))
                if text == "":
                    rep.configure(state="normal")
                    lien = "Votre lien ne contient pas de texte"
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state="disabled")
                    os.remove('histo')
                    return
                else:
                    try:
                        os.remove('histo')
                    except FileNotFoundError or OSError:
                        pass
                    with open('result', 'w+') as result:
                        for line in text:
                            try:
                                result.writelines(line)
                            except UnicodeEncodeError:
                                line.replace("\\","/")   
                    verif_ouverture2 = askyesno(title="Message",message="Voulez-vous ouvrir le resultat?")
                    if verif_ouverture2 == True:    
                        os.startfile('result')
                    else:
                        showinfo(title="Information",message="Vous pouvez ré-ouvrir le tableau dans le menu en haut de la page")
                    lien = "Votre lien est bon, Merci"
                    rep.configure(state="normal")
                    rep.delete(0, END)
                    rep.insert(0, lien)
                    rep.configure(state="disabled")
                    histo = tlien_traiter
                    with open('histo', 'w+') as historique:
                        historique.write(histo)
                    return        
        else:
            lien = "Votre lien est invalide"
            rep.delete(0, END)
            rep.insert(0, lien)
            os.remove('histo')
            return

    but_ex = Button(can_princip, text="Débuter l'OCR en mode 'Approfondi'", font=("Courrier", 30),disabledforeground='medium blue',
    bg='medium blue', fg='#224466', command=ocr_core_expert,state='disabled')
    but_ex.pack(pady=10)
    can_princip.create_window(w/2,550, window=but_ex)

    rep = Entry(can_princip, textvariable=ocr_core, bg='#224466',font=("Ink Free", 35), fg='deepskyblue2', relief=FLAT,state='disable')
    rep.pack(pady=10)
    can_princip.create_window(w/2,650, window=rep)

    but_2 = Button(can_princip, text="Supprimer le fichier de resultat", font=("Courrier", 15), bg='deepskyblue2', fg='#224466', command= Sup)
    but_2.pack(pady=10)
    can_princip.create_window(w/2,750, window=but_2)

    window.mainloop()