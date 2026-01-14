### 3. How to Setup and Run (The "Painful" Way)

To demonstrate **Factor 5 (Build/Release/Run) violations**, you should perform these steps manually in front of the audience (or explain that you had to do them).

### Step 1: Install Dependencies

```Bash
pip install -r requirements_legacy.txt

```

### Step 2: Manual Folder Creation (The Trap)
Don't run this yet!
In a 12-factor app, the app creates what it needs or uses external services.
In this legacy app, if you run python `legacy_app.py`, it might fail or behave weirdly if permissions aren't right, or you have to "prep" the server.

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

### Scaling
```Bash
    docker-compose up -d --scale web=3 
```