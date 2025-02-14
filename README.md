run the webhook listener and run the CURL command
```
curl -X POST http://localhost:5000/sentry-webhook -H "Content-Type: application/json" -d '{
  "id": "12345",
  "culprit": "app/views.py:42",
  "message": "ZeroDivisionError: division by zero",
  "repository": { "full_name": "SHINO-01/Sentry_FastAPI" }
}'

```
