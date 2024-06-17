from token_group import TokenGroup
from address_constants import *

class TokenGroupFactory:
    @staticmethod
    def etherfi_eETH_Jun():
        return TokenGroup("etherfi_eETH_Jun", ETHERIUM_CHAIN_ID, eETH_UNDERLYING_ADDRESS, etherfi_eETH_Jun_PT_ADDRESS, etherfi_eETH_Jun_YT_ADDRESS)

    @staticmethod
    def etherfi_eETH_Sep():
        return TokenGroup("etherfi_eETH_Sep", ETHERIUM_CHAIN_ID, eETH_UNDERLYING_ADDRESS, etherfi_eETH_Sep_PT_ADDRESS, etherfi_eETH_Sep_YT_ADDRESS)

    @staticmethod
    def etherfi_eETH_Dec():
        return TokenGroup("etherfi_eETH_Dec", ETHERIUM_CHAIN_ID, eETH_UNDERLYING_ADDRESS, etherfi_eETH_Dec_PT_ADDRESS, etherfi_eETH_Dec_YT_ADDRESS)

    @staticmethod
    def zircuit_eETH_Jun():
        return TokenGroup("zircuit_eETH_Jun", ETHERIUM_CHAIN_ID, eETH_UNDERLYING_ADDRESS, zircuit_eETH_Jun_PT_ADDRESS, zircuit_eETH_Jun_YT_ADDRESS)

    @staticmethod
    def ezETH_Sep():
        return TokenGroup("ezETH_Sep", ETHERIUM_CHAIN_ID, ezETH_UNDERLYING_ADDRESS, ezETH_Sep_PT_ADDRESS, ezETH_Sep_YT_ADDRESS)

    @staticmethod
    def ezETH_Dec():
        return TokenGroup("ezETH_Dec", ETHERIUM_CHAIN_ID, ezETH_UNDERLYING_ADDRESS, ezETH_Dec_PT_ADDRESS, ezETH_Dec_YT_ADDRESS)

    @staticmethod
    def pufETH_Jun():
        return TokenGroup("pufETH_Jun", ETHERIUM_CHAIN_ID, pufETH_UNDERLYING_ADDRESS, pufETH_Jun_PT_ADDRESS, pufETH_Jun_YT_ADDRESS)

    @staticmethod
    def pufETH_Sep():
        return TokenGroup("pufETH_Sep", ETHERIUM_CHAIN_ID, pufETH_UNDERLYING_ADDRESS, pufETH_Sep_PT_ADDRESS, pufETH_Sep_YT_ADDRESS)

    @staticmethod
    def uniETH_Jun():
        return TokenGroup("uniETH_Jun", ETHERIUM_CHAIN_ID, uniETH_UNDERLYING_ADDRESS, uniETH_Jun_PT_ADDRESS, uniETH_Jun_YT_ADDRESS)

    @staticmethod
    def uniETH_Sep():
        return TokenGroup("uniETH_Sep", ETHERIUM_CHAIN_ID, uniETH_UNDERLYING_ADDRESS, uniETH_Sep_PT_ADDRESS, uniETH_Sep_YT_ADDRESS)



