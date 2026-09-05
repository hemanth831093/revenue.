# RecoverAI --- Deployment Plan

## 1. Repository

Create one GitHub repository:

``` text
recoverai/
├── frontend/
├── backend/
├── database/
├── docs/
├── README.md
└── .gitignore
```

## 2. Environment Configuration

Frontend: - `VITE_API_BASE_URL`

Backend: - `DATABASE_URL` - `RAZORPAY_KEY_ID` - `RAZORPAY_KEY_SECRET` -
`LLM_API_KEY`

Secrets must be stored in the hosting provider's environment-variable
settings.

## 3. Database Deployment

1.  Create Supabase project.
2.  Create required tables.
3.  Apply SQL schema.
4.  Insert synthetic demo data.
5.  Verify indexes and constraints.

## 4. Backend Deployment

Recommended: Render or Railway.

Steps: 1. Connect GitHub repository. 2. Select backend directory. 3.
Install dependencies. 4. Start FastAPI with Uvicorn. 5. Add environment
variables. 6. Test `/health`.

Example health endpoint: `GET /health` → `{ "status": "ok" }`

## 5. Frontend Deployment

Recommended: Vercel.

Steps: 1. Import GitHub repository. 2. Select frontend directory. 3.
Configure build command. 4. Configure output directory. 5. Add
`VITE_API_BASE_URL`. 6. Deploy. 7. Test all routes.

## 6. CORS

Allow only the deployed frontend origin in production.

## 7. Security

-   HTTPS only.
-   Never expose Razorpay secret keys to frontend.
-   Validate all API input.
-   Add authentication before production use.
-   Rate-limit recovery endpoints.
-   Make recovery operations idempotent.
-   Maintain audit logs.

## 8. Production Safety

The hackathon demo should use synthetic/test transactions. Autonomous
financial actions must remain bounded, logged, and subject to explicit
stopping rules.

## 9. Final Verification Checklist

-   [ ] Dashboard loads
-   [ ] Transactions load
-   [ ] AI analysis works
-   [ ] Recovery action works in test/simulation
-   [ ] Recovered revenue updates
-   [ ] Audit logs update
-   [ ] No secrets in GitHub
-   [ ] Backend health check works
-   [ ] Frontend can reach backend
-   [ ] Demo dataset is reproducible
-   [ ] README contains setup and demo instructions

## 10. Demo URL

After deployment, record: - Frontend URL - Backend URL - GitHub
repository - Demo credentials if used
