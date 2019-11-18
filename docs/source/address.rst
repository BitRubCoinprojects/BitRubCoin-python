Addresses and payment IDs
=========================

The first, original address of the wallet is usually known as the *master
address*. All others are just *subaddresses*, even if they represent a separate
account within the wallet.

Sumokoin addresses are base58-encoded strings.

While the ordinary string representation is perfectly valid to use, you may
want to use validation and other features provided by the ``sumokoin.address``
package.


Address validation and instantiation
------------------------------------

The function ``sumokoin.address.address()`` will recognize and validate Sumokoin
address, returning an instance that provides additional functionality.

The following example uses addresses from the wallet :doc:`we have generated in
the previous chapter <wallet>`.

Let's start with the master address:

.. code-block:: python

    In [1]: from sumokoin.address import address

    In [2]: a = address('Sumoo1QnfdRP3b3tTYAPvVaTWxrEyxYDGAJhFuxFEFSuPDurPn15XJpc9M2YVGcskb5HKSVWJNuuqY2yJBAY72VHaUH5SkChadz')

    In [3]: a.is_mainnet()
    Out[3]: True

    In [4]: a.spend_key()
    Out[4]: '011ba47b9083cbcbdcead9c18ec807056cf557a61b37a1a23995e88c1e84dc3bec'

    In [5]: a.view_key()
    Out[5]: '95345401d21c8ee93c11ec101998b2ef28e82540b98a3ed4e38d270cc81b1777'

    In [6]: type(a)
    Out[6]: sumokoin.address.Address

We may use a subaddress too:

.. code-block:: python

    In [7]: b = address('SuboDemZvQS8LhzXkCse7aPTXaGRufnpMAueo2faZDb78tSRvhyQsxz4fAkkBY4SkZZ5HQpgFtsGa6N8adHZ9D7K21gG3L4VPu')

    In [8]: b.is_testnet()
    Out[8]: False

    In [9]: type(b)
    Out[9]: sumokoin.address.SubAddress

These two classes, ``Address`` and ``SubAddress`` have similar functionality
but one significant difference. Only the former may form *integrated address*.

Generating subaddresses
-----------------------

It is possible to get subaddresses in two ways:

 1. Creating them in the wallet file by calling ``.new_address()`` on ``Account`` or ``Wallet``
    instance.  In properly synced wallet this will return an address that is guaranteed to be fresh
    and unused.  It is the right way if you plan to use one-time addresses to identify payments or
    to improve your privacy by avoiding address reuse.
 2. Requesting arbitrary subaddress by calling ``Wallet.get_address(major, minor)`` where ``major``
    is the account index and ``minor`` is the index of the address within an account. Addresses
    obtained this way are not guaranteed to be fresh and **will not be saved as already generated
    within the wallet file**. (Watch out for unintentional address reuse!)

Payment IDs and integrated addresses
------------------------------------

Each Sumokoin transaction may carry a **payment ID**. It is a 64 or 256-bit long
number that carries additional information between parties. For example, a
merchant can generate a payment ID for each order, or an exchange can assign
one to each user. The customer/user would then attach the ID to the transaction,
so the site operator would know what is the purpose of incoming payment.

A short, 64-bit payment ID can be integrated into an address, creating, well...
an **integrated address**.

.. code-block:: python

    In [10]: ia = a.with_payment_id(0xfeedbadbeef)

    In [11]: ia
    Out[11]: SumipBg1kMDP3b3tTYAPvVaTWxrEyxYDGAJhFuxFEFSuPDurPn15XJpc9M2YVGcskb5HKSVWJNuuqY2yJBAY72VHaUH5SfQzTz5dkACFzBUUZs

    In [12]: ia.base_address()
    Out[12]: Sumoo1QnfdRP3b3tTYAPvVaTWxrEyxYDGAJhFuxFEFSuPDurPn15XJpc9M2YVGcskb5HKSVWJNuuqY2yJBAY72VHaUH5SkChadz

    In [13]: ia.base_address() == a
    Out[13]: True

    In [14]: ia.payment_id()
    Out[14]: 00000feedbadbeef


Since subaddresses have been introduced, merchants may generate a separate
address for each order, user or any other object they expect the payments
coming to. Therefore, it has been decided that `subaddresses cannot generate
integrated addresses`_.

.. _`subaddresses cannot generate integrated addresses`: https://monero.stackexchange.com/questions/6606/how-to-make-an-integrated-address-based-on-a-subaddress

.. code-block:: python

    In [15]: b.with_payment_id(0xfeedbadbeef)
    ---------------------------------------------------------------------------
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "sumokoin\address.py", line 170, in with_payment_id
        raise TypeError("SubAddress cannot be integrated with payment ID")
    TypeError: SubAddress cannot be integrated with payment ID

The ``sumokoin.numbers.PaymentID`` class validates payment IDs. It accepts both
integer and hexadecimal string representations.

.. code-block:: python

    In [16]: from sumokoin.numbers import PaymentID

    In [17]: p1 = PaymentID(0xfeedbadbeef)

    In [18]: p2 = PaymentID('feedbadbeef')

    In [19]: p1 == p2
    Out[19]: True

    In [20]: p1.is_short()
    Out[20]: True

    In [21]: p3 = PaymentID('1234567890abcdef0')

    In [22]: p3
    Out[22]: 000000000000000000000000000000000000000000000001234567890abcdef0

    In [23]: p3.is_short()
    Out[23]: False

Long payment IDs cannot be integrated:

.. code-block:: python

    In [24]: a.with_payment_id(p3)
    ---------------------------------------------------------------------------
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "sumokoin\address.py", line 132, in with_payment_id
        raise TypeError("Payment ID {0} has more than 64 bits and cannot be integrated".format(payment_id))
    TypeError: Payment ID 000000000000000000000000000000000000000000000001234567890abcdef0 has more than 64 bits and cannot be integrated

API reference
-------------

.. automodule:: sumokoin.address
   :members:
