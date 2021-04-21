# v1 User Endpoints

> **Important:** all routes have to be prefixed with `/v1`<br>
> E.g. `https://backend.cosmicsail.online/v1/status`

API routes that are described in this document are used by our frontend,
enabling users to manage their boats, view telemetry data and configure boat hardware.

## General information

**Content:**
- [Status](#status)
- Boats
  - [Register Boats](#register-boat)
  - [Get Boats](#get-boats)
- [Trips](#trips)
- Hardware
  - [Add](#register-new-hardware)
  - [Change](#update-hardware)
  - [Delete](#delete-hardware)

To use user endpoints, every request has to have an
Authorization header including a bearer token. (see [Authentication](./Authentication.md))

**Error codes for missing/invalid Authentication**

`400` - Bad Request<br>
Authorization header not present

`403` - Forbidden<br>
Token invalid



# Status

Verify token and get user information.

### Request

POST `/status`

**Authorization:** Bearer Token<br>
**Query Params:** None<br>
**Body:** None<br>

### Response

`200` - Success
```json
{
  "payload": {
    "Username": "cosmicSailor",
    "FullName": "Cosmic Sailor",
    "Email": "vip@cosmicsail.online",
    "IsAdmin": false
  }
}
```

# Boats

Register new and get existing boats.

## Register Boat

Register a new boat.

### Request

POST `/boats`

**Authorization:** Bearer Token<br>
**Query Params:** None<br>
**Body:**
| Name    | Description     | Type       | Required |
| ------- | --------------- | ---------- | -------- |
| name    | Name of boat    | String     | Yes      |
| series  | Production line | String     | Yes      |
| make    | Manufacturer    | String     | Yes      |

### Response

`200` - Success<br>
The token has to be used on boat side and is only displayed **once**.
```json
{
  "Token": ...,
  "Boat": {
    "BoatEmblem": "zUi7o",
    "Name": "Rasselbande",
    "Owner": "cosmicSailor"
  }
}
```

`400` - Bad Request<br>
1. Body could not be parsed
2. Error while creating Database entry

`500` - Internal Server Error<br>
Please contact us.

## Get Boats

Get all boats the token/user has access to.

### Request

GET `/boats`

**Authorization:** Bearer Token<br>
**Query Params:** None<br>
**Body:** None

### Response

`200` - Success<br>
```json
[
  {
    "BoatEmblem": "zUi7o",
    "Name": "Rasselbande",
    "Series": "Model 3000",
    "Make": "Selfmade",
    "Online": false,
    "LastOnline": "2020-09-27T15:07:29.618628+02:00",
    "Motors": [
      {
        "Name": "Rudder",
        "Channel": 1,
        "Min": 2000,
        "Max": 3000,
        "Default": 2500,
        "Cycle": 24
      },
      ...
    ],
    "Sensors": [
      {
        "Name": "Position",
        "Channel": "/dev/ttyAMA0",
        "Type": "gps"
      },
      ...
    ]
  },
  ...
]
```

# Trips

Get all trips a boat has made.

### Request

GET `/boats/:emblem/trips`

**Authorization:** Bearer Token<br>
**Query Params:** None<br>
**Body:** None

### Response

`200` - Success<br>
```json
[
  {
    "ID": 1,
    "BoatID": 1,
    "Name": "16:24 25.9.2020",
    "StartDate": "2020-09-25T16:24:00.000000+02:00",
    "EndDate": "2020-09-25T17:10:46.629442+02:00",
    "Datapoints": [
      {
        "TripID": 1,
        "Timestamp": "2020-09-25T16:24:00.000000+02:00",
        "Data": ...
      }
    ]
  },
  ...
]
```

`403` - Forbidden<br>
User has no access to the requested boat

`404` - Not found<br>
Error while loading trips

# Hardware

Following endpoints are used to add, change or remove hardware configuration, that is then automatically loaded by the boat.

## Register new Hardware

Add new hardware to the config

### Request

POST `/boats/:emblem/hardware`

**Authorization:** Bearer Token<br>
**Query Params:**
| Name     | Description        | Type           | Required |
| -------- | ------------------ | -------------- | -------- |
| hardware | Kind of hardware   | String(*motor* or *sensor*) | Yes |

**Body:** 
- Motor

| Name     | Description          | Type           | Required |
| -------- | -------------------- | -------------- | -------- |
| name     | Name of motor        | String         | Yes      |
| channel  | PWM Channel of motor | Integer        | Yes      |
| min      | Minimum PWM cycle    | Float          | Yes      |
| max      | Maximum PWM cycle    | Float          | Yes      |
| default  | Default motor state  | Float(-1 to 1) | Yes      |
| cycle    | Dutycycle (currently not used by boat) | Integer | Yes |

- Sensor

| Name     | Description          | Type           | Required |
| -------- | -------------------- | -------------- | -------- |
| name     | Name of motor        | String         | Yes      |
| channel  | Where is the sensor connected? | String | Yes      |
| type     | Type of sensor       | String          | Yes      |

### Response

`200` - Success<br>
```text
Motor added!
```
```text
Sensor added!
```

`400` - Bad Request<br>
1. The hardware query parameter could not resolve to *motor* or *sensor*.
2. Body could not be parsed
3. Field name or fields name, type and channel are empty

`403` - Forbidden<br>
No access to requested boat


## Update Hardware

Change existing hardware to match a new configuration.

### Request

PUT `/boats/:emblem/hardware/:id`

**Authorization:** Bearer Token<br>
**Query Params:**
| Name     | Description        | Type           | Required |
| -------- | ------------------ | -------------- | -------- |
| hardware | Kind of hardware   | String(*motor* or *sensor*) | Yes |

**Body:** 
- Motor

| Name     | Description          | Type           | Required |
| -------- | -------------------- | -------------- | -------- |
| name     | Name of motor        | String         | No       |
| channel  | PWM Channel of motor | Integer        | No       |
| min      | Minimum PWM cycle    | Float          | No       |
| max      | Maximum PWM cycle    | Float          | No       |
| default  | Default motor state  | Float(-1 to 1) | No       |
| cycle    | Dutycycle (currently not used by boat) | Integer | No |

- Sensor

| Name     | Description          | Type           | Required |
| -------- | -------------------- | -------------- | -------- |
| name     | Name of motor        | String         | No       |
| channel  | Where is the sensor connected? | String | No     |
| type     | Type of sensor       | String         | No       |

### Response

`200` - Success<br>
```text
Motor updated!
```
```text
Sensor updated!
```

`400` - Bad Request<br>
1. The hardware query parameter could not resolve to *motor* or *sensor*.
2. Body could not be parsed
3. Hardware with requested ID for boat not found

`403` - Forbidden<br>
No access to requested boat


## Delete Hardware

Delete obsolete hardware.

### Request

Delete `/boats/:emblem/hardware/:id`

**Authorization:** Bearer Token<br>
**Query Params:**
| Name     | Description        | Type           | Required |
| -------- | ------------------ | -------------- | -------- |
| hardware | Kind of hardware   | String(*motor* or *sensor*) | Yes |

**Body:** None

### Response

`200` - Success<br>
```text
Motor deleted!
```
```text
Sensor deleted!
```

`400` - Bad Request<br>
1. The hardware query parameter could not resolve to *motor* or *sensor*.
3. Hardware with requested ID for boat not found

`403` - Forbidden<br>
No access to requested boat



