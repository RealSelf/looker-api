A Python 2.7 wrapper for lookers api.

# Example usage

```
from looker_api import Looker
import os

client_id = os.environ['LOOKER_CLIENT']
client_secret = os.environ['LOOKER_SECRET']

looker = Looker('subdomain',client_id,client_secret)

looker.run_look(look_id,'/json')
```