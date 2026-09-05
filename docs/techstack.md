# RecoverAI --- Technology Stack

## Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS
-   Recharts
-   Axios

## Backend

-   Python
-   FastAPI
-   Pydantic
-   Uvicorn

## AI / ML

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   LLM API for diagnosis, explanation, and decision reasoning

## Database

-   Supabase PostgreSQL

## Payment Integration

-   Razorpay Test Mode APIs

## Authentication

For MVP: simple demo authentication if required. For production:
Supabase Auth or secure JWT-based authentication.

## Deployment

-   Frontend: Vercel
-   Backend: Render or Railway
-   Database: Supabase

## Development Tools

-   VS Code
-   Git
-   GitHub
-   Postman/Thunder Client

## Environment Variables

Frontend:

``` text
VITE_API_BASE_URL=
```

Backend:

``` text
DATABASE_URL=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
LLM_API_KEY=
```

Never commit `.env` files or API secrets to GitHub.

## Why This Stack

React provides a fast dashboard UI, FastAPI is simple for Python AI
integration, Supabase provides PostgreSQL and convenient backend
services, Scikit-learn supports an explainable baseline model, and
Razorpay Test Mode allows payment workflows to be demonstrated safely.
