from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ, remove
from subprocess import run as srun
from requests import get as rget
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient

if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

if ospath.exists('rlog.txt'):
    remove('rlog.txt')

basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

load_dotenv('config.env', override=True)

try:
    if bool(environ.get('_____REMOVE_THIS_LINE_____')):
        log_error('The README.md file there to be read! Exiting now!')
        exit()
except:
    pass

BOT_TOKEN = environ.get('BOT_TOKEN', '7919432581:AAEnomP-oxHd2Q0wVRPJiGnGL6UJXEIUZAw')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', 'mongodb+srv://sdswap09:sdswap09@cluster0.fvpny.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL is not None:
    conn = MongoClient(DATABASE_URL)
    db = conn.wzmlx
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    config_dict = db.settings.config.find_one({'_id': bot_id})
    if old_config is not None:
        del old_config['_id']
    if (old_config is not None and old_config == dict(dotenv_values('config.env')) or old_config is None) \
            and config_dict is not None:
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
    conn.close()

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://gitlab.com/mindaheroku/wzmlxadvancepbx1')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = None

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'hk_nordbotz')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'

if UPSTREAM_REPO is not None:
    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"])

    update = srun([f"git init -q \
                     && git config --global user.email doc.adhikari@gmail.com \
                     && git config --global user.name weebzone \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

    repo = UPSTREAM_REPO.split('/')
    UPSTREAM_REPO = f"https://github.com/{repo[-2]}/{repo[-1]}"
    if update.returncode == 0:
        log_info('Successfully updated with latest commits !!')
        log_info(f'UPSTREAM_REPO: {UPSTREAM_REPO} | UPSTREAM_BRANCH: {UPSTREAM_BRANCH}')
    else:
        log_error('Something went Wrong !!')
        log_error(f'UPSTREAM_REPO: {UPSTREAM_REPO} | UPSTREAM_BRANCH: {UPSTREAM_BRANCH}')
