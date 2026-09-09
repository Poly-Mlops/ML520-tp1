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

```2026-09-08T17:50:58 INFO     inferapi.train | model_trained positive_rate=0.11266237707903363 accuracy=0.9008134029379629 precision=0.696113074204947 recall=0.2122844827586207 roc_auc=0.8110943758521615 average_precision=0.4891524469862889
```

```2026-09-08T17:52:49 INFO     inferapi.train | model_trained positive_rate=0.11266237707903363 accuracy=0.8864877989559306 precision=0.49641025641025643 recall=0.521551724137931 roc_auc=0.8110943758521615 average_precision=0.4891524469862889

```

Quelle exactitude obtiendrait un modèle qui prédit « non » systématiquement, et que
vaut donc la vôtre ? , et 

Dans notre contexte, 11,27% des cas sont 'oui' (positive_rate), donc cela veut dire que (100% − 11,27%) = 88,73% des cas sont 'non'. Un modèle qui répondrait toujours 'non' aurait donc une exactitude de 88,73%.
Or, mon modèle obtient 90,08% d'exactitude, et avec --decision-threshold 0.3, cela tombe à 88,65 ce qui est même en dessous du modèle qui répond toujours 'non'. Donc se baser uniquement sur l'exactitude ne suffit pas pour dire que le modèle est bon. Il faut regarder d'autres métriques, comme  precision, recall.

Commentez le déplacement de la précision et du rappel, dites quel
seuil vous mettriez en production et pour qui ?

Seuil de 0,5 : précision = 0,7 et rappel = 0,2.
Seuil de 0,3 : précision = 0,5 et rappel = 0,52.

Baisser le seuil augmente le recall donc on rate moins de vrais cas positifs, mais la précision diminue.

Je choisirais le seuil de 0,3 car je ne veux pas louper un client potentiel, même si cela demande un peu plus de vérification. Cela reste un outil d'aide à la prise de décision, pas une décision automatique. C'est donc pour l'équipe qui traite les alertes ou fait les relances clients, qui peut filtrer manuellement les faux positifs supplémentaires.

Expliquez ce qui se produit si `training.decision_threshold` et `serving.prediction_threshold` divergent.

`training.decision_threshold` est le seuil utilisé pour évaluer le modèle à l'entraînement. `serving.prediction_threshold` est le seuil réellement appliqué en prod.

Si les deux divergent, les métriques qu'on a validées (recall et precision) correspondent plus à ce qui tourne vraiment en production. On mesure avec un seuil, mais le système en donne un autre. Du coup le monitoring est faux et on peut croire que tout va bien alors que non.

## Question 3 - Le jeton, la configuration et les logs

Roulez l'application: collez la au complet la ligne `settings_loaded` et expliquez ce que `SecretStr` y a changé.

```2026-09-08T17:57:53 DEBUG    inferapi.app | settings_loaded settings={'data': {'csv_path': 'data/dataset.csv', 'parquet_path': 'data/dataset.parquet'}, 'serving': {'model_path': 'out/models/model.joblib', 'prediction_threshold': 0.5, 'simulate_work_ms': 0}, 'security': {'api_token': '**********', 'enable_api_key_check': True}, 'logging': {'level': 'INFO', 'debug_file': 'out/logs/app.log'}}

```
Sans `SecretStr`, le champ api_token afficherait le token en clair. En utilisant `SecretStr`, on masque automatiquement la valeur quand elle est sérialisée pour les logs ou autre.


Pourquoi deux objets de réglages plutôt qu'un seul, et qu'est-ce que cela empêche
concrètement ? 

Nous avons deux classes pour les réglages en entraînement et en inférence : TrainingSettings et InferApiSettings lisent le même configs/config.yaml, mais chacun ne déclare que les sections dont il a besoin. Ça empêche qu'un code lancé par inferapi train puisse accéder à security.api_token, parce que ce champ n'existe tout simplement pas dans TrainingSettings. Et donc cela évite les fuites de secret, ou de copier le token sans le vouloir par exemple.

Qu'est-ce qui doit remplacer `.env` quand le service tourne ailleurs
que sur votre machine, et pourquoi ?

En local, .env est pratique : on le modifie à la main, on régénère un token rapidement. En production, on ne peut pas faire ça manuellement ni exposer le secret de cette façon, parce que le risque c'est que le fichier .env soit accidentellement commité dans git, copié sur un serveur non sécurisé, ou lu par n'importe qui sur la machine.

On utilise à la place les variables d'environnement injectées par un serveur externe comme AWS ou Kubernetes. Le fichier .env disparaît : c'est la plateforme qui gère et injecte le secret au démarrage, donc le token n'est jamais exposé ni copié à la main.

## Question 4 - Ce que `app.py` ne fait pas

`app.py` ne construit ni ses réglages ni son modèle: qu'est-ce qui permet ceci?

C'est serve.py qui fait tout avant : il crée la configuration InferApiSettings() (qui lit configs/config.yaml) et la fonction load_predictor (qui sait créer un SklearnPredictor). Ensuite serve.py passe ces deux choses à create_app(settings, load_predictor).

app.py reçoit juste des objets déjà construits, sans savoir comment les fabriquer.

Si `app.py` instanciait lui-même son modèle et sa configuration, qu'est-ce qui serait plus difficile à faire?

app.py ne reçoit que ses settings et son modèle de serve.py. Si app.py construisait lui-même ses affaires, create_app() contiendrait InferApiSettings() et SklearnPredictor(...) dedans.

Pour our tester app.py, il faudrait un vrai configs/config.yaml, un vrai .env avec un vrai token, et un vrai .joblib sur disque. Avec l'injection actuelle, un test peut juste passer une fausse config en mémoire et un faux modèle pas besoin de vrais fichiers.


Enfin: que faudrait-il changer, et où exactement, pour servir un modèle PyTorch
plutôt que le modèle scikit-learn ?

Juste deux fichiers à toucher, et rien dans app.py :

predictor.py, créer une nouvelle classe PyTorchPredictor qui sait charger un modèle PyTorch et faire une prédiction avec.
serve.py, remplacer SklearnPredictor par PyTorchPredictor dans la fonction load_predictor.

app.py ne changerait pas du tout : il ne connaît que l'interface Predictor, pas quelle classe concrète est utilisée derrière

## Extrait de log

Un court extrait de `out/logs/app.log` montrant une requête `/v1/predict` complète
(l'événement DEBUG et l'événement de prédiction).

```
2026-09-08T20:19:33 DEBUG    inferapi.app | prediction_started request_id=f4af77d1
2026-09-08T20:19:33 INFO     inferapi.app | The prediction is finish with :request_id=f4af77d1, model_version=2026-09-08 21:50:58.740710+00:00, latency_ms=71.66932302061468, label=0 , probability=0.06017314513219236

```

## Débogueur

Capture d'écran du débogueur arrêté sur un point d'arrêt, panneau des variables
lisible. Commitez l'image dans `reports/img/` et référencez-la ici, le bundle de
remise la contiendra:

![Point d'arrêt](img/debogueur.png)
