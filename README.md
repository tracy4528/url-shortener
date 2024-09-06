# URL Shortener Service

This is a simple URL shortener service built with Flask and PostgreSQL. It allows users to create short URLs for long web addresses.

## Prerequisites

- Git
- Docker
- Docker Compose

## Getting Started

Follow these steps to get the URL shortener service running on your local machine:

1. Clone the repository:

```bash
git clone https://github.com/tracy4528/url-shortener.git
cd url-shortener
```

2. Create a `.env` file in the project root directory with the following content:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=url_shortener
```

Replace `your_secure_password` with a strong password of your choice.

3. Build and start the services using Docker Compose:

```bash
docker-compose up -d
```

This command will build the Flask application image and start both the Flask app and PostgreSQL database containers in detached mode.

4. Check if the services are running:

```bash
docker-compose ps
```

You should see two services running: `web` and `db`.

5. The URL shortener service should now be accessible at `http://localhost:5000`.

## API document
[api document](https://github.com/tracy4528/url-shortener/blob/main/api.md)
## Usage

- To create a short URL, send a POST request to `http://localhost:5000/shorten` with a JSON body containing the `original_url`:

```json
{
    "original_url": "https://www.apple.com/tw/"
}
```

- To use a short URL, simply access it in your browser: `http://localhost:5000/{short_url}`

## Stopping the Service

To stop and remove the containers, networks, and volumes associated with the URL shortener service, run:

```bash
docker-compose down -v
```



## Future Work

We have several exciting features and improvements planned for future releases:

1. **User Authentication**: Implement user accounts to allow users to manage their shortened URLs.

2. **Custom Short URLs**: Allow users to create custom short URLs instead of only using randomly generated ones.

3. **Analytics Dashboard**: Provide basic analytics for each shortened URL, such as click count and geographic information of visitors.

4. **URL Expiration Options**: Allow users to set custom expiration dates for their shortened URLs.

5. **Improved Error Handling**: Enhance error handling and provide more informative error messages to users.

6. **AWS Deployment (EC2 + RDS)**: Migrate the application to AWS, using EC2 for hosting the application and RDS for the PostgreSQL database. This will improve scalability and reliability.

7. **Redis Caching**: Implement Redis caching to store frequently accessed URLs. This will significantly reduce database load and improve response times for popular short URLs.



We welcome contributions in any of these areas or other improvements you think would benefit the project!


