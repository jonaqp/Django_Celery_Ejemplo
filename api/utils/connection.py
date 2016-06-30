import boto.s3.connection

AWS_STORAGE_BUCKET_NAME = 'shellcatch'
AWS_S3_CUSTOM_DOMAIN = 'https://{0:s}.s3.amazonaws.com/'.format(str(AWS_STORAGE_BUCKET_NAME))
AWS_ACCESS_KEY_ID = 'AKIAJRA5Z7OCTBF7JPNA'
AWS_SECRET_ACCESS_KEY = '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'


def get_connection_bucket():
    con = boto.connect_s3(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
    return con

