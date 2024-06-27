from token_group_factory import TokenGroupFactory
from token_group import TokenGroup
from pendle_api import PendleAPI

class DataFetcher:
    @staticmethod
    def fetch_token_group_data(token_group: TokenGroup):
        PendleAPI.fetch_and_save_ohlcv_data_daily(token_group.pt_token.token_name, token_group.pt_token.token_address, token_group.chain_id)
        PendleAPI.fetch_and_save_ohlcv_data_daily(token_group.yt_token.token_name, token_group.yt_token.token_address, token_group.chain_id)

def main():
    # Define a list of tuples containing the factory method and its corresponding maturity
    token_group_factories = [
        (TokenGroupFactory.etherfi_eETH_Jun, "Jun"),
        (TokenGroupFactory.etherfi_eETH_Sep, "Sep"),
        (TokenGroupFactory.etherfi_eETH_Dec, "Dec"),
        (TokenGroupFactory.zircuit_eETH_Jun, "Jun"),
        (TokenGroupFactory.ezETH_Sep, "Sep"),
        (TokenGroupFactory.ezETH_Dec, "Dec"),
        (TokenGroupFactory.pufETH_Jun, "Jun"),
        (TokenGroupFactory.pufETH_Sep, "Sep"),
        (TokenGroupFactory.uniETH_Jun, "Jun"),
        (TokenGroupFactory.uniETH_Sep, "Sep"),
        (TokenGroupFactory.rsETH_Jun, "Jun"),
        (TokenGroupFactory.rsETH_Sep, "Sep")
    ]

    # Iterate over the list and perform operations
    for factory, maturity in token_group_factories:
        token_group = factory()
        print(token_group.underlying_token.token_name)
        DataFetcher.fetch_token_group_data(token_group)

if __name__ == '__main__':
    main()
