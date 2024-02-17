#!/bin/bash


echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate


echo "Creating superuser..."
echo "from users.models import User; User.objects.create_superuser('admin', 'admin@exmaple.com', '12345')" | python manage.py shell

# Start the Django development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
