import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import User, UserResponse
from database import get_db, init_db

app = FastAPI()

# Инициализация базы данных при запуске приложения
init_db()

@app.get('/')
async def root() -> Dict:
    return {'code': 200}

@app.get('/users', response_model=List[UserResponse])
async def users() -> List[UserResponse]:
    conn = get_db()
    cursor = conn.cursor()

    # Исправленный SQL-запрос
    cursor.execute("""
        SELECT id, name FROM users
    """)

    data = cursor.fetchall()

    # Преобразуем данные в список UserResponse
    return [UserResponse(id=row[0], name=row[1]) for row in data]

@app.post('/create-user', response_model=UserResponse)
async def create_user(user: User) -> UserResponse:
    conn = get_db()
    cursor = conn.cursor()

    try:
        # Исправленная передача параметров (добавлена запятая)
        cursor.execute("""
            INSERT INTO users (name) VALUES (?)
        """, (user.name,))  # Запятая после user.name делает это кортежем

        conn.commit()

        # Получаем ID последней вставленной записи
        user_id = cursor.lastrowid

        # Возвращаем созданного пользователя
        return UserResponse(id=user_id, name=user.name)

    except Exception as e:
        # Логируем ошибку и возвращаем 500
        print(f"Ошибка при создании пользователя: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя")

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)