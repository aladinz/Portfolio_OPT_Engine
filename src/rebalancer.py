"""
Rebalancing Module
Monitors portfolio drift and suggests rebalancing trades.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class PortfolioRebalancer:
    """
    Monitors portfolio allocation and suggests rebalancing when needed.
    """
    
    def __init__(self, target_weights: np.ndarray, tickers: List[str], 
                 drift_threshold: float = 0.05):
        """
        Initialize the rebalancer.
        
        Args:
            target_weights: Target portfolio weights
            tickers: List of asset ticker symbols
            drift_threshold: Maximum allowed drift from target weights (e.g., 0.05 = 5%)
        """
        self.target_weights = target_weights
        self.tickers = tickers
        self.drift_threshold = drift_threshold
        self.n_assets = len(tickers)
        
    def calculate_current_weights(self, current_values: np.ndarray) -> np.ndarray:
        """
        Calculate current portfolio weights from asset values.
        
        Args:
            current_values: Current value of each asset position
        
        Returns:
            Array of current weights
        """
        total_value = np.sum(current_values)
        
        if total_value == 0:
            raise ValueError("Total portfolio value is zero")
        
        return current_values / total_value
    
    def check_drift(self, current_weights: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Check if portfolio has drifted beyond threshold.
        
        Args:
            current_weights: Current portfolio weights
        
        Returns:
            Tuple of (needs_rebalancing, weight_differences)
        """
        weight_diff = np.abs(current_weights - self.target_weights)
        needs_rebalancing = np.any(weight_diff > self.drift_threshold)
        
        return needs_rebalancing, weight_diff
    
    def calculate_rebalancing_trades(self, current_values: np.ndarray, 
                                    current_prices: np.ndarray) -> pd.DataFrame:
        """
        Calculate trades needed to rebalance portfolio.
        
        Args:
            current_values: Current value of each asset position
            current_prices: Current price of each asset
        
        Returns:
            DataFrame with rebalancing trade suggestions
        """
        total_value = np.sum(current_values)
        current_weights = self.calculate_current_weights(current_values)
        
        # Calculate target values
        target_values = self.target_weights * total_value
        
        # Calculate value to trade
        value_to_trade = target_values - current_values
        
        # Calculate shares to trade
        shares_to_trade = value_to_trade / current_prices
        
        # Create DataFrame
        trades = pd.DataFrame({
            'Ticker': self.tickers,
            'Current Weight': current_weights,
            'Target Weight': self.target_weights,
            'Weight Drift': current_weights - self.target_weights,
            'Current Value': current_values,
            'Target Value': target_values,
            'Value to Trade': value_to_trade,
            'Current Price': current_prices,
            'Shares to Trade': shares_to_trade
        })
        
        # Add action column
        trades['Action'] = trades['Shares to Trade'].apply(
            lambda x: 'BUY' if x > 0 else ('SELL' if x < 0 else 'HOLD')
        )
        
        # Add drift percentage
        trades['Drift %'] = (trades['Weight Drift'] / trades['Target Weight'] * 100).fillna(0)
        
        return trades
    
    def get_rebalancing_summary(self, trades: pd.DataFrame) -> Dict:
        """
        Get summary statistics for rebalancing.
        
        Args:
            trades: DataFrame of rebalancing trades
        
        Returns:
            Dictionary with summary statistics
        """
        total_buy_value = trades[trades['Value to Trade'] > 0]['Value to Trade'].sum()
        total_sell_value = abs(trades[trades['Value to Trade'] < 0]['Value to Trade'].sum())
        
        max_drift = trades['Weight Drift'].abs().max()
        max_drift_ticker = trades.loc[trades['Weight Drift'].abs().idxmax(), 'Ticker']
        
        n_buys = len(trades[trades['Action'] == 'BUY'])
        n_sells = len(trades[trades['Action'] == 'SELL'])
        n_holds = len(trades[trades['Action'] == 'HOLD'])
        
        return {
            'Total Buy Value': total_buy_value,
            'Total Sell Value': total_sell_value,
            'Max Drift': max_drift,
            'Max Drift Ticker': max_drift_ticker,
            'Number of Buys': n_buys,
            'Number of Sells': n_sells,
            'Number of Holds': n_holds,
            'Turnover': (total_buy_value + total_sell_value) / 2 / trades['Current Value'].sum()
        }
    
    def suggest_minimal_rebalancing(self, current_values: np.ndarray, 
                                   current_prices: np.ndarray,
                                   transaction_cost: float = 0.001) -> pd.DataFrame:
        """
        Suggest minimal trades to bring portfolio within threshold.
        Only rebalances assets that have drifted beyond threshold.
        
        Args:
            current_values: Current value of each asset position
            current_prices: Current price of each asset
            transaction_cost: Transaction cost as a fraction of trade value
        
        Returns:
            DataFrame with minimal rebalancing trades
        """
        current_weights = self.calculate_current_weights(current_values)
        needs_rebalancing, weight_diff = self.check_drift(current_weights)
        
        if not needs_rebalancing:
            # No rebalancing needed
            return pd.DataFrame({
                'Ticker': self.tickers,
                'Action': ['HOLD'] * self.n_assets,
                'Message': ['Within threshold'] * self.n_assets
            })
        
        # Identify assets that need rebalancing
        assets_to_rebalance = weight_diff > self.drift_threshold
        
        # Calculate trades only for drifted assets
        total_value = np.sum(current_values)
        new_weights = current_weights.copy()
        
        # Adjust drifted assets back to target
        for i in range(self.n_assets):
            if assets_to_rebalance[i]:
                new_weights[i] = self.target_weights[i]
        
        # Renormalize weights
        new_weights = new_weights / np.sum(new_weights)
        
        # Calculate trades
        target_values = new_weights * total_value
        value_to_trade = target_values - current_values
        shares_to_trade = value_to_trade / current_prices
        
        # Calculate transaction costs
        trade_costs = np.abs(value_to_trade) * transaction_cost
        
        trades = pd.DataFrame({
            'Ticker': self.tickers,
            'Current Weight': current_weights,
            'Target Weight': self.target_weights,
            'New Weight': new_weights,
            'Weight Drift': current_weights - self.target_weights,
            'Needs Rebalancing': assets_to_rebalance,
            'Current Value': current_values,
            'Target Value': target_values,
            'Value to Trade': value_to_trade,
            'Shares to Trade': shares_to_trade,
            'Transaction Cost': trade_costs,
            'Current Price': current_prices
        })
        
        trades['Action'] = trades.apply(
            lambda row: ('BUY' if row['Shares to Trade'] > 0 
                        else ('SELL' if row['Shares to Trade'] < 0 else 'HOLD')),
            axis=1
        )
        
        return trades
    
    def monitor_portfolio(self, current_values: np.ndarray, 
                         timestamp: Optional[datetime] = None) -> Dict:
        """
        Monitor portfolio and generate alerts if rebalancing is needed.
        
        Args:
            current_values: Current value of each asset position
            timestamp: Optional timestamp for the monitoring
        
        Returns:
            Dictionary with monitoring results and alerts
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        current_weights = self.calculate_current_weights(current_values)
        needs_rebalancing, weight_diff = self.check_drift(current_weights)
        
        # Generate alerts for assets that have drifted
        alerts = []
        for i, ticker in enumerate(self.tickers):
            if weight_diff[i] > self.drift_threshold:
                drift_pct = (current_weights[i] - self.target_weights[i]) / self.target_weights[i] * 100
                alerts.append({
                    'Ticker': ticker,
                    'Current Weight': current_weights[i],
                    'Target Weight': self.target_weights[i],
                    'Drift': weight_diff[i],
                    'Drift %': drift_pct,
                    'Status': 'OVERWEIGHT' if current_weights[i] > self.target_weights[i] else 'UNDERWEIGHT'
                })
        
        return {
            'Timestamp': timestamp,
            'Needs Rebalancing': needs_rebalancing,
            'Max Drift': np.max(weight_diff),
            'Avg Drift': np.mean(weight_diff),
            'Alerts': alerts,
            'Current Weights': dict(zip(self.tickers, current_weights)),
            'Target Weights': dict(zip(self.tickers, self.target_weights))
        }
    
    def print_rebalancing_report(self, trades: pd.DataFrame):
        """
        Print a formatted rebalancing report.
        
        Args:
            trades: DataFrame of rebalancing trades
        """
        print("\n" + "="*80)
        print("PORTFOLIO REBALANCING REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Drift Threshold: {self.drift_threshold*100:.1f}%")
        print()
        
        # Summary
        summary = self.get_rebalancing_summary(trades)
        print("SUMMARY")
        print("-"*80)
        print(f"Total Buy Value:        ${summary['Total Buy Value']:,.2f}")
        print(f"Total Sell Value:       ${summary['Total Sell Value']:,.2f}")
        print(f"Portfolio Turnover:     {summary['Turnover']*100:.2f}%")
        print(f"Max Weight Drift:       {summary['Max Drift']*100:.2f}% ({summary['Max Drift Ticker']})")
        print(f"Actions: {summary['Number of Buys']} BUY, {summary['Number of Sells']} SELL, {summary['Number of Holds']} HOLD")
        print()
        
        # Detailed trades
        print("DETAILED TRADES")
        print("-"*80)
        
        # Format for display
        display_trades = trades.copy()
        display_trades['Current Weight'] = (display_trades['Current Weight'] * 100).map('{:.2f}%'.format)
        display_trades['Target Weight'] = (display_trades['Target Weight'] * 100).map('{:.2f}%'.format)
        display_trades['Drift %'] = display_trades['Drift %'].map('{:.2f}%'.format)
        display_trades['Value to Trade'] = display_trades['Value to Trade'].map('${:,.2f}'.format)
        display_trades['Shares to Trade'] = display_trades['Shares to Trade'].map('{:.2f}'.format)
        
        print(display_trades[['Ticker', 'Action', 'Current Weight', 'Target Weight', 
                             'Drift %', 'Shares to Trade', 'Value to Trade']].to_string(index=False))
        
        print("="*80 + "\n")
    
    def print_monitoring_report(self, monitoring_result: Dict):
        """
        Print a formatted monitoring report.
        
        Args:
            monitoring_result: Dictionary from monitor_portfolio()
        """
        print("\n" + "="*80)
        print("PORTFOLIO MONITORING REPORT")
        print("="*80)
        print(f"Timestamp: {monitoring_result['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Drift Threshold: {self.drift_threshold*100:.1f}%")
        print()
        
        print("STATUS")
        print("-"*80)
        status = "⚠️  REBALANCING NEEDED" if monitoring_result['Needs Rebalancing'] else "✓  Within Threshold"
        print(f"Portfolio Status:       {status}")
        print(f"Maximum Drift:          {monitoring_result['Max Drift']*100:.2f}%")
        print(f"Average Drift:          {monitoring_result['Avg Drift']*100:.2f}%")
        print()
        
        if monitoring_result['Alerts']:
            print("ALERTS")
            print("-"*80)
            for alert in monitoring_result['Alerts']:
                print(f"\n{alert['Ticker']} - {alert['Status']}")
                print(f"  Current Weight: {alert['Current Weight']*100:.2f}%")
                print(f"  Target Weight:  {alert['Target Weight']*100:.2f}%")
                print(f"  Drift:          {alert['Drift']*100:.2f}% ({alert['Drift %']:.1f}% relative)")
        else:
            print("No alerts - All assets within threshold")
        
        print("\n" + "="*80 + "\n")
