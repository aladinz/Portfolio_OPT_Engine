"""
Example Script - Portfolio Optimization Engine
Demonstrates usage with sample assets (AAPL, MSFT, TSLA, GLD, BTC-USD)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.data_handler import DataHandler
from src.optimizer import PortfolioOptimizer
from src.metrics import PortfolioMetrics
from src.visualizer import PortfolioVisualizer
from src.rebalancer import PortfolioRebalancer


def main():
    """
    Main example demonstrating all features of the Portfolio Optimization Engine.
    """
    print("\n" + "="*80)
    print("PORTFOLIO OPTIMIZATION ENGINE - EXAMPLE RUN")
    print("="*80 + "\n")
    
    # 1. Define portfolio parameters
    tickers = ['AAPL', 'MSFT', 'TSLA', 'GLD', 'BTC-USD']
    period_months = 24  # 2 years of historical data
    risk_free_rate = 0.02  # 2% annual risk-free rate
    
    print(f"Assets: {', '.join(tickers)}")
    print(f"Historical Period: {period_months} months")
    print(f"Risk-Free Rate: {risk_free_rate*100:.1f}%\n")
    
    # 2. Fetch and prepare data
    print("="*80)
    print("STEP 1: DATA FETCHING")
    print("="*80)
    
    data_handler = DataHandler(tickers, period_months, risk_free_rate)
    prices = data_handler.fetch_data()
    returns = data_handler.calculate_returns()
    
    # Display asset statistics
    print("\nAsset Statistics:")
    print("-"*80)
    stats = data_handler.get_asset_statistics()
    print(stats.to_string())
    
    # Prepare data for optimization
    mean_returns, cov_matrix = data_handler.prepare_optimization_data()
    
    # 3. Run multiple optimization strategies
    print("\n" + "="*80)
    print("STEP 2: PORTFOLIO OPTIMIZATION")
    print("="*80 + "\n")
    
    optimizer = PortfolioOptimizer(mean_returns, cov_matrix, risk_free_rate)
    
    strategies = {
        'Maximum Sharpe Ratio': 'max_sharpe',
        'Minimum Volatility': 'min_volatility',
        'Risk Parity': 'risk_parity',
        'Equal Weight': 'equal_weight'
    }
    
    results = {}
    
    for strategy_name, strategy_key in strategies.items():
        print(f"\n{strategy_name}")
        print("-"*80)
        
        weights, metrics = optimizer.optimize(strategy_key)
        
        # Calculate all metrics
        all_metrics = PortfolioMetrics.get_all_metrics(
            weights, mean_returns, cov_matrix, returns, risk_free_rate
        )
        
        results[strategy_name] = {
            'weights': weights,
            'metrics': all_metrics
        }
        
        # Print metrics
        PortfolioMetrics.print_metrics(all_metrics, weights, data_handler.tickers)
    
    # 4. Generate Efficient Frontier
    print("\n" + "="*80)
    print("STEP 3: EFFICIENT FRONTIER GENERATION")
    print("="*80 + "\n")
    
    print("Generating efficient frontier with 100 portfolios...")
    ef_returns, ef_vols, ef_sharpes = optimizer.generate_efficient_frontier(n_portfolios=100)
    print(f"Generated {len(ef_returns)} efficient portfolios")
    
    # 5. Visualizations
    print("\n" + "="*80)
    print("STEP 4: VISUALIZATIONS")
    print("="*80 + "\n")
    
    visualizer = PortfolioVisualizer()
    
    # Plot efficient frontier
    print("Generating efficient frontier plot...")
    optimal_points = {}
    for strategy_name, result in results.items():
        weights = result['weights']
        ret = PortfolioMetrics.portfolio_return(weights, mean_returns)
        vol = PortfolioMetrics.portfolio_volatility(weights, cov_matrix)
        optimal_points[strategy_name] = (ret, vol)
    
    fig_ef = visualizer.plot_efficient_frontier(
        ef_returns, ef_vols, ef_sharpes,
        optimal_points=optimal_points,
        show_cml=True,
        risk_free_rate=risk_free_rate
    )
    plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: efficient_frontier.png")
    plt.close()
    
    # Plot allocations for each strategy
    for strategy_name, result in results.items():
        weights = result['weights']
        fig = visualizer.plot_weights(
            weights, 
            data_handler.tickers,
            title=f"{strategy_name} Portfolio"
        )
        filename = f"allocation_{strategy_name.lower().replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename}")
        plt.close()
    
    # Plot correlation matrix
    print("Generating correlation matrix...")
    corr_matrix = data_handler.get_correlation_matrix()
    fig_corr = visualizer.plot_correlation_matrix(corr_matrix)
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: correlation_matrix.png")
    plt.close()
    
    # Plot cumulative returns
    print("Generating cumulative returns plot...")
    # Use Maximum Sharpe portfolio
    max_sharpe_weights = results['Maximum Sharpe Ratio']['weights']
    fig_cum = visualizer.plot_cumulative_returns(
        returns,
        weights=max_sharpe_weights
    )
    plt.savefig('cumulative_returns.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: cumulative_returns.png")
    plt.close()
    
    # 6. Rebalancing Analysis
    print("\n" + "="*80)
    print("STEP 5: REBALANCING ANALYSIS")
    print("="*80 + "\n")
    
    # Use Maximum Sharpe portfolio for rebalancing example
    target_weights = results['Maximum Sharpe Ratio']['weights']
    drift_threshold = 0.05  # 5% drift threshold
    
    rebalancer = PortfolioRebalancer(target_weights, data_handler.tickers, drift_threshold)
    
    # Simulate portfolio drift
    print("Simulating portfolio drift...")
    print("Assuming initial investment: $100,000\n")
    
    initial_investment = 100000
    initial_values = target_weights * initial_investment
    
    # Simulate some price changes (random for demonstration)
    np.random.seed(42)  # For reproducibility
    price_changes = np.random.uniform(0.85, 1.25, len(data_handler.tickers))
    current_values = initial_values * price_changes
    current_prices = prices.iloc[-1].values * price_changes
    
    print("Simulated price changes:")
    for ticker, change in zip(data_handler.tickers, price_changes):
        print(f"  {ticker}: {(change-1)*100:+.2f}%")
    print()
    
    # Monitor portfolio
    monitoring = rebalancer.monitor_portfolio(current_values)
    rebalancer.print_monitoring_report(monitoring)
    
    # Calculate rebalancing trades
    if monitoring['Needs Rebalancing']:
        trades = rebalancer.calculate_rebalancing_trades(current_values, current_prices)
        rebalancer.print_rebalancing_report(trades)
    
    # 7. Strategy Comparison
    print("\n" + "="*80)
    print("STEP 6: STRATEGY COMPARISON")
    print("="*80 + "\n")
    
    comparison_df = pd.DataFrame({
        strategy: {
            'Expected Return': results[strategy]['metrics']['Expected Return'],
            'Volatility': results[strategy]['metrics']['Volatility'],
            'Sharpe Ratio': results[strategy]['metrics']['Sharpe Ratio'],
            'Max Drawdown': results[strategy]['metrics']['Maximum Drawdown'],
            'Sortino Ratio': results[strategy]['metrics']['Sortino Ratio']
        }
        for strategy in strategies.keys()
    }).T
    
    print("Performance Comparison Across Strategies:")
    print("-"*80)
    print(comparison_df.to_string())
    
    # Find best strategy by different criteria
    print("\n\nBest Strategy by Criteria:")
    print("-"*80)
    print(f"Highest Return:       {comparison_df['Expected Return'].idxmax()}")
    print(f"Lowest Volatility:    {comparison_df['Volatility'].idxmin()}")
    print(f"Highest Sharpe Ratio: {comparison_df['Sharpe Ratio'].idxmax()}")
    print(f"Lowest Drawdown:      {comparison_df['Max Drawdown'].idxmax()}")
    
    # 8. Save results to CSV
    print("\n" + "="*80)
    print("STEP 7: SAVING RESULTS")
    print("="*80 + "\n")
    
    # Save portfolio weights
    weights_df = pd.DataFrame({
        strategy: results[strategy]['weights']
        for strategy in strategies.keys()
    }, index=data_handler.tickers)
    weights_df.to_csv('portfolio_weights.csv')
    print("✓ Saved: portfolio_weights.csv")
    
    # Save metrics comparison
    comparison_df.to_csv('strategy_comparison.csv')
    print("✓ Saved: strategy_comparison.csv")
    
    # Save asset statistics
    stats.to_csv('asset_statistics.csv')
    print("✓ Saved: asset_statistics.csv")
    
    print("\n" + "="*80)
    print("EXAMPLE RUN COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nGenerated files:")
    print("  - efficient_frontier.png")
    print("  - allocation_*.png (one per strategy)")
    print("  - correlation_matrix.png")
    print("  - cumulative_returns.png")
    print("  - portfolio_weights.csv")
    print("  - strategy_comparison.csv")
    print("  - asset_statistics.csv")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
