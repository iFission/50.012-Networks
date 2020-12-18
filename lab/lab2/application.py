from flask import Flask, session, request, jsonify
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps

app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:

    @app.after_request
    def after_request(response):
        response.headers[
            "Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session to use filesystem for temp storage (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

user_1 = {'username': 'admin', 'password': 'admin'}
user_2 = {'username': 'alex', 'password': 'alex'}
users = [user_1, user_2]

# {'username': 'message'}
tweets = [{'alex': 'hello world!'}]


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return 'Log in at /api/v1/login via POST form: username, password'
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return "Hello world"


@app.route('/api/v1/users', methods=["GET"])
def get_users():
    return jsonify([{
        f'user_{index}': user['username']
    } for index, user in enumerate(users)])


@app.route('/api/v1/users/<username>', methods=["GET"])
def get_user(username):
    print(request.headers)
    username_list = [user['username'] for user in users]

    username_index = -1
    try:
        username_index = username_list.index(username)
    except:
        return 'no user found'

    user_tweets = [tweet for tweet in tweets if username in tweet.keys()]

    if request.headers['Accept'] == 'text/plain':
        response = ""
        response += f"User {username} has {len(user_tweets)} tweets\n"
        response += "Tweets:\n"

        for user_tweet in user_tweets:
            response += f'{username}: {user_tweet[username]}\n'

        return response

    else:
        return jsonify([{
            'username': username,
            'tweet_count': len(user_tweets)
        }, user_tweets])


@app.route('/api/v1/tweets', methods=["GET", "POST"])
@login_required
def get_tweets():
    if request.method == "GET":
        return jsonify([{'tweet_count': len(tweets)}, tweets])

    elif request.method == "POST":

        # ensure username was submitted
        if not request.form.get("tweet"):
            return "must provide tweet"

        user_id = session["user_id"]
        username = users[user_id]['username']

        tweet = {username: request.form.get("tweet")}
        tweets.append(tweet)

        return jsonify(tweet)

    return 'error'


@app.route('/api/v1/tweets/<tweet_index>', methods=["GET", "DELETE"])
@login_required
def get_tweet(tweet_index):
    if request.method == "GET":
        return jsonify(tweets[int(tweet_index)])

    elif request.method == "DELETE":
        user_id = session["user_id"]
        username = users[user_id]['username']

        tweet = -1
        try:
            tweet = tweets[int(tweet_index)]
            if username not in tweet.keys():
                return 'no permission'

            tweets.pop(int(tweet_index))
        except IndexError:
            return 'tweet not found'

        return jsonify(tweet)

    return 'error'


@app.route("/api/v1/login", methods=["POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        # ensure username exists and password is correct
        user_id = -1
        for index, user in enumerate(users):
            for username, password in user.items():
                if request.form.get(
                        "username") == username and request.form.get(
                            "password") == password:
                    user_id = index

        # remember which user has logged in
        session["user_id"] = user_id

        # redirect user to home page
        return "200\n"


if __name__ == "__main__":
    app.run(debug=True)