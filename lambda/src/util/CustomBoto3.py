import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

class CustomBoto3:

    def uploadFileToS3(self, file_name: str , bucket: str, object_name: str=None) -> bool: 
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        :raises: :exc:':ClientError' if error occured.
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def getQuickSightUserFromSSM(self)-> str:         
        """Get User Inforamtion to Login QuickSight from SSM

        :return: ID/PW if can get infromation from secretsmanager else Error string
        :raises: :exc:':ClientError' if error occured.
        """
        try:
            secret_name = "quicksight/pdf/user"
            region_name = "ap-northeast-2"

            # Create a Secrets Manager client
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            # Decrypts secret using the associated KMS key.
            secret = json.loads(get_secret_value_response['SecretString'])

            return secret['quicksight_user'],secret['quicksight_pw']         # SSM의 시크릿(Secret)에서 사용자 정보를 가져오고, 해당 정보를 반환합니다

        except ClientError as e:
            print(e)
            return e

