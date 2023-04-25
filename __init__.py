from flask import Flask, jsonify

from rebalance_server.main import main

app = Flask(__name__)


@app.route("/")
def get_suggestions():
    response = main(
        defi_portfolio_service_name="debank",
        optimize_apr_mode="new_pool",
        strategy_name="all_weather_portfolio",
    )
    return jsonify(response)
