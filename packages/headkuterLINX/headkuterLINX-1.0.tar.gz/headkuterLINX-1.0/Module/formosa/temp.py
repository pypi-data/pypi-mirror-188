import argparse
import hvac
import os

def main():
    """
    The main program entry-point.
    """

    parser = argparse.ArgumentParser(__file__, __doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--vault-address",
        default=os.getenv("VAULT_ADDR"),
        help="The address of the Vault server."
    )
    parser.add_argument("--vault-token",
        default=os.getenv("VAULT_TOKEN"),
        help="The token for authentication to the Vault server."
    )
    parser.add_argument("--vault-path",
        required=True,
        help="The path of the target secret in Vault."
    )
    args = parser.parse_args()

    if not args.vault_address:
        parser.exit(status=1, message="Must specify address of Vault server using --vault-address argument or VAULT_ADDR environment variable.")

    if not args.vault_token:
        parser.exit(status=1, message="Must specify security token for Vault server using --vault-token argument or VAULT_TOKEN environment variable.")

    client = hvac.Client(args.vault_address, token=args.vault_token)
    secret = client.read(args.vault_path)
    if secret is None:
        parser.exit(status=2, message="Secret not found at '{}/{}'.".format(args.vault_address, args.vault_path))

    secret_data = secret["data"]
    for name, value in secret_data.items():
        # Escape symbols commonly used by Bash.
        value = value.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

        print('export TF_VAR_{}="{}"'.format(
            name,
            value
        ))

if __name__ == '__main__':
    main()
