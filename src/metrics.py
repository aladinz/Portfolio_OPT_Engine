"""
Portfolio Metrics Module
Calculates various portfolio performance metrics.
"""

import numpy as np
import pandas as pd
from typing import Union, Tuple


class PortfolioMetrics:
    """
    Calculates portfolio performance and risk metrics.
    """
    
    @staticmethod
    def portfolio_return(weights: np.ndarray, mean_returns: np.ndarray) -> float:
        """
        Calculate expected portfolio return.
        
        Args:
            weights: Portfolio weights
            mean_returns: Mean returns for each asset
        
        Returns:
            Expected portfolio return
        """
        return np.sum(weights * mean_returns)
    
    @staticmethod
    def portfolio_volatility(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
        """
        Calculate portfolio volatility (standard deviation).
        
        Args:
            weights: Portfolio weights
            cov_matrix: Covariance matrix of returns
        
        Returns:
            Portfolio volatility
        """
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    @staticmethod
    def sharpe_ratio(weights: np.ndarray, mean_returns: np.ndarray, 
                    cov_matrix: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio.
        
        Args:
            weights: Portfolio weights
            mean_returns: Mean returns for each asset
            cov_matrix: Covariance matrix of returns
            risk_free_rate: Risk-free rate
        
        Returns:
            Sharpe ratio
        """
        portfolio_ret = PortfolioMetrics.portfolio_return(weights, mean_returns)
        portfolio_vol = PortfolioMetrics.portfolio_volatility(weights, cov_matrix)
        
        return (portfolio_ret - risk_free_rate) / portfolio_vol
    
    @staticmethod
    def maximum_drawdown(returns: Union[pd.Series, np.ndarray]) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
        """
        Calculate maximum drawdown of a return series.
        
        Args:
            returns: Series of returns
        
        Returns:
            Tuple of (max_drawdown, peak_date, trough_date)
        """
        if isinstance(returns, np.ndarray):
            returns = pd.Series(returns)
        
        # Calculate cumulative returns
        cumulative = (1 + returns).cumprod()
        
        # Calculate running maximum
        running_max = cumulative.expanding().max()
        
        # Calculate drawdown
        drawdown = (cumulative - running_max) / running_max
        
        # Find maximum drawdown
        max_dd = drawdown.min()
        
        # Find the dates
        trough_date = drawdown.idxmin()
        peak_date = cumulative[:trough_date].idxmax()
        
        return max_dd, peak_date, trough_date
    
    @staticmethod
    def calculate_portfolio_returns(weights: np.ndarray, returns: pd.DataFrame) -> pd.Series:
        """
        Calculate portfolio returns time series.
        
        Args:
            weights: Portfolio weights
            returns: DataFrame of asset returns
        
        Returns:
            Series of portfolio returns
        """
        return (returns * weights).sum(axis=1)
    
    @staticmethod
    def sortino_ratio(weights: np.ndarray, mean_returns: np.ndarray, 
                     returns: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sortino ratio (uses downside deviation instead of total volatility).
        
        Args:
            weights: Portfolio weights
            mean_returns: Mean returns for each asset
            returns: DataFrame of asset returns
            risk_free_rate: Risk-free rate
        
        Returns:
            Sortino ratio
        """
        portfolio_ret = np.sum(weights * mean_returns)
        portfolio_returns = (returns * weights).sum(axis=1)
        
        # Calculate downside deviation
        downside_returns = portfolio_returns[portfolio_returns < 0]
        downside_std = downside_returns.std() * np.sqrt(252)
        
        if downside_std == 0:
            return np.inf
        
        return (portfolio_ret - risk_free_rate) / downside_std
    
    @staticmethod
    def calmar_ratio(weights: np.ndarray, mean_returns: np.ndarray, 
                    returns: pd.DataFrame) -> float:
        """
        Calculate Calmar ratio (return / max drawdown).
        
        Args:
            weights: Portfolio weights
            mean_returns: Mean returns for each asset
            returns: DataFrame of asset returns
        
        Returns:
            Calmar ratio
        """
        portfolio_ret = np.sum(weights * mean_returns)
        portfolio_returns = (returns * weights).sum(axis=1)
        
        max_dd, _, _ = PortfolioMetrics.maximum_drawdown(portfolio_returns)
        
        if max_dd == 0:
            return np.inf
        
        return portfolio_ret / abs(max_dd)
    
    @staticmethod
    def value_at_risk(weights: np.ndarray, returns: pd.DataFrame, 
                     confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR) using historical simulation.
        
        Args:
            weights: Portfolio weights
            returns: DataFrame of asset returns
            confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
        
        Returns:
            Value at Risk
        """
        portfolio_returns = (returns * weights).sum(axis=1)
        var = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
        
        return var
    
    @staticmethod
    def conditional_value_at_risk(weights: np.ndarray, returns: pd.DataFrame, 
                                 confidence_level: float = 0.95) -> float:
        """
        Calculate Conditional Value at Risk (CVaR/Expected Shortfall).
        
        Args:
            weights: Portfolio weights
            returns: DataFrame of asset returns
            confidence_level: Confidence level (e.g., 0.95 for 95% CVaR)
        
        Returns:
            Conditional Value at Risk
        """
        portfolio_returns = (returns * weights).sum(axis=1)
        var = PortfolioMetrics.value_at_risk(weights, returns, confidence_level)
        
        # CVaR is the mean of returns below VaR
        cvar = portfolio_returns[portfolio_returns <= var].mean()
        
        return cvar
    
    @staticmethod
    def information_ratio(portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate Information Ratio (tracking error adjusted return).
        
        Args:
            portfolio_returns: Portfolio return series
            benchmark_returns: Benchmark return series
        
        Returns:
            Information ratio
        """
        excess_returns = portfolio_returns - benchmark_returns
        tracking_error = excess_returns.std() * np.sqrt(252)
        
        if tracking_error == 0:
            return np.inf
        
        return (excess_returns.mean() * 252) / tracking_error
    
    @staticmethod
    def get_all_metrics(weights: np.ndarray, mean_returns: np.ndarray, 
                       cov_matrix: np.ndarray, returns: pd.DataFrame, 
                       risk_free_rate: float = 0.02) -> dict:
        """
        Calculate all portfolio metrics.
        
        Args:
            weights: Portfolio weights
            mean_returns: Mean returns for each asset
            cov_matrix: Covariance matrix
            returns: DataFrame of asset returns
            risk_free_rate: Risk-free rate
        
        Returns:
            Dictionary with all metrics
        """
        portfolio_ret = PortfolioMetrics.portfolio_return(weights, mean_returns)
        portfolio_vol = PortfolioMetrics.portfolio_volatility(weights, cov_matrix)
        sharpe = PortfolioMetrics.sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate)
        
        portfolio_returns = PortfolioMetrics.calculate_portfolio_returns(weights, returns)
        max_dd, peak_date, trough_date = PortfolioMetrics.maximum_drawdown(portfolio_returns)
        
        sortino = PortfolioMetrics.sortino_ratio(weights, mean_returns, returns, risk_free_rate)
        calmar = PortfolioMetrics.calmar_ratio(weights, mean_returns, returns)
        var_95 = PortfolioMetrics.value_at_risk(weights, returns, 0.95)
        cvar_95 = PortfolioMetrics.conditional_value_at_risk(weights, returns, 0.95)
        
        return {
            'Expected Return': portfolio_ret,
            'Volatility': portfolio_vol,
            'Sharpe Ratio': sharpe,
            'Sortino Ratio': sortino,
            'Calmar Ratio': calmar,
            'Maximum Drawdown': max_dd,
            'VaR (95%)': var_95,
            'CVaR (95%)': cvar_95
        }
    
    @staticmethod
    def print_metrics(metrics: dict, weights: np.ndarray = None, tickers: list = None):
        """
        Pretty print portfolio metrics.
        
        Args:
            metrics: Dictionary of metrics
            weights: Optional portfolio weights to display
            tickers: Optional list of ticker names
        """
        print("\n" + "="*50)
        print("PORTFOLIO PERFORMANCE METRICS")
        print("="*50)
        
        for key, value in metrics.items():
            if isinstance(value, float):
                if 'Ratio' in key:
                    print(f"{key:.<30} {value:.4f}")
                elif 'Return' in key or 'Volatility' in key:
                    print(f"{key:.<30} {value*100:.2f}%")
                else:
                    print(f"{key:.<30} {value*100:.2f}%")
            else:
                print(f"{key:.<30} {value}")
        
        if weights is not None and tickers is not None:
            print("\n" + "-"*50)
            print("PORTFOLIO ALLOCATION")
            print("-"*50)
            for ticker, weight in zip(tickers, weights):
                print(f"{ticker:.<30} {weight*100:.2f}%")
        
        print("="*50 + "\n")
