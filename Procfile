web: daphne blendjoy.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=blendjoy.settings -v2