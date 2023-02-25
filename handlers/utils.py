import json
def mapping_table_checking_logic(
    address, asset, net_worth_of_position, categories, apr
):
    # my sentry logic
    if net_worth_of_position > 200 and (not categories or apr == 0):
        print(json.dumps(asset))
        raise Exception(
            f"Address {address} no category, need to update your ADDRESS_2_CATEGORY, or update its APR"
        )

