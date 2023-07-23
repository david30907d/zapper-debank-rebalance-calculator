from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS

from rebalance_server.main import main

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


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/addresses", methods=["GET"])
@cache.cached(timeout=300)
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
