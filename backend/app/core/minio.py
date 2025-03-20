from minio import Minio
from minio.error import S3Error

from app.core.config import settings

# Create MinIO client
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)

# Bucket names
AVATAR_BUCKET = "avatars"
ATTACHMENT_BUCKET = "attachments"

def ensure_buckets_exist():
    """
    Ensure the required buckets exist in MinIO.
    This is called at startup.
    """
    try:
        # Check if avatar bucket exists, create if not
        if not minio_client.bucket_exists(AVATAR_BUCKET):
            minio_client.make_bucket(AVATAR_BUCKET)
            # Set policy to allow public read access to avatars
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{AVATAR_BUCKET}/*"],
                    }
                ],
            }
            minio_client.set_bucket_policy(AVATAR_BUCKET, policy)
        
        # Check if attachment bucket exists, create if not
        if not minio_client.bucket_exists(ATTACHMENT_BUCKET):
            minio_client.make_bucket(ATTACHMENT_BUCKET)
            # Set policy to allow public read access to attachments
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{ATTACHMENT_BUCKET}/*"],
                    }
                ],
            }
            minio_client.set_bucket_policy(ATTACHMENT_BUCKET, policy)
            
    except S3Error as err:
        print(f"Error creating MinIO buckets: {err}")
        raise 