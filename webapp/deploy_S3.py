import boto
from boto.s3.key import Key


BUCKET_NAME = 'www.funf.org'

if __name__ == "__main__":
    conn = boto.connect_s3()
    
    FunfBucket = conn.get_bucket(BUCKET_NAME)
    AppTemplate = Key(FunfBucket)
    AppTemplate.key = 'app_generator.tar.gz'
    AppTemplate.set_contents_from_filename('app_generator.tar.gz')