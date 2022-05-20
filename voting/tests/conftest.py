#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
from brownie import *


@pytest.fixture(scope="module")
def voting(Ballot, accounts):
    return Ballot.deploy(["0x666f6f"], {'from': accounts[0]})


@pytest.fixture
def voting_voter1(accounts):
    yield accounts[1]  # 投票人


@pytest.fixture
def voting_voter(accounts):
    yield accounts[2]  # 投票人


@pytest.fixture
def voting_delegate(accounts):
    yield accounts[3]  # 投票人&被委托人


@pytest.fixture
def proposal1():
    proposal = 0  # 第一个提案索引
    yield proposal

