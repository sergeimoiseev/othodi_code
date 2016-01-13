# -*- coding: UTF-8 -*-
import os
# import logging
import logging.config
import my_module

import yaml, sys

def setup_logging(
    default_path='logging.yaml', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    print("Main start")
    my_module.foo()
    bar = my_module.Bar()
    bar.bar()
    logger.info('Hi, world')
    logger.debug('Hi, world')

if __name__ == '__main__':
    import logging.config
    # load the logging configuration
    setup_logging()

    # logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # fh = logging.FileHandler('%s.log' % sys.argv[0].split('.')[0])
    # fh.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    main()
