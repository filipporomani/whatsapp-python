# Manual / live API smoke tests

These scripts call the real WhatsApp Cloud API and require environment variables:

- `TOKEN` (preferred) or `GRAPH_API_TOKEN`
- `TEST_PHONE_NUMBER_ID`
- `DEST_PHONE_NUMBER`
- `TEST_IMAGE_PATH` (async upload smoke only)

Run from the repo root after exporting those values:

```bash
python3 tests/manual/sync_smoke.py
python3 tests/manual/async_smoke.py
```
