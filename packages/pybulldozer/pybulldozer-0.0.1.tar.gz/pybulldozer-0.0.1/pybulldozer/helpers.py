import logging
import os

loggername = 'pybulldozer'
spacing = max([len(l.replace(".py", "")) for l in os.listdir(os.path.dirname(__file__)) if (l[:2] != "__")]) #.py
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s [%(name)s] %(lineno)-3s @ %(module)-{spacing}s  %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(loggername)
logger.setLevel(level=logging.DEBUG)

