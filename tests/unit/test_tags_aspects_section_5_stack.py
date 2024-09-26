import aws_cdk as core
import aws_cdk.assertions as assertions

from tags_aspects_section_5.tags_aspects_section_5_stack import TagsAspectsSection5Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in tags_aspects_section_5/tags_aspects_section_5_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TagsAspectsSection5Stack(app, "tags-aspects-section-5")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
