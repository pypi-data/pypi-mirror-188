#!/usr/bin/env python

"""Tests for `cryptoolz` package."""

import pytest

from click.testing import CliRunner

from cryptoolz import cryptoolz
from cryptoolz import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://codeberg.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'Codeberg' in BeautifulSoup(response.content).title.string
