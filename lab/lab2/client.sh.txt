# get all users
curl -X GET 127.0.0.1:5000/api/v1/users --output -

# get user alex's info (in application/json)
curl -X GET 127.0.0.1:5000/api/v1/users/alex --output -

# get user alex's info in text/plain
curl -X GET -H "Accept: text/plain" 127.0.0.1:5000/api/v1/users/alex --output -

# get user admin's info
curl -X GET 127.0.0.1:5000/api/v1/users/admin --output -

# user authentication
curl -X POST 127.0.0.1:5000/api/v1/login -F 'username=alex' -F 'password=alex' -b cookie_alex.txt -c cookie_alex.txt --output -

# get all tweets
curl -X GET 127.0.0.1:5000/api/v1/tweets -b cookie_alex.txt -c cookie_alex.txt --output -

# get first tweet
curl -X GET 127.0.0.1:5000/api/v1/tweets/0 -b cookie_alex.txt -c cookie_alex.txt --output -

# post new tweet as alex
curl -X POST 127.0.0.1:5000/api/v1/tweets -F 'tweet=is the post request working?' -b cookie_alex.txt -c cookie_alex.txt --output -

# delete first tweet
curl -X DELETE 127.0.0.1:5000/api/v1/tweets/0 -b cookie_alex.txt -c cookie_alex.txt --output -