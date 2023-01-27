import os
import boto3
s3 = boto3.resource('s3')
sts_client = boto3.client('sts')

def assume_role (assume_role_arn, session_name):
    '''
    Assumes a role from AWS account and uses the temporary credentials from
    that role to perform actions inside of the AWS account with TTL on the session to
    make sure there are no long lasting credentials.

    The assumed role must grant permission to list the buckets in the other account.

    :param assume_role_arn: The Amazon Resource Name (ARN) of the role that
                            grants access to deploy/access ec2.
    :param session_name: The name of the STS session.
    :param mfa_serial_number: The serial number of the MFA device. For a virtual MFA
                              device, this is an ARN.
    :param mfa_totp: A time-based, one-time password issued by the MFA device.
    :param sts_client: A Boto3 STS instance that has permission to assume the role.
    '''

    response = sts_client.assume_role(
        RoleArn=assume_role_arn,
        RoleSessionName=session_name)
        #SerialNumber=mfa_serial_number,
        #TokenCode=mfa_totp)
    temp_credentials = response['Credentials']
    #print(response)

#for bucket in s3.buckets.all():
 #   print(bucket.name)
    print(f"Assumed role {assume_role_arn} and got temporary credentials.")

    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=temp_credentials['AccessKeyId'],
        aws_secret_access_key=temp_credentials['SecretAccessKey'],
        aws_session_token=temp_credentials['SessionToken'])

    print(f"Listing buckets for the assumed role's account:")
    for bucket in s3_resource.buckets.all():
        print(bucket.name)

#export local vars for role arn and session name
assume_role("ROLE_ARN", "SESSION_NAME")