from crypto_token import CryptoToken

class TokenGroup:
    def __init__(self, token_name: str, chain_id: int, underlying_address: str, pt_address: str, yt_address: str):
        self.chain_id = chain_id
        self.underlying_token = CryptoToken(token_name, underlying_address)
        self.pt_token = CryptoToken(f"{token_name}_pt", pt_address)
        self.yt_token = CryptoToken(f"{token_name}_yt", yt_address)
