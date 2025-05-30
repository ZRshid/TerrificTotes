import logging

def lambda_handler(event, context):
    logging.info(msg='hello')
    return 'works'



