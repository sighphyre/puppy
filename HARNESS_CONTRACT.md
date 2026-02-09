# Harness Contract

## Purpose
Define a consistent, SDK-agnostic format for driving SDK behavior and capturing observable results. A test is a sequence of instructions (steps) that the harness executes against the SDK.

## Runtime Contract (Current Ruby Harness)
- Test input is fetched from Puppy over HTTP.
- Harness executes steps in order and emits a single JSON payload to stdout.
- Harness posts the same payload to Puppy report ingestion.

## Environment Variables
- `UNLEASH_API_URL` (default: `http://localhost:4242/api/`)
- `UNLEASH_API_KEY` (default: `SOME-SECRET`)
- `PUPPY_BASE_URL` (default: `http://localhost:4242`)
- `PUPPY_RUN_ID` (default: `default`)
- `PUPPY_DEBUG` (`false` disables logs)

## Derived Endpoints
- Tests input URL: `${PUPPY_BASE_URL}/api/tests`
- Report ingestion URL: `${PUPPY_BASE_URL}/api/report/ingest`

## Input Shape
```json
{
  "tests": [
    {
      "id": "string",
      "name": "optional string",
      "steps": [
        {
          "op": "isEnabled",
          "toggleName": "string",
          "context": { "userId": "1" },
          "defaultValue": false
        }
      ]
    }
  ]
}
```

## Step Operations
### `isEnabled`
- **Inputs**
  - `toggleName` (string, required)
  - `context` (object, required)
  - `defaultValue` (boolean, optional)
- **Output**
  - `result` (boolean)

### `getVariant`
- **Inputs**
  - `toggleName` (string, required)
  - `context` (object, required)
  - `defaultVariant` (object, optional)
    - `name` (string)
    - `enabled` (boolean)
    - `payload` (object or null)
- **Output**
  - `result` (object)
    - `name` (string)
    - `enabled` (boolean)
    - `payload` (object or null)

## Output Shape
```json
{
  "meta": {
    "sdk": "ruby",
    "runId": "..."
  },
  "results": [
    {
      "testId": "t1",
      "stepIndex": 0,
      "op": "isEnabled",
      "toggleName": "myToggle",
      "result": true
    },
    {
      "testId": "t1",
      "stepIndex": 1,
      "op": "getVariant",
      "toggleName": "myToggle",
      "result": { "name": "blue", "enabled": true, "payload": null }
    }
  ]
}
```
