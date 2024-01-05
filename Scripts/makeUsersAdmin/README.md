# makeUsersAdmin
Script to run on an interval and make any non-admin an admin

## Setup
* Run pip and install dependencies on requirements.txt

```
pip3 install -r requirements.txt
```

* Configure creds.yaml
```
# Org Creds
email: username@company.com
password: ABC123
orgId: F2ax3-53sd3
realm: us1

```

* Add the following to crontab -e (use location of script)

```
0 * * * * python3 /home/ubuntu/show-makeadmins/makeUsersAdmin.py
```

