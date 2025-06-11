Questa guida fornisce istruzioni passo-passo per l'utilizzo di **Git Flow**, assicurando un processo di sviluppo coerente per tutto il team.

---

## Requisiti
- `git` e `git-flow` installati
- Accesso al repository su **GitLab**
- Configurazione dell'utente Git:
  ```sh
  git config --global user.name "IlTuoNome"
  git config --global user.email "tuaemail@example.com"
  ```

---

## Inizializzare Git Flow
Se non è ancora stato fatto:
```sh
git flow init
```
Accetta i nomi di default per i branch (`develop`, `main`, `feature/`, ecc.).

---

## Aggiungere una Nuova Feature

1. Assicurati di essere su `develop` e aggiornalo:
   ```sh
   git checkout develop
   git pull origin develop
   ```
2. Crea un branch per la feature:
   ```sh
   git flow feature start nome-feature
   ```
3. Sviluppa la feature facendo commit regolari:
   ```sh
   git add .
   git commit -m "feat: Implementata funzionalità X"
   ```
4. Pusha il branch remoto per condividerlo:
   ```sh
   git push origin feature/nome-feature
   ```
5. Quando la feature è pronta, fai il merge **senza eliminare il branch**:
   ```sh
   git checkout develop
   git merge --no-ff feature/nome-feature
   git push origin develop
   git push origin feature/nome-feature  # Mantiene il branch remoto
   ```

---

## Creare una Merge Request su GitLab

1. Vai su **GitLab** → Repository → **Merge Requests** → **New Merge Request**
2. Seleziona `feature/nome-feature` come **source** e `develop` come **target**
3. Aggiungi una descrizione chiara del lavoro svolto
4. Assegna la MR a un membro del team per revisione (opzionale)
5. Una volta approvata, esegui il merge!

---

## Rilasciare una Versione

1. Assicurati che `develop` sia aggiornato:
   ```sh
   git checkout develop
   git pull origin develop
   ```
2. Crea il branch di release:
   ```sh
   git flow release start v1.0.0
   ```
3. Se necessario, applica eventuali fix e commit.
4. Finalizza la release **senza eliminare il branch**:
   ```sh
   git checkout main
   git merge --no-ff release/v1.0.0
   git checkout develop
   git merge --no-ff release/v1.0.0
   ```
   Questo fonderà la release in `main` e `develop`, creando anche un **tag**.

5. Pusha i branch aggiornati e i tag **senza eliminare il branch di release**:
   ```sh
   git push origin main develop --tags
   git push origin release/v1.0.0  # Mantiene il branch della release
   ```

---

## 🛠 Cosa fare in caso di errori?

### Ho dimenticato di creare una feature branch e ho già fatto commit su `develop`!
1. Crea un branch feature a partire da `develop`:
   ```sh
   git branch feature/nome-feature
   ```
2. Sposta i commit sulla feature branch:
   ```sh
   git checkout feature/nome-feature
   git rebase develop
   ```
3. Torna su `develop` e resetta all'ultimo stato stabile:
   ```sh
   git checkout develop
   git reset --hard origin/develop
   ```

### Ho fatto il merge di una feature ma ci sono bug!
1. Crea un **hotfix**:
   ```sh
   git flow hotfix start fix-bug
   ```
2. Correggi il bug, fai commit e chiudi l’hotfix:
   ```sh
   git flow hotfix finish fix-bug
   ```
3. Pusha i branch aggiornati:
   ```sh
   git push origin main develop
   ```

---

## Buone Pratiche
✔️ Pulla sempre `develop` prima di iniziare una nuova feature  
✔️ Scrivi commit chiari e descrittivi  
✔️ Testa il codice prima di fare il merge  
✔️ Usa le Merge Request per revisioni e feedback  
✔️ Evita di lavorare direttamente su `develop` o `main`  

---

## 🔧 Cambiare Editor Predefinito di Git (Opzionale)

Se non vuoi usare Vim per i messaggi di commit:
- **Nano (più semplice):**
  ```sh
  git config --global core.editor "nano"
  ```
- **VS Code:**
  ```sh
  git config --global core.editor "code --wait"
  ```

---

Se hai domande, chiedi nel gruppo
