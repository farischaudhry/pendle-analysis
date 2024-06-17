from token_group_factory import TokenGroupFactory
from token_group import TokenGroup
from pendle_api import PendleAPI

class DataFetcher:
    @staticmethod
    def fetch_token_group_data(token_group: TokenGroup):
        PendleAPI.fetch_and_save_ohlcv_data_daily(token_group.pt_token.token_name, token_group.pt_token.token_address, token_group.chain_id)
        PendleAPI.fetch_and_save_ohlcv_data_daily(token_group.yt_token.token_name, token_group.yt_token.token_address, token_group.chain_id)

def main():
    token_group = TokenGroupFactory.etherfi_eETH_Jun()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.etherfi_eETH_Sep()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.etherfi_eETH_Dec()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.zircuit_eETH_Jun()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.ezETH_Sep()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.ezETH_Dec()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.pufETH_Jun()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.pufETH_Sep()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.uniETH_Jun()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

    token_group = TokenGroupFactory.uniETH_Sep()
    print(token_group.underlying_token.token_name)
    DataFetcher.fetch_token_group_data(token_group)

if __name__ == '__main__':
    main()
