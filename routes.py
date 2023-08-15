from rebalance_server.main import load_evm_raw_positions


def get_debank_data():
    evm_positions = load_evm_raw_positions(
        "debank", "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
    )
    token_metadata_table: dict[str, dict] = {}
    for position in evm_positions["data"]["result"]["data"]:
        for portfolio_item in position["portfolio_item_list"]:
            for token in portfolio_item["detail"].get(
                "reward_token_list", []
            ) + portfolio_item["detail"].get("supply_token_list", []):
                token_metadata_table[token["id"]] = {
                    "img": token["logo_url"],
                    "price": token["price"],
                    "symbol": token["symbol"],
                    "chain": token["chain"],
                }
    return token_metadata_table
