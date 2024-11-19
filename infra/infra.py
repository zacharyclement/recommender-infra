from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import core as cdk


class ApiFargateServiceStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC for ECS Cluster
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # ECS Cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # Fargate Service with ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FargateService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=2,
            task_image_options={
                "image": ecs.ContainerImage.from_asset("./"),
            },
        )

        # Existing Cognito User Pool (Assume it's already created)
        user_pool = cognito.UserPool.from_user_pool_id(
            self, "ExistingUserPool", user_pool_id="us-east-1_ABC123"
        )

        # Cognito Authorizer for API Gateway
        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer", cognito_user_pools=[user_pool]
        )

        # API Gateway
        api = apigateway.RestApi(
            self,
            "TrendingLivestreamsApi",
            rest_api_name="Trending Livestreams Service",
            description="API to get trending livestreams",
        )

        # Integrate API Gateway with ALB
        integration = apigateway.HttpIntegration(
            f"http://{fargate_service.load_balancer.load_balancer_dns_name}",
            options=apigateway.HttpIntegrationOptions(http_method="GET", proxy=True),
        )

        # Add /get_trending_livestreams endpoint with authorization
        resource = api.root.add_resource("get_trending_livestreams")
        resource.add_method(
            "GET",
            integration,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )

        # Outputs for API Gateway and Fargate service
        cdk.CfnOutput(self, "ApiUrl", value=api.url)
        cdk.CfnOutput(
            self,
            "LoadBalancerDns",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )
