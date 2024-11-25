import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)



def main():
    logging.info('STARTING PROGRAM')
    pass

main()