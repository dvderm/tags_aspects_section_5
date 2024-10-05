# network_stack and the application stack will be nested stacks created by a root stack. Nested stacks have a special base class in CDK, in order to become network stacks, network_stack and the application stack should be derived from the aws_cdk NestedStack class. 
from aws_cdk import (               
    NestedStack,                    # NestedStack from aws_cdk instead of Stack
    aws_ec2 as ec2
)
from constructs import Construct

class NetworkStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # vpc = ec2.Vpc(self, 'MyVpc',                             # This way would not work because It just creates the Vpc construct, but doesn't have any attributes to return it as "vpc" is just a local variable under the __init__ method. To make it accessible from the instances of the NetworkStack class, we need to turn it into an instance variable. You can do this by defining it under the 'self' variable as below. 
        #                  nat_gateways=0)
        
        self.vpc = ec2.Vpc(self, 'MyVpc',                          # Now the objects of the NetworkStack class will have an attribute named 'vpc' returning the vpc construct unitialized. 
                         nat_gateways=0)