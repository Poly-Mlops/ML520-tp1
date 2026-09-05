# Workflow Git – ML520 TP1 (2 dépots : orga + perso)

**Dé··pots** :  
- Orga : `git@github.com:Poly-Mlops/ML520-tp1.git`  
- Perso : `git@github.com:delinocode/Poly-ML520-tp1-Structuring-a-Machine-Learning-Project.git`

**Rè··gle** :  
- `dev` existe déjà → **jamais de `-b`**, on utilise `git switch dev`.  
- Nouvelle branche (feature) → `git switch -b <nom>` pour créer + switcher.

---

## 1. Configuration initiale (une seule fois)

```bash
cd ~/code

# Cloner
git clone git@github.com:Poly-Mlops/ML520-tp1.git Ml520-tp1
cd Ml520-tp1

# Nom / email
git config --global user.name "delinocode"
git config --global user.email "abdel.ferchi38@gmail.com"

# Remotes
git remote rename origin orga
git remote add perso git@github.com:delinocode/Poly-ML520-tp1-Structuring-a-Machine-Learning-Project.git

git remote -v
```

Tu dois voir `orga` et `perso` en SSH.

---

## 2. Workflow quotidien (sur `dev`)

```bash
cd ~/code/Ml520-tp1

git fetch --all
git switch dev
git pull orga dev

# modifs...

git add .
git commit -m "Message"

git push orga dev
git push perso dev
```

---

## 3. Créer une nouvelle branche (sans switcher dedans)

Depuis `dev` (ou `main`) :

```bash
cd ~/code/Ml520-tp1

git switch dev

# Créer feature-x sans basculer dessus
git branch feature-x
```

À·à··partir de là, `feature-x` existe localement, mais tu es toujours sur `dev`.

---

## 4. Switcher dans cette nouvelle branche, travailler, pousser

```bash
cd ~/code/Ml520-tp1

# Basculer sur feature-x
git switch feature-x

# modifs...
git add .
git commit -m "Message"

# Pousser sur les deux dépots (premiè··re fois avec -u)
git push -u orga feature-x
git push -u perso feature-x
```

Ensuite, les fois suivantes :

```bash
git push orga feature-x
git push perso feature-x
```

---

## 5. Merger une branche dans `main`

Quand `dev` ou `feature-x` est prête :

```bash
cd ~/code/Ml520-tp1

git switch main
git pull orga main

git merge dev
# ou : git merge feature-x

git push orga main
git push perso main
```

---

## 6. Mini-explications Git

- `git clone <url> <dossier>` : télécharge un dépot dans un nouveau dossier.
- `git remote rename origin orga` : renomme le remote `origin` en `orga`.
- `git remote add perso <url>` : ajoute un second remote nommé `perso`.
- `git remote -v` : affiche les remotes et leurs URLs.

- `git fetch --all` : met à jour les infos des branches distantes.
- `git pull <remote> <branche>` : met ta branche locale à jour avec le remote.
- `git switch <branche>` : change de branche (ex. `dev`, `main`, `feature-x`).
- `git branch <nom>` : crée une branche locale sans changer de branche.
- `git switch -b <nom>` : crée une branche et bascule dessus.

- `git add .` : prépare tous les fichiers modifié··s pour le commit.
- `git commit -m "Message"` : crée un commit avec un message.
- `git push <remote> <branche>` : envoie ta branche vers le remote.
- `git push -u <remote> <branche>` : pousse et configure le “tracking”.

- `git merge <branche>` : fusionne cette branche dans celle où tu es.

---

Tu peux garder ce fichier comme référence unique :  
- config initiale (une fois),  
- workflow quotidien,  
- création / utilisation de nouvelles branches,  
- merge dans `main`,  
- et un mini-guide des commandes à la fin.