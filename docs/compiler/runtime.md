# Runtime Contract

The Runtime represents the standard library and external capabilities of the Lala language.

## Architecture
The compiler backend must **never** hardcode the behavior of runtime functions (like `graphics.circle`). Instead, it communicates with the runtime via **Stable IDs**.

## JSON Manifests
Runtime modules are defined in JSON manifests, exposing their API surface to the compiler:
```json
{
  "module": "graphics",
  "backend_name": "Raylib",
  "functions": [
    {
      "name": "circle",
      "parameters": ["number", "number", "number", "number", "number", "number"],
      "returns": "void",
      "pure": false,
      "platform": "all",
      "intrinsic": false,
      "stable_id": "GRAPHICS_CIRCLE"
    }
  ]
}
```

The frontend binds the call to `RuntimeID.GRAPHICS_CIRCLE`. The backend executes it by looking up the corresponding implementation for its target.
