import logging

#this can set any level of that the message actually appears 
#otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    pass