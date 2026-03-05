# 🤖 Planification Robuste sur Grille : A* + Chaînes de Markov

Ce projet s'inscrit dans le cadre du module d'Intelligence Artificielle (Master 1 SDIA). L'objectif est de planifier un chemin optimal pour un agent autonome dans un environnement avec obstacles (grille 2D), en combinant une **Recherche Heuristique (A*)** et une modélisation de l'incertitude via les **Chaînes de Markov** et la **Simulation Monte-Carlo**.

---

## 🗺️ Environnement de Test
La configuration étudiée est une grille 5x5 avec obstacles. Le tracé bleu représente le plan déterministe optimal (coût de 8 pas) généré par l'algorithme A*, permettant de relier l'état initial (0,0) au but (4,4).

<img width="902" height="719" alt="image" src="https://github.com/user-attachments/assets/16458905-9fa3-4530-aa97-f967ebf50f38" />

Figure 1 : Environnement de test (Grille Moyenne) et chemin déterministe optimal généré par l'algorithme A.*

---

## 📊 Expérience 1 : Comparaison des Algorithmes
Nous avons comparé les performances de UCS, Greedy et A* sur trois niveaux de complexité d'environnement (Facile, Moyenne, Difficile).

| Grille | Algorithme | Coût du chemin | Nœuds développés | Temps d'exécution (s) |
| :--- | :--- | :---: | :---: | :---: |
| **Facile** | UCS | 8 | 25 | 0.00036 |
| | Greedy | 8 | 9 | 0.00012 |
| | A* | 8 | 25 | 0.00030 |
| **Moyenne** | UCS | 8 | 20 | 0.00019 |
| | Greedy | 8 | 9 | 0.00008 |
| | A* | 8 | 20 | 0.00015 |
| **Difficile** | UCS | 8 | 12 | 0.00020 |
| | Greedy | 8 | 9 | 0.00012 |
| | A* | 8 | 9 | 0.00013 |

> **Analyse :** Tous les algorithmes convergent vers un coût optimal de 8. Cependant, sur la grille difficile, A* démontre toute l'efficacité de son heuristique de Manhattan (admissible et cohérente) en réduisant l'espace de recherche à seulement 9 nœuds, contre 12 pour UCS.

 <img width="1006" height="463" alt="image" src="https://github.com/user-attachments/assets/135158bc-ff33-41f3-8331-cca9afffbd0b" />

Figure 2 : Comparaison des performances (Nœuds développés, Temps d'exécution, Coût) des           algorithmes UCS, Greedy et A sur trois niveaux de complexité.*

---

## 🎲 Expérience 2 : Impact de l'Incertitude sur le Plan
En nous basant sur le chemin généré par A*, nous avons fait varier le taux d'incertitude ε (déviations stochastiques) pour confronter la théorie markovienne à une simulation Monte-Carlo.

<img width="856" height="522" alt="image" src="https://github.com/user-attachments/assets/cfd890a4-8174-4f8f-b2bc-0483fac4c593" />

Figure 3 : Évolution de la probabilité de succès et du temps moyen d'absorption en fonction    du taux d'incertitude ε

### 🥧 Divergence des modèles pour une forte incertitude (ε = 0.3)

<img width="504" height="262" alt="image" src="https://github.com/user-attachments/assets/51a04e18-d316-43f4-a020-ab886e5e0f7e" />

Figure 4 : Comparaison des taux de réussite prévus par le modèle théorique markovien stricte face à la simulation empirique Monte-Carlo pour une forte incertitude (ε = 0.3).

> **Analyse de l'écart :** Le modèle théorique markovien est strict (une sortie du chemin = échec absolu, soit 47.1% de succès). À l'inverse, la simulation Monte-Carlo met en évidence la résilience réelle de l'agent qui parvient à retrouver son but dans 73.6% des cas malgré les glissements.

---

## 📈 Expérience 3 : Matrice de Transition Stochastique
Modélisation de la dynamique de l'agent via la matrice P pour ε = 0.2.

![Heatmap Matrice P](Heatmap.png)
*(Remplacer Heatmap.png par l'image de la matrice bleue)*

> **Analyse :** La heatmap confirme que notre matrice P est bien stochastique et creuse. Les fortes probabilités (bleu foncé) se concentrent sur la diagonale (suivi du plan optimal), tandis que les valeurs plus claires illustrent les probabilités de glissement vers des états latéraux.

---

## 🛠️ Comment exécuter le code localement
1. Cloner ce repository :
   `git clone https://github.com/atiqaessayouti/...`
2. Installer les bibliothèques requises :
   `pip install matplotlib numpy`
3. Lancer les expériences globales :
   `python experiments.py`

---
🎓 *Projet réalisé par **Atiqa Essayouti** - Master 1 SDIA - ENSET Mohammedia*
