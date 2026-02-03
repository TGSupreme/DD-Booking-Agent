# 🚌 Bus Booking API Documentation

Base URL:
```
/api
```

---

# 1️⃣ Login

### Name
`login`

### Method
`POST`

### URL
```
/api/login
```

### Purpose
Authenticate user credentials and create a secure session using a JWT access token stored in an HTTP-only cookie.

### Query Params
None

### Body
```json
{
  "email": "user@example.com",
  "password": "string (min 6+ characters recommended)"
}
```

### Response
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "MongoDB ObjectId",
    "name": "string",
    "email": "user@example.com",
    "phone": 1234567890,
    "role": "user | admin"
  }
}
```

### Cookies Set
- `accesstoken` → JWT  
  - HttpOnly  
  - SameSite=Lax  
  - Max-Age=86400 seconds  
  - Path=/

---

# 2️⃣ Get All Stops

### Name
`get_all_stops`

### Method
`GET`

### URL
```
/api/admin/route/stops
```

### Purpose
Fetch all available bus stops/locations configured in the system.

### Query Params
None

### Body
None

### Response
```json
{
  "success": true,
  "message": "Stops fetched successfully",
  "allstops": ["City A", "City B", "City C"]
}
```

---

# 3️⃣ Search Buses

### Name
`search_bus`

### Method
`POST`

### URL
```
/api/user/search
```

### Purpose
Search available buses for a given source, destination, and travel date.

### Query Params
None

### Body
```json
{
  "from": "string",
  "to": "string",
  "traveldate": "YYYY-MM-DD"
}
```

### Response
```json
{
  "success": true,
  "message": "Buses found",
  "buses": [
    {
      "busId": "MongoDB ObjectId",
      "tripId": "MongoDB ObjectId",
      "busname": "string",
      "busnumber": "string",
      "type": "sleeper | seating",
      "from": "string",
      "to": "string",
      "totaltime": {
        "hour": 5,
        "minute": 30
      },
      "totalseats": 40,
      "price": 500,
      "fromtime": "10:00 AM",
      "totime": "03:30 PM",
      "days": [0,1,2,3,4,5,6],
      "availableseat": 20,
      "amenties": ["WiFi", "AC"]
    }
  ]
}
```

---

# 4️⃣ Get Seats

### Name
`get_all_seats`

### Method
`POST`

### URL
```
/api/ticket/seat/get
```

### Purpose
Fetch all already booked seat numbers for a specific trip and travel date.

### Query Params
None

### Body
```json
{
  "tripId": "MongoDB ObjectId",
  "from": "string",
  "to": "string",
  "traveldate": "YYYY-MM-DD"
}
```

### Response
```json
{
  "success": true,
  "message": "Seats fetched",
  "bookedseat": [1, 2, 5, 10]
}
```

---

# 5️⃣ Create Ticket

### Name
`create_ticket`

### Method
`POST`

### URL
```
/api/ticket/
```

### Purpose
Create a new ticket booking for a trip with selected seats and passenger details.

### Query Params
None

### Body
```json
{
  "tripId": "MongoDB ObjectId",
  "from": "string",
  "to": "string",
  "price": 1200,
  "seats": [1, 2],
  "passengers": [
    {
      "name": "John",
      "age": 25,
      "gender": "male"
    }
  ],
  "ticketdate": "YYYY-MM-DD"
}
```

### Response
```json
{
  "success": true,
  "message": "Ticket created",
  "ticket": {
    "user": "MongoDB ObjectId",
    "trip": "MongoDB ObjectId",
    "pnr": "123456789",
    "from": "string",
    "to": "string",
    "seats": [1,2],
    "passengers": [
      {
        "name": "John",
        "age": 25,
        "gender": "male",
        "_id": "MongoDB ObjectId"
      }
    ],
    "ticketdate": "YYYY-MM-DD",
    "status": "booked | cancelled",
    "totalamount": 1200,
    "paymentstatus": "pending | paid | failed",
    "_id": "MongoDB ObjectId",
    "createdAt": "ISO 8601 datetime",
    "updatedAt": "ISO 8601 datetime"
  }
}
```

---

# 6️⃣ Complete Booking Payment

### Name
`complete_ticket_payment`

### Method
`PUT`

### URL
```
/api/ticket/update/payment/:ticketId
```

### Purpose
Mark a ticket’s payment as completed and update its payment status.

### Path Params
| Param | Type | Description |
|-------|--------|-------------|
| ticketId | string | MongoDB ObjectId |

### Body
```json
{
  "price": 1200
}
```

### Response
```json
{
  "success": true,
  "message": "Payment completed",
  "updatedTicket": {
    "_id": "MongoDB ObjectId",
    "user": "MongoDB ObjectId",
    "trip": "MongoDB ObjectId",
    "pnr": "123456789",
    "from": "string",
    "to": "string",
    "seats": [1,2],
    "passengers": [
      {
        "name": "John",
        "age": 25,
        "gender": "male",
        "_id": "MongoDB ObjectId"
      }
    ],
    "ticketdate": "YYYY-MM-DD",
    "status": "booked | cancelled",
    "totalamount": 1200,
    "paymentstatus": "completed | pending | failed",
    "createdAt": "ISO 8601 datetime",
    "updatedAt": "ISO 8601 datetime"
  }
}
```

---

# ✅ End of Documentation
