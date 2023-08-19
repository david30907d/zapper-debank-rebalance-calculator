import os

import requests
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS

from rebalance_server.main import main
from rebalance_server.routes import (
    fetch_1inch_swap_data,
    get_APR_composition,
    get_debank_data,
)

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)
CORS(app, resources={r"*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})


def send_exception_to_discord(webhook_url):
    def decorator(func):
        # Set a unique name for the wrapper function
        # to avoid naming conflicts with other endpoints
        wrapper_name = f"{func.__name__}_decorated"

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Format the exception details as a message
                message = f"⚠️ Exception occurred in {func.__name__}: {str(e)}"

                # Create a JSON payload with the message
                payload = {"username": "Cloud Run", "content": message}

                # Send the message to the Discord webhook
                try:
                    response = requests.post(webhook_url, json=payload)
                    response.raise_for_status()
                except requests.exceptions.RequestException as re:
                    print(f"Error sending exception to Discord: {re}")
                else:
                    print("Exception sent to Discord successfully.")
                finally:
                    # Re-raise the exception to maintain the original behavior
                    raise e

        # Set the name of the wrapper function
        wrapper.__name__ = wrapper_name
        return wrapper

    return decorator


@app.route("/", methods=["GET"])
@send_exception_to_discord(webhook_url=os.getenv("DISCORD_WEBHOOK"))
def health():
    return "Healthy", 200


@app.route("/addresses", methods=["GET"])
@cache.cached(timeout=300)
@send_exception_to_discord(webhook_url=os.getenv("DISCORD_WEBHOOK"))
def get_suggestions():
    response = main(
        defi_portfolio_service_name="debank",
        optimize_apr_mode="new_pool",
        strategy_name="all_weather_portfolio",
        addresses=request.args.get("addresses").split(),
    )
    resp = jsonify(response)
    return resp


@app.route("/demo", methods=["GET"])
@cache.cached(timeout=300)
def get_demo():
    response = main(
        defi_portfolio_service_name="debank",
        optimize_apr_mode="new_pool",
        strategy_name="all_weather_portfolio",
        addresses=["demo"],
    )
    resp = jsonify(response)
    return resp


@app.route("/debank", methods=["GET"])
@cache.cached(timeout=300)
def debank():
    response = get_debank_data()
    resp = jsonify(response)
    return resp


@app.route("/apr_composition", methods=["GET"])
@cache.cached(timeout=300)
def apr_composition():
    response = get_APR_composition(1, "permanent_portfolio")
    resp = jsonify(response)
    return resp


@app.route("/one_1inch_swap_data", methods=["GET"])
@cache.cached(timeout=300)
def one_1inch_swap_data():
    chainId = request.args.get("chainId")
    fromTokenAddress = request.args.get("fromTokenAddress")
    toTokenAddress = request.args.get("toTokenAddress")
    amount = request.args.get("amount")
    fromAddress = request.args.get("fromAddress")
    slippage = request.args.get("slippage")
    response = fetch_1inch_swap_data(
        chainId, fromTokenAddress, toTokenAddress, amount, fromAddress, slippage
    )
    resp = jsonify(response)
    return resp
