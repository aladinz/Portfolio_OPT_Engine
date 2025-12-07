# Quick Reference Guide

## 🚀 Getting Started (3 Steps)

### 1. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 2. Verify Installation
```powershell
python test_setup.py
```

### 3. Run Example or Dashboard
```powershell
# Option A: Run example script
python example.py

# Option B: Launch dashboard
streamlit run app.py
```

---

## 📚 Common Use Cases

### Use Case 1: Optimize a Portfolio
```python
from src import DataHandler, PortfolioOptimizer

# 1. Fetch data
data = DataHandler(['AAPL', 'MSFT', 'GOOGL', 'AMZN'], period_months=12)
mean_returns, cov_matrix = data.prepare_optimization_data()

# 2. Optimize
optimizer = PortfolioOptimizer(mean_returns, cov_matrix, risk_free_rate=0.02)
weights, metrics = optimizer.optimize('max_sharpe')

# 3. View results
print(f"Expected Return: {metrics['Expected Return']:.2%}")
print(f"Volatility: {metrics['Volatility']:.2%}")
print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.3f}")
```

### Use Case 2: Generate Efficient Frontier
```python
from src import DataHandler, PortfolioOptimizer, PortfolioVisualizer

data = DataHandler(['AAPL', 'MSFT', 'GOOGL'], period_months=12)
mean_returns, cov_matrix = data.prepare_optimization_data()

optimizer = PortfolioOptimizer(mean_returns, cov_matrix)
returns, vols, sharpes = optimizer.generate_efficient_frontier(n_portfolios=100)

viz = PortfolioVisualizer()
fig = viz.plot_efficient_frontier(returns, vols, sharpes)
plt.show()
```

### Use Case 3: Monitor Rebalancing
```python
from src import PortfolioRebalancer
import numpy as np

# Target weights
target_weights = np.array([0.25, 0.25, 0.25, 0.25])
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Current portfolio values (after price changes)
current_values = np.array([28000, 22000, 26000, 24000])

# Monitor
rebalancer = PortfolioRebalancer(target_weights, tickers, drift_threshold=0.05)
monitoring = rebalancer.monitor_portfolio(current_values)

if monitoring['Needs Rebalancing']:
    print("⚠️ Rebalancing needed!")
    for alert in monitoring['Alerts']:
        print(f"{alert['Ticker']}: {alert['Status']}")
```

### Use Case 4: Compare Strategies
```python
from src import DataHandler, PortfolioOptimizer
import pandas as pd

data = DataHandler(['AAPL', 'MSFT', 'GOOGL', 'AMZN'], period_months=12)
mean_returns, cov_matrix = data.prepare_optimization_data()

optimizer = PortfolioOptimizer(mean_returns, cov_matrix)

strategies = ['max_sharpe', 'min_volatility', 'risk_parity', 'equal_weight']
results = {}

for strategy in strategies:
    weights, metrics = optimizer.optimize(strategy)
    results[strategy] = metrics

# Compare
comparison = pd.DataFrame(results).T
print(comparison)
```

---

## 🎯 Optimization Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `max_sharpe` | Maximum Sharpe Ratio | Risk-adjusted returns |
| `min_volatility` | Minimum Volatility | Low risk, stable returns |
| `max_return` | Maximum Return | Aggressive growth |
| `risk_parity` | Equal Risk Contribution | Balanced risk allocation |
| `equal_weight` | 1/N Portfolio | Simplicity, diversification |

---

## 📊 Key Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Sharpe Ratio** | (Return - RFR) / Volatility | Risk-adjusted return (higher is better) |
| **Sortino Ratio** | (Return - RFR) / Downside Dev | Downside risk-adjusted return |
| **Calmar Ratio** | Return / Max Drawdown | Return per unit of downside risk |
| **Max Drawdown** | Max(Peak - Trough) / Peak | Worst peak-to-trough decline |
| **VaR 95%** | 5th percentile return | Maximum loss at 95% confidence |
| **CVaR 95%** | Mean of returns below VaR | Expected loss beyond VaR |

---

## 🔧 Configuration Options

### Data Handler
```python
DataHandler(
    tickers=['AAPL', 'MSFT'],     # List of ticker symbols
    period_months=12,              # 6-60 months
    risk_free_rate=0.02            # Annual risk-free rate (0.02 = 2%)
)
```

### Optimizer
```python
PortfolioOptimizer(
    mean_returns,                  # Expected returns array
    cov_matrix,                    # Covariance matrix
    risk_free_rate=0.02            # Risk-free rate
)

# Optimize with options
optimizer.optimize(
    objective='max_sharpe',        # Strategy
    allow_short=False,             # Allow short selling?
    target_volatility=0.15         # Max volatility (for max_return)
)
```

### Rebalancer
```python
PortfolioRebalancer(
    target_weights,                # Target allocation
    tickers,                       # Asset names
    drift_threshold=0.05           # 5% drift threshold
)
```

---

## 🎨 Visualization Options

### Static (Matplotlib)
```python
viz = PortfolioVisualizer()
fig = viz.plot_weights(weights, tickers, interactive=False)
viz.save_figure(fig, 'allocation.png', dpi=300)
```

### Interactive (Plotly)
```python
viz = PortfolioVisualizer()
fig = viz.plot_weights(weights, tickers, interactive=True)
fig.show()  # Opens in browser
```

---

## 📁 Output Files

### From example.py
- `efficient_frontier.png` - Efficient frontier chart
- `allocation_*.png` - Portfolio allocations for each strategy
- `correlation_matrix.png` - Asset correlation heatmap
- `cumulative_returns.png` - Cumulative returns over time
- `portfolio_weights.csv` - Portfolio weights for all strategies
- `strategy_comparison.csv` - Performance metrics comparison
- `asset_statistics.csv` - Individual asset statistics

---

## ⚡ Performance Tips

1. **Reduce n_portfolios** for faster efficient frontier generation
   ```python
   optimizer.generate_efficient_frontier(n_portfolios=50)  # Instead of 100
   ```

2. **Cache data** for repeated analyses
   ```python
   data.fetch_data()
   data.prices.to_csv('cached_prices.csv')  # Save
   prices = pd.read_csv('cached_prices.csv', index_col=0, parse_dates=True)  # Load
   ```

3. **Use fewer assets** for initial testing
   ```python
   tickers = ['AAPL', 'MSFT', 'GOOGL']  # Start with 3-5 assets
   ```

---

## 🐛 Troubleshooting

### Problem: "No data available for ticker"
**Solution**: Check ticker symbol is correct on Yahoo Finance

### Problem: "Optimization failed to converge"
**Solution**: 
- Increase data period
- Check for highly correlated assets
- Try different initial weights

### Problem: "Singular matrix error"
**Solution**: Remove perfectly correlated assets

### Problem: Streamlit port already in use
**Solution**: 
```powershell
streamlit run app.py --server.port 8502
```

---

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` for detailed setup
2. Review `IMPLEMENTATION_SUMMARY.md` for feature details
3. Run `test_setup.py` to verify installation
4. Examine `example.py` for usage patterns
5. Read docstrings in source code

---

## 🎓 Learning Resources

### Understanding MPT
- Efficient Frontier: Set of optimal portfolios
- Sharpe Ratio: Return per unit of risk
- Diversification: Reduces unsystematic risk
- Risk-Return Tradeoff: Core principle

### Key Concepts
- **Long-only**: No short selling (weights ≥ 0)
- **Risk parity**: Equal risk contribution
- **Rebalancing**: Maintain target allocation
- **Drift**: Deviation from target weights

---

## ✅ Quick Checklist

- [ ] Dependencies installed (`python -m pip install -r requirements.txt`)
- [ ] Tests passed (`python test_setup.py`)
- [ ] Example run completed (`python example.py`)
- [ ] Dashboard launched (`streamlit run app.py`)
- [ ] Understood basic usage patterns
- [ ] Ready to optimize your portfolio!

---

**Happy Optimizing! 📈**
