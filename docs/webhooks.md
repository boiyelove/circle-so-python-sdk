# Webhooks

## Signature Verification

```python
from circle.webhooks import verify_signature

# In your webhook handler
payload = request.body  # raw bytes
signature = request.headers["X-Circle-Signature"]
secret = "your_webhook_secret"

if not verify_signature(payload, signature, secret):
    return Response(status=401)
```

## Parsing Webhook Payloads

```python
from circle.webhooks import parse_webhook

event = parse_webhook(request.json())
print(event.event_type)   # e.g. "post.created"
print(event.community_id)
print(event.data)          # full event payload dict
```
