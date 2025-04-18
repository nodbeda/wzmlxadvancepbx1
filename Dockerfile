FROM mysterysd/wzmlx:heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app 
RUN pip install --upgrade pip setuptools wheel

RUN uv venv --system-site-packages

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]
