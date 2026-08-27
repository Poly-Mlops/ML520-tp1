# TP1 - Rapport d'équipe

Équipe : <numéro>
Membres : <Abdelrahmane Ferchichi>

- Pour trouver les runtime dependencies, il a fallu regarder les imports dans le notebook et dans les fichiers sous `src/inferapi/`. Ce sont les dépendances nécessaires pour faire tourner l'API et le code ML.

- Les groupes de dépendances : nous avons deux groupes. `notebooks` correspond à l'exécution des notebooks (jupyter, ipykernel, ipython, seaborn), ces dépendances ne sont pas utiles en production. Le groupe `dev` contient ce qui est utilisé uniquement durant le développement : tester (pytest), qualité (ruff) et le debug (debugpy). Analyser le fichier Makefile a permis de trouver ces dépendances.

- Tout ce qui a été retiré du requirements.txt correspond à ce qui ne ressortait pas avec la commande `grep -r "import" src/` qui va chercher les imports sous src. Par exemple, seaborn n'apparaît pas dans les imports de src et uniquement dans le notebook `work.ipynb`.

- Pour `scikit-learn-intelex`, il est placé dans les extras `[project.optional-dependencies]` car c'est une fonctionnalité optionnelle : c'est une librairie qui permet d'accélérer certains traitements mais qui fonctionne seulement en x86 (Linux) ou AMD64 (Windows). `uv.lock` contient les contraintes pour toutes les plateformes : par exemple sur mon Mac ARM, cela ne s'installe pas, mais pour un coéquipier s'il est équipé de Linux ou Windows, cela va s'installer (il peut aussi choisir de ne pas l'installer). La syntaxe qui respecte PEP est : `sys_platform == 'linux' or (sys_platform == 'win32' and platform_machine == 'AMD64')`.


## Question 2 - Les métriques et le seuil

Collez votre ligne `model_trained` au seuil configuré, puis celle obtenue avec
`--decision-threshold 0.3`.

```json
```

```json
```

Quelle exactitude obtiendrait un modèle qui prédit « non » systématiquement, et que
vaut donc la vôtre ? Commentez le déplacement de la précision et du rappel, dites quel
seuil vous mettriez en production et pour qui, et expliquez ce qui se produit si
`training.decision_threshold` et `serving.prediction_threshold` divergent.

> Votre réponse ici.

## Question 3 - Le jeton, la configuration et les logs

Roulez l'application: collez la au complet la ligne `settings_loaded` et expliquez ce que `SecretStr` y a changé.

```json
```

Pourquoi deux objets de réglages plutôt qu'un seul, et qu'est-ce que cela empêche
concrètement ? Qu'est-ce qui doit remplacer `.env` quand le service tourne ailleurs
que sur votre machine, et pourquoi ?

> Votre réponse ici.

## Question 4 - Ce que `app.py` ne fait pas

`app.py` ne construit ni ses réglages ni son modèle: qu'est-ce qui permet ceci?

> Votre réponse ici.


Si `app.py` instanciait lui-même son modèle et sa configuration, qu'est-ce qui serait plus difficile à faire?

> Votre réponse ici.


Enfin: que faudrait-il changer, et où exactement, pour servir un modèle PyTorch
plutôt que le modèle scikit-learn ?

> Votre réponse ici.

## Extrait de log

Un court extrait de `out/logs/app.log` montrant une requête `/v1/predict` complète
(l'événement DEBUG et l'événement de prédiction).

```json
```

## Débogueur

Capture d'écran du débogueur arrêté sur un point d'arrêt, panneau des variables
lisible. Commitez l'image dans `reports/img/` et référencez-la ici, le bundle de
remise la contiendra:

![Point d'arrêt](img/debogueur.png)
