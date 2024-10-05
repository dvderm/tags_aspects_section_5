import jsii         # AWS primary CDK language is JavaScript. However, the jsii package allows code in any language to interact with Javascript classes, which is why we need it. We will use one of its Python decorators while defining our Aspect classes.
from aws_cdk import (
    IAspect,
    Annotations,    # To attach information, warnings or error messages to your constructs during synthesis, you need the annotations class from the core CDK library
    aws_ec2 as ec2,        # Checks will be performed on the EC2 instances, so we neec aws_ec2 as well

)

# Using the jsii module's "implement" method (Python decorator) which automatically adds the necessary configuration to your Python class during synthesis. 
@jsii.implements(IAspect)

# Defining Python class for aspect class using the above decorator. 
class EC2InstanceTypeChecker:
    
    # # # # # # # # # Example to see what an Aspect does; what visiting constructs by an Aspect looks like # # # # # # # # 
    # # CDK Aspects employ the visitor-design pattern of object oriented programming. In the visitor-design pattern you run separate algorithms on the scope of an object structure such as a CDK Stack and its sub-constructs in the CKD tree. To implement this pattern, you create classes for your CKD Aspects having a special method called "visit()". Then during the preparation phase of the CDK app lifecycle, CDK calls this visit() method for each construct in the Aspect's scope. So you write the code of your Aspects in the visit() method. You access the construct visited by using one of the visit() method's arguments. 
    # def visit(self, construct_visited):    # As this is an instance method, its first argument must be "self". Don't confuse this with the "scope"-argument we provided in previous lectures. Second argument is the only argument the visit() method takes, the construct it visits. In examples on the web, the second argument is often called "node" instead of "construct_visited". This is not the same "node" as the "node" attribute of each CDK construct that is used in the print() below. 
        
    #     # Visit method here will print the path of the construct visited in your CDK app's construct tree and the name of its Python class. Using this print() you can see what this .visit() method does during synthesis. Mostly however, you use Aspects to do checks (see below). 
    #     print(f'{construct_visited.node.path} - {construct_visited.__class__.__name__}') # Each CDK construct has a common node attribute representing its node in the CDK construct tree in your app. Names with double underscores represent special attributes or methods in Python.
    # # # # # # # # # End example # # # # # # # # 
    

    # Creating a list of allowed instances 
    allowed_instance_types = ['t2.micro', 't3.micro']

    def visit(self, node):
        
        # If the visited construct is an EC2 instance...
        if isinstance(node, ec2.CfnInstance):    # How to check the class of an object in Python? With isinstance(). This takes an object and a class as parameters and returns True if the object belongs to that class. The object we check is the node parameter of the visit() method representing the construct visited, and we then check if this is an ec2.CfnInstance (the L1 level construct created under the hoofd of our L2 level construct tags_aspects_section_5_stack.web_server)
            
            # Check if the instance is of the allowed type
            if node.instance_type not in self.allowed_instance_types:

                Annotations.of(node).add_error(f'{node.instance_type} instance type is invalid')    # This will raise messages on the terminal. node represents the construct visited. 

                # Also possible instead of the line of code above: raises a warning and changes the node type. Using Aspects to change your stack is however, not a best practise. 
                # Annotations.of(node).add_warning(f'{node.instance_type} instance type is invalid. It will be set to t2.micro')
                # node.instance_type = 't2.micro' # Changing the instance_type (whenever the visited construct is a ec2.CfnInstance)