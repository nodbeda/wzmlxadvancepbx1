FROM mysterysd/wzmlx:heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY . .

# Upgrade pip, setuptools, and install compatible setuptools-scm before anything else
RUN pip3 install --upgrade pip setuptools>=61 setuptools-scm<8

# Now install the rest of the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]
