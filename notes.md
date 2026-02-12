## 1. Fork this repo into your GitHub Account and clone

## Legacy application: How to Setup and Run (The "Painful" Way)

To demonstrate **Factor 5 (Build/Release/Run) violations**, you should perform these steps manually in front of the audience (or explain that you had to do them).

### Step 1: Create a venv

```python3 -m venv .venv
. .venv/bin/activate
```

### Step 2: Install Dependencies

```Bash
pip install -r requirements_legacy.txt
# or
pip install Flask
```

### Step 3: Manual Folder Creation (The Trap)
To run the application: `python3 legacy-app.py`
In a 12-factor app, the app creates what it needs or uses external services.
In this legacy app, if you run python `legacy_app.py`, it might fail or behave weirdly if permissions aren't right, or you have to "prep" the server.
Failure: No `logs`, `uploads`, and `counter` directories.

### Check the output in the browser

## Violations
    - 2: Dependencies not requirements.txt used
    - 3: Hard coded secrets
    - 4: The Database is coupled to the Application Code
    - 5: manual and single build, run, release process
    - 6: State is stored in files
    - 7: Hard coded port
    - 8: Unable spwan concurrent processes, the parallel app will be stand alone (have their own state)
    - 9: It is not disposable as the state and logs are in the server itself
    - 10: Depends on the provided environment
    - 11: Logs in file
    - 12: Need to SSH into the server, cannot configure anything from remote

## In the Modern application
### Step 1: Run the docker compose
```
docker compose up -d
```

### Check the output in the browser

### Step 2: Scaling
```Bash
    docker-compose up -d --scale web=3 
```

## Can be expanded to
- Docker volumes to store uploaded files so that if the container crashes the data is safe
- Can include ci/cd pipline for build/release/run
- Can also introduce any admin-process