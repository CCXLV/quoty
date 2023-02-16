# About

This is a simple website where people can post their favorite  quotes with the correct category. Admins also can delete the quotes in the database from the website. Made with Python(Flask) and JavaScript for the backend and HTML & CSS for the frontend.

Author: [CCXLV](https://github.com/CCXLV)



# How to set up
1. **Install the requirements.**

Install by running `pip install -r requirement.txt`

2. **Create MySQL database.**

```sql
CREATE DATABASE quoty;
```

3. **Head to `/utils/table.sql`**

Run the template in sql query.

4. **Head to `/config.py`** 

Fill in like the following template:

```py
SECRET_KEY = 'LlmYzFf7giAVx27rt01WasdAdasvVuyx6AeMcCbd' # Put there simple string.
MySQL_URL = 'mysql://user:password@localhost:port/database_name' # Put your MySQL URL
ADMIN_PASSWORD = 'admin123' # Just put a password in there
```
5. **Now you can run the website by running:**

```sh
python app.py
```

# Copyright

Copyright (c) 2023 CCXLV

All rights reserved.
