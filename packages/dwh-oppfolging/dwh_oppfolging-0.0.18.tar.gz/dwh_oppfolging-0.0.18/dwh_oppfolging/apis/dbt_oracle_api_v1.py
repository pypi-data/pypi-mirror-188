
import os
import subprocess
import sys
from contextlib import contextmanager
from typing import Generator
from dwh_oppfolging.apis.secrets_api_v1 import get_dbt_oracle_secrets_for


@contextmanager
def create_dbt_oracle_context(username: str) -> Generator[None, None, None]:
    """
    use in with statement
    yields nothing
    but sets and unsets environment variables referenced by dbt profile
    """
    secrets = get_dbt_oracle_secrets_for(username)
    os.environ.update(secrets)
    yield
    for k in secrets:
        os.environ.pop(k)
#    #secrets = get_dbt_oracle_secrets_for(username)
#    try:
#        file = open(file="profiles.yml", mode="wt", encoding="utf-8")
#        ... write to file
#        file.close()
#        yield
#    finally:
#        os.remove("profiles.yml")


def run_dbt(profiles_dir: str | None = None, project_dir: str | None = None) -> None:
    """
    executes dbt test and run as subprocess
    assuming profiles yaml file is located
    this should be done inside a dbt_oracle context
    """
    profiles_dir = profiles_dir or sys.path[0]
    project_dir = project_dir or sys.path[0]
    try:
        subprocess.run(
            ["dbt", "test", "--profiles-dir", profiles_dir, "--project-dir", project_dir],
            check=True, capture_output=True
        )
        subprocess.run(
            ["dbt", "run", "--profiles-dir", profiles_dir, "--project-dir", project_dir],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as exc:
        raise Exception(exc.stdout.decode("utf-8")) from None
