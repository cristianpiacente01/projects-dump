import pytest

def pytest_addoption(parser):
    # Set up arguments for pytest.
    parser.addoption("--gitlab-user", action="store", help="GitLab user")
    parser.addoption("--db-name", action="store", help="Database host", default="sys")
    parser.addoption("--db-host", action="store", help="Database host")
    parser.addoption("--db-port", action="store", help="Database port")
    parser.addoption("--db-user", action="store", help="Database user")
    parser.addoption("--db-password", action="store", help="Database password")