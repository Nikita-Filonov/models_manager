Inside the library there is a wrapper over the standard Python enum object. The wrapper extends the functionality of the
standard enum, this is done for ease of use.

```python
from models_manager import FieldGenericEnum


class Roles(FieldGenericEnum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    EXPERT = 'expert'


Roles.to_list()
['junior', 'middle', 'senior', 'expert']

Roles.to_list(exclude=[Roles.EXPERT])
['junior', 'middle', 'senior']
```
