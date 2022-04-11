Operators are equivalent to SQL functions/operators that we can use from our python code to query the database

### Supported operators

| Operator      | SQL equivalent   | Example |
| :------------ | :--------------- | :---- |
| `__in`        | `IN`             | `id__in=(1, 2, 3)` |
| `__not_in`    | `NOT IN`         | `id__not_in=(1, 2, 3)` |
| `__not_equal` | `!=`             | `id__not_equal=5` |
| `__lt`        | `<`              | `id__lt=5` |
| `__le`        | `<=`             | `id__le=5` |
| `__gt`        | `>`              | `id__gt=5` |
| `__ge`        | `>=`             | `id__ge=5` |
| `__like`      | `LIKE`           | `email__like='@mail.com'` |
