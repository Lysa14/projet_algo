from random import * # pour faire les tirages aléatoires
from math import * 
#import matplotlib.pyplot as plt # pour dessiner le réseau

class Noeud:
  """Chaque noeud a un certain nombre de voisins.
     Un voisin est un liste [noeud, valeur].
     Chaque noeud a un identifiant nom qui est un entier.""" 
  # méthode de construction d'une instance de noeud
  def __init__(self, nom, réseau):
    self.nom=nom
    self.tier=réseau
    self.voisins=[]
    self.marque = False # marque du noeud initialisée à False
    self.prédécesseur = self
    self.table_routage={} # Table de routage. Dictionnaire
    # calcul d'un couple de coordonnées aléatoires 
    # La coordonnée est x est choisie entre 0 et 100
    # la coordonnée y est choisie en fonction du réseau d'appartenance
    y = None
    if réseau == "T1":
      y=uniform(90,100)
    elif réseau== "T2":
      y=uniform(70,90)
    else:
      y=uniform(0,70)
    self.coord=[uniform(0,100),y] 

  # méthode permettant d'imprimer un noeud
  def __str__(self):
    return "{}-{}".format(self.tier,self.nom)

# ici, on choisit le nombre de noeuds de chacun des réseaux
# Pour débugger le programme on choisit des petites valeurs
nb_noeuds_T1 = 10
nb_noeuds_T2 = 20
# Attention, le nombre de noeurs du T3 doit être pair (voir plus loin pourquoi)
nb_noeuds_T3 = 70
# Fonctions d'affichage et de dessin
# Ces fonctions sont aussi utilisées pour le débuggage

def affiche_noeud(n, voisins=False, marque=False, pred=False, table=False):
  print("Noeud {}-{}".format(n.tier, n.nom))
  if voisins:
    print("  Voisins : {}".format([x[0].nom for x in n.voisins]))
  if marque:
    print("  Marque : {:.0f}".format(n.marque))
  if pred:
    print("  Prédécésseur : {}".format(n.prédécesseur))
  if table:
    affiche_table(n.table_routage)

# affichage d'une table de routage
def affiche_table(table):
  for clé, valeur in table.items():
    print("   Pour aller à {} : {}".format(clé, valeur))

def affichage_réseau(réseau, voisins=False, marque=False, pred=False, table=False):
  for n in réseau:
    affiche_noeud(n, voisins, marque, pred, table)

def couleur_noeud(n):
  if n.tier=="T1":
    couleur = 'r'
  elif n.tier=="T2":
    couleur = 'b'
  else:
    couleur ='y'
  return couleur

def couleur_arc(n1, n2):
  couleur='silver'
  if n1.tier=="T1" and n2.tier=="T1":
    couleur = 'r'
  if n1.tier=="T2" and n2.tier=="T2":
    couleur = 'b'
  if n1.tier=="T3" and n2.tier=="T3":
    couleur = 'y'
  return couleur


def dessine_réseau(graphe):
  for n in graphe:
    plt.scatter(n.coord[0], n.coord[1], color=couleur_noeud(n), s=30)
    for voisin in n.voisins:
      if voisin[0] in graphe:
        if voisin[0].nom > n.nom:
          plt.plot([n.coord[0], voisin[0].coord[0]], [n.coord[1], voisin[0].coord[1]], couleur_arc(n, voisin[0]))
  plt.show()

# Création du réseau T1 (uniquement les noeuds)
# Amélioration à apporter : que les noeuds sont moins collés les uns aux autres.
réseau_T1= []
 
def création_réseau_T1():
  for i in range (1, nb_noeuds_T1 +1):
    réseau_T1.append(Noeud(i, "T1"))
  print("Création du réseau T1 (backbone) : {} noeuds".format(len(réseau_T1)))

création_réseau_T1()
affichage_réseau(réseau_T1)
dessine_réseau(réseau_T1)

# Maillage du réseau T1 intra-backbone

# on initialise à vide les voisins
for n in réseau_T1:
  n.voisins=[]

# probabilité d'occurence d'un arc interne au réseau T1
# Valeur de l'énoncé : 0,75
# Remarque : régler cette valeur pour obtenir un réseau  réaliste
proba_arc_interne_T1 = 0.45
 
# Effet : le maillage met à jour l'attribut voisins de chaque noeud
def maillage_intra_T1():
  print("Maillage de chaque noeud T1 vers {:.0%} des autres noeuds T1.".format(proba_arc_interne_T1))
  nb_arcs=0
  for n1 in réseau_T1:
    for n2 in réseau_T1:
        if n2.nom > n1.nom:
          # un arc est crée dans 75 % des cas
          if random() < proba_arc_interne_T1:
            valeur=uniform(5 , 10)
            # on crée un voisin pour n1 et pour n2 (arc dans les deux sens)
            n1.voisins.append([n2, valeur])
            n2.voisins.append([n1, valeur])
            nb_arcs=nb_arcs+1
  print("Nombre d'arcs intra-T1 créés : {}".format(nb_arcs))

maillage_intra_T1()
affichage_réseau(réseau_T1, voisins=True)
dessine_réseau(réseau_T1)
réseau_T2 = []

 
def création_réseau_T2():
  # on crée les noeuds de T2 en leur donnant des noms entiers à la suite de ceux du T1.
  # Typiquement, si on crée 20 noeuds, les noms vont de 11 à 30.
  for i in range (len(réseau_T1)+1, len(réseau_T1)+nb_noeuds_T2+1):
    réseau_T2.append(Noeud(i,"T2"))
  print("Création du réseau T2 (transit) : {} noeuds".format(len(réseau_T2)))

création_réseau_T2()
affichage_réseau(réseau_T2)
dessine_réseau(réseau_T2)

# Maillage du réseau de transit
 
def maillage_T2():

  # on initialise à vide les voisins
  for n in réseau_T2:
    n.voisins=[]
  
  print("Maillage de chaque noeud T2 vers un ou deux noeuds T1.")
  nb_arcs_T2_T1 = 0
  for n2 in réseau_T2:
    # on sélectionne aléatoirement un ou deux noeuds du T1
    noeuds_T1_choisis=sample(réseau_T1, choice([1, 2]))
    for n1 in noeuds_T1_choisis:
      valeur=uniform(10,20)
      n2.voisins.append([n1, valeur])
      n1.voisins.append([n2, valeur])
      nb_arcs_T2_T1 = nb_arcs_T2_T1 + 1
  print("Nombre d'arcs T2-T1 créés : {}".format(nb_arcs_T2_T1))
  
  print("Maillage de chaque noeud T2 à 2 ou 3 autres noeuds de T2.")
  nb_arcs_T2_T2 = 0
  for n2 in réseau_T2:
    # on selectionne aléatoirement 2 ou 3 autres noeuds du réseau T2
    # On crée une copie des noeuds du réseau de transit
    L=réseau_T2.copy()
    # on enlève le noeud n2 de cette copie
    L.remove(n2)
    noeuds_T2_choisis=sample(L, choice([2, 3]))
    for nc in noeuds_T2_choisis:
      if nc.nom > n2.nom:
        # On crée un arc entre le noeud n2 et nc après avoir calculé sa valeur :
        valeur=uniform(10,20)
        n2.voisins.append([nc, valeur])
        nc.voisins.append([n2, valeur])
        nb_arcs_T2_T2 = nb_arcs_T2_T2 +1
  print("Nombre d'arcs T2-T2 créés : {}".format(nb_arcs_T2_T2)) 

maillage_T2()
affichage_réseau(réseau_T1, voisins=True)
affichage_réseau(réseau_T2, voisins=True)
dessine_réseau(réseau_T1+réseau_T2)

réseau_T3 = []
 
def création_réseau_T3():
  for i in range (len(réseau_T1)+len(réseau_T2)+1, len(réseau_T1)+len(réseau_T2)+nb_noeuds_T3+1):
    réseau_T3.append(Noeud(i,"T3"))
  print("Création du réseau T3 (local) : {} noeuds".format(len(réseau_T3)))

création_réseau_T3()
affichage_réseau(réseau_T3)
dessine_réseau(réseau_T3)

# maillage du réseau T3
# Chaque noeud du T3 est relié à 2 noeuds du T2 
# Chaque noeud du T3 est relié à 1 autre noeud du T3
# Les liens sont valués par une valeur comprise entre 15 et 20
 
def maillage_réseau_T3():
  print("Maillage de chaque noeud T3 vers 2 noeuds du T2.")
  nb_noeuds_T3_T2 = 0
  for n3 in réseau_T3:
    # on sélectionne aléatoirement 2 noeuds du T2
    noeuds_T2_choisis=sample(réseau_T2, 2)
    for n2 in noeuds_T2_choisis:
      valeur=uniform(15, 20)
      n3.voisins.append([n2, valeur])
      n2.voisins.append([n3, valeur])
      nb_noeuds_T3_T2 = nb_noeuds_T3_T2 +1
  print("Nombre d'arcs T3-T2 : {}".format(nb_noeuds_T3_T2))
 
  print("Maillage de chaque noeud T3 vers 1 autre noeud T3.")
  nb_noeuds_T3_T3 = 0
  #Pour relier les noeuds du T3 2 à 2,
  # On fait une boucle avançant d'un pas de 2 
  for i in range (0, nb_noeuds_T3-1, 2):
    # création d'un arc reliant 2 noeuds du T3
    valeur=uniform(15, 20)
    réseau_T3[i].voisins.append([réseau_T3[i+1], valeur])
    réseau_T3[i+1].voisins.append([réseau_T3[i], valeur])
    nb_noeuds_T3_T3 = nb_noeuds_T3_T3 +1
  print("Nombre d'arcs T3-T3 : {}".format(nb_noeuds_T3_T3))

maillage_réseau_T3()
affichage_réseau(réseau_T2, voisins=True)
affichage_réseau(réseau_T3, voisins=True)
dessine_réseau(réseau_T1+réseau_T2+réseau_T3)
# fonction appelée récursivement
# - on marque le noeud n
# - on recherche son premier voisin non marqué
# - on appelle la fonction avec ce vosin non marqué
def explorer_a_partir_du_noeud(n):
  # on marque le noeud n
  n.marque = True
  #print("Noeud exploré : {}".format(n))
  # On recherche le premier voisin du noeud non marqué
  for v in n.voisins:
    if v[0].marque == False:
      # on applique la même fonction à ce noeud
      explorer_a_partir_du_noeud(v[0])
      
def vérification_connectivité(graphe, nd):
  # graphe est une liste de noeuds
  # nd est le noeud de départ
  # On met toutes les marques à False
  for n in graphe:
    n.marque=False
  
  explorer_a_partir_du_noeud(nd)
 
  # On vérifie s'il reste des neoeuds non marqués
  nb_noeuds_isolés = 0
  for n in graphe:
    if n.marque == False:
      nb_noeuds_isolés = nb_noeuds_isolés +1 
      print("Noeud isolé : {}".format(n))
  print("Nombre de noeuds isolés : {}".format(nb_noeuds_isolés))

vérification_connectivité(réseau_T1 + réseau_T2 + réseau_T3, réseau_T3[0])
#vérification_connectivité(réseau_T3, réseau_T3[0])

# Entrées :
#    graphe est une liste des noeuds du graphe. ex : réseau_T1 + réseau_T2+ réseau_T3
#    nd est le noeud de départ
# Effet :
#    Calcule les plus courts chemins (PCCH) de nd à tous les autres noeuds.
#    Inscrit pour chaque noeud n:
#    marque : valeur du PCCH de nd à n.
#    prédecesseur : noeud qui permet d'atteindre n dans le PPCH
def plus_courts_chemins(nd, graphe):
  # On initialise toutes les marques des noeuds à l'infini (inf) sauf la marque de nd qui est initailisée à 0.
  for n in graphe:
    n.marque=inf
  nd.marque=0

  # liste des noeuds à visiter
  # Elle est initialisée par la copie des noeuds du graphe.
  noeuds_à_visiter = graphe.copy()
  
  # Tant qu'il reste des noeuds à visiter
  while len(noeuds_à_visiter)!=0:
    # On cherche le noeud à visiter ayant la marque minimum.
    # On utilise ici la fonction min avec le paramètre key indiquant avec une fonction lambda la valeur à tester.
    noeud_minimum = min(noeuds_à_visiter, key = lambda x: x.marque)
    #print("noeud minimum : ", noeud_minimum)

    # on explore les voisins du noeud minimum
    for voisin in noeud_minimum.voisins:
      if noeud_minimum.marque + voisin[1] < voisin[0].marque:
        voisin[0].marque = noeud_minimum.marque + voisin[1]
        voisin[0].prédécesseur = noeud_minimum
    # On retire le noeud_minimum de la liste des noeuds à visiter
    noeuds_à_visiter.remove(noeud_minimum)
  
#plus_courts_chemins(réseau_T1[0], réseau_T1 + réseau_T2+ réseau_T3) 
#plus_courts_chemins(réseau_T1[0], réseau_T1)
#affichage_réseau(réseau_T1 + réseau_T2+ réseau_T3, voisins=True, marque=True, pred=True)
# Entrées :
#    nd : noeud de départ
#    graphe : liste de noeuds de la classe Noeud.
# Contexte : on a auparavant calculé les plus courts chemins du noeud nd à tous les autres
# Fonction : 
def fabrication_table_routage_pour_noeud_cible(nd, graphe):
  #print("Noeud nd : {}".format(nd))
  # on parcourt tous les noeuds n du graphe (sauf nd)
  for n in graphe:
    if n != nd:
      # on va remonter les prédécesseurs de n jusqu'à ce que l'on tombe sur nd
      nx = n
      pred=None
      while nx != nd:
        pred=nx.prédécesseur
        # on met à jour la table de routage de pred
        # La table dit : Quand on est sur pred, pour atteindre n, pendre le voisin nx
        pred.table_routage[n]=nx
        nx=pred

#fabrication_table_routage_pour_noeud_cible(réseau_T1[0], réseau_T1 + réseau_T2+ réseau_T3)


def fabrications_toutes_tables_routage(graphe):
  for n in graphe:
    n.table_routage = {}
  for n in graphe:
    plus_courts_chemins(n, graphe)
    fabrication_table_routage_pour_noeud_cible(n, graphe)

fabrications_toutes_tables_routage(réseau_T1 + réseau_T2+ réseau_T3)

def affiche_chemin(ne, nd):
  # ne : nord émetteur
  print("Plus court chemin de {} à {}".format(ne, nd))
  n=ne
  plt.scatter(nd.coord[0], nd.coord[1], color=couleur_noeud(nd), s=30)
  while n != nd:
    print("{}-{}".format(n, n.table_routage[nd]))
    plt.plot([n.coord[0], n.table_routage[nd].coord[0]], [n.coord[1], n.table_routage[nd].coord[1]], couleur_arc(n, n.table_routage[nd]))
    plt.scatter(n.coord[0], n.coord[1], color=couleur_noeud(n), s=30)
    n=n.table_routage[nd]
plt.show()

affiche_chemin(choice(réseau_T1), choice(réseau_T3))

#affichage_réseau(réseau_T1+réseau_T2+réseau_T3, voisins=True, marque=True, pred=True, table=True)