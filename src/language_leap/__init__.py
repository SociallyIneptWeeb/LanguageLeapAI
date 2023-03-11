from logging import DEBUG, INFO, basicConfig

from language_leap.environment import LOGGING

basicConfig(
    level=DEBUG if LOGGING else INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
