from dataclasses import dataclass
import enum


@dataclass
class EnvironmentProperties:
    host: str
    s3_host: str
    s3_bucket_name: str


# TODO remove - official CLI builds should only point toward production


class CliEnvironment(enum.Enum):
    value: EnvironmentProperties
    LOCALHOST = EnvironmentProperties(
        host="http://localhost",
        s3_host="http://localhost:4566",
        s3_bucket_name="predictor-bucket",
    )
    STAGING = EnvironmentProperties(
        host="http://54.83.236.20",
        s3_host="https://autodl-staging.s3-accelerate.amazonaws.com",
        s3_bucket_name="autodl-staging",
    )
    PRODUCTION = EnvironmentProperties(
        host="https://autodl.autumn8.ai",
        s3_host="https://autodl-staging.s3-accelerate.amazonaws.com",
        s3_bucket_name="autodl-production",
    )
