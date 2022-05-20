#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
from brownie import *


@pytest.fixture(scope="module")
def voting(Ballot, accounts):
    return Ballot.deploy(["0x666f6f"], {'from': accounts[0]})


@pytest.fixture
def voting_voter(accounts):
    # msg.sender = accounts[2]
    yield accounts[2]  # 投票人


@pytest.fixture
def voting_delegate(accounts):
    yield accounts[3]  # 被委托人

