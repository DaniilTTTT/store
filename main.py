import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import User, UserResponse, UserDelete
from database import get_db, init_db

app = FastAPI()

@app.get('/')
async def root() -> Dict:
    return {'code': 200}

@app.get('/users', response_model=List[UserResponse])
async def users() -> List[UserResponse]:
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, name FROM users
        """)

        data = cursor.fetchall()

        return [UserResponse(id=row[0], name=row[1]) for row in data]
    except Exception as e:
        print(f"Geting users error: {e}")
        raise HTTPException(status_code=500, detail="Geting users error")

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
        print(f"Posting user error: {e}")
        raise HTTPException(status_code=500, detail="Posting user error")
    
@app.put('/update-user', response_model=UserResponse)
async def update_user(user: UserResponse) -> UserResponse:
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET name = ?
            WHERE id = ?
        """, (user.name, user.id))

        conn.commit()

        cursor.execute("""
            SELECT id, name FROM users WHERE id = ?
        """, (user.id,))

        updated_user = cursor.fetchone()

        return UserResponse(id=updated_user[0], name=updated_user[1])

    except Exception as e:
        print(f"Huinya: {e}")
        raise HTTPException(status_code=500, detail="Huinya")
    
@app.delete('/delete-user', response_model=Dict)
async def delete_user(user: UserDelete) -> Dict:
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM users WHERE id = ?
        """, (user.id,))

        conn.commit()

        return {'message': 'user successfully deleted'}
    
    except Exception as e:
        print(f"Huinya: {e}")
        raise HTTPException(status_code=500, detail="Huinya")

if __name__ == '__main__':
    init_db()
    uvicorn.run('main:app', reload=True)