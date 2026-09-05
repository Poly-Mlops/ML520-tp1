# TP1 – Analyse Complète : État des Lieux

*Fichier généré le: 2026-08-31*
*Mis à jour le: 2026-09-01*
*Répertoire: /Users/delino/code/python/poly/520/s1/Lab 1 /ML520_TP1*

> ⚠️ Cette version **corrige** plusieurs points de l'édition du 31/08 (voir « Corrections »).
> Les tests n'ont **pas** pu être relancés ici (cache uv inaccessible) : les statuts de
> tests sont donc *à confirmer* en roulant `make tests`.

---

## 📋 Légende

| Symbole | Signification |
|---------|---------------|
| ✅ | **Terminé / implémenté** |
| 🟡 | **En cours / Partiel** |
| ❌ | **Non commencé** |
| 🔴 | **Cassé / erreur de code** |
| 📝 | **Commentaire TODO(LAB) présent mais non vérifié** |
| ⚠️ | **À vérifier (tests non relancés)** |

---

## 🆕 Corrections par rapport à l'édition du 31/08

| Point | Version 31/08 | Réalité constatée (01/09) |
|-------|---------------|---------------------------|
| `requirements.txt` | « Fichier toujours présent » | ✅ **Supprimé du projet** (plus présent) |
| Entrypoint `pyproject.toml` | « TODO non rempli » | ✅ **Déclaré** : `inferapi = "inferapi.cli:main"` |
| Flags du parser `train` (cli.py:47) | « certains flags déjà ajoutés » | ✅ **Complets** (`--data`, `--n-estimators`, `--max-depth`, `--seed`, `--decision-threshold`, `--overwrite`) |
| `run_train` (cli.py:103) | « partiel » | 🔴 **Erreur de syntaxe** : `dataframe:Data` dans un *appel* de fonction = SyntaxError ; `Data` non défini. Le module `cli` ne peut pas être importé → toutes les commandes CLI sont mortes. |
| `training_procedure` (train.py) | « coquille vide » | 🟡 **Brouillon cassé** : 3 lignes déjà écrites mais incorrectes (`fit()` sur un `Dataset` au lieu d'un `DataFrame`, `get_model_evaluation_metrics` sans appel, aucun `return`). |
| `test_predictor` | « 100 % passent » | ⚠️ **À confirmer** : dépend de `training_procedure` qui est cassé → très probablement en échec en l'état. |
| `test_api_key_check_without_a_token_is_refused` | « fait » | ⚠️ **Passe peut-être pour la mauvaise raison** : `SecurityConfig` n'a pas encore de champ `api_token` ; c'est `extra="forbid"` qui rejette le paramètre inconnu, pas la validation demandée. |

---

## 1. Tous les `# TODO(LAB)` dans le code source

Total : **19 commentaires** répartis dans 7 fichiers.

### 1.1 `src/inferapi/config.py` (2 TODOs)

| Ligne | TODO | Statut |
|-------|------|--------|
| 60 | `add api_token, and the validation that refuses to load when the check…` | ❌ Non commencé |
| 121 | `declare the sections the serving entrypoint needs, and only those.` | ❌ Non commencé (`InferApiSettings` est vide `class …(WithYamlSources): ...`) |

**Actions nécessaires :**
- Ajouter `api_token: SecretStr` dans `SecurityConfig`
- Ajouter un `model_validator` qui lève `ValidationError` si `enable_api_key_check=True` et pas de jeton
- Remplir `InferApiSettings` avec (et seulement) les sections serving : `serving`, `security`, `logging`
- Rappeler que `app.py:157` attend déjà `settings.security.api_token.get_secret_value()`

### 1.2 `src/inferapi/train.py` (5 TODOs)

| Ligne | TODO | Statut |
|-------|------|--------|
| 58 | pipeline à 2 étapes nommées, hyperparams depuis config | ✅ **Fait** — `data_processor` + `model`, hyperparams depuis `TrainingConfig` |
| 82 | mêmes métriques que le notebook | ✅ **Fait** — 6 métriques retournées |
| 98 | fit, et rien d'autre | ✅ **Fait** — `train()` ne fit que sur `train_x/train_y` |
| 99 | debug log des shapes des splits | ✅ **Fait** — `logger.debug("split data …")` |
| 117 | split/fit/score val/log `model_trained`/persist/return | 🔴 **Brouillon cassé** — `fit()` reçoit un `Dataset`, aucune évaluation, aucun persist, aucun log `model_trained`, aucun `return` |

**Actions nécessaires :**
- `training_procedure` : splitter avec `get_dataset`, entraîner via `train()`, évaluer sur la **validation** avec `training.decision_threshold`, `persist_model`, journaliser `model_trained` en une ligne, retourner `(model, metrics)`, respecter `overwrite_model`.

### 1.3 `src/inferapi/serve.py` (3 TODOs)

| Ligne | TODO | Statut |
|-------|------|--------|
| 10 | `load_predictor()` + module-level `app` | ❌ Non commencé |
| 20 | implémenter `load_predictor` | ❌ Non commencé (retourne `...`) |
| 25 | `app = create_app(...)` | ❌ Non commencé |

**Actions nécessaires :**
- Implémenter `load_predictor(settings: InferApiSettings) -> Predictor` (construire un `SklearnPredictor` depuis `settings.serving.model_path` + `prediction_threshold`)
- Créer l'instance `app = create_app(settings, load_predictor)` avec `settings = InferApiSettings()` — seul module autorisé à nommer une implémentation concrète de `Predictor`

### 1.4 `src/inferapi/cli.py` (2 TODOs)

| Ligne | TODO | Statut |
|-------|------|--------|
| 47 | compléter le parser `train` | ✅ **Fait** (tous les flags + mapping `config_flags` correct) |
| 100 | `run_train` : charger le frame et passer à `training_procedure` | 🔴 **SyntaxError** — `dataframe:Data` invalide dans l'appel, `Data` non défini, `train_config` reçoit `TrainingSettings` au lieu de `settings.training`, pas de `return` |

**Actions nécessaires :**
- Corriger le SyntaxError de `run_train`, charger le frame via `load_raw(settings.data.parquet_path)`, passer `settings.training`, passer `args.output`/`args.overwrite`, et `return 0`

### 1.5 `src/inferapi/predictor.py` (1 TODO)

| Ligne | TODO | Statut |
|-------|------|--------|
| 48 | implémenter `SklearnPredictor` (chargement joblib + seuil) | ❌ Non commencé |

**Actions nécessaires :**
- `__init__` : stocker `artifact_path` + `threshold`, charger le pipeline via `joblib.load`
- `predict` : `proba = model.predict_proba(features)[:, 1]`, label = `int(proba[0] >= threshold)`, retourner `(label, float(proba[0]))`
- Optionnel : override `get_version()` avec `file_creation_time(artifact_path)`

### 1.6 `src/inferapi/logging_setup.py` (2 TODOs)

| Ligne | TODO | Statut |
|-------|------|--------|
| 33 | handler fichier `out/logs/app.log` qui capture toujours DEBUG | ❌ Non commencé |
| 41 | ajouter le fichier si configuré | ❌ Non commencé |

**Actions nécessaires :**
- `FileHandler` sur `log_settings.debug_file`, `setLevel(logging.DEBUG)`, `mkdir(parents=True, exist_ok=True)` sur le parent, puis `root.addHandler(file_handler)`

### 1.7 `src/inferapi/app.py` (1 TODO)

| Ligne | TODO | Statut |
|-------|------|--------|
| 209 | log `request_id`, `model_version`, `latency_ms`, prédiction | ❌ Non commencé |

**Actions nécessaires :**
- Avant le `return` de la route `/v1/predict` : `logger.info("prediction_completed request_id=%s model_version=%s latency_ms=%s prediction=%s probability=%s", ...)` (lazy evaluation `%s`)

---

## 2. Toutes les tâches du TP1 (telles que définies dans TP1.md)

Total : **10 tâches** (A à J) + questions du rapport

### Tâche A – Gestion des dépendances 🟡 ~60 %

| Élément | Statut | Notes |
|---------|--------|-------|
| Runtime deps en contraintes d'intervalle | 🟡 Partiel | Tout est listé, mais `pandas==2.2.3` est un *pin*, pas un intervalle ; les consignes demandent des bornes supérieures (`>=X,<Y`) |
| `joblib` déclaré dans `dependencies` ? | ❌ Manquant | Importé dans `train.py` et `predictor.py` mais absent du `pyproject.toml` |
| Groupe `dev` | ✅ | `pytest`, `ruff`, `debugpy` |
| Groupe `notebooks` (`make notebook-launch`) | ✅ | `jupyter`, `ipykernel`, `ipython`, `seaborn` |
| Extras `scikit-learn-intelex` avec garde de plateforme | 🟡 Partiel | Présent, mais la condition n'exclut pas Linux ARM (`sys_platform == 'linux'` sans filtre `platform_machine`) |
| Entrypoint `inferapi = "inferapi.cli:main"` | ✅ Déclaré | |
| Supprimer ou régénérer `requirements.txt` | ✅ Supprimé | |

### Tâche B – Outils de qualité de code ❌ non testée

| Élément | Statut | Notes |
|---------|--------|-------|
| `make code-quality` (ruff lint + format) | ❌ Échoue | Notamment à cause de la SyntaxError dans `cli.py` |

### Tâche C – Configuration typée ❌ non commencé

- `InferApiSettings` vide
- `SecurityConfig` sans `api_token` ni validateur
- `TrainingSettings` complet (servir d'exemple)

### Tâche D – Migration notebook vers `src/` 🟡 partiel

| Élément | Statut |
|---------|--------|
| Code pipeline/entraînement dans `src/train.py` | 🟡 `build_model()`/métriques OK ; `training_procedure` cassé |
| Pas d'hyperparamètres en dur dans `src/` | ✅ |
| Deux étapes nommées du pipeline | ✅ |
| Notebook importe depuis `inferapi` | ❌ À vérifier |
| Activation `scikit-learn-intelex` en dur dans notebook | ❌ À déplacer dans les extras |

### Tâche E – Métriques d'évaluation 🟡 ~50 %

- `get_model_evaluation_metrics()` migré ✅
- Seuil depuis `training.decision_threshold` 🟡 accepté mais pas utilisé par `training_procedure`
- Évaluer sur l'ensemble de **validation** ❌
- Journaliser `model_trained` en une seule ligne ❌

### Tâche F – Le débogueur ❌ non commencé
- Aucun point d'arrêt testé ; dépend de la tâche J pour être faite

### Tâche G – Gestion des secrets ❌ non commencé
- Identique à C pour `SecurityConfig` (`api_token` en `SecretStr`, fail-fast si check activé sans jeton)

### Tâche H – Journalisation avec `logging` 🟡 ~40 %

- Niveau paramétrable par config ✅
- Handler fichier (`out/logs/app.log`, toujours DEBUG) ❌
- Ligne de clôture chaque requête `/v1/predict` ❌
- `getLogger(__name__)` dans chaque module ✅
- Lazy evaluation `%s` 🟡 (utilisé dans `data.py`, `train.py`, `app.py`)

### Tâche I – Ligne de commande (CLI) 🔴 cassée

- Parser `train` : tous les flags présents et bien mappés ✅
- `run_train` : SyntaxError (`dataframe:Data`) → tout le CLI est mort 🔴
- Point d'entrée déclaré dans `pyproject.toml` ✅
- Précedence flags/env/YAML 🟡 à vérifier après correction

### Tâche J – Le service ❌ non commencé

- `SklearnPredictor` : squelette seulement ❌
- `serve.py` : non fonctionnel ❌
- `create_app()` : existe, avec `ApiTokenMiddleware` + `request_id` + `served_by_header` 🟡 (l'`app` de `serve.py` est une coquille)

### Questions du rapport (à répondre dans `reports/tp1.md`)

| Question | Statut |
|----------|--------|
| Q1 – Gestion des dépendances | ✅ Ébauche rédigée (à compléter : `joblib` manquant, pins, garde intelex) |
| Q2 – Métriques et seuil | ❌ Non commencée |
| Q3 – Jeton, config et logs | ❌ Non commencée |
| Q4 – Ce que `app.py` ne fait pas | ❌ Non commencée |
| Q5 – Modèle PyTorch plutôt que scikit-learn | ❌ Non commencée |
| Extrait de logs | ❌ Non généré |

---

## 3. Ce qui est déjà fait (✅)

### 3.1 Structure du projet
- ✅ Disposition `src/inferapi/` avec tous les modules attendus
- ✅ `Makefile` avec toutes les cibles attendues
- ✅ `pyproject.toml` structuré (`[project]`, `[project.scripts]`, `[project.optional-dependencies]`, `[dependency-groups]`, `[tool.ruff]`, `[tool.pytest.ini_options]`)
- ✅ `uv.lock` commité (environnement verrouillé)
- ✅ `.env.example` pour les secrets
- ✅ `.gitignore` qui exclut `.env` et `.venv`
- ✅ `configs/config.yaml` avec toute la configuration non secrète
- ✅ Tests existants dans `tests/`
- ✅ Notebook `notebooks/work.ipynb` avec les notes 📝
- ✅ `requirements.txt` **supprimé**

### 3.2 Code source existant
- ✅ `src/inferapi/data.py` – Chargement, conversion CSV→Parquet, splitting train/val/test
- ✅ `src/inferapi/utils.py` – `file_creation_time()`
- ✅ `src/inferapi/__init__.py` – Version `__version__ = "0.1.0"`
- ✅ `src/inferapi/config.py` – Modèles `DataConfig`, `TrainingConfig`, `ServingConfig`, `LoggingConfig` + `TrainingSettings` (YAML + `.env` + env vars, préfixe `ML520_`, séparateur `__`)
- ✅ `src/inferapi/train.py` – `build_model()` (pipeline 2 étapes), `get_model_evaluation_metrics()` (6 métriques), `train()`, `persist_model()`
- ✅ `src/inferapi/serve.py` – Structure avec `create_app()`, routes et middlewares câblés
- ✅ `src/inferapi/app.py` – Routes FastAPI, `ApiTokenMiddleware`, middleware `request_id`, middleware `served_by_header`
- ✅ `src/inferapi/cli.py` – `data-convert` complet ; parseur `train` avec tous les flags + `config_flags` corrects
- ✅ `src/inferapi/predictor.py` – ABC `Predictor` avec `predict()` et `get_version()` ; squelette `SklearnPredictor`
- ✅ `src/inferapi/logging_setup.py` – Configuration handler stdout + formatage des logs

### 3.4 Tests
- ⚠️ `tests/test_data.py` – conversion CSV↔Parquet, feature/label splitting, tailles de split : **indépendants de `training_procedure` → probablement verts**
- ⚠️ `tests/test_config.py` – le test `api_token` passe peut-être, mais pour la mauvaise raison (voir Corrections)
- ⚠️ `tests/test_predictor.py` – dépend de `training_procedure` : **très probablement en échec**

---

## 4. Recommandations d'ordre de priorité

### Priorité 1 (Critique – sans quoi le lab ne tourne pas)
1. **Corriger la SyntaxError de `cli.py` (`run_train`)** : c'est ce qui bloque *tout* le CLI et possiblement `make tests`
2. **Réécrire `training_procedure`** (`train.py`) : split → train → évaluation validation → persistance → log `model_trained` → retour
3. **Implémenter `SklearnPredictor`** (`predictor.py`) : chargement joblib + seuil de décision
4. **Compléter `SecurityConfig` + `InferApiSettings`** (`config.py`) : `api_token: SecretStr`, validateur fail-fast, sections serving-only

### Priorité 2 (Important – fonctionnalités manquantes)
5. **Implémenter `load_predictor` et `app`** dans `serve.py`
6. **Handler fichier** dans `logging_setup.py` (`out/logs/app.log`, DEBUG toujours capturé)
7. **Ligne de clôture `/v1/predict`** dans `app.py` (lazy eval, `clé=%s`)

### Priorité 3 (Report / Nettoyage)
8. **Corriger `pyproject.toml`** : ajouter `joblib`, passer `pandas` en intervalle, resserrer la garde `scikit-learn-intelex`
9. **Migrer le notebook** vers des imports depuis `inferapi`
10. Rouler `make code-quality` et corriger sans toucher aux règles
11. Lancer le débogueur (`make serve-debug`) et capturer les écrans dans `reports/img/`
12. Répondre aux questions restantes dans `reports/tp1.md`

---

## 5. État global résumé

| Catégorie | Pourcentage Terminé | Commentaire |
|-----------|-------------------|-------------|
| **Sécurité syntaxique** | 🔴 bloqué | SyntaxError dans `cli.py` ; tous les appels CLI meurent |
| **Code source (TODO LAB)** | ~30 % (6/19) | `build_model`, métriques, `train`, shapes de split, flags du parser `train` |
| **Dépendances (`pyproject.toml`)** | ~70 % | Entrypoint OK, groupes OK, extras OK, `requirements.txt` supprimé ; reste `joblib` + intervalles + garde intelex |
| **Configuration (`config.py`)** | ~30 % | `TrainingSettings` complet ; `InferApiSettings` et `SecurityConfig` incomplets |
| **Entraînement (`train.py`)** | ~50 % | Pipeline + métriques OK ; `training_procedure` est un brouillon cassé |
| **Service/API (`serve.py` + `app.py`)** | ~35 % | `create_app` OK ; prédiction et logs de clôture manquants |
| **CLI (`cli.py`)** | 🔴 bloqué | Parseur OK ; `run_train` invalide |
| **Outils qualité (ruff)** | 0 % | Non relancé ; la SyntaxError fera échouer `make code-quality` |
| **Tests** | ⚠️ à confirmer | `test_data` probablement OK ; `test_predictor` probablement KO |

**Conclusion :** La base est **plus solide** qu'indiqué le 31/08 (dépendances majoritairement déclarées, entrypoint fait, `requirements.txt` supprimé, flags CLI complets). Le vrai blocage n'est pas la config ni les secrets : c'est la **SyntaxError dans `cli.py`** et le **brouillon de `training_procedure`**. Corriger ces deux-là en premier, puis enchaîner config/secrets → predictor → logging → `serve.py`.
