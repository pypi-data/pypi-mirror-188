import click
from autumn8.cli import options

from autumn8.cli.commands import models, cloud
from autumn8.cli.interactive import fetch_user_data
from autumn8.common._version import __version__

from autumn8.cli import pending_uploads
from autumn8.lib.service import resume_upload_model
import sys

import questionary
from questionary import Choice

try:
    current_pending_uploads = pending_uploads.retrieve_pending_uploads()
except ValueError:
    # data format stored is incompatible with the current version
    pending_uploads.drop_all_uploads()
    current_pending_uploads = {}

# TODO: save costs by configuring https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html
# TODO: detect if the cached upload is still available on S3
for key in current_pending_uploads:
    resume_args = current_pending_uploads[key]
    print("You have pending upload of {}".format(resume_args["model_file"]))
    continue_upload = questionary.select(
        "Do you want to continue upload?",
        choices=[
            Choice(title="Yes", value="Y"),
            Choice(title="No", value="n"),
            Choice(title="Drop upload", value="drop"),
        ],
        use_shortcuts=True,
    ).unsafe_ask()

    if continue_upload == "" or continue_upload == "Y":
        resume_upload_model({**resume_args, **resume_args["kwargs"]})
        sys.exit(0)

    if continue_upload == "drop":
        pending_uploads.remove_upload(resume_args["run_id"])


@options.use_environment
def test_connection(environment):
    """
    Test AutoDL connection with the current API key.
    Displays the user's email address upon successful connection.
    """
    user_data = fetch_user_data(environment)
    print(f"Hello! You're authenticated as {user_data['email']}")


@click.group()
@click.version_option(version=__version__)
def main():
    pass


main.command()(test_connection)

main.command()(models.submit_model)
main.command()(models.login)
main.command()(models.submit_checkpoint)

main.command()(cloud.list_deployments)
main.command()(cloud.deploy)
main.command()(cloud.terminate_deployment)

if __name__ == "__main__":
    main()
