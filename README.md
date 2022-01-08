### Smart News Website 

- Serves [Smart News](https://news.vatave.com) [Work in Progress, Frontend Needs a facelift]  
- This website started as a project for me to get relevant news related to stocks and crypto currencies that I was interested in. But I would like to take it further.
- Currently, shows news articles based on the triggers defined by a file (triggers.csv and triggers-crypto.csv)
  - Features to be added:
    - Infrastructure
      - Hosted on my home lab server
      - Hosted behind a HA reverse proxy (https://github.com/choudhary314/haproxy-configs/blob/main/haproxy.cfg) (Note: Usually served by a two back-end servers, currently only one is being used due to a problem with gunicorn on my second server)
      - Monitored through my Nagios core server
      - Served using gunicorn NGINX workers
      - Running on LXC containers (redundant pairs) -- Soon to be moved to a auto-scaling K8s cluster
    - Improvement
      - Switch from pickle and csv files to a SQLLite DB with SQLAlchemy and Marshmallow models
      - In addition to local logs push the logs to logstash instance
    - Feature roadmap
      - Sentimental Analysis
      - Ticker Prices
      - Personalized Views
      - Currently the trigger search words are controlled by https://github.com/choudhary314/smart-news/blob/master/triggers.csv and https://github.com/choudhary314/smart-news/blob/master/triggers-crypto.csv
