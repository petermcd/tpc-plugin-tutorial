"""Module to provide shared behaviour for the platforms."""
from abc import abstractmethod
from getpass import getpass
from ipaddress import IPv4Address, IPv6Address

from netmiko import (BaseConnection, ConnectHandler,
                     NetmikoAuthenticationException, NetmikoTimeoutException)


class BasePlatform(object):
    """Module to support base functionality."""

    __slots__ = (
        '_connection',
        '_local_username',
        '_new_password',
        '_password',
        '_username',
    )

    def __init__(self, ip: IPv4Address | IPv6Address) -> None:
        """
        Init to set up BasePlatform.

        Args:
            ip (IPv4Address | IPv6Address): IP address of the device to connect too.
        """
        self._local_username: str = ''
        self._new_password: str = ''
        self._username: str = ''
        self._password: str = ''
        self._connection: BaseConnection | None = None
        self._connect(ip=ip)

    @abstractmethod
    def changepass(self) -> None:
        """Abstract method for the changepass process."""

    def logon(self) -> None:
        """Handle the logon process."""
        self.verifypass()

    def prereconcilepass(self) -> None:
        """
        Handle the prereconcilepass process.

        The prereconcilepass process matches the verify process but should log in with an alternate account.
        """
        self.verifypass()

    @abstractmethod
    def reconcilepass(self) -> None:
        """Abstract method for the reconcilepass process."""

    def verifypass(self) -> None:
        """Handle the verifypass process."""
        if not self._connection:
            # Added to satisfy myoy
            self._output_failure('We could not connect to the device.')

        if self._connection.is_alive():  # type: ignore
            self._output_success('verification successful')

        self._output_failure('We could not connect to the device.')

    def _connect(self, ip: IPv4Address | IPv6Address) -> None:
        """
        Connect to the device with the given IP.

        Args:
            ip (IPv4Address | IPv6Address): IP address of the device to connect too.
        """
        try:
            self._connection = ConnectHandler(
                device_type=self.device_type,
                host=str(ip),
                username=self.username,
                password=self.password,
            )
        except KeyboardInterrupt:
            # Capture someone cancelling the input, this should not happen in the real world.
            self._output_failure('We did not receive the required credentials to log in.')
        except NetmikoTimeoutException:
            # Handle inability to connect due to timeouts.
            self._output_failure('We could not connect to the device.')
        except NetmikoAuthenticationException:
            # Handle inability to connect due to authentication issues.
            self._output_failure('We could not log into the device.')
        except Exception:
            # Handle every other exception.
            self._output_failure('We could not connect to the device.')

    def _output_failure(self, message: str):
        """
        Handle outputting failure messages to the screen.

        Results in exit(1).

        Args:
            message: The message to output.
        """
        if self._connection and self._connection.is_alive():
            self._connection.disconnect()

        print(message)
        exit(1)

    def _output_success(self, message: str):
        """
        Handle outputting success messages to the screen.

        Results in exit(0).

        Args:
            message: The message to output.
        """
        if self._connection and self._connection.is_alive():
            self._connection.disconnect()

        print(message)
        exit(0)

    @property
    @abstractmethod
    def device_type(self) -> str:
        """
        Abstract property to provide functionality for fetching the Netmiko device type.

        Raises:
            NotImplementedError: On failure to override this property.
        """
        raise NotImplementedError("device_type needs to be declared in the platform type class.")

    @property
    def local_username(self) -> str:
        """
        Property for the new password.

        If the new password has not been retrieved yet, it will prompt for it, otherwise it will return what
        it already has.

        Returns:
            new password as a string.
        """
        if not self._local_username:
            self._local_username = input('Enter the local username: ')
        return self._local_username

    @property
    def new_password(self) -> str:
        """
        Property for the new password.

        If the new password has not been retrieved yet, it will prompt for it, otherwise it will return what
        it already has.

        Returns:
            new password as a string.
        """
        if not self._new_password:
            self._new_password = getpass('Enter your desired new password: ')
        return self._new_password

    @property
    def password(self) -> str:
        """
        Property for the password.

        If the password has not been retrieved yet, it will prompt for it, otherwise it will return what
        it already has.

        Returns:
            password as a string.
        """
        if not self._password:
            self._password = getpass('Enter your password: ')
        return self._password

    @property
    def username(self) -> str:
        """
        Property for the username.

        If the username has not been retrieved yet, it will prompt for it, otherwise it will return what
        it already has.

        Returns:
            username as a string.
        """
        if not self._username:
            self._username = input('Enter your username: ')
        return self._username
