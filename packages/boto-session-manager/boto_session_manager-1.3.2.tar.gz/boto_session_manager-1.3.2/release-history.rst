.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add refreshable session support
- use ``boto3-stubs`` to provide type hint and auto complete

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.3.2 (2022-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- allow to call :meth:`~boto_session_manager.manager.BotoSesManager.clear_cache()`` to clear all cached boto session and client.
- add ton's of property method to access the cached boto client.
- update the list of AWS service to the latest (as of 2022-12-10), which are 333 services.


1.2.2 (2022-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- now ``boto_session_manager`` doesn't force to install ``boto3`` when installing itself. You have to manage your ``boto3`` installation separately.


1.2.1 (2022-11-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add :meth:`~boto_session_manager.manager.BotoSesManager.awscli` context manager to pass boto session credential to AWS CLI.


1.1.1 (2022-11-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- the first API stable version

**Minor Improvements**

- add ``delta`` arguments for :meth:`~boto_session_manager.manager.BotoSesManager.is_expired` method. allow to check if the session will expire in X seconds.


0.0.4 (2022-05-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``default_client_kwargs`` argument for :class:`boto_session_manager.manager.BotoSesManager`.

**Miscellaneous**

- use `localstack <https://localstack.cloud/>`_ for unit test.


0.0.3 (2022-05-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add additional keyword arguments for :meth:`boto_session_manager.manager.BotoSesManager.get_client` method

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.2 (2022-04-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- now :class:`boto_session_manager.manager.BotoSesManager`
- add :meth:`boto_session_manager.manager.BotoSesManager.get_resource` method


0.0.1 (2022-04-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add :class:`boto_session_manager.manager.BotoSessionManager` class
- Add :class:`boto_session_manager.services.BotoSessionManager` class
