import numpy as np
import pandas as pd

from rebalance_server.apr_utils.apr_calculator import get_lowest_or_default_apr
from rebalance_server.metrics.historical_price_reader import get_historical_price_reader
from rebalance_server.metrics.lp_token import calculate_daily_return_per_lp_token
from rebalance_server.metrics.utils import DAY_TIMEDELTA


def calculate_performance_related_metrics(
    categorized_positions_with_token_balance: dict,
) -> float:
    """Calculate the Sharpe ratio of a portfolio.

    Args:
        categorized_positions (dict): A dictionary of categorized_positions in the portfolio. The keys are
            the ticker symbols and the values are the token balance.
        risk_free_rate (float, optional): The risk free rate of return. Defaults
            to 0.041, which is the APR of Lido

    Returns:
        float: The Sharpe ratio of the portfolio.
    """
    daily_return_percentages, roi_metadatas = _get_daily_return_percentage_array(
        categorized_positions_with_token_balance
    )
    return {
        "sharpe_ratio": _calculate_sharpe_ratio(daily_return_percentages),
        "ROI": _calcualte_ROI(roi_metadatas),
    }


def _get_daily_return_percentage_array(
    categorized_positions_with_token_balance: dict,
) -> pd.Series:
    series = pd.Series(dtype=float)
    historical_price_reader = get_historical_price_reader(source="coingecko")

    series_of_lp_tokens: list[tuple] = []
    shortest_series_length = float("inf")
    for (
        addr_project_symbol,
        lp_token,
    ) in categorized_positions_with_token_balance.items():
        daily_return_per_lp_token: pd.Series = calculate_daily_return_per_lp_token(
            lp_token, historical_price_reader
        )
        series_of_lp_tokens.append((addr_project_symbol, daily_return_per_lp_token))
        if daily_return_per_lp_token.size < shortest_series_length:
            shortest_series_length = daily_return_per_lp_token.size

    array_of_roi_for_each_position = []
    for addr_project_symbol, lp_token_series in series_of_lp_tokens:
        lp_token_series.drop(
            lp_token_series.tail(len(lp_token_series) - shortest_series_length).index,
            inplace=True,
        )
        # [TODO](david): need to figure out why `reversed_lp_token_series = lp_token_series[::-1]` doesn't work
        reversed_lp_token_series = pd.Series(list(lp_token_series)[::-1])

        array_of_roi_for_each_position.append(
            {
                "symbol": addr_project_symbol.split(":")[-1],
                "initial_value_of_investment": reversed_lp_token_series[0],
                "current_value_of_investment": reversed_lp_token_series[
                    len(reversed_lp_token_series) - 1
                ],
                "days": len(reversed_lp_token_series),
            }
        )
        # daily_return_percentages_with_farm_reward_per_lp_token = _add_farm_reward(
        #     addr_project_symbol, daily_return_percentages_per_lp_token
        # )
        daily_return_percentages_per_lp_token = (
            _calculate_daily_return_percentages_per_lp_token(reversed_lp_token_series)
        )
        if series.empty:
            series = daily_return_percentages_per_lp_token
        else:
            series = series.add(daily_return_percentages_per_lp_token).dropna()
    return series, array_of_roi_for_each_position


def _calculate_daily_return_percentages_per_lp_token(price_pd: pd.Series):
    return price_pd.pct_change()


def _add_farm_reward(
    addr_project_symbol: str, daily_return_percentages_per_lp_token: pd.Series
):
    splitted_data = addr_project_symbol.split(":")
    addr_with_metadata = ":".join(splitted_data[:-2])
    project, symbol = splitted_data[-2], splitted_data[-1]
    address_project = f"{addr_with_metadata}:{project}"
    project_symbol = f"{project}:{symbol}"
    apr = get_lowest_or_default_apr(project_symbol, address_project)
    return daily_return_percentages_per_lp_token * (1 + apr / 365)


def _calculate_sharpe_ratio(
    daily_return_percentages: pd.Series, risk_free_rate: float = 0.041
) -> float:
    # why multiply by sqrt(DAY_TIMEDELTA) ? Assumed that there's DAY_TIMEDELTA trading days. And since denomitor is daily's std. daily stuff is already under the effect of sqrt, so need to multply with sqrt(DAY_TIMEDELTA) to make it back to annualized
    return {
        "value": np.sqrt(DAY_TIMEDELTA)
        * (daily_return_percentages.mean() - risk_free_rate)
        / daily_return_percentages.std(),
        "days": len(daily_return_percentages),
    }


def _calcualte_ROI(roi_metadatas: list[dict]):
    result = {}
    total_current_value_of_investment = 0
    total_initial_value_of_investment = 0
    days = roi_metadatas[0]["days"]
    for metadata in roi_metadatas:
        # TODO(david): for now, we only support the same days for all positions. Will do more investigation on how to calculate the ROI for different days
        assert metadata["days"] == days
        result[metadata["symbol"]] = (
            (
                metadata["current_value_of_investment"]
                - metadata["initial_value_of_investment"]
            )
            / metadata["initial_value_of_investment"]
            / metadata["days"]
            * 365
        )
        total_current_value_of_investment += metadata["current_value_of_investment"]
        total_initial_value_of_investment += metadata["initial_value_of_investment"]
    result["total"] = (
        (total_current_value_of_investment - total_initial_value_of_investment)
        / total_initial_value_of_investment
        / days
        * 365
    )
    return result
