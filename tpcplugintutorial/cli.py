"""Entry point for tpcplugintututorial."""
import argparse
import ipaddress

from tpcplugintutorial import platforms


def arguments():
    """Configure application arguments."""
    parser = argparse.ArgumentParser(
                        prog='TPC Plugin Tutorial',
                        description='Demo application to verify and change credentials on devices',
    )
    parser.add_argument('--ip', action='store', required=True,)
    parser.add_argument('--device-type', action='store', required=True,)
    parser.add_argument(
        '--action',
        choices=['logon', 'verifypass', 'changepass', 'prereconcilepass', 'reconcilepass'],
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the application."""
    args = arguments()
    try:
        if hasattr(platforms, args.device_type):
            ip = ipaddress.ip_address(args.ip)
            platform = getattr(platforms, args.device_type)(ip=ip)
            getattr(platform, args.action)()
            return
    except TypeError:
        # Fall through as this may happen if the platform is in the wrong case.
        pass
    print('Platform not supported')
    exit(1)


if __name__ == '__main__':
    main()
