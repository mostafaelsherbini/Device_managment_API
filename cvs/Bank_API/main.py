from fastapi import FastAPI, HTTPException,Header# pyright: ignore[reportMissingImports]
import uuid


app = FastAPI()
tokens = {}  
users = {}

@app.post("/Register")
def register(username: str , password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[username] = {
        "password":password,
        "balance":1000
    }
    
    return {"message": "User registered successfully"}


@app.post("/login")
def login(username: str , password: str):
    user = users.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())
    tokens[token] = username

    return {"Token":token}

@app.get("/balance")
def balance(token:str = Header()):
    username = tokens.get(token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    return {
        "username": username,
        "balance": users[username]["balance"]
    }
    
    
@app.post("/transfer")
def transfer(token: str, to_username: str, amount: int):
    # 1️⃣ نجيب صاحب التوكن
    from_user = tokens.get(token)
    if not from_user:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 2️⃣ نتأكد إن الاتنين موجودين
    if from_user not in users or to_username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    # 3️⃣ مبلغ محترم
        #if amount <= 0 :
            #raise HTTPException(status_code=400, detail="Invalid amount")

    # 4️⃣ رصيد كفاية
    if users[from_user]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Not enough balance")

    # 5️⃣ التحويل الحقيقي
    users[from_user]["balance"] -= amount
    users[to_username]["balance"] += amount

    return {
        "message": "Transfer done",
        "your_balance": users[from_user]["balance"]
    }