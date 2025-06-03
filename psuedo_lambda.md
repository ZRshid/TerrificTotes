know which folder to transform data from bucket
get the json from the s3 bucket
turn into dictionary then into dataframe through pandas
get rid of time stamps
join relevent data to a table

option 1
dump all json into 1 table
then pick relevent data and joins through pandas

option 2
have seperate tables
pick table requried for the join
after joining, create list of strings containing the coloumns names we want to load
use pandas to export only these coloumns

save these data into parquet file, then load to processed s3 bucket

note to self:
to save to the file to the bucket without doing it locally 
need to look into pyarrow/fastparquet libaries

something like 

import io
f = io.BytesIO()

def dataframe_to_s3(s3_client, input_datafame, bucket_name, filepath, format):
        if format == 'parquet':
            out_buffer = BytesIO()
            input_datafame.to_parquet(out_buffer, index=False)
        s3_client.put_object(Bucket=bucket_name, Key=filepath, Body=out_buffer.getvalue())

could also use awswrangler library to do this
https://github.com/aws/aws-sdk-pandas
