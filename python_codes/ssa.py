from secretsharing import SecretSharer

def split_secret(secret: str, total_shares: int, threshold: int) -> list:
    """
    Splits a secret into `total_shares` using Shamir's Secret Sharing algorithm.
    Any `threshold` number of shares can reconstruct the secret.

    Args:
        secret (str): The secret string to split.
        total_shares (int): Total number of shares to generate.
        threshold (int): Minimum number of shares needed to reconstruct the secret.

    Returns:
        list: A list of secret shares.
    """
    return SecretSharer.split_secret(secret, threshold, total_shares)

def recover_secret(shares: list) -> str:
    """
    Recovers the original secret from the given shares.

    Args:
        shares (list): A list of valid shares (minimum threshold required).

    Returns:
        str: The original secret.
    """
    return SecretSharer.recover_secret(shares)
