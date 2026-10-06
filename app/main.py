from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os

from auth import create_token, verify_token
from customer import add_customer, get_customers
from account import add_account, get_accounts, delete_account
from transaction import deposit, withdraw, get_transactions
from risk import calculate_risk, save_risk

app = FastAPI(title="Financial Risk Analytics API")

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
class LoginRequest(BaseModel):
    username: str
    password: str


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str


class Account(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float


class Transaction(BaseModel):
    account_id: str
    amount: float


class RiskRequest(BaseModel):
    customer_id: str
    account_id: str
    amount: float
    frequency: int


@app.get("/")
def home():
    return {"message": "Financial Risk Analytics API is running"}


@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin123":
        token = create_token(request.username)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    return {"message": "Invalid username or password"}


@app.post("/customers", dependencies=[Depends(verify_token)])
def create_customer(customer: Customer):
    return {
        "message": add_customer(
            customer.customer_id,
            customer.name,
            customer.email,
            customer.phone
        )
    }


@app.get("/customers", dependencies=[Depends(verify_token)])
def read_customers():
    return {"customers": get_customers()}


@app.post("/accounts", dependencies=[Depends(verify_token)])
def create_account(account: Account):
    try:
        return {
            "message": add_account(
                account.account_id,
                account.customer_id,
                account.account_type,
                account.balance
            )
        }
    except Exception as e:
        if "ForeignKeyViolation" in type(e).__name__:
            raise HTTPException(status_code=400, detail="Customer ID does not exist. Add the customer first.")
        if "UniqueViolation" in type(e).__name__:
            raise HTTPException(status_code=400, detail="Account ID already exists.")
        raise HTTPException(status_code=500, detail="Unable to add account.")


@app.get("/accounts", dependencies=[Depends(verify_token)])
def read_accounts():
    return {"accounts": get_accounts()}


@app.delete("/accounts/{account_id}", dependencies=[Depends(verify_token)])
def remove_account(account_id: str):
    message = delete_account(account_id)
    if message == "Account not found":
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}


@app.post("/transactions/deposit", dependencies=[Depends(verify_token)])
def make_deposit(transaction: Transaction):
    return {
        "message": deposit(
            transaction.account_id,
            transaction.amount
        )
    }


@app.post("/transactions/withdraw", dependencies=[Depends(verify_token)])
def make_withdrawal(transaction: Transaction):
    return {
        "message": withdraw(
            transaction.account_id,
            transaction.amount
        )
    }


@app.get("/transactions", dependencies=[Depends(verify_token)])
def read_transactions():
    return {"transactions": get_transactions()}


@app.post("/risk", dependencies=[Depends(verify_token)])
def analyze_risk(request: RiskRequest):
    score, level, indicators = calculate_risk(
        request.amount,
        request.frequency
    )

    save_risk(
        request.customer_id,
        request.account_id,
        score,
        level,
        indicators
    )

    return {
        "customer_id": request.customer_id,
        "account_id": request.account_id,
        "risk_score": score,
        "risk_level": level,
        "risk_indicators": indicators
    }