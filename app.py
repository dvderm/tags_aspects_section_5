#!/usr/bin/env python3
# In app.py stacks are initalized / instances of the defined classes (NetworkStack (from network_stack.py), TagsAspectsSection5Stack (from tags_aspects_section_5_stack.py), etc.) are created 
import os

import aws_cdk as cdk

from tags_aspects_section_5.tags_aspects_section_5_stack import TagsAspectsSection5Stack
from tags_aspects_section_5.network_stack import NetworkStack
from tags_aspects_section_5.aspects import EC2InstanceTypeChecker                # From the tags_aspects_section_5 package's module "aspects", import EC2InstanceTypeChecker class


app = cdk.App()

# Defining root_stack as an instance of the Stack class/initialize an instance of CDK stack class
root_stack = cdk.Stack(app, 'RootStack')

network_stack = NetworkStack(root_stack, 'NetworkStack')

application_stack = TagsAspectsSection5Stack(root_stack, "TagsAspectsSection5Stack",
                         my_vpc=network_stack.vpc)

# Attaching Aspect to a stack so it will visit all CDK constructs defined in the stack to perform the operation you coded in the Aspect's .visit() method. 
cdk.Aspects.of(root_stack).add(EC2InstanceTypeChecker()) # .of() method will return an API for managing its aspects, similar to tagging. Use the .add() method to add an aspect and provide an aspect object as an argument. Therefore, initializing an instance of our aspect class, using parenthesis: EC2InstanceTypeChecker()

# Stack level tagging
cdk.Tags.of(network_stack).add('category', 'network')   # First positional argument of the .add() method is the tag key. Second positional argument is its value (key-value pair). In this case, we defined the tag of the network_stack as being of the 'network' category. This tag will be added to the network_stack and all constructs under it. 
cdk.Tags.of(application_stack).add('category', 'application',
                                   priority=200)        # priority is a keyword argument. By default .add() operations have a priority value of 100. Increasing this value will increase priority. 

app.synth()
