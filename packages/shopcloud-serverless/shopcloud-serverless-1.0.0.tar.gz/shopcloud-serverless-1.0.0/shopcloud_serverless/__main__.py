import argparse
import sys

from . import cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Serverless',
        prog='shopcloud-serverless'
    )

    subparsers = parser.add_subparsers(help='commands', title='commands')
    parser.add_argument('--debug', '-d', help='Debug', action='store_true')
    parser.add_argument('--simulate', '-s', help='Simulate the process', action='store_true')
    parser.add_argument('--secrethub-token', help='Secrethub-Token', type=str)

    parser_init = subparsers.add_parser('init', help='init the eventbus')
    parser_init.add_argument('--base-dir', help='Base directory', type=str)
    parser_init.add_argument('--api-title', help='API title', type=str)
    parser_init.add_argument('--api-description', help='API description', type=str)
    parser_init.add_argument('--gcp-project', help='Google cloud project id', type=str)
    parser_init.add_argument('--gcp-region', help='Google cloud region', type=str)
    parser_init.set_defaults(which='init')

    parser_service = subparsers.add_parser('services', help='services')
    parser_service.add_argument(
        'action',
        const='generate',
        nargs='?',
        choices=['list', 'create', 'describe', 'deploy']
    )
    parser_service.add_argument('service', const='generate', nargs='?')
    parser_service.set_defaults(which='services')

    parser_gateway = subparsers.add_parser('gateway', help='api gateway')
    parser_gateway.add_argument(
        'action',
        const='generate',
        nargs='?',
        choices=['init', 'deploy']
    )
    parser_gateway.set_defaults(which='gateway')


    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    rc = cli.main(args)
    if rc != 0:
        sys.exit(rc)
