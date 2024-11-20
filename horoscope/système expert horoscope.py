import tkinter as tk
from tkinter import messagebox
from experta import *

class InterfaceGraphique(tk.Tk):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.current_index = 0
        self.selected_season = ''
        self.question_label = None
        self.bouton = None
        self.listeBoutons = []

        self.title("AstroDevinez!")
        self.geometry("900x500")
        self.img = tk.PhotoImage(file="images/background.png")
        canvas = tk.Canvas(self)
        canvas.pack(fill="both", expand=True)
        rectangle_width=610
        rectangle_height=160
        x=(900-rectangle_width)/2
        y=(500-rectangle_height)/2
        canvas.create_image(0, 0, anchor="nw", image=self.img)
        canvas.create_rectangle(x,y,x+rectangle_width,y+rectangle_height,fill='#D8BFD8')


        self.bienvenue_label = tk.Label(self, text="Trouvez le signe qui reflète votre personnalité",font=("Helvetica", 16,"bold italic"),bg="#D8BFD8",fg="#800080")
        self.bienvenue_label.place(relx=0.5, rely=0.15, anchor="center")

        self.afficher_question("Quelle est ta saison préférée?",['hiver','printemps','ete','automne'],'saison')
        
        self.quitter_bouton = tk.Button(self,text="Quitter",font=("Helvetica", 12), bg="#D8BFD8",fg="navy",command=self.destroy)
        self.quitter_bouton.place(relx=0.25, rely=0.9, anchor="center")

        self.restart_bouton = tk.Button(self,text="Réessayer", font=("Helvetica", 12),bg="#D8BFD8",fg="navy",command=self.restart)
        self.restart_bouton.place(relx=0.1, rely=0.9, anchor="center")

    def restart(self):
        self.engine.reset()
        self.current_index = 0
        self.afficher_question("Quelle est ta saison préférée?",['hiver','printemps','ete','automne'],'saison')
    
    def afficher_question(self, question, reponses,fact):
        #effacer question précédente et ses choix 
        if self.question_label != None :
            self.question_label.destroy()
            for j in range(len(self.listeBoutons)):
                self.listeBoutons[j].destroy()

        self.question_label = tk.Label(self,text=question,font=("Helvetica", 20,"bold"),fg="#800080",bg="#D8BFD8")
        self.question_label.place(relx=0.5, rely = 0.4, anchor="center")
        for i in range(len(reponses)):
            self.bouton = tk.Button(self,font=("Helvetica", 12,"bold"),bg="#800080",fg="#D8BFD8",text=reponses[i], command=lambda i=i: self.choisir_reponse(i, reponses,fact))
            self.listeBoutons.append(self.bouton)
            if len(reponses)==2 :
                self.bouton.place(relx=0.4+i*0.2, rely=0.55, anchor="center")
            elif len(reponses)==3 :
                self.bouton.place(relx=0.3+i*0.2, rely=0.55, anchor="center")
            elif len(reponses)==4 :
                self.bouton.place(relx=0.25+i*0.15, rely=0.55, anchor="center")

    def choisir_reponse(self, index, reponses,fact):
        self.current_index = self.current_index + 1
        choice = reponses[index]
        fact_data = {fact: choice}
        self.engine.declare(Fact(**fact_data))
        print(self.engine.facts)

        if fact=="saison":
            self.selected_season=choice
        
        self.poser_questions(self.selected_season)
        self.engine.run()
        
        #Voir si questions de la saison choisie sont finies ou pas encore pour afficher résultat
        if self.selected_season=='ete':
            if (self.current_index==5):
                self.afficher_resultat()
        elif self.selected_season=='hiver':
            if (self.current_index==4):
                self.afficher_resultat()
        elif (self.selected_season=='automne') | (self.selected_season=='printemps') :
            if (self.current_index==6):
                self.afficher_resultat()

    def afficher_resultat(self):
        if (self.engine.result!=""):
            messagebox.showinfo("Résultat AstroDevinez!","Ton signe astrologique prédominant : \n\n  \t"+ self.engine.result)
        else : 
            print("Aucun signe astrologique conforme à ces choix")

    def poser_questions(self,choice):
        if choice == "hiver":
            if self.current_index==1:
                self.afficher_question("Quelle est ta préférence de lieu ? ",["montagne","endroits urbains","mer"],"pref_lieu")
            elif self.current_index==2:
                self.afficher_question("T'es attiré par le soleil ? ",["oui","non"],"pref_soleil")
            elif self.current_index==3:
                self.afficher_question("T'es inspiré par quel type de musique ? ",["relaxante","énergique"],"musique")

        elif choice == "automne":
            if self.current_index==1:
                self.afficher_question("Quel est ton type d'activité préféré ? ? ",["stable","créative"],"pref_activite")
            elif self.current_index==2:
                self.afficher_question("T'es attiré par le soleil ? ",["oui","non"],"pref_soleil")
            elif self.current_index==3:
                self.afficher_question("Aimes-tu les activités sportives ? ",["oui","non"],"sport")
            elif self.current_index==4:
                self.afficher_question("Quelle est ta réaction face aux défis ? ",["flexible","déterminé"],"reaction_defis")
            elif self.current_index==5:
                self.afficher_question("Quelle est ta préférence culinaire ?",["varié","épicé","doux"],"pref_culinaire")

        elif choice == "printemps":
            if self.current_index==1:
                self.afficher_question("T'es inspiré par quel type de musique ? ",["relaxante","énergique"],"musique")
            elif self.current_index==2:
                self.afficher_question("Aimes-tu les activités sportives ? ",["oui","non"],"sport")
            elif self.current_index==3:
                self.afficher_question("Quelle est ta préférence de planification ? ",["improvisation","à l'avance"],"planification")
            elif self.current_index==4:
                self.afficher_question("T'es attiré par la montagne ? ",["oui","non"],"pref_montagne")
            elif self.current_index==5:
                self.afficher_question("Quelle est ta préférence sociale ?",["seul","entouré"],"pref_sociale")

        elif choice == "ete":
            if self.current_index==1:
                self.afficher_question("T'es attiré par la mer  ?",["oui","non"],"attirance_mer")
            elif self.current_index==2:
                self.afficher_question("Quelle est ta réaction face au changement ? ",["réticent","enthousiaste"],"reaction_chgt")
            elif self.current_index==3:
                self.afficher_question("Préféres-tu l'ordre et la structure ? ",["oui","non"],"pref_ordre")
            if self.current_index==4:
                self.afficher_question("Quelle est ta préférence culinaire ? ",["varié","épicé","doux"],"pref_culinaire")


class InferenceEngine(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.result=''
   
    #*********************************************categorie1// préférence saisonniére = ETE ****************************************************
    @Rule(AND(Fact(saison="ete"), Fact(attirance_mer='oui'),Fact(reaction_chgt='enthousiaste'),Fact(pref_ordre='non'),Fact(pref_culinaire='épicé')),salience=2)
    def belier(self):
        self.result="Belier"

    @Rule(AND(Fact(saison="ete"), Fact(attirance_mer='oui'),Fact(reaction_chgt='réticent'),Fact(pref_ordre='oui'),Fact(pref_culinaire='doux')),salience=2)
    def cancer(self):
        self.result="Cancer"

    @Rule(AND(Fact(saison="ete"), Fact(attirance_mer='non'),Fact(reaction_chgt='enthousiaste'),Fact(pref_ordre='oui'),Fact(pref_culinaire='épicé')),salience=2)
    def lion(self):
        self.result="Lion"

    @Rule(AND(Fact(saison="ete"), Fact(attirance_mer='non'),Fact(reaction_chgt='enthousiaste'),Fact(pref_ordre='non'),Fact(pref_culinaire='varié')),salience=2)
    def sagittaire(self):
        self.result="Sagittaire"

    #*******************************************categorie2// préférence saisonniére = PRINTEMPS*********************************************
    @Rule(AND(Fact(saison="printemps"), Fact(musique='relaxante'),Fact(sport='non'),Fact(planification="à l'avance"),Fact(pref_montagne='oui'),Fact(pref_sociale='seul')),salience=3)
    def taureau(self):
        self.result="Taureau"

    @Rule(AND(Fact(saison="printemps"), Fact(musique='énergique'),Fact(sport='oui'),Fact(planification='improvisation'),Fact(pref_montagne='non'),Fact(pref_sociale='entouré')),salience=3)
    def gémeaux(self):
        self.result="Gémeaux"

    @Rule(AND(Fact(saison="printemps"), Fact(musique='relaxante'),Fact(sport='non'),Fact(planification="à l'avance"),Fact(pref_montagne='non'),Fact(pref_sociale='entouré')),salience=3)
    def poissons(self):
        self.result="Poissons"

    #***********************************************categorie3// préférence saisonniére = AUTOMNE *******************************************
    @Rule(AND(Fact(saison="automne"), Fact(pref_activite='stable'),Fact(pref_culinaire='varié'),Fact(pref_soleil='non'),Fact(sport='non'),Fact(reaction_defis='déterminé')),salience=4)
    def vierge(self):
        self.result="Vierge"

    @Rule(AND(Fact(saison="automne"), Fact(pref_activite='créative'),Fact(pref_culinaire='varié'),Fact(pref_soleil='oui'),Fact(sport='oui'),Fact(reaction_defis='flexible')),salience=4)
    def balance(self):
        self.result="Balance"

    @Rule(AND(Fact(saison="automne"), Fact(pref_activite='stable'),Fact(pref_culinaire='épicé'),Fact(pref_soleil='non'),Fact(sport='non'),Fact(reaction_defis='déterminé')),salience=4)
    def scorpion(self):
        self.result="Scorpion"

    #*******************************************categorie4// préférence saisonniére = HIVER *******************************************
    @Rule(AND(Fact(saison="hiver"), Fact(pref_lieu='montagne'),Fact(pref_soleil='non'),Fact(musique='relaxante')),salience=5)
    def capricorne(self):
        self.result="Capricorne"
    
    @Rule(AND(Fact(saison="hiver"), Fact(pref_lieu='endroits urbains'),Fact(pref_soleil='oui'),Fact(musique='énergique')),salience=5)
    def verseau(self):
        self.result="Verseau"  
     
engine = InferenceEngine()
engine.reset()
interface = InterfaceGraphique(engine)
interface.mainloop()