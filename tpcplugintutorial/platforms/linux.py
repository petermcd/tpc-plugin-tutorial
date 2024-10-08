"""Module to handle verifying and changing passwords for Linux."""
from tpcplugintutorial.platforms.base_platform import BasePlatform


class Linux(BasePlatform):
    """Module to support managing Linux boxes."""

    def changepass(self) -> None:
        """Handle the changepass process."""
        if not self._connection:
            # Added to satisfy myoy
            self._output_failure('We could not connect to the device.')

        response = self._connection.send_command_timing(  # type: ignore
            command_string=f'passwd {self.username}',
            strip_command=False,
            strip_prompt=False,
            last_read=2.0,
        )
        old_password_prompt = 'Current password'
        new_password_prompt = 'ew password'
        loop_count = 0
        while loop_count < 3:
            loop_count += 1
            if old_password_prompt in response:
                password_to_enter = self.password
            elif new_password_prompt in response:
                password_to_enter = self.new_password
            else:
                break
            response = self._connection.send_command_timing(  # type: ignore
                command_string=password_to_enter,
                strip_command=False,
                strip_prompt=False,
                last_read=2.0,
            )

        if 'passwd: password updated successfully' in response:
            self._output_success('password updated successfully.')
        self._output_failure('Failed to change password.')

    def reconcilepass(self) -> None:
        """Handle the reconcilepass process."""
        if not self._connection:
            # Added to satisfy myoy
            self._output_failure('We could not connect to the device.')

        response = self._connection.send_command_timing(  # type: ignore
            command_string=f'passwd {self.local_username}',
            strip_command=False,
            strip_prompt=False,
            last_read=2.0,
        )
        old_password_prompt = 'Current password'
        new_password_prompt = 'ew password'
        loop_count = 0
        while loop_count < 3:
            loop_count += 1
            if old_password_prompt in response:
                password_to_enter = self.password
            elif new_password_prompt in response:
                password_to_enter = self.new_password
            else:
                break
            response = self._connection.send_command_timing(  # type: ignore
                command_string=password_to_enter,
                strip_command=False,
                strip_prompt=False,
                last_read=2.0,
            )

        if 'passwd: password updated successfully' in response:
            self._output_success('password updated successfully.')

        self._output_failure('Failed to change password.')

    @property
    def device_type(self) -> str:
        """
        Property to return the Netmiko device type.

        Returns:
             Linux
        """
        return 'linux'
