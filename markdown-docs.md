# Stadium Scheduling System API Documentation

This document provides details about the API endpoints available in the Stadium Scheduling System.

## Table of Contents

- [Authentication](#authentication)
- [Stadiums](#stadiums)
- [Departments](#departments)
- [Schedules](#schedules)
- [Usage Tracking](#usage-tracking)
- [Users](#users)

## Authentication

The API uses token-based authentication for protected endpoints. After login, include the token in the Authorization header for all protected requests.

### Login

```
POST /api/login/
```

Authenticates a user and returns a token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "user_id": "integer",
  "username": "string",
  "department": "string"
}
```

## Stadiums

### List All Stadiums

```
GET /stadiums/
```

Returns a list of all stadiums.

**Response:**
```json
[
  {
    "id": "integer",
    "name": "string",
    "location": "string",
    "capacity": "integer",
    "is_active": "boolean",
    "image": "string"
  }
]
```

### Get Stadium Detail

```
GET /stadiums/{id}/
```

Returns details of a specific stadium.

**Response:**
```json
{
  "id": "integer",
  "name": "string",
  "location": "string",
  "capacity": "integer",
  "is_active": "boolean",
  "image": "string"
}
```

### Create Stadium

```
POST /stadiums/
```

Creates a new stadium.

**Request Body:**
```json
{
  "name": "string",
  "location": "string",
  "capacity": "integer",
  "is_active": "boolean",
  "image": "string (optional)"
}
```

### Update Stadium

```
PUT /stadiums/{id}/
```

Updates all fields of a stadium.

**Request Body:**
```json
{
  "name": "string",
  "location": "string",
  "capacity": "integer",
  "is_active": "boolean",
  "image": "string (optional)"
}
```

### Partial Update Stadium

```
PATCH /stadiums/{id}/
```

Updates selected fields of a stadium.

**Request Body:**
```json
{
  "name": "string (optional)",
  "location": "string (optional)",
  "capacity": "integer (optional)",
  "is_active": "boolean (optional)",
  "image": "string (optional)"
}
```

### Delete Stadium

```
DELETE /stadiums/{id}/
```

Deletes a stadium.

## Departments

### List All Departments

```
GET /departments/
```

Returns a list of all departments.

**Response:**
```json
[
  {
    "id": "integer",
    "name": "string",
    "image_team": "string"
  }
]
```

### Get Department Detail

```
GET /departments/{id}/
```

Returns details of a specific department.

**Response:**
```json
{
  "id": "integer",
  "name": "string",
  "image_team": "string"
}
```

### Create Department

```
POST /departments/
```

Creates a new department.

**Request Body:**
```json
{
  "name": "string",
  "image_team": "string (optional)"
}
```

### Update Department

```
PUT /departments/{id}/
```

Updates all fields of a department.

**Request Body:**
```json
{
  "name": "string",
  "image_team": "string (optional)"
}
```

### Partial Update Department

```
PATCH /departments/{id}/
```

Updates selected fields of a department.

**Request Body:**
```json
{
  "name": "string (optional)",
  "image_team": "string (optional)"
}
```

### Delete Department

```
DELETE /departments/{id}/
```

Deletes a department.

## Schedules

### List All Schedules

```
GET /schedules/
```

Returns a list of all schedules with optional filtering.

**Query Parameters:**
- `date`: Filter by date (YYYY-MM-DD)
- `department`: Filter by department ID
- `stadium`: Filter by stadium ID

**Response:**
```json
[
  {
    "id": "integer",
    "department": "integer",
    "department_name": "string",
    "date": "date",
    "start_time": "time",
    "end_time": "time",
    "is_active": "boolean",
    "stadium": "integer",
    "stadium_name": "string"
  }
]
```

### Get Schedule Detail

```
GET /schedules/{id}/
```

Returns details of a specific schedule.

**Response:**
```json
{
  "id": "integer",
  "department": "integer",
  "department_name": "string",
  "date": "date",
  "start_time": "time",
  "end_time": "time",
  "is_active": "boolean",
  "stadium": "integer",
  "stadium_name": "string"
}
```

### Create Schedule

```
POST /schedules/
```

Creates a new schedule with time conflict validation.

**Request Body:**
```json
{
  "department": "integer",
  "date": "date",
  "start_time": "time",
  "end_time": "time",
  "is_active": "boolean",
  "stadium": "integer"
}
```

**Error Response (400):**
```json
{
  "error": "Time conflict with an existing schedule."
}
```

### Update Schedule

```
PUT /schedules/{id}/
```

Updates all fields of a schedule.

**Request Body:**
```json
{
  "department": "integer",
  "date": "date",
  "start_time": "time",
  "end_time": "time",
  "is_active": "boolean",
  "stadium": "integer"
}
```

### Partial Update Schedule

```
PATCH /schedules/{id}/
```

Updates selected fields of a schedule.

**Request Body:**
```json
{
  "department": "integer (optional)",
  "date": "date (optional)",
  "start_time": "time (optional)",
  "end_time": "time (optional)",
  "is_active": "boolean (optional)",
  "stadium": "integer (optional)"
}
```

### Delete Schedule

```
DELETE /schedules/{id}/
```

Deletes a schedule.

### Get Available Time Slots

```
GET /schedules/available-slots/
```

Returns available time slots for a specific date and stadium.

**Query Parameters:**
- `date`: Date to check (YYYY-MM-DD) (required)
- `stadium`: Stadium ID (required)

**Response:**
```json
[
  {
    "start_time": "string (format: HH:MM)",
    "end_time": "string (format: HH:MM)"
  }
]
```

**Error Response (400):**
```json
{
  "error": "Both date and stadium parameters are required."
}
```

## Usage Tracking

### List All Usage Records

```
GET /checks/
```

Returns a list of all usage tracking records.

**Response:**
```json
[
  {
    "id": "integer",
    "counter": "integer",
    "depertment": "integer",
    "department_name": "string",
    "stadium": "integer",
    "stadium_name": "string"
  }
]
```

### Get Usage Record Detail

```
GET /checks/{id}/
```

Returns details of a specific usage tracking record.

**Response:**
```json
{
  "id": "integer",
  "counter": "integer",
  "depertment": "integer",
  "department_name": "string",
  "stadium": "integer",
  "stadium_name": "string"
}
```

### Create Usage Record

```
POST /checks/
```

Creates a new usage tracking record.

**Request Body:**
```json
{
  "counter": "integer",
  "depertment": "integer",
  "stadium": "integer"
}
```

### Update Usage Record

```
PUT /checks/{id}/
```

Updates all fields of a usage tracking record.

**Request Body:**
```json
{
  "counter": "integer",
  "depertment": "integer",
  "stadium": "integer"
}
```

### Partial Update Usage Record

```
PATCH /checks/{id}/
```

Updates selected fields of a usage tracking record.

**Request Body:**
```json
{
  "counter": "integer (optional)",
  "depertment": "integer (optional)",
  "stadium": "integer (optional)"
}
```

### Delete Usage Record

```
DELETE /checks/{id}/
```

Deletes a usage tracking record.

### Increment Usage Counter

```
POST /checks/increment-counter/
```

Increments the usage counter for a department-stadium pair.

**Request Body:**
```json
{
  "department": "integer",
  "stadium": "integer"
}
```

**Response:**
```json
{
  "id": "integer",
  "counter": "integer",
  "depertment": "integer",
  "department_name": "string",
  "stadium": "integer",
  "stadium_name": "string"
}
```

**Error Response (400):**
```json
{
  "error": "Both department and stadium IDs are required."
}
```

### Get Usage Statistics

```
GET /checks/usage-stats/
```

Returns usage statistics filtered by stadium or department.

**Query Parameters:**
- `department`: Filter by department ID
- `stadium`: Filter by stadium ID

**Response:**
```json
[
  {
    "id": "integer",
    "counter": "integer",
    "depertment": "integer",
    "department_name": "string",
    "stadium": "integer",
    "stadium_name": "string"
  }
]
```

## Users

### List All Users

```
GET /users/
```

Returns a list of all users (requires authentication).

**Response:**
```json
[
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "depertment": "string"
  }
]
```

### Get User Detail

```
GET /users/{id}/
```

Returns details of a specific user (requires authentication).

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "depertment": "string"
}
```

### Create User

```
POST /users/
```

Creates a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "confirm_password": "string",
  "first_name": "string",
  "last_name": "string",
  "depertment": "string"
}
```

**Error Response (400):**
```json
{
  "confirm_password": ["Passwords do not match."]
}
```

### Update User

```
PUT /users/{id}/
```

Updates all fields of a user (requires authentication).

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "current_password": "string (required for password change)",
  "new_password": "string (optional)",
  "confirm_new_password": "string (required if new_password is provided)",
  "first_name": "string",
  "last_name": "string",
  "depertment": "string"
}
```

### Partial Update User

```
PATCH /users/{id}/
```

Updates selected fields of a user (requires authentication).

**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "current_password": "string (required for password change)",
  "new_password": "string (optional)",
  "confirm_new_password": "string (required if new_password is provided)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "depertment": "string (optional)"
}
```

### Delete User

```
DELETE /users/{id}/
```

Deletes a user account (requires authentication).

### Get User Profile

```
GET /profile/?user_id={id}
```

Returns the current user's profile (requires authentication).

**Query Parameters:**
- `user_id`: User ID (required)

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "depertment": "string"
}
```

### Get Users by Department

```
GET /users-by-department/?department={name}
```

Returns users filtered by department (requires authentication).

**Query Parameters:**
- `department`: Department name (required)

**Response:**
```json
[
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "depertment": "string"
  }
]
```

**Error Response (400):**
```json
{
  "error": "Department parameter is required"
}
```
