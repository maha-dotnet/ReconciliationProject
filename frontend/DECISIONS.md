# Technical Decisions

## 1. React for Frontend

React is used to build a responsive and reusable user interface.

Components are separated to improve code readability and maintenance.

## 2. Django REST Framework for Backend

Django REST Framework is used to create REST APIs.

It handles CSV uploads, data processing, reconciliation, and result retrieval.

## 3. Axios for API Communication

Axios is used to send HTTP requests from React to Django.

It supports file uploads using FormData.

## 4. CSV as Input Data

CSV files are used as input because they are simple to create,
read, and exchange between systems.

## 5. Transaction ID as Matching Key

The transaction_id field is used to identify corresponding records
in System A and System B.

## 6. Reconciliation Rules

The application compares:

- Transaction ID
- Amount
- Transaction Date
- Status

A record is marked MATCHED when the compared fields are equal.

A record is marked MISMATCHED when the transaction exists in both
systems but one or more compared fields differ.

A record is marked MISSING_IN_A or MISSING_IN_B when it exists
in only one system.

## 7. Separate Frontend and Backend

The frontend and backend are maintained separately.

They communicate using REST APIs, making the application easier
to maintain and extend.