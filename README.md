A Python 2.7 wrapper for Looker's api.

# Example usage

```
from looker_api import Looker
import os

client_id = os.environ['LOOKER_CLIENT']
client_secret = os.environ['LOOKER_SECRET']

looker = Looker('subdomain',client_id,client_secret)

looker.run_look(look_id,'/json')
```

Note that this python wrapper only works for instances hosted by Looker. For locally hosted instances of Looker, you'll need to download the repo and modiy the \_make\_base_url method of the Looker class.