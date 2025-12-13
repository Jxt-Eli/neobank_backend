from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from pydantic import BaseModel, Field ,EmailStr 
import httpx
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models import User, Transaction
from auth import hash_password, verify_password, create_access_token, verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid






# JWT DEPENDENCY FUNCTION

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security), 
        db: AsyncSession = Depends(get_db)
):
    
    '''dependency that extracts and validates the current user from the JWT token'''
    
    #getting token directly from credentials
    token = credentials.credentials

    # verify token and user_id from database
    user_id = verify_access_token(token)
    if not user_id:
         raise HTTPException(status_code=401, detail='invalid or expired token')
    
    # fetch user from database for comparison
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail='user not found')
    
    return user










app = FastAPI()

# ==============check app status and platform name ================
@app.get("/")
def get_status():
    return {
        "name": "Quantevo Ledgers",
        "status": "operational",
        "version": "0.1.0"
    }
@app.get("/health")
def health_check():
    return {"status": "healthy"}

class Login(BaseModel):
    email: EmailStr     # HACK: JUST A TEMPORARY FIX SINCE WE WILL NEED EXTRA VALIDATION AND PIP INSTALLS TO WORK WITH EmailStr
    password: str = Field(min_length=8, description='password must be 8 or more characters')

@app.post("/login", status_code=200)
async def login(detail: Login, db: AsyncSession = Depends(get_db)):
    email_result = await db.execute(select(User)
                     .where(
                         User.email == detail.email
                     ))
    
    user_exists = email_result.scalar_one_or_none()
    
    if not user_exists:
        raise HTTPException(status_code=401, detail='Invalid email or password')
   
    pwd_check_result = verify_password(detail.password, user_exists.password)

    if not pwd_check_result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": str(user_exists.user_id), 'email': user_exists.email}
    )
    return {
        'message': 'login successful', 
        'access_token': access_token, 
        'token_type': 'bearer', 
        'user': 
        {
        'user_id': user_exists.user_id, 
        'email': user_exists.email, 
        'full_name': user_exists.full_name, 
        }, 
    }
        

'''=====================check user balance with user id==========================='''
@app.get("/balance")
async def get_user_balance(current_user: User = Depends(get_current_user)):
    return{
        "name": current_user.full_name, 
        "balance": current_user.balance, 
        "currency": current_user.currency, 
    }






# =====================transfer endpoint===========================

class TransferRequest(BaseModel):
    receiver_id: int
    amount: float
    # transaction_id: int
    currency: str

@app.post("/transfer")
async def create_transfer(transfer: TransferRequest, 
                          db: AsyncSession = Depends(get_db), 
                          current_user: User = Depends(get_current_user)
                          ):

    if transfer.amount > current_user.balance:
        raise HTTPException(status_code=400, detail= "Insufficient balance")    

    receiver_result = await db.execute(select(User).where(User.user_id == transfer.receiver_id)) 
    receiver = receiver_result.scalar_one_or_none()
    if not receiver:
        raise HTTPException(status_code=404, detail= 'receipient not found')
    
    initial_sender_balance  = current_user.balance
    initial_receiver_balance = receiver.balance

    # update balances
    current_user.balance -= transfer.amount
    receiver.balance += transfer.amount

    # generate unique transaction id for the new_transaction class and for function return
    transaction_id = str(uuid.uuid4())
    
    # create transaction record

    new_transaction = Transaction(
        sender_id = current_user.user_id, 
        receiver_id = transfer.receiver_id, 
        amount = transfer.amount,
        currency = transfer.currency, 
        transaction_id = transaction_id, 
        initial_balance = initial_sender_balance,  
        remaining_balance = current_user.balance, 
        status = "completed"
    )
    db.add(receiver)
    db.add(current_user)
    db.add(new_transaction)
    await db.commit()
    await db.refresh(receiver)
    await db.refresh(current_user)
    await db.refresh(new_transaction)
    
    return {
        "transaction":
        {
        "transaction_id": transaction_id, 
        "sender_id": current_user.user_id,
        "receiver_id": transfer.receiver_id,
        "amount": transfer.amount,
        "currency": transfer.currency, 
        "status": "pending"
        },
        "sender": {'name': current_user.full_name, 'initial_balance': initial_sender_balance, 'remaining_balance': current_user.balance }, 
        "receiver": {'name': receiver.full_name, 'initial balance': initial_receiver_balance, 'remaining_balance': receiver.balance}
        
    }






    
# ==================get user transactions====================

@app.get("/transactions")
async def get_transactions(limit: int = 10, 
                           offset: int = 0, #user_id: int = None, 
                           db: AsyncSession = Depends(get_db), 
                           current_user: User = Depends(get_current_user)):
    query = select(Transaction)
    if current_user:
        query = query.where(
            or_(
                Transaction.sender_id == current_user.user_id, 
                )
            )

    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    transactions = result.scalars().all()

    return{
        'limit': limit,
        'offset': offset,
        'user_id': current_user.user_id,
        'message': f"Fetching {limit} transactions starting from {offset}", 
        'count': len(transactions), 
        'transactions': [
            {
            'transaction_id': t.transaction_id, 
            'receiver_id': t.receiver_id, 
            'amount': t.amount, 
            'timestamp': t.timestamp.isoformat(), 
            'status': t.status, 
            }
            for t in transactions
        ]
    }




''' ============================================ create new user endpoint ============================================='''
# ---------POST ENDPOINT----------
# add user to database (not too complete I'll improve it over time since we'll later deal with fetching and adding information to the DB instead of adding it to some mockup inside the codebase (which is making it more complicated))
class CreateUserRequest(BaseModel):
    email: str
    full_name: str
    initial_deposit: float = Field(gt=0, description="Must be greater than 0")
    password: str = Field(min_length=8, description="password must exceed 8 characters")
    phone: str

@app.post("/users", status_code=201)
async def create_user(new_user: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(
        select(User).where(
            or_(
                User.email == new_user.email, 
                User.phone == new_user.phone, 
            )
        )
    )
    user_exists = exists.scalar_one_or_none()
    if user_exists:
        raise HTTPException(status_code=400, detail='User exists already or details are being used for an existing account ')
    
    hashed_pwd = hash_password(new_user.password)   

    save_info = User(
        email = new_user.email, 
        balance = new_user.initial_deposit, 
        phone = new_user.phone, 
        full_name = new_user.full_name, 
        password = hashed_pwd
    )
    db.add(save_info)
    await db.commit()
    await db.refresh(save_info)
    return {
        "message": "user created successfully",
        "email": new_user.email,
        "full_name": new_user.full_name,
        "phone": new_user.phone,
        "balance": new_user.initial_deposit
    }


''' ===========currency conversion (probably temporary) =============='''
@app.get("/convert/{amount}")
async def convert_currency(amount: float, from_currency: str = "USD", to_currency: str = "GHS"):
    # Call a real exchange rate API
    async with httpx.AsyncClient() as client:
        start = time.time()
        response = await client.get(
            f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        )
        data = response.json()
        end = time.time()
        print(end - start)
    if to_currency not in data["rates"]:
        raise HTTPException(status_code=400, detail="Unsupported currency")
    
    # Get the conversion rate
    rate = data["rates"][to_currency]
    converted_amount = amount * rate
    time_taken =  (f" total time taken: {end - start:.2f}s")
    print(time_taken)
    return {
        "original_amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "exchange_rate": rate,
        "converted_amount": converted_amount,
    }
