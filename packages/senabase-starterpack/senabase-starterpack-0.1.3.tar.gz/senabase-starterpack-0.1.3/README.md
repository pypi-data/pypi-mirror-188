# senabase-starterpack

Starterpack for fast prototyping

## Example

### sb_pg

Postgresql starterpack

```python
from senabase.starterpack import sb_pg

sb_pg.configure('127.0.0.1', 5432, 'postgres', 'userid', 'userpassword')

q1 = 'select now()'
rs = sb_pg.get(q1)
```

### sb_log

Logging starterpack

```python
from senabase.starterpack import sb_log

sb_log.configure('proto')

sb_log.i('Information')
sb_log.d('Debug')
sb_log.e(Exception('Example exception'))
```