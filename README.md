**FastAPI Mega Tutorial**

*installation Note*

Install dependency by using command:
```bash
pip install -r requirements.txt
```

run lates migration by issuing command:
```bash
alembic upgrade head
```

*Development Note*

make migration using alembic with command:

```bash
alembic revision --autogenerate -m "your comment"
```

*Run Development Server*

run local server with command:
```bash
uvicorn main:app --reload
```