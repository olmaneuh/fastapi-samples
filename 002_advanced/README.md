# **Advanced FastAPI application**

This project is a **Todos Management API** built with [FastAPI](https://fastapi.tiangolo.com/).

It provides:

- Basic CRUD endpoints.
- Data Validations.
- Exception Handling.
- Status Codes.
- Swagger Configurations.
- Python Request Objects.
- SQL Database interaction.
- Authentication.
- Autorization.
- Hashing Passwords.

## **Run the server**

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## **Testing the API**

FastAPI provides an automatic interactive documentation for the API using Swagger UI. After running the server, you can access the documentation at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
