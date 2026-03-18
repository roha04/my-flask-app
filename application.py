from flask import Flask

application = Flask(__name__)

@application.route("/")
def index():
    return "Hello from csv12cr0 Elastic Beanstalk CI-CD verification-2026031809035521200"

if __name__ == "__main__":
    application.run()
