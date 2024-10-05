from aws_cdk import (
    CfnOutput,
    NestedStack,
    aws_ec2 as ec2,
    aws_s3_assets as s3_assets,
    Tags
)
from constructs import Construct

class TagsAspectsSection5Stack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, my_vpc: ec2.Vpc, **kwargs) -> None:  # my_vpc: the colon means that you set the datatype of the argument my_vpc. In this case it is aws_ec2 package's "Vpc" class (L2-level Vpc construct type). You set this argument in "app.py". 
        super().__init__(scope, construct_id, **kwargs)

        
        web_server = ec2.Instance(self, 'WebServer',                # Initalize object of the ec2 package's instance class
                                  machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                  instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.T2,
                                                                    instance_size=ec2.InstanceSize.MICRO),
                                  vpc=my_vpc,                        # Using an L1 level construct here will not work, you need an L2 level construct. Imported from another stack this time instead of defining it in the same stack. 
                                  vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC), # Documentation: google search "aws_cdk.aws_ec2"
                                  user_data_causes_replacement=True)                   
        
        # Attaching an elastic IP to keep the DNS name on updates because whenever the instance is updated, it is replaced because of the "user_data_causes_replacement=True" above
        ec2.CfnEIP(self, 'ElasticIP',                               # L1 construct (the class CfnEIP starts with Cfn, after all).
                   instance_id=web_server.instance_id)              # You can't reference the L2 variable in an L1 construct alone (just "web_server") because the expected input value is a string. However, you can generate a string value by using the .instance_id attribute of the variable "web_server".
        
        # Installing packages at instance launch
        web_server.add_user_data(                                   # On CDK you can provide commands to the user data script of an EC2 instance, by calling the instance .add_user_data() method.
                                'yum update -y',                    # Command to update package repositories
                                 'amazon-linux-extras install nginx1', # Command to install nginx1 package. Nginx is a webserver that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache. 
                                 'rm -rf /usr/share/nginx/html/*',)  # Remove all old files in the folder where index.html will be downloaded (command below in this script), so only the new index.html is used. rm -rf = remove recursively forcefully (with other words, delete all files, hence the *). 
                                #  'service nginx start')             # Starting the Nginx web server at this point would start the web server without the index.html, because that will be downloaded later to the web server from the S3 asset. This is why this command has to be added AFTER downloading the index.html file. 
        
        # Add stack output in order to find webserver DNS name easily. This output can be found after deployment in the terminal of VS code, but also in the tab "Output" of your stack in CloudFormation. 
        CfnOutput(self, "WebServerDnsName",
                  value=web_server.instance_public_dns_name)
        
        # Allowing connections to the webserver
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(80), 'Allow HTTP access from the internet')     # When trying to access the public IPv4 DNS from the EC2 instance, use the HTTP-protocol (in your browser) and not HTTPS since HTTP is what it is configured for.
        web_server.connections.allow_from_any_ipv4(ec2.Port.tcp(22), 'Allow SSH access from the internet')      # 22 Is the SSH port. 

        # Deploying a web page to the web server
        web_page_asset = s3_assets.Asset(self, 'WebPageAsset',      # First parameter is scope, which is set to self, meaning the stack. There are also optional parameters to exclude certain files. See CDK construct library reference for them. 
                                         path='web_pages/index.html')          # If you only enter 'web_pages', CDK will compress folder "web_pages" and upload to the primary CDK bucket on S3 in the AWS region you use, so you will need to unzip the package to use its contents after downloading it to your server. If you have a single file like in this example, you can also provide its local path as an alternative, then there will be no need for unzipping because files are not compressed by CDK when uploaded. 
        
        # Download the index.html to our web_server
        # web_server.add_user_data('aws s3 cp') # This is a possibility but AWS CDK provides the helper method .user_data() to download objects from an S3 bucket. 
        web_server.user_data.add_s3_download_command(               # The user_data property's type is 'UserData' class on the CDK construct library > aws_ec2 > Instance > UserData (under Construct Properties). It provides various helper methods to add commands to the instance's user data script. Here we will use the method .add_s3_download_command()
                                                    bucket=web_page_asset.bucket,               # Where to get the name of the S3 bucket where CDK uploaded the asset? You can access this information through the asset construct that was initialized (web_page_asset). Using the "bucket" attribute which will return the asset's bucket name. 
                                                    bucket_key=web_page_asset.s3_object_key,    # Bucket name is not enough, bucket_key is also required. 
                                                    local_file='/usr/share/nginx/html/index.html') # Location where the file is downloaded on the EC2 instance. In this case index.html will be downloaded in the default Nginx folder. 
        
        # Grant permission to EC2 instance IAM role to read the asset in the S3 bucket
        web_page_asset.grant_read(web_server.role)

        # Starting the Nginx web server after the index.html is downloaded to the web server
        web_server.add_user_data('service nginx start')

        # Tagging constructs
        Tags.of(web_server).add('category', 'web server')   # Tag added at a construct-level instead of at the stack-level, like in app.py. 
        Tags.of(web_server).add('subcategory', 'primary',   # subcategory tag 'primary' added to the EC2 instance (the EC2 instance is the primary construct)
                                include_resource_types=['AWS::EC2::Instance'])
        Tags.of(web_server).add('subcategory', 'side',      # All other resources in web_server construct get 'side' as subcategory
                                exclude_resource_types=['AWS::EC2::Instance'],
                                priority=300)               # By default .remove() method has a priority of 200, so 300 will take precedence over the .remove() statement below. 
        
        Tags.of(web_server.role).remove('subcategory') # Provide web_server.role attribute to .of() method of Tags class to remove the subcategory tag from the role of the web server. Of course, adding the role to exclude_resource_types as seen above also works. 