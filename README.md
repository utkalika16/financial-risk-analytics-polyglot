# Financial Risk Analytics System

## Project Title

**Financial Risk Analytics System**

## Project Description

Financial Risk Analytics System is a web-based application developed to manage and analyze financial information such as customers, accounts, and transactions.

The system provides APIs for managing financial data and implements secure user authentication and authorization using JSON Web Tokens (JWT). Protected API endpoints can be accessed only after successful authentication.

The application was developed and tested using sample and trial records entered directly into the database. The APIs were tested using Swagger UI, and the application was also tested through the frontend.

The main purpose of the project is to provide a structured platform for managing financial information and supporting financial risk-related operations.

## Technologies Used

### Backend

* Python
* FastAPI
* Uvicorn
* JSON Web Token (JWT)
* Python-JOSE

### Frontend

* HTML
* CSS
* JavaScript

### Database

* PostgreSQL
* pgAdmin
* MongoDB

### API Testing

* Swagger UI
* REST APIs

### Development Tools

* Visual Studio Code
* Git
* GitHub

## Installation / Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Financial-Risk-Analytics.git
cd Financial-Risk-Analytics
```

### 2. Create a Virtual Environment

For Windows:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Required Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Database

The application uses databases for storing application data.

Create a `.env` file in the project and configure the required database connection details and secret key.

Example:

```text
DATABASE_URL=your_database_connection
MONGO_URI=your_mongodb_connection
SECRET_KEY=your_secret_key
```

Replace the example values with the appropriate local database configuration.

**Do not upload the `.env` file to GitHub because it may contain database credentials and secret keys.**

## How to Run the Project

### Run the Backend

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the FastAPI application:

```powershell
uvicorn main:app --reload
```

The backend will normally run at:

```text
http://127.0.0.1:8000
```

### Open Swagger UI

Open the following URL in a web browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface for viewing and testing the available APIs.

### Authentication and Authorization

1. Open the `/login` endpoint in Swagger UI.
2. Enter the required login credentials.
3. Execute the request.
4. A JWT access token is generated after successful authentication.
5. Click the **Authorize** button in Swagger UI.
6. Enter the generated token in the **HTTPBearer** authorization field.
7. Click **Authorize**.
8. Access the protected API endpoints.

### Authorization Testing

The protected endpoint:

```text
GET /customers
```

was tested using a valid JWT Bearer token.

The server successfully returned:

```text
200 OK
```

along with the customer records.

This confirms that the JWT-based authentication and authorization mechanism is working correctly.

## Screenshots / Results

Screenshots of the working project and API testing are included in the `screenshots` folder.

The screenshots include:


* Login page-
 <img width="700" height="690" alt="image" src="https://github.com/user-attachments/assets/98b52c3f-3641-4e2d-92df-6440e0e15db1" />

* Swagger UI-<img width="1538" height="947" alt="image" src="https://github.com/user-attachments/assets/18d81cd5-c995-4159-a60c-a3aa96c81d18" />


* Successful login and JWT token generation-<img width="1457" height="970" alt="image" src="https://github.com/user-attachments/assets/ed32c079-1f82-4131-bcd0-86d4d301f896" />


* Swagger HTTPBearer authorization-<img width="1532" height="790" alt="image" src="https://github.com/user-attachments/assets/1afd2d9b-053b-44cf-8206-86d6ae44505e" />


* Authorized `GET /customers` request-<img width="1453" height="977" alt="image" src="https://github.com/user-attachments/assets/4b391483-5d79-417c-acac-4c5759888f8b" />


* Successful `200 OK` response-<img width="1440" height="285" alt="image" src="https://github.com/user-attachments/assets/eabc2ab5-f877-4d42-abb8-5627636de0a7" />


* Frontend application-<img width="1917" height="987" alt="image" src="https://github.com/user-attachments/assets/90802321-767c-40a1-8d78-aa62fd16bf87" />


* Risk Score page/result-<img width="1676" height="985" alt="image" src="https://github.com/user-attachments/assets/e6d181c6-7b85-419b-be69-59b319322322" />


* Customerpage-<img width="1677" height="977" alt="image" src="https://github.com/user-attachments/assets/5e86dbd1-559d-4682-bfed-bf281e9fbb23" />


* Account page-<img width="1902" height="990" alt="image" src="https://github.com/user-attachments/assets/3665726e-34cb-4673-9838-cb147ca7d39f" />


* Transaction page-<img width="1667" height="982" alt="image" src="https://github.com/user-attachments/assets/22e19c25-7a7d-4f26-92e0-37e1954dbfe9" />


* Project folder structure in VS Code-
 <img width="422" height="777" alt="image" src="https://github.com/user-attachments/assets/e13fcf04-cee7-4898-84aa-dad366e28aa2" />


### Authorization Test Result

```text
Login
  ↓
JWT Access Token Generated
  ↓
Swagger HTTPBearer Authorization
  ↓
GET /customers
  ↓
200 OK
  ↓
Customer Data Returned
```

### Result

The Financial Risk Analytics System was successfully developed and tested.

The login API successfully generated a JWT access token. The generated token was successfully used through Swagger UI to authorize access to protected API endpoints.

The protected `GET /customers` endpoint returned a **200 OK** response with customer records after valid authorization.

Therefore, the authentication and authorization functionality was successfully implemented and verified.


### Team Members

1. **utkalika** — 2510080004
2. **divya sri** — 2510080025
3. **Ambika Naidu** — 2510080035
4. **Kavitha Reddy** — 2510080033

## Academic Project

This project was developed as part of an academic/student project for educational and demonstration purposes.
