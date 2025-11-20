
### Quote Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_quote = meta.get_quote()
```

### Quote Type Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_quote = meta.get_quote_type()
```

### Search Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_search = meta.get_search()
```

### Recommendations Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_recommendations = meta.get_recommendations()
```

### Insights Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_insights = meta.get_insights()
```
