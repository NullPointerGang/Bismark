import os
import yaml
from dotenv import load_dotenv

load_dotenv()

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file) or {}

HOST = config['server_host']
PORT = config['server_port']

PROXY_LIST = config['proxy_list']

SECRET_KEY = os.getenv('SECRET_KEY')