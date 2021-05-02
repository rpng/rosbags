==================
Contribution guide
==================

Thank you for considering to contribute to rosbags. Below is information on how to report issues and submit your contributions to rosbags.


Rights to and license of contributions
======================================

Rosbags is licensed under `Apache 2.0`_. Your submission of an issue, merge request, comment, or code to us is:

1. If your employer has rights in your contributions, your representation that your employer has authorized you to enter into this agreement on its behalf;

2. Your agreement, or your employer's agreement, with the terms and conditions in this document;

3. Your signature of the `Developer Certificate of Origin`_; and

4. Your grant of a license to your contributions under `Apache 2.0`_.


Contributing code / merge requests
==================================

In order to contribute code there are a few noteworthy things:

1. Especially for non-trivial contributions, please **submit an issue first** to discuss your ideas.

2. If your merge requests relates to an existing issue, please reference it from your merge request.

3. When creating a merge request, please `allow collaboration`_. This enables us to make small adjustments and rebase the branch as needed. Please use dedicated branches for your merge request and don't give us access to a branch that is dear to you.

4. Stick to *The seven rules of a great Git commit message* (see below).

5. We require you to **sign-off your commits** (see below). Your sign-off indicates that you agreed to the terms and conditions laid out in this document, if applicable on behalf of your employer.

.. _allow collaboration:
   https://docs.gitlab.com/ee/user/project/merge_requests/allow_collaboration.html


The seven rules of a great Git commit message
---------------------------------------------

We like `The seven rules of a great Git commit message`_, summarized here for completeness, follow links for further reading.

1. `Separate subject from body with a blank line <https://chris.beams.io/posts/git-commit/#separate>`_

2. `Limit the subject line to 50 characters <https://chris.beams.io/posts/git-commit/#limit-50>`_ (soft-limit 50, hard-limit 72)

3. `Start subject line with uppercase letter <https://chris.beams.io/posts/git-commit/#capitalize>`_

4. `Do not end the subject line with a period <https://chris.beams.io/posts/git-commit/#end>`_

5. `Use the imperative mood in the subject line <https://chris.beams.io/posts/git-commit/#imperative>`_

6. `Wrap the body at 72 characters <https://chris.beams.io/posts/git-commit/#wrap-72>`_

7. `Use the body to explain what and why vs. how <https://chris.beams.io/posts/git-commit/#why-not-how>`_

.. _The seven rules of a great Git commit message: https://chris.beams.io/posts/git-commit/#seven-rules


Signing off a commit
--------------------

You sign off a commit by adding a line like the following to the bottom of its commit message, separated by an empty line.

::

   Signed-off-by: Fullname <email@example.net>

Make sure it reflects your real name and email address. Git does this automatically when using ``git commit -s``.

Except for the licenses granted herein, you reserve all right, title, and interest in and to your contributions.


.. _Apache 2.0: ./LICENSE.txt
.. _Developer Certificate of Origin: https://developercertificate.org/
