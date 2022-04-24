import json
import boto3
import paramiko
import os

def lambda_handler(event, context):
    # boto3 client
    client = boto3.client("ec2")
    s3_client = boto3.client("s3")

    # getting instance information
    describeInstance = client.describe_instances()

    hostPublicIP = []
    # fetchin public IP address of the running instances
    for i in describeInstance["Reservations"]:
        for instance in i["Instances"]:
            if instance["State"]["Name"] == "running":
                hostPublicIP.append(instance["PublicIpAddress"])

    print(hostPublicIP)

    # downloading pem filr from S3
    s3_client.download_file("youtube-comments-mmds", "youtube-comment-analysis-ec2-ohio.pem", "/tmp/file.pem")

    # reading pem file and creating key object
    key = paramiko.RSAKey.from_private_key_file("/tmp/file.pem")
    # an instance of the Paramiko.SSHClient
    ssh_client = paramiko.SSHClient()
    # setting policy to connect to unknown host
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = hostPublicIP[0]
    print("Connecting to : " + host)
    # connecting to server
    ssh_client.connect(hostname=host, username="ubuntu", pkey=key)
    print("Connected to :" + host)

    # command list
    # commands = ["ls", "mkdir trial-hello", "python3 build/ec2trial.py ec2"]
    
    url_code =  event.get("url")
    API_KEY = 'AIzaSyBDxsT_4J155fDCsY8zlOkjvxaosXa43ts'
    
    command_1 = 'python3 build/scrape_code.py '+ url_code + ' ' + API_KEY
    command_2 = 'cd build'
    command_3 = 'aws s3 cp build/comment_data/' + url_code + '.csv s3://youtube-comments-mmds/comment_data/' + url_code + '.csv'
    command_4 = 'rm build/comment_data/' + url_code + '.csv'
    
    commands=[command_1, command_2, command_3, command_4]
    # executing list of commands within server
    for command in commands:
        print("Executing {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read())
        print(stderr.read())

    return {"statusCode": 200, "body": json.dumps("Thanks!")}