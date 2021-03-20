  
#!/bin/bash

rm -rf holygrailapi/migrations
rm db.sqlite3
python manage.py makemigrations holygrailapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata closetProduct
python manage.py loaddata closet
python manage.py loaddata product
