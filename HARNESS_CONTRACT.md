# Harness Contract (Draft)

## Purpose
Define a consistent, SDK-agnostic format for driving SDK behavior and capturing observable results. A test is a sequence of instructions (steps) that the harness executes against the SDK.

## Top-Level Shape
```json
{
  "meta": {
    "runId": "optional string",
    "suite": "optional string",
    "sdk": "optional string",
    "version": "optional string"
  },
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
  - `context` (object, optional)
  - `defaultValue` (boolean, optional)
- **Output**
  - `result` (boolean)

### `getVariant`
- **Inputs**
  - `toggleName` (string, required)
  - `context` (object, optional)
  - `defaultVariant` (object, optional)
    - `name` (string)
    - `enabled` (boolean)
    - `payload` (object or null)
- **Output**
  - `result` (object)
    - `name` (string)
    - `enabled` (boolean)
    - `payload` (object or null)

## Expected Output Shape (Harness Result)
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

## Notes / Open Questions
- Should we support assertions in the input (expected results), or keep tests purely imperative?
- Should `context` include standard keys only, or allow arbitrary properties?
- Should `getVariant` always include `payload` key (even when null)?
- Do we need step-level timing controls (sleep, wait, retry)?

