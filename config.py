import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # Database settings
    DB_NAME: str = "alerts.db"

    # Price checker settings
    CHECK_INTERVAL: int = 30  # seconds
    PRICE_CACHE_TIME: int = 30  # seconds

    # Alert settings
    MAX_ALERTS_PER_USER: int = 1000
    MIN_PRICE: float = 0.000001
    MAX_PRICE: float = 1000000000

    SYMBOL_PRIORITY_MAP = {
        # Top Market Cap Coins (Verified December 2023)
        "btc": "bitcoin",
        "eth": "ethereum",
        "usdt": "tether",
        "bnb": "binancecoin",
        "sol": "solana",
        "xrp": "ripple",
        "usdc": "usd-coin",
        "steth": "staked-ether",
        "ada": "cardano",
        "avax": "avalanche-2",
        "doge": "dogecoin",
        "dot": "polkadot",
        "trx": "tron",
        "matic": "matic-network",
        "link": "chainlink",
        "wbtc": "wrapped-bitcoin",
        "ton": "the-open-network",
        "dai": "dai",
        "etc": "ethereum-classic",
        "ltc": "litecoin",
        "bch": "bitcoin-cash",
        "icp": "internet-computer",
        "atom": "cosmos",
        "uni": "uniswap",
        "hbar": "hedera-hashgraph",
        "fil": "filecoin",
        "ldo": "lido-dao",
        "near": "near",
        "inj": "injective-protocol",
        "apt": "aptos",
        "arb": "arbitrum",
        "stx": "blockstack",
        "op": "optimism",
        "sui": "sui",
        "mkr": "maker",
        "aave": "aave",
        "egld": "multiversx-egld",
        "rpl": "rocket-pool",
        "kcs": "kucoin-shares",
        "fsn": "fsn",
        "comp": "compound-governance-token",
        "snx": "synthetix-network-token",
        "crv": "curve-dao-token",
        "grt": "the-graph",
        "imx": "immutable-x",
        "mana": "decentraland",
        "chz": "chiliz",
        "rndr": "render-token",
        "kava": "kava",
        "blur": "blur",
        "cake": "pancakeswap-token",
        "sand": "the-sandbox",
        "mina": "mina-protocol",
        "ftm": "fantom",
        "neo": "neo",
        "cfx": "conflux-token",
        "pepe": "pepe",
        "wld": "worldcoin-org",
        "gmx": "gmx",
        "kas": "kaspa",
        "sei": "sei-network",
        "pyth": "pyth-network",

        # Stablecoins
        "busd": "binance-usd",
        "tusd": "true-usd",
        "usdd": "usdd",
        "usdp": "paxos-standard",
        "gusd": "gemini-dollar",
        "lusd": "liquity-usd",
        "cusd": "celo-dollar",
        "frax": "frax",
        "mai": "mai",
        "susd": "nusd",

        # DeFi & DEX Tokens
        "sushi": "sushi",
        "yfi": "yearn-finance",
        "1inch": "1inch",
        "bal": "balancer",
        "dydx": "dydx",

        # Exchange Tokens
        "mnt": "mantle",
        "bgb": "bitget-token",
        "okb": "okb",
        "gt": "gatetoken",
        "ht": "huobi-token",
        "ftx": "ftx-token",

        # Gaming & Metaverse
        "axs": "axie-infinity",
        "gala": "gala",
        "enj": "enjincoin",
        "theta": "theta-token",
        "magic": "magic",

        # Layer 2 & Scaling
        "metis": "metis-token",
        "zks": "zksync-io",

        # Privacy Focused
        "xmr": "monero",
        "zec": "zcash",
        "scrt": "secret",

        # Infrastructure & Oracle
        "api3": "api3",
        "band": "band-protocol",
        "glm": "golem",
        "storj": "storj",
        "ar": "arweave",

        # Misc Notable Projects
        "vet": "vechain",
        "waves": "waves",
        "xem": "nem",
        "bat": "basic-attention-token",
        "one": "harmony",
        "zen": "horizen",
        "iota": "iota",
        "dash": "dash",
        "dcr": "decred",
        "zil": "zilliqa",
        "qtum": "qtum",
        "sc": "siacoin",
        "xdc": "xdce-crowd-sale",
        "rose": "oasis-network",
    }


config = Config()