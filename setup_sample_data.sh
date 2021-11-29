python3 -c "
from app import db, create_app;
db.create_all(app=create_app());"

curl -X POST http://0.0.0.0:5000/signup -H "Content-Type: multipart/form-data" -F "email=admin-test@example.com" -F "password=test" -F "name=test admin"
curl -X POST http://0.0.0.0:5000/signup -H "Content-Type: multipart/form-data" -F "email=user-test@example.com" -F "password=test" -F "name=test user"
curl -X POST http://0.0.0.0:5000/signup -H "Content-Type: multipart/form-data" -F "email=manager-test@example.com" -F "password=test" -F "name=test manager" -F "manager=yes"