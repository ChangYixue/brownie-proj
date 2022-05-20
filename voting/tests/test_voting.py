#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
"投票"合约的单元测试用例(测试重点：外部函数，不包含构造函数)：

【giveRightToVote】
1. 主席给出某选民投票权后，该选民拥有投票权
2. msg.sender == chairperson  //检查发起者是否是主席
3. !voters[voter].voted  //检查选民是否已投票
4. 选民地址为空(边界值)

【delegate】
1. 委托投票权给某个选民后，若该选民暂未投票，则该选民增加了一份投票权；
2. 委托投票权给某个选民后，若该选民已经投票，则该选民投票权为0；
3. !sender.voted  //检查选民是否已投票
4. to != msg.sender  //检查委托地址与选民地址不一致
5. delegate_.weight >= 1  // 检查被委托人的权重大于等于1

【vote】
1. 某选民投票给某个提案后，该提案的投票总量增加，增量为该选民的权重；
2. sender.weight !=0  // 检查投票者权重是否等于0
3. !sender.voted   //检查投票者是否已投票

【winningProposal】
1. winningProposal_与预期获胜提案索引值相等

【winnerName】
1. winnerName与预期获胜提案的名称相等
"""
import pytest


# 赋予选民投票权
# @pytest.mark.skip()
@pytest.mark.parametrize("accounts_index", [1, 2, 3])
def test_give_right_to_vote(voting, accounts, accounts_index):
    assert accounts[accounts_index] != '0x0'  # 选民地址不为空
    assert voting.voters(accounts[accounts_index])[1] is False  # 选民未投票
    voting.giveRightToVote(accounts[accounts_index])  # 给选民投票权
    # print("voters-->", voting.voters(accounts[1].address))
    # assert voting.voters(accounts[1].address)[0] == 1 # 该方式不可取
    # assert voting.getWeight(accounts[1]) == 1  # 创建函数getWeight()获取权重weight
    assert voting.voterHasRight(accounts[accounts_index])  # 创建函数voterHasRight()判断权重weight是否等于1


# 委托投票
def test_delegate(voting, voting_voter, voting_delegate):
    voter2 = voting.voters(voting_voter)
    voter3 = voting.voters(voting_delegate)  # 保证委托人未委托他人
    assert voter2[1] is False  # 选民未投票
    assert voting_delegate != voting_voter  # 委托地址与选民地址不一致
    assert voter3[2] == '0x0000000000000000000000000000000000000000'  # 委托人的委托地址为空
    assert voter3[0] >= 1  # 检查被委托人的权重大于等于1
    voting.delegate(voting_delegate, {"from": voting_voter})  # accounts[2]投票权委托给accounts[3]
    # print("voting_voter-->", voting.voters(voting_voter))
    voter2 = voting.voters(voting_voter)  # 执行委托操作后，voter2和voter3的值有变化，需要重新赋值
    voter3 = voting.voters(voting_delegate)
    assert voter2[1] is True
    assert voter3[0] == 2


# 投票
def test_vote(voting, voting_voter1, proposal1):
    assert voting.voters(voting_voter1)[0] >= 1  # 选民有投票权
    assert voting.voters(voting_voter1)[1] is False  # 选民未投票
    proposal1_count = voting.proposals(proposal1)[1]  # 未投票前提案的总票数
    voting.vote(proposal1, {"from": voting_voter1})  # 选民voting_voter1投票

    assert voting.voters(voting_voter1)[1] is True  # 选民已投票
    assert voting.proposals(proposal1)[1] == proposal1_count + voting.voters(voting_voter1)[0]  # 提案proposal1的总投票数增加


# 获胜提案索引值
def test_winning_proposal(voting, proposal1):
    # name = voting.winnerName()
    # print("winningProposal-->", voting.winningProposal(), bytes.decode(name), voting.proposals(proposal1)[1])
    assert voting.winningProposal() == 0  # 提案列表中仅有一个提案
    assert voting.proposals(proposal1)[1] == 1  # proposal1提案有一票


# 获胜提案的名称
def test_winner_name(voting):
    name = bytes.decode(voting.winnerName()[-3:])
    assert name == "foo"
