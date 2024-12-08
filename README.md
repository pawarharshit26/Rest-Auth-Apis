## This Project contains rest apis for authentication
Uses django and djangorestframework as framework

## for running it locally, please follow the steps below
(Please install docker for running via single command)
1) clone repo
2) open terminal in clone repository
3) create .env file and paste the content given
4) run docker-compose up --build

### env file
	SECRET_KEY=sjncdjf76rhbyhuyhy7gRDED#TBHH&Y&YGVGGVR$R%DFRTV
	DEBUG=True
	ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,
	SUPER_USER_NAME="Admin"
	SUPER_USER_PASSWORD="Admin@123"

## Testing curls

### Signup API
	curl --location 'localhost:8000/auth/signup/' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	    "email": "harshit@gmail.cs",
	    "password": "hars12123"
	}'

### SingIn API
	curl --location 'localhost:8000/auth/signin/' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	    "email": "harshit@gmail.cs",
	    "password": "hars12123"
	}'

### Authenticated API (Replce bearer token from token 
	curl --location 'localhost:8000/auth/authorized-api/' \
	--header 'Authorization: Bearer {singin_token}'

### Refresh token
	curl --location --request POST 'localhost:8000/auth/refresh-token/' \
	--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXN0X3Rva2VuIjoiYWZlYThjZWU3M2I2ODQ3Yjk4ZTcwNzlhOWY5ZDJhYWI4NTcxNjQ3YyIsImV4cCI6MTczMzY4MzE1OH0.X1scdZKW225h4_ll3TZGjfBpGf3p-8MKaM66G3WjENM' \
	--data ''



