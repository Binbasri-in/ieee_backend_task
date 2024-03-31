# User Management API Documentation

## Overview

This document outlines the specifications and expected functionality for the User Management API. The API uses SQL as the underlying database and provides endpoints for inviting users, signing up, logging in, logging out, and editing user details.

# API Documentation

## 1. Signup
- **Endpoint:** `/signup`
- **Method:** POST
- **Description:** Allows an invitee to sign up using an invitation ID.
- **Request Body:**
  - `invitation_id`: The unique ID of the invitation.
  - `password`: The password for the new user account.
- **Response:** JSON object with a message indicating success or failure.

**cURL Command:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"invitation_id": "<INVITATION_ID>", "password": "testuser1"}' http://127.0.0.1:5000/signup

{
  "message": "Registered successfully"
}
```


## 2. Login
- **Endpoint:** `/login`
- **Method:** POST
- **Description:** Allows a user to log in using their email and password.
- **Request Body:**
  - `email`: The email of the user.
  - `password`: The password of the user.
- **Response:** JSON object with an access token and user details.

**cURL Command:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "testuser1@example.com", "password": "testuser1"}' http://127.0.0.1:5000/login


{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMTg0OTY0OCwianRpIjoiYjM0ZDUzMDctMzI5OS00Y2MyLTliZWYtMzkzNTcxNTRkOTgyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImpvaG5AZXhhbXBsZS5jb20iLCJuYmYiOjE3MTE4NDk2NDgsImNzcmYiOiJkMDZjZjc3My1lMGUxLTQyNjktYTQ4OS05YTRiNWJiYzllNjQiLCJleHAiOjE3MTE4NTA1NDh9.tpfU9KPDwMRaL0s86PN0T5cYDoRadH8SUmEZmVSNEfs",
  "user_details": {
    "email": "john@example.com",
    "profile_picture": null,
    "username": "John Doe"
  }
}
```

## 3. Logout
- **Endpoint:** `/logout`
- **Method:** GET
- **Description:** Allows a user to log out.
- **Response:** JSON object with a message indicating success.

**cURL Command:**
```bash
curl -X GET http://127.0.0.1:5000/logout

{
  "message": "Logged out successfully"
}
```

## 4. Invite
- **Endpoint:** `/invite`
- **Method:** POST
- **Description:** Allows a user to invite someone by entering their details.
- **Request Body:**
  - `name`: Name of the invitee.
  - `email`: Email of the invitee.
  - `phone_number`: Phone number of the invitee.
  - `alternate_email` (optional): Alternate email of the invitee.
  - `organizations` (optional): List of organizations with `name`, `role`, and `valid_till` date.
- **Response:** JSON object with a message indicating success and the invitation ID.

**cURL Command:**
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"name": "John Doe", "email": "johndoe@example.com", "phone_number": "1234567890"}' http://127.0.0.1:5000/invite


{
  "invitation_id": "74fc615a-e120-4204-92b1-13a0a47616f9",
  "message": "Invitation sent successfully"
}
```

## 5. Edit User
- **Endpoint:** `/edit_user`
- **Method:** PUT
- **Description:** Allows a user to edit their own details.
- **Request Body:**
  - `username` (optional): New username.
  - `email` (optional): New email.
- **Response:** JSON object with a message indicating success.

**cURL Command:**
```bash
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"username": "newusername", "email": "newemail@example.com"}' http://127.0.0.1:5000/edit_user
```

## 6. Upload Profile Picture
- **Endpoint:** `/upload_profile_picture`
- **Method:** POST
- **Description:** Allows a user to upload a profile picture.
- **Request Body:**
  - `file`: The profile picture file.
- **Response:** JSON object with a message indicating success.

**cURL Command:**
```bash
curl -X POST -F "file=@/path/to/profile.jpg" -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/upload_profile_picture
```

## 7. Uploaded File
- **Endpoint:** `/uploads/<filename>`
- **Method:** GET
- **Description:** Retrieves an uploaded file by its filename.
- **Response:** The requested file.

**cURL Command:**
```bash
curl -X GET http://127.0.0.1:5000/uploads/<FILENAME>
```


Replace placeholders (`<INVITATION_ID>`, `<ACCESS_TOKEN>`, `<FILENAME>`, etc.) with actual values as needed.

## Notes

- The Invitation API is marked as private and should be accessible only to authorized users.
- The Sign Up, Login, and Logout APIs are public and accessible to all users.
- The Edit User API is private and should allow users to edit only their own details.