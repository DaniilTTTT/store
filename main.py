import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import User, UserResponse
from database import get_db, init_db

app = FastAPI()

@app.get('/')
async def root() -> Dict:
    return {'code': 200}

@app.get('/users', response_model=List[UserResponse])
async def users() -> List[UserResponse]:
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name FROM users
    """)

    data = cursor.fetchall()

    return [UserResponse(id=row[0], name=row[1]) for row in data]

@app.post('/create-user', response_model=UserResponse)
async def create_user(user: User) -> UserResponse:
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name) VALUES (?)
        """, (user.name,)) 

        conn.commit()

        user_id = cursor.lastrowid

        return UserResponse(id=user_id, name=user.name)

    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя")

if __name__ == '__main__':
    init_db()
    uvicorn.run('main:app', reload=True)