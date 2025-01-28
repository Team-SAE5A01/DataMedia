from fastapi import FastAPI
import aiomysql
import asyncio

app = FastAPI()

# Database connection details
DB_HOST = "localhost"  # Adjust if necessary, e.g., to the container IP or Docker service name
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "JesusATM12!"  # Password you set in Dockerfile
DB_NAME = "Logistix"

# MySQL connection pool
async def get_db_pool():
    return await aiomysql.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/endpoint")
async def create_item(data: dict):
    # You can interact with the database here
    async with get_db_pool() as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Example query to insert data into a table (adjust as needed)
                query = "INSERT INTO some_table (column_name) VALUES (%s)"
                await cursor.execute(query, (data['some_field'],))
                return {"message": "Data received and inserted into the database", "data": data}

@app.get("/items")
async def get_items():
    async with get_db_pool() as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "SELECT * FROM Pmr"  # Replace with your actual query
                await cursor.execute(query)
                result = await cursor.fetchall()
                return {"items": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, debug=True)
