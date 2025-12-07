# 📈 Portfolio Optimization Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional-grade portfolio optimization platform implementing Modern Portfolio Theory with AI-powered insights, comprehensive educational resources, and interactive visualizations.

## 🌐 Live Demo

**Access the app from anywhere**: [Live Portfolio Optimizer](https://aladinz-portfolio-opt-engine.streamlit.app) *(will be available after deployment)*

Build and optimize your investment portfolio with institutional-quality tools, now accessible to everyone!

## ✨ Features

### Core Optimization
- **5 Optimization Strategies**: Maximum Sharpe Ratio, Minimum Volatility, Maximum Return, Risk Parity, Equal Weight
- **Flexible Portfolio Size**: 3-10 holdings with size-aware recommendations
- **Smart Constraints**: Position limits with feasibility checking and portfolio-size suggestions
- **Efficient Frontier**: Interactive risk-return visualization with your portfolio position

### AI-Powered Insights 🤖
- **Portfolio Health Score**: 0-100 rating with letter grades (A+ to F)
- **Multi-Dimensional Analysis**: Diversification, risk profile, concentration, correlations, strategy effectiveness
- **Actionable Recommendations**: Priority-based improvement suggestions with real-world context
- **Improvement Roadmap**: Step-by-step plan to reach A/B grade portfolios

### Educational Help System 📚
- **Modern Portfolio Theory Guide**: Learn core MPT principles while optimizing
- **Strategy Explanations**: Detailed guides for each optimization approach with formulas
- **Metrics Glossary**: All 8 metrics explained with interpretations and examples
- **Specialized Guides**: Constraints, Monte Carlo, rebalancing, strategy comparison

### Advanced Features
- **Monte Carlo Simulation**: 10,000 scenarios projecting 1-30 year outcomes
- **Strategy Comparison**: Side-by-side analysis of all optimization approaches
- **Rebalancing Analysis**: Drift tracking with buy/sell/hold recommendations
- **Interactive Visualizations**: Plotly charts for efficient frontier, allocations, correlations, returns

### Comprehensive Metrics
- Performance: Expected return, volatility, Sharpe ratio, Sortino ratio, Calmar ratio
- Risk: Maximum drawdown, VaR (95%), CVaR, diversification score
- All metrics include educational explanations and benchmarks

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/aladinz/Portfolio_OPT_Engine.git
cd Portfolio_OPT_Engine
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 🌐 Cloud Deployment (Access from Anywhere)

Deploy your own instance for free on Streamlit Cloud:

1. Fork this repository
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub
3. Click "New app" and select your fork
4. Your app will be live in 2-3 minutes!

**Detailed instructions**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Using the Example Script
```bash
python example.py
```

## 📁 Project Structure

```
Portfolio_Opt_Engine/
├── src/
│   ├── ai_insights.py        # AI analysis with educational context
│   ├── data_handler.py       # Data fetching and preprocessing
│   ├── help_system.py        # Comprehensive educational guides
│   ├── metrics.py            # Portfolio performance metrics
│   ├── monte_carlo.py        # Monte Carlo simulation engine
│   ├── optimizer.py          # Optimization algorithms (5 strategies)
│   ├── rebalancer.py         # Rebalancing logic and drift tracking
│   └── visualizer.py         # Interactive Plotly visualizations
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── app.py                   # Main Streamlit dashboard (1774 lines)
├── example.py               # Command-line usage examples
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── DEPLOYMENT_GUIDE.md     # Cloud deployment instructions
├── SETUP_GUIDE.md          # Detailed setup instructions
├── IMPLEMENTATION_SUMMARY.md # Technical implementation details
├── QUICK_REFERENCE.md      # User guide and workflows
├── PROJECT_REVIEW.md       # Comprehensive project assessment
├── ENHANCEMENT_SUMMARY.md  # Recent improvements changelog
└── HELP_SYSTEM_GUIDE.md   # Help system user guide
```

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy to Streamlit Cloud (FREE)
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation and setup instructions
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - User guide and common workflows
- **[HELP_SYSTEM_GUIDE.md](HELP_SYSTEM_GUIDE.md)** - How to use the educational help system
- **[PROJECT_REVIEW.md](PROJECT_REVIEW.md)** - Comprehensive project assessment (5/5 rating)
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details for developers
- **[ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)** - Recent improvements and educational enhancements

## License

MIT License
