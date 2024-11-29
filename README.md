# min-max-list-backend


### Description
- Provides database management with postgresql
- Provides endpoints for frontend to use using fastapi

### Installation Requirements

```
pip install "fastapi[standard]"
pip install psycopg2-binary
pip install pytz 
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

### Chatgpt Requirements
- If you don't want to deal or test chatgpt stuff just comment out:
```
# client = OpenAI()
```

- add a .env file and put in 
```
OPENAI_API_KEY="YOUR KEY HERE"
chatgpt key from https://platform.openai.com/api-keys
```
