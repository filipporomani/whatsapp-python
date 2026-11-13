# whatsapp-python 4.5.0

## Highlights

Closer alignment with the WhatsApp Cloud API (Graph API `v27.0` fallback), new interactive message helpers, and correctness fixes for sync/async clients.

## New APIs (sync + async)

- `send_flow` — WhatsApp Flows
- `send_catalog_message` — catalog thumbnail
- `send_product` / `send_product_list` — commerce messages
- `send_address_message` — address request
- `send_call_permission_request` — call permission request

## Fixes

- `create_button` accepts plain strings or Meta-shaped header/body/footer objects (no double-wrapping)
- `Message` / `AsyncMessage` raise typed Graph errors via `Handle` on failure
- Async send helpers now `await` the HTTP call and return the JSON dict (no unfinished `Future`)
- `AsyncWhatsApp.upload_media` uses `aiohttp` (no blocking `requests`)
- `query_media_url` (async) returns the media URL string, matching sync
- Corrected inverted `link=` docs on image / sticker / video helpers
- Manual smoke tests accept `TOKEN` or `GRAPH_API_TOKEN`

## Notes

Some interactive types (Flows, catalog, address, calling) require the matching feature to be enabled on the WABA / phone number. The client now raises typed errors when Meta rejects those payloads.

## Install

```bash
pip install -U whatsapp-python==4.5.0
```
