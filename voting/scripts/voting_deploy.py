#!/usr/bin/env python
# -*- coding:utf-8 -*-
from brownie import Ballot, accounts


def main():
    print("Deploying Voting")
    Ballot.deploy(["0x666f6f"], {'from': accounts[0]})

