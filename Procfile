web: sh target/bin/webapp
web: lein run -m demo.web $PORT
web: bundle exec rails server -p $PORT
worker:  bundle exec rake jobs:work
