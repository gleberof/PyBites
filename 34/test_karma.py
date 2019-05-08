from karma import User, Transaction

alice = User('alice')
bob = User('bob')
tim = User('tim')

transactions = [
    Transaction(giver=alice, points=1),
    Transaction(giver=bob, points=2),
    Transaction(giver=tim, points=3),
    Transaction(giver=tim, points=4),
]


def test_init():
    assert alice.name == 'alice'
    assert bob.name == 'bob'
    assert alice._transactions == []
    assert bob._transactions == []


def test_adding_karma():
    bob + transactions[0]
    assert bob.karma == 1
    alice + transactions[1]
    assert alice.karma == 2
    bob + transactions[2]
    assert bob.karma == 4
    alice + transactions[3]
    assert alice.karma == 6


def test_upvotes_property():
    assert bob.points == [1, 3]
    assert alice.points == [2, 4]


def test_fans_property():
    assert tim.fans == 0
    assert bob.fans == 2
    assert alice.fans == 2


def test_str_dunder():
    assert str(tim) == 'tim has a karma of 0 and 0 fans'
    assert str(alice) == 'alice has a karma of 6 and 2 fans'
    assert str(bob) == 'bob has a karma of 4 and 2 fans'