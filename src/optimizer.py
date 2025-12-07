"""
Portfolio Optimizer Module
Implements various portfolio optimization strategies.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint
from typing import Tuple, Dict, Optional
from src.metrics import PortfolioMetrics


class PortfolioOptimizer:
    """
    Implements multiple portfolio optimization objectives.
    """
    
    def __init__(self, mean_returns: np.ndarray, cov_matrix: np.ndarray, 
                 risk_free_rate: float = 0.02):
        """
        Initialize the optimizer.
        
        Args:
            mean_returns: Expected returns for each asset
            cov_matrix: Covariance matrix of returns
            risk_free_rate: Risk-free rate for Sharpe ratio calculation
        """
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.risk_free_rate = risk_free_rate
        self.n_assets = len(mean_returns)
        
        if self.n_assets == 0:
            raise ValueError("No assets available for optimization. Please check your ticker symbols.")
    
    def _get_constraints(self, allow_short: bool = False) -> list:
        """
        Get optimization constraints.
        
        Args:
            allow_short: Whether to allow short selling
        
        Returns:
            List of constraints
        """
        # Weights must sum to 1
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        
        return constraints
    
    def _get_bounds(self, allow_short: bool = False, min_weight: float = 0.0, max_weight: float = 1.0) -> tuple:
        """
        Get bounds for portfolio weights.
        
        Args:
            allow_short: Whether to allow short selling
            min_weight: Minimum weight per asset (0 to 1)
            max_weight: Maximum weight per asset (0 to 1)
        
        Returns:
            Tuple of bounds
        """
        if allow_short:
            return tuple((-1, 1) for _ in range(self.n_assets))
        else:
            return tuple((min_weight, max_weight) for _ in range(self.n_assets))
    
    def optimize_max_sharpe(self, allow_short: bool = False, min_weight: float = 0.0, max_weight: float = 1.0) -> Tuple[np.ndarray, dict]:
        """
        Optimize for maximum Sharpe ratio.
        
        Args:
            allow_short: Whether to allow short selling
            min_weight: Minimum weight per asset
            max_weight: Maximum weight per asset
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        # Negative Sharpe ratio for minimization
        def neg_sharpe(weights):
            return -PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        
        # Initial guess (equal weights if possible, else proportional to bounds)
        if min_weight * self.n_assets > 1.0:
            # Infeasible, adjust
            x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        else:
            x0 = np.array([max(min_weight, 1.0 / self.n_assets)] * self.n_assets)
            x0 = x0 / x0.sum()  # Normalize
        
        # Optimize
        result = minimize(
            neg_sharpe,
            x0,
            method='SLSQP',
            bounds=self._get_bounds(allow_short, min_weight, max_weight),
            constraints=self._get_constraints(allow_short)
        )
        
        weights = result.x
        
        metrics = {
            'Expected Return': PortfolioMetrics.portfolio_return(weights, self.mean_returns),
            'Volatility': PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix),
            'Sharpe Ratio': PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        }
        
        return weights, metrics
    
    def optimize_min_volatility(self, allow_short: bool = False, min_weight: float = 0.0, max_weight: float = 1.0) -> Tuple[np.ndarray, dict]:
        """
        Optimize for minimum volatility.
        
        Args:
            allow_short: Whether to allow short selling
            min_weight: Minimum weight per asset
            max_weight: Maximum weight per asset
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        def portfolio_vol(weights):
            return PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix)
        
        if min_weight * self.n_assets > 1.0:
            x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        else:
            x0 = np.array([max(min_weight, 1.0 / self.n_assets)] * self.n_assets)
            x0 = x0 / x0.sum()
        
        result = minimize(
            portfolio_vol,
            x0,
            method='SLSQP',
            bounds=self._get_bounds(allow_short, min_weight, max_weight),
            constraints=self._get_constraints(allow_short)
        )
        
        weights = result.x
        
        metrics = {
            'Expected Return': PortfolioMetrics.portfolio_return(weights, self.mean_returns),
            'Volatility': PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix),
            'Sharpe Ratio': PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        }
        
        return weights, metrics
    
    def optimize_max_return(self, target_volatility: Optional[float] = None,
                           allow_short: bool = False, min_weight: float = 0.0, max_weight: float = 1.0) -> Tuple[np.ndarray, dict]:
        """
        Optimize for maximum return (optionally with volatility constraint).
        
        Args:
            target_volatility: Optional maximum volatility constraint
            allow_short: Whether to allow short selling
            min_weight: Minimum weight per asset
            max_weight: Maximum weight per asset
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        # Negative return for minimization
        def neg_return(weights):
            return -PortfolioMetrics.portfolio_return(weights, self.mean_returns)
        
        if min_weight * self.n_assets > 1.0:
            x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        else:
            x0 = np.array([max(min_weight, 1.0 / self.n_assets)] * self.n_assets)
            x0 = x0 / x0.sum()
        
        constraints = self._get_constraints(allow_short)
        
        # Add volatility constraint if specified
        if target_volatility is not None:
            constraints.append({
                'type': 'ineq',
                'fun': lambda x: target_volatility - PortfolioMetrics.portfolio_volatility(x, self.cov_matrix)
            })
        
        result = minimize(
            neg_return,
            x0,
            method='SLSQP',
            bounds=self._get_bounds(allow_short, min_weight, max_weight),
            constraints=constraints
        )
        
        weights = result.x
        
        metrics = {
            'Expected Return': PortfolioMetrics.portfolio_return(weights, self.mean_returns),
            'Volatility': PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix),
            'Sharpe Ratio': PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        }
        
        return weights, metrics
    
    def optimize_risk_parity(self, min_weight: float = 0.0, max_weight: float = 1.0) -> Tuple[np.ndarray, dict]:
        """
        Optimize for risk parity (equal risk contribution).
        
        Args:
            min_weight: Minimum weight per asset
            max_weight: Maximum weight per asset
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        def risk_parity_objective(weights):
            """
            Objective function for risk parity optimization.
            Minimizes the sum of squared differences between risk contributions.
            """
            portfolio_vol = PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix)
            
            # Calculate marginal risk contribution for each asset
            marginal_contrib = np.dot(self.cov_matrix, weights)
            
            # Calculate risk contribution for each asset
            risk_contrib = weights * marginal_contrib / portfolio_vol
            
            # Target is equal risk contribution
            target_risk = portfolio_vol / self.n_assets
            
            # Minimize squared deviations from target
            return np.sum((risk_contrib - target_risk) ** 2)
        
        # Adjust initial guess for constraints
        if min_weight * self.n_assets > 1.0:
            x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        else:
            x0 = np.array([max(min_weight, 1.0 / self.n_assets)] * self.n_assets)
            x0 = x0 / x0.sum()
        
        result = minimize(
            risk_parity_objective,
            x0,
            method='SLSQP',
            bounds=self._get_bounds(allow_short=False, min_weight=min_weight, max_weight=max_weight),
            constraints=self._get_constraints(allow_short=False)
        )
        
        weights = result.x
        
        metrics = {
            'Expected Return': PortfolioMetrics.portfolio_return(weights, self.mean_returns),
            'Volatility': PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix),
            'Sharpe Ratio': PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        }
        
        return weights, metrics
    
    def optimize_equal_weight(self) -> Tuple[np.ndarray, dict]:
        """
        Equal weight portfolio (1/N).
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        weights = np.array([1.0 / self.n_assets] * self.n_assets)
        
        metrics = {
            'Expected Return': PortfolioMetrics.portfolio_return(weights, self.mean_returns),
            'Volatility': PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix),
            'Sharpe Ratio': PortfolioMetrics.sharpe_ratio(
                weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
            )
        }
        
        return weights, metrics
    
    def generate_efficient_frontier(self, n_portfolios: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate the efficient frontier.
        
        Args:
            n_portfolios: Number of portfolios to generate
        
        Returns:
            Tuple of (returns, volatilities, sharpe_ratios)
        """
        # Find min and max return portfolios
        min_vol_weights, _ = self.optimize_min_volatility()
        max_ret_weights, _ = self.optimize_max_return()
        
        min_return = PortfolioMetrics.portfolio_return(min_vol_weights, self.mean_returns)
        max_return = PortfolioMetrics.portfolio_return(max_ret_weights, self.mean_returns)
        
        # Generate target returns
        target_returns = np.linspace(min_return, max_return, n_portfolios)
        
        returns = []
        volatilities = []
        sharpe_ratios = []
        
        for target_return in target_returns:
            try:
                # Optimize for minimum volatility given target return
                def portfolio_vol(weights):
                    return PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix)
                
                constraints = self._get_constraints(allow_short=False)
                constraints.append({
                    'type': 'eq',
                    'fun': lambda x: PortfolioMetrics.portfolio_return(x, self.mean_returns) - target_return
                })
                
                x0 = np.array([1.0 / self.n_assets] * self.n_assets)
                
                result = minimize(
                    portfolio_vol,
                    x0,
                    method='SLSQP',
                    bounds=self._get_bounds(allow_short=False),
                    constraints=constraints
                )
                
                if result.success:
                    weights = result.x
                    returns.append(PortfolioMetrics.portfolio_return(weights, self.mean_returns))
                    volatilities.append(PortfolioMetrics.portfolio_volatility(weights, self.cov_matrix))
                    sharpe_ratios.append(PortfolioMetrics.sharpe_ratio(
                        weights, self.mean_returns, self.cov_matrix, self.risk_free_rate
                    ))
            except:
                continue
        
        return np.array(returns), np.array(volatilities), np.array(sharpe_ratios)
    
    def optimize(self, objective: str = 'max_sharpe', **kwargs) -> Tuple[np.ndarray, dict]:
        """
        Optimize portfolio based on specified objective.
        
        Args:
            objective: Optimization objective
                - 'max_sharpe': Maximum Sharpe ratio
                - 'min_volatility': Minimum volatility
                - 'max_return': Maximum return
                - 'risk_parity': Risk parity
                - 'equal_weight': Equal weight (1/N)
            **kwargs: Additional arguments for specific objectives
        
        Returns:
            Tuple of (optimal_weights, metrics_dict)
        """
        objective = objective.lower()
        
        if objective == 'max_sharpe':
            return self.optimize_max_sharpe(**kwargs)
        elif objective == 'min_volatility':
            return self.optimize_min_volatility(**kwargs)
        elif objective == 'max_return':
            return self.optimize_max_return(**kwargs)
        elif objective == 'risk_parity':
            return self.optimize_risk_parity(**kwargs)
        elif objective == 'equal_weight':
            return self.optimize_equal_weight()
        else:
            raise ValueError(f"Unknown objective: {objective}")
