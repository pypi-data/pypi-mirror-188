## Pyroadd

- A simple tool Made for adding members to groups
- support logging name 
- diff wait time
- JSON config for numbers and setting
- spoof login as an android device
- custom device configuration

## Config

```json
{
    "group_source": "1599603923", # group identifier
    "group_target": "1599603923", # group identifier
    "group_source_username": "nimmadev", # source group username
    "group_target_username": "nimmadev;", # target group username
    "from_date_active": "UserStatus.LONG_AGO", # active status
    "auto_join": true, # auto join groups 
    "spam_check": true, # check spam
    "wait_time": 300, # wait after each join [waittime/accounts] = real wait for each number
    "accounts": [ # add all acount like below 
        {
            "phone": "91857100***2",
            "api_id": "676*", # get api key and hashfrom my.telegram.org
            "api_hash": "eb06d*****b1aeb98ae0f581e",
            "app_version" : "9.3.3",
            "device_model" : "Android 10",
            "system_version" :"Moto G8 Power"
}
    ]
}
```


## usage example

### Signup

```python
from pyroadd import pyroadd

app = pyroadd('config.json')
app.Signup('logger-name', 'work_dir')
```
### Login

```python
from pyroadd import pyroadd

app = pyroadd('config.json')
app.Login('logger-name', 'work_dir', False)
```

### Get data

```python
from pyroadd import pyroadd

app = pyroadd('config.json')
app.get_data('logger-name', 'work_dir', 'username' or 'id')

# username will run once for all numbers
# id will run for each number
```

### add member

```python
from pyroadd import pyroadd

app = pyroadd('config.json')
applist = app.Login('logger-name', 'work_dir', True)
app.add_member('logger-name', 'work_dir', 'username' or 'id',  applist)

# username will add user with usernames
# id try to add all user even without username
```

## install pyroadd

```python
pip install  pyroadd
```