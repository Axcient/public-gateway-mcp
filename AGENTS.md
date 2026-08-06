# AGENTS.md

This file provides guidance to AI coding agents when working with this repository.

## Development Workflow

**IMPORTANT**: Always use `just` commands instead of underlying tools directly. Do not run `uv`, `pytest`, `ruff`, `mypy`, or other tools directly - use the `just` wrappers instead.

### Test-Driven Development

The development workflow follows TDD principles:

1. **Write tests first** in the `tests/` directory
2. **Run `just fix`** to auto-fix linting/formatting issues in case of linting errors
4. **Run `just check-all`** is the most important command, as always should run this before committing

## Testing

## Naming Conventions

### Files
- Source modules: `snake_case.py`
- Test files: `module_name_test.py`

### Code
- Classes: `PascalCase` (e.g., `PostgresInteractor`, `CreatePartnerRequest`)
- Functions/methods: `snake_case` (e.g., `create_partner`, `filter_contacts_by_partner`)
- Constants: `SCREAMING_SNAKE_CASE`
- Pydantic fields: `snake_case`
- Multiple Variables: Never use enumerated variable names like `partner_1` or `partner1` and instead create a new list like `partners = []`

### Testing Style
- **No enumerated variables**: Use lists instead of `result1`, `result2`, etc.
- **Assert the full response and objects, not a part of it**: Always assert against the complete expected object (the entire returned model or response). Never assert only a portion of the response—such as a single field, a derived set of ids, a length/count, or a filtered projection. Build the full expected object and compare it for equality. In addition to that, don't assert individual attributes multiple times. Compare against the full expected object:

```python
# Bad - multiple asserts on same object
result = interactor.create_partner(obj=request)
assert result.name == "Test Partner"
assert result.country == "US"

# Good - assert the full object
assert interactor.create_partner(obj=request) == schemas.PartnerInDB.model_validate(
    {
        "name": "Test Partner"
        # ... all fields
    }
)
```

### Schema Naming
- Request models: `Create{Entity}Request`, `{Action}{Entity}Request`
- Response models: `Filter{Entity}Response`, `{Entity}Response`
- Record insert helpers: `{Entity}RecordInsert` (TypedDict for SQL params)

### Error Naming
- `{Entity}NotFoundError` for 404 errors
- `Duplicate{Entity}Error` for unique constraint violations
- All inherit from `turbo_lambda.errors.GeneralError`
- `{Entity}Error` for all application-defined exceptions
