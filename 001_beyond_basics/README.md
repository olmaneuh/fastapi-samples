# **Beyond A Basic FastAPI application**

This project is a simple **Book Management API** built with [FastAPI](https://fastapi.tiangolo.com/). It provides basic CRUD endpoints with Data Validations, Exception Handling, Status Codes, Swagger Configurations and Python Request Objects. The data is stored in a simulated in-memory list of books.

## **Run the server**

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## **Testing the API**

FastAPI provides an automatic interactive documentation for the API using Swagger UI. After running the server, you can access the documentation at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
