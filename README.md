# min-max-list-backend


### Description
- Provides database management with postgresql
- Provides endpoints for frontend to use using fastapi

### Installation Requirements

```
pip install "fastapi[standard]"
pip install psycopg2-binary
```
- Install postgresql on own system 
    - Ensure that it runs
    - Change app.py to password of user's posgresql (password in file is currently dog)

### Usage
- run in terminal:
```
fastapi dev app.py
```

### Files
- app.py: Contains main app along with fastapi crud commands 
- task_database.py: Main back end interface used in crud commands

