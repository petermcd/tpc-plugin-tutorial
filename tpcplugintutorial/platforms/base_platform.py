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
        self._username: str = ''
        self._password: str = ''
        self._new_password: str = ''
        self._connection: BaseConnection | None = None
        self._connect(ip=ip)

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

    @abstractmethod
    def changepass(self) -> None:
        """Abstract method for the changepass process."""

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

    @abstractmethod
    def prereconcile(self) -> None:
        """Abstract method for the prereconcile process."""

    @abstractmethod
    def reconcile(self) -> None:
        """Abstract method for the reconcile process."""

    @abstractmethod
    def verifypass(self) -> None:
        """Abstract method for the verifypass process."""

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
