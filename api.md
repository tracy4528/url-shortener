# URL Shortener API Documentation

This document provides a comprehensive guide to the URL shortener service API endpoints, including sample requests and responses, HTTP methods, status codes, and error messages.

## Base URL

All URLs referenced in the documentation have the following base:

```
http://localhost:5000
```

## API Endpoints

### 1. Create Short URL

Creates a shortened URL from a long URL.

- **URL:** `/shorten`
- **Method:** `POST`
- **Content Type:** `application/json`

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| original_url | string | The long URL to be shortened. Must be a valid URL format and not exceed 2048 characters. |

#### Sample Request

```http
POST /shorten HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "original_url": "https://www.example.com/very/long/url/that/needs/shortening"
}
```

#### Success Response

- **Code:** 201 Created
- **Content:**

```json
{
  "short_url": "http://localhost:5000/abcdef",
  "expiration_date": "2024-09-05T12:00:00",
  "success": true
}
```

#### Error Responses

1. Missing original_url
   - **Code:** 400 Bad Request
   - **Content:**
     ```json
     {
       "success": false,
       "reason": "Missing original_url"
     }
     ```

2. Invalid URL
   - **Code:** 400 Bad Request
   - **Content:**
     ```json
     {
       "success": false,
       "reason": "Invalid URL"
     }
     ```

3. URL Too Long
   - **Code:** 400 Bad Request
   - **Content:**
     ```json
     {
       "success": false,
       "reason": "URL too long"
     }
     ```

### 2. Redirect Using Short URL

Redirects from a short URL to the original long URL.

- **URL:** `/<short_url>`
- **Method:** `GET`

#### Sample Request

```http
GET /abcdef HTTP/1.1
Host: localhost:5000
```

#### Success Response

- **Code:** 302 Found
- **Headers:** 
  ```
  Location: https://www.example.com/very/long/url/that/needs/shortening
  ```
- **Action:** Redirects to the original URL

#### Error Responses

1. Invalid Short URL
   - **Code:** 404 Not Found
   - **Content:**
     ```json
     {
       "success": false,
       "reason": "Invalid short URL"
     }
     ```

2. Expired URL
   - **Code:** 410 Gone
   - **Content:**
     ```json
     {
       "success": false,
       "reason": "URL has expired"
     }
     ```

## Notes

- Short URLs are valid for 365 days from the date of creation.
- If the same long URL is submitted multiple times, the existing short URL will be returned instead of creating a new one.
- The service uses a PostgreSQL database to store URL mappings.

## Error Handling

The API uses the following HTTP status codes:

- 200 OK: The request was successful (some API calls may use 201 instead).
- 201 Created: The request was successful and a resource was created.
- 302 Found: Redirect to another URL.
- 400 Bad Request: The request was invalid or cannot be served.
- 404 Not Found: The requested resource could not be found.
- 410 Gone: The requested resource is no longer available.

## Rate Limiting

Currently, there are no rate limits imposed on the API. However, excessive use may be monitored and restricted if necessary.