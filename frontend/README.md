# Reconciliation Project

## Project Description

This project compares financial transaction records from two different
systems (System A and System B).

It identifies:
- Matched transactions
- Mismatched transactions
- Transactions missing in System A
- Transactions missing in System B

## Technologies

### Frontend
- React.js
- JavaScript
- Axios
- HTML
- CSS

### Backend
- Python
- Django
- Django REST Framework

### Data
- CSV files

## Project Structure

ReconciliationProject/
|
|-- backend/
|-- frontend/
|-- data/
|   |-- system_a.csv
|   |-- system_b.csv
|   |-- locations.csv
|
|-- README.md
|-- DECISIONS.md

## Backend Setup

Open PowerShell and navigate to the backend folder:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Run database migrations:

python manage.py migrate

Start the Django server:

python manage.py runserver

Backend URL:

http://127.0.0.1:8000/

## Frontend Setup

Open another PowerShell terminal:

cd frontend

Install dependencies:

npm install

Start the React application:

npm run dev

Frontend URL:

http://localhost:5173/

## Reconciliation Process

1. Upload System A CSV.
2. Upload System B CSV.
3. Click Reconcile Transactions.
4. The backend compares the transaction records.
5. The frontend displays reconciliation results.
6. The dashboard displays summary counts.

## CSV Format

The CSV files must contain these columns:

- transaction_id
- amount
- transaction_date
- status