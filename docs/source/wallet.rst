Using wallet and accounts
=========================

Since ``Sumokoin 'Sapporo' (0.2.x)`` the wallet handles accounts and deterministically
generated addresses, known as *subaddresses*.

The wallet
----------

The following example shows how to create and retrieve wallet's accounts and
addresses:

.. code-block:: python

    In [1]: from sumokoin.wallet import Wallet

    In [2]: from sumokoin.backends.jsonrpc import JSONRPCWallet

    In [3]: w = Wallet(JSONRPCWallet(port=29738))

    In [4]: w.address()
    Out[4]: Sutoe7aoJy357oxqg5E1nDQa3PFybMxk2EnCnwqvyXhaBJtGe4q7QHLAXmu81AfUTEhTy4ogDsFVMD4BFkKLcCWCRNi4ZyD7RH1

Accounts and subaddresses
-------------------------

The accounts are stored in wallet's ``accounts`` attribute, which is a list.

Regardless of the version, **the wallet by default operates on its account of
index 0**, which makes it consistent with the behavior of the CLI wallet
client.

.. code-block:: python

    In [5]: len(w.accounts)
    Out[5]: 1

    In [6]: w.accounts[0]
    Out[6]: <sumokoin.account.Account at 0x7f78992d6898>

    In [7]: w.accounts[0].address()
    Out[7]: Sutoe7aoJy357oxqg5E1nDQa3PFybMxk2EnCnwqvyXhaBJtGe4q7QHLAXmu81AfUTEhTy4ogDsFVMD4BFkKLcCWCRNi4ZyD7RH1

    In [8]: w.addresses()
    Out[8]: [Sutoe7aoJy357oxqg5E1nDQa3PFybMxk2EnCnwqvyXhaBJtGe4q7QHLAXmu81AfUTEhTy4ogDsFVMD4BFkKLcCWCRNi4ZyD7RH1]


Creating accounts and addresses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every wallet can have separate accounts and each account can have numerous
addresses. The ``Wallet.new_account()`` and ``Account.new_address()`` will
create new instances, then return a tuple consisting of the subaddress itself,
and the subaddress index within the account.

.. code-block:: python

    In [9]: w.new_address()
    Out[9]: (SusumFvtVvh9VRypBRppHXbvGUEQUZeaFbFLPjHroeWHVs2Tkb4t5W6Kd9Vw5ooqZg6S9Gk6dErr61VYCkkvdnko9cMag1JPy6, 1)

    In [10]: w.addresses()
    Out[10]:
    [Sutoe7aoJy357oxqg5E1nDQa3PFybMxk2EnCnwqvyXhaBJtGe4q7QHLAXmu81AfUTEhTy4ogDsFVMD4BFkKLcCWCRNi4ZyD7RH1,
     SusumFvtVvh9VRypBRppHXbvGUEQUZeaFbFLPjHroeWHVs2Tkb4t5W6Kd9Vw5ooqZg6S9Gk6dErr61VYCkkvdnko9cMag1JPy6]

    In [11]: w.new_account()
    Out[11]: <sumokoin.account.Account at 0x7f7894dffbe0>

    In [12]: len(w.accounts)
    Out[12]: 2

    In [13]: w.accounts[1].address()
    Out[13]: SusuhHD9wkV7ZChCYv4gMu6Jw5NeZoAdFC9hTB3vSg8XYoceAbcMR936T18ZXSK97BAmSUsU9L5BH4Uhw35bt7ro7z3QVLeSdT

    In [14]: w.accounts[1].new_address()
    Out[14]: (SusuekQ5hoL7iQwaMEsWW7RTFo6K2muCnPpCk5Z1SAHsCGsWBe1zEPJ1VGeFHmrFKSZcBPsmSLARJbBry1cA3d6w8kZuREUAiC, 1)

    In [15]: w.accounts[1].addresses()
    Out[15]:
    [SusuhHD9wkV7ZChCYv4gMu6Jw5NeZoAdFC9hTB3vSg8XYoceAbcMR936T18ZXSK97BAmSUsU9L5BH4Uhw35bt7ro7z3QVLeSdT,
     SusuekQ5hoL7iQwaMEsWW7RTFo6K2muCnPpCk5Z1SAHsCGsWBe1zEPJ1VGeFHmrFKSZcBPsmSLARJbBry1cA3d6w8kZuREUAiC]


As mentioned above, the wallet by default operates on the first account, so
``w.new_address()`` is equivalent to ``w.accounts[0].new_address()``.

In the next chapter we will :doc:`learn about addresses <address>`.

API reference
-------------

.. automodule:: sumokoin.wallet
   :members:

.. automodule:: sumokoin.account
   :members:
