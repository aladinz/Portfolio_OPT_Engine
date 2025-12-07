# Portfolio Optimization Engine - Setup Guide

## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run the Example Script
```powershell
python example.py
```

This will:
- Fetch historical data for AAPL, MSFT, TSLA, GLD, BTC-USD
- Run all optimization strategies
- Generate visualizations (saved as PNG files)
- Create CSV reports
- Demonstrate rebalancing analysis

### 3. Launch the Interactive Dashboard
```powershell
streamlit run app.py
```

Then open your browser to the URL shown (typically http://localhost:8501)

## Features Overview

### Core Optimization Strategies
1. **Maximum Sharpe Ratio** - Best risk-adjusted returns
2. **Minimum Volatility** - Lowest risk portfolio
3. **Maximum Return** - Highest expected return
4. **Risk Parity** - Equal risk contribution from each asset
5. **Equal Weight** - Simple 1/N allocation

### Data Handling
- Historical data from Yahoo Finance (yfinance)
- Configurable period: 6-60 months
- Automatic data cleaning and validation
- Returns, covariance, and correlation calculations

### Performance Metrics
- Expected Return (annualized)
- Volatility (standard deviation)
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Maximum Drawdown
- Value at Risk (VaR)
- Conditional VaR (CVaR)

### Visualizations
- Efficient Frontier with optimal portfolios
- Capital Market Line (CML)
- Portfolio allocation (bar and pie charts)
- Correlation heatmap
- Cumulative returns over time
- Asset return distributions

### Rebalancing System
- Monitor portfolio drift
- Configurable drift threshold
- Calculate required trades
- Transaction cost estimation
- Detailed rebalancing reports

## Project Structure

```
Portfolio_Opt_Engine/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── data_handler.py       # Data fetching and preprocessing
│   ├── metrics.py            # Performance metrics calculation
│   ├── optimizer.py          # Portfolio optimization algorithms
│   ├── visualizer.py         # Charting and visualization
│   └── rebalancer.py         # Rebalancing logic
├── app.py                    # Streamlit interactive dashboard
├── example.py                # Example script with sample run
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── SETUP_GUIDE.md           # This file
```

## Usage Examples

### Python API Usage

```python
from src.data_handler import DataHandler
from src.optimizer import PortfolioOptimizer
from src.visualizer import PortfolioVisualizer

# 1. Fetch data
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
data_handler = DataHandler(tickers, period_months=12)
data_handler.fetch_data()

# 2. Prepare for optimization
mean_returns, cov_matrix = data_handler.prepare_optimization_data()

# 3. Optimize portfolio
optimizer = PortfolioOptimizer(mean_returns, cov_matrix)
weights, metrics = optimizer.optimize('max_sharpe')

# 4. Visualize
visualizer = PortfolioVisualizer()
visualizer.plot_weights(weights, tickers)
```

### Streamlit Dashboard

1. Select assets in the sidebar
2. Choose historical data period
3. Set risk-free rate
4. Select optimization strategy
5. Click "Run Optimization"
6. Explore results interactively

## Sample Assets

### Stocks
- **Tech**: AAPL, MSFT, GOOGL, AMZN, NVDA
- **Consumer**: TSLA, DIS, NKE, SBUX
- **Finance**: JPM, BAC, GS, V

### ETFs
- **Bonds**: TLT, AGG, BND
- **Commodities**: GLD, SLV, DBA
- **International**: EFA, EEM, VWO

### Cryptocurrency
- **Major**: BTC-USD, ETH-USD
- **Stable**: USDT-USD, USDC-USD

## Advanced Configuration

### Custom Constraints
Modify `optimizer.py` to add custom constraints:
- Sector limits
- Individual asset limits
- Turnover constraints

### Custom Metrics
Add new metrics in `metrics.py`:
```python
@staticmethod
def custom_metric(weights, returns):
    # Your calculation here
    return value
```

### Custom Visualizations
Extend `visualizer.py` for additional charts:
```python
@staticmethod
def plot_custom_chart(data):
    # Your plotting code here
    return fig
```

## Troubleshooting

### Import Errors
```powershell
# Ensure you're in the project directory
cd Portfolio_Opt_Engine

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Data Fetching Issues
- Check internet connection
- Verify ticker symbols are correct
- Try reducing the historical period
- Some tickers may be delisted or unavailable

### Optimization Warnings
- "Optimization failed" - Try different initial weights
- "Singular matrix" - Assets may be too correlated
- Reduce number of assets or check data quality

## Performance Tips

1. **Data Fetching**: Cache data locally for repeated runs
2. **Efficient Frontier**: Reduce n_portfolios for faster generation
3. **Visualization**: Use `interactive=False` for faster rendering
4. **Large Portfolios**: Consider using sparse matrices for 50+ assets

## Next Steps

1. **Backtest**: Add historical backtesting functionality
2. **Constraints**: Implement sector/asset constraints
3. **Monte Carlo**: Add Monte Carlo simulation
4. **Factor Models**: Implement Fama-French factors
5. **Black-Litterman**: Add Black-Litterman model
6. **Database**: Store results in SQLite/PostgreSQL

## Support

For issues or questions:
1. Check documentation in README.md
2. Review example.py for usage patterns
3. Examine source code comments and docstrings

## License

MIT License - Feel free to modify and extend!
