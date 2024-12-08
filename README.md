## This Project contains rest apis for authentication
Uses django and django rest framework 

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
	--header 'Authorization: Bearer {signin_token}'

### Refresh token (Replce bearer token from token 
	curl --location --request POST 'localhost:8000/auth/refresh-token/' \
	--header 'Authorization: Bearer {signin_token}'


### For Revoke token Functionality
	open "http://localhost:8000/admin/" on browser
 	login via username: Admin, password: Admin@123 
	click on Authapp -> User
  	
  <img width="995" alt="Screenshot 2024-12-08 at 11 49 39 PM" src="https://github.com/user-attachments/assets/3ad0f2e8-e90a-425b-a7c4-dc62b31ed0ca">

 	Hear you are able to see the list of users and which user currently have token
	for revoke those token select checkbox as shown in image, select revoke token action from dropdown and click on go
 <img width="995" alt="Screenshot 2024-12-08 at 11 52 37 PM" src="https://github.com/user-attachments/assets/4584da83-7e4b-4d44-a152-8d25e6ee3d09">



