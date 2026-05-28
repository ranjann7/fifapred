# API Documentation

## Overview
This API provides endpoints for match predictions, tournament simulation, and team analysis.

## Base URL
```
http://localhost:5000
```

## Authentication
Currently no authentication required. For production, add API keys.

---

## Endpoints

### 1. Get All Teams
Get information about all teams in the system.

**Request:**
```
GET /api/teams
```

**Response:**
```json
{
    "Argentina": {
        "fifa_rank": 1,
        "attack": 88,
        "defense": 82
    },
    "France": {
        "fifa_rank": 2,
        "attack": 87,
        "defense": 81
    },
    ...
}
```

**Status Codes:**
- 200: Success
- 500: Server error

---

### 2. Predict Match
Get AI prediction for a match between two teams.

**Request:**
```
POST /api/predict
Content-Type: application/json

{
    "team1": "Argentina",
    "team2": "France"
}
```

**Response:**
```json
{
    "team1": "Argentina",
    "team2": "France",
    "predicted_winner": "Argentina",
    "team1_win_prob": 55.2,
    "team2_win_prob": 35.8,
    "draw_prob": 8.0,
    "predicted_score": "2-1"
}
```

**Status Codes:**
- 200: Success
- 400: Bad request (missing teams)
- 400: Invalid team names
- 500: Server error

**Parameters:**
- `team1` (required): Name of team 1
- `team2` (required): Name of team 2

**Response Fields:**
- `team1`: Team 1 name
- `team2`: Team 2 name
- `predicted_winner`: Which team is predicted to win
- `team1_win_prob`: Probability team 1 wins (0-100%)
- `team2_win_prob`: Probability team 2 wins (0-100%)
- `draw_prob`: Probability of draw (0-100%)
- `predicted_score`: Expected scoreline (e.g., "2-1")

---

### 3. Simulate Tournament
Simulate FIFA World Cup 2026 and get predicted winner.

**Request:**
```
POST /api/tournament-simulate
```

**Response:**
```json
{
    "phase": "Semi-Finals",
    "matches": [
        {
            "team1": "Argentina",
            "team2": "France",
            "winner": "Argentina",
            "prob": 55
        },
        {
            "team1": "Brazil",
            "team2": "Germany",
            "winner": "Brazil",
            "prob": 60
        }
    ],
    "final": {
        "team1": "Argentina",
        "team2": "Brazil",
        "predicted_winner": "Argentina",
        "confidence": 52
    }
}
```

**Status Codes:**
- 200: Success
- 500: Server error

**Response Fields:**
- `phase`: Current tournament phase
- `matches`: Array of semi-final predictions
- `final.team1`: First finalist
- `final.team2`: Second finalist
- `final.predicted_winner`: Tournament champion
- `final.confidence`: Champion confidence (0-100%)

---

## Error Handling

### Error Response Format
```json
{
    "error": "Error message describing what went wrong"
}
```

### Common Errors

**400 - Bad Request**
```json
{
    "error": "Teams required"
}
```

**400 - Invalid Team**
```json
{
    "error": "Invalid team"
}
```

**500 - Server Error**
```json
{
    "error": "Internal server error"
}
```

---

## Examples

### Using cURL

**Get Teams:**
```bash
curl http://localhost:5000/api/teams
```

**Predict Match:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"team1":"Argentina","team2":"France"}'
```

**Simulate Tournament:**
```bash
curl -X POST http://localhost:5000/api/tournament-simulate
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Get teams
response = requests.get(f"{BASE_URL}/api/teams")
teams = response.json()
print(teams)

# Predict match
prediction = requests.post(
    f"{BASE_URL}/api/predict",
    json={"team1": "Argentina", "team2": "France"}
)
print(prediction.json())

# Simulate tournament
tournament = requests.post(f"{BASE_URL}/api/tournament-simulate")
print(tournament.json())
```

### Using JavaScript

```javascript
const BASE_URL = "http://localhost:5000";

// Get teams
fetch(`${BASE_URL}/api/teams`)
  .then(r => r.json())
  .then(teams => console.log(teams));

// Predict match
fetch(`${BASE_URL}/api/predict`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({team1: "Argentina", team2: "France"})
})
  .then(r => r.json())
  .then(prediction => console.log(prediction));

// Simulate tournament
fetch(`${BASE_URL}/api/tournament-simulate`, {
  method: 'POST'
})
  .then(r => r.json())
  .then(result => console.log(result));
```

---

## Rate Limiting
- Currently unlimited
- For production, implement rate limiting:
  - 100 requests/minute per IP
  - 10 simulations/minute per IP

---

## Response Times
- Get teams: 10-50ms
- Predict match: 100-500ms
- Simulate tournament: 1-3 seconds

---

## Data Types
- `string`: Text data
- `number`: Integer or decimal
- `boolean`: True/false
- `object`: JSON object
- `array`: JSON array

---

## Valid Team Names
```
Argentina, France, Brazil, England, Spain, Germany, 
Netherlands, Belgium, Italy, Portugal, Uruguay, Mexico
```

---

## Status Codes Reference
- **200 OK**: Successful request
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

---

## Best Practices

1. **Error Handling**
   - Always check response status code
   - Handle error responses gracefully
   - Implement retry logic for failures

2. **Performance**
   - Cache team data locally
   - Batch requests when possible
   - Use compression for responses

3. **Security**
   - Use HTTPS in production
   - Validate input data
   - Implement rate limiting
   - Add authentication

4. **Testing**
   - Test with all team combinations
   - Verify response formats
   - Check error handling
   - Monitor response times

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | May 2026 | Initial release |

---

## Support
For API issues or improvements, refer to code comments and documentation.

---

**Last Updated:** May 2026  
**API Version:** 1.0.0
