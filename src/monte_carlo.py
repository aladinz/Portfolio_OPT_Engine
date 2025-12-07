"""
Monte Carlo Simulation Module
Implements portfolio forecasting using Monte Carlo methods.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict
from scipy.stats import norm


class MonteCarloSimulator:
    """
    Monte Carlo simulator for portfolio forecasting.
    """
    
    def __init__(self, mean_returns: np.ndarray, cov_matrix: np.ndarray):
        """
        Initialize the simulator.
        
        Args:
            mean_returns: Expected annual returns for each asset
            cov_matrix: Covariance matrix of returns
        """
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.n_assets = len(mean_returns)
    
    def simulate_portfolio(self, weights: np.ndarray, initial_investment: float,
                          time_horizon_years: int, n_simulations: int = 10000,
                          annual_contribution: float = 0.0) -> Dict:
        """
        Run Monte Carlo simulation for a portfolio.
        
        Args:
            weights: Portfolio weights
            initial_investment: Initial investment amount
            time_horizon_years: Investment horizon in years
            n_simulations: Number of Monte Carlo simulations
            annual_contribution: Annual contribution amount
        
        Returns:
            Dictionary containing simulation results
        """
        # Portfolio statistics
        portfolio_return = np.dot(weights, self.mean_returns)
        portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
        portfolio_std = np.sqrt(portfolio_variance)
        
        # Run simulations
        final_values = np.zeros(n_simulations)
        paths = np.zeros((n_simulations, time_horizon_years + 1))
        paths[:, 0] = initial_investment
        
        for sim in range(n_simulations):
            value = initial_investment
            
            for year in range(1, time_horizon_years + 1):
                # Generate random return from normal distribution
                annual_return = np.random.normal(portfolio_return, portfolio_std)
                
                # Update value
                value = value * (1 + annual_return) + annual_contribution
                paths[sim, year] = value
            
            final_values[sim] = value
        
        # Calculate statistics
        percentiles = {
            '10th': np.percentile(final_values, 10),
            '25th': np.percentile(final_values, 25),
            '50th': np.percentile(final_values, 50),  # Median
            '75th': np.percentile(final_values, 75),
            '90th': np.percentile(final_values, 90)
        }
        
        # Calculate probability of loss
        prob_loss = np.sum(final_values < initial_investment) / n_simulations
        
        # Calculate expected final value
        expected_value = np.mean(final_values)
        
        # Calculate value at risk (VaR) and conditional VaR (CVaR)
        var_95 = np.percentile(final_values, 5)
        cvar_95 = np.mean(final_values[final_values <= var_95])
        
        return {
            'final_values': final_values,
            'paths': paths,
            'percentiles': percentiles,
            'expected_value': expected_value,
            'prob_loss': prob_loss,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'portfolio_return': portfolio_return,
            'portfolio_std': portfolio_std
        }
    
    def compare_scenarios(self, weights: np.ndarray, initial_investment: float,
                         scenarios: list) -> Dict:
        """
        Compare multiple investment scenarios.
        
        Args:
            weights: Portfolio weights
            initial_investment: Initial investment amount
            scenarios: List of dicts with 'years', 'contributions'
        
        Returns:
            Dictionary of simulation results for each scenario
        """
        results = {}
        
        for scenario in scenarios:
            years = scenario['years']
            contributions = scenario.get('contributions', 0.0)
            
            result = self.simulate_portfolio(
                weights, 
                initial_investment, 
                years, 
                n_simulations=10000,
                annual_contribution=contributions
            )
            
            results[f"{years}yr"] = result
        
        return results
    
    def calculate_retirement_probability(self, weights: np.ndarray, 
                                        current_portfolio: float,
                                        years_to_retirement: int,
                                        annual_contribution: float,
                                        retirement_goal: float,
                                        n_simulations: int = 10000) -> Dict:
        """
        Calculate probability of reaching retirement goal.
        
        Args:
            weights: Portfolio weights
            current_portfolio: Current portfolio value
            years_to_retirement: Years until retirement
            annual_contribution: Annual contribution
            retirement_goal: Target retirement amount
            n_simulations: Number of simulations
        
        Returns:
            Dictionary with retirement analysis
        """
        result = self.simulate_portfolio(
            weights,
            current_portfolio,
            years_to_retirement,
            n_simulations,
            annual_contribution
        )
        
        final_values = result['final_values']
        success_count = np.sum(final_values >= retirement_goal)
        success_rate = success_count / n_simulations
        
        # Calculate expected shortfall if goal not met
        shortfalls = retirement_goal - final_values[final_values < retirement_goal]
        avg_shortfall = np.mean(shortfalls) if len(shortfalls) > 0 else 0
        
        # Calculate years needed for different confidence levels
        confidence_levels = [0.50, 0.75, 0.90, 0.95]
        years_needed = {}
        
        for conf in confidence_levels:
            target_value = retirement_goal
            for test_years in range(1, 50):
                test_result = self.simulate_portfolio(
                    weights, current_portfolio, test_years,
                    n_simulations=1000, annual_contribution=annual_contribution
                )
                percentile_val = np.percentile(test_result['final_values'], conf * 100)
                if percentile_val >= target_value:
                    years_needed[f"{int(conf*100)}%"] = test_years
                    break
        
        return {
            'success_rate': success_rate,
            'expected_value': result['expected_value'],
            'median_value': result['percentiles']['50th'],
            'retirement_goal': retirement_goal,
            'shortfall': avg_shortfall,
            'years_needed': years_needed,
            'simulation_data': result
        }
