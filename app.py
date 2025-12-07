"""
Streamlit Dashboard for Portfolio Optimization Engine
Updated: 2025-12-07 - v10 (Action items - direct display)
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_handler import DataHandler
from src.optimizer import PortfolioOptimizer
from src.metrics import PortfolioMetrics
from src.visualizer import PortfolioVisualizer
from src.rebalancer import PortfolioRebalancer
from src.monte_carlo import MonteCarloSimulator
from src.ai_insights import AIInsights
from src.help_system import PortfolioHelp


# Page configuration
st.set_page_config(
    page_title="Portfolio Optimization Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        border: none !important;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 10px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        opacity: 0.95 !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #f0f0f0 !important;
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """
    Main application function.
    """
    st.title("📈 Portfolio Optimization Engine")
    st.markdown("### Modern Portfolio Theory with Multiple Optimization Strategies")
    
    # Sidebar inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("---")
        
        # Asset selection
        st.subheader("🎯 Portfolio Holdings")
        st.markdown("*Enter comma-separated tickers*")
        default_tickers = "VTI,BND,SCHD,SCHG,VIG,VXUS,VOO,AGG,VEA,VNQ"
        tickers_input = st.text_input(
            "Portfolio Holdings",
            value=default_tickers,
            help="Enter ETF/fund tickers separated by commas. Flexible: 3-10 holdings (3-5 = Focused, 6-7 = Balanced, 8-10 = Diversified)"
        )
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        
        if len(tickers) < 3:
            st.warning("⚠️ Enter at least 3 tickers for a valid portfolio")
        elif len(tickers) > 10:
            st.info(f"ℹ️ {len(tickers)} assets - consider 3-10 for manageable diversification")
            st.success(f"✓ {len(tickers)} assets selected")
        elif len(tickers) <= 5:
            st.success(f"✓ {len(tickers)} assets selected (Focused portfolio)")
        elif len(tickers) <= 7:
            st.success(f"✓ {len(tickers)} assets selected (Balanced portfolio)")
        else:
            st.success(f"✓ {len(tickers)} assets selected (Well-diversified portfolio)")
        
        st.markdown("---")
        
        # Time period
        st.subheader("📅 Data Period")
        period_months = st.slider(
            "Historical data (months)",
            min_value=6,
            max_value=60,
            value=12,
            step=1,
            help="More data provides better statistics but may not reflect current market conditions"
        )
        st.caption(f"*{period_months} months ≈ {period_months/12:.1f} years*")
        
        st.markdown("---")
        
        # Risk-free rate
        st.subheader("💵 Risk Parameters")
        risk_free_rate = st.number_input(
            "Risk-Free Rate (annual %)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            format="%.1f",
            help="Used for Sharpe ratio calculation. Typical: 2-4% for US Treasury rates"
        ) / 100
        
        st.markdown("---")
        
        # Optimization objective
        st.subheader("🎯 Optimization Strategy")
        
        # Add help button for strategies
        with st.expander("📚 Learn About Optimization Strategies"):
            st.markdown("### Modern Portfolio Theory Overview")
            mpt_help = PortfolioHelp.get_mpt_overview()
            st.markdown(mpt_help['content'])
            st.caption(f"*Reference: {mpt_help['reference']}*")
        
        objective = st.selectbox(
            "Select your goal",
            [
                "Maximum Sharpe Ratio",
                "Minimum Volatility",
                "Maximum Return",
                "Risk Parity",
                "Equal Weight"
            ],
            help="Different strategies optimize for different objectives - click 'Learn About Optimization Strategies' above for details"
        )
        
        # Add detailed explanation for selected strategy
        strategy_key = objective.lower().replace(' ', '_')
        strategy_help = PortfolioHelp.get_strategy_explanation(strategy_key)
        
        with st.expander(f"ℹ️ About {objective}"):
            st.markdown(f"### {strategy_help['title']}")
            st.markdown(strategy_help['description'])
            st.markdown(strategy_help['how_it_works'])
            if 'math' in strategy_help:
                st.latex(strategy_help['math'])
            if 'tips' in strategy_help and strategy_help['tips']:
                st.markdown("**💡 Tips:**")
                for tip in strategy_help['tips']:
                    st.markdown(f"- {tip}")
        
        st.markdown("---")
        
        # Portfolio Constraints
        st.subheader("⚖️ Portfolio Constraints")
        
        # Add help for constraints
        with st.expander("📖 Constraints Guide"):
            constraints_help = PortfolioHelp.get_constraints_guide()
            st.markdown(constraints_help['content'])
        
        use_constraints = st.checkbox(
            "Enable position limits",
            value=True,
            help="Add min/max constraints to ensure diversification across all holdings"
        )
        
        if use_constraints:
            col1, col2 = st.columns(2)
            with col1:
                max_weight = st.slider(
                    "Max weight per asset (%)",
                    min_value=10,
                    max_value=50,
                    value=20,
                    step=5,
                    help="Maximum allocation to any single asset (Suggested: 20-25% for 3-5 assets, 15-20% for 6-10 assets)"
                ) / 100
            
            with col2:
                min_weight = st.slider(
                    "Min weight per asset (%)",
                    min_value=0,
                    max_value=20,
                    value=8,
                    step=2,
                    help="Minimum allocation to each asset (Suggested: 10-15% for 3-5 assets, 8-12% for 6-10 assets)"
                ) / 100
            
            num_assets = len(tickers)
            if min_weight > 0:
                min_total = min_weight * num_assets * 100
                if min_total > 100:
                    st.error(f"⚠️ Infeasible: {num_assets} assets × {min_weight*100:.0f}% min = {min_total:.0f}% (must be ≤100%)")
                    
                    # Suggest maximum feasible min_weight
                    max_feasible_min = (100 / num_assets) - 1
                    st.info(f"💡 With {num_assets} assets, max feasible min weight is ~{max_feasible_min:.0f}%")
                else:
                    st.success(f"✓ With {num_assets} assets: Min total = {min_total:.0f}%, Max position = {max_weight*100:.0f}%")
        else:
            max_weight = 1.0
            min_weight = 0.0
        
        st.markdown("---")
        
        # Rebalancing settings
        st.subheader("🔄 Rebalancing")
        drift_threshold = st.slider(
            "Drift threshold (%)",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Trigger rebalancing when any asset drifts this much from target"
        ) / 100
        st.caption(f"*Alert when drift > {drift_threshold*100:.0f}%*")
        
        st.markdown("---")
        
        # Run optimization button
        run_optimization = st.button(
            "🚀 Run Optimization", 
            type="primary", 
            use_container_width=True,
            help="Click to fetch data and optimize portfolio"
        )
        
        st.markdown("---")
        st.caption("💡 **Tip**: Start with 3-5 diverse assets for best results")
    
    # Main content area
    if run_optimization:
        with st.spinner("Fetching data and optimizing portfolio..."):
            try:
                # Fetch data
                st.subheader("📊 Data Loading")
                data_handler = DataHandler(tickers, period_months, risk_free_rate)
                prices = data_handler.fetch_data()
                returns = data_handler.calculate_returns()
                
                # Check if we have valid data
                if len(data_handler.tickers) == 0:
                    st.error("❌ No valid data found for the provided tickers. Please check your ticker symbols and try again.")
                    st.info("💡 Tips:\n- Make sure tickers are valid Yahoo Finance symbols\n- Try common stocks like AAPL, MSFT, GOOGL\n- For crypto, use format: BTC-USD, ETH-USD")
                    return
                
                st.success(f"✓ Successfully loaded data for {len(data_handler.tickers)} assets")
                
                # Display asset statistics
                with st.expander("📈 Individual Asset Statistics", expanded=False):
                    stats = data_handler.get_asset_statistics()
                    
                    # Add color coding for better readability
                    styled_stats = stats.style.format({
                        'Mean Return (Annual)': '{:.2%}',
                        'Volatility (Annual)': '{:.2%}',
                        'Sharpe Ratio': '{:.3f}',
                        'Min': '{:.4f}',
                        'Max': '{:.4f}',
                        'Skewness': '{:.3f}',
                        'Kurtosis': '{:.3f}'
                    }).background_gradient(subset=['Sharpe Ratio'], cmap='RdYlGn')
                    
                    st.dataframe(styled_stats, use_container_width=True)
                    
                    st.info("💡 **Tip**: Higher Sharpe Ratios indicate better risk-adjusted returns for individual assets")
                
                # Prepare optimization data
                mean_returns, cov_matrix = data_handler.prepare_optimization_data()
                
                # Run optimization
                st.subheader("🎯 Portfolio Optimization")
                optimizer = PortfolioOptimizer(mean_returns, cov_matrix, risk_free_rate)
                
                # Map objective names to function calls
                objective_map = {
                    "Maximum Sharpe Ratio": "max_sharpe",
                    "Minimum Volatility": "min_volatility",
                    "Maximum Return": "max_return",
                    "Risk Parity": "risk_parity",
                    "Equal Weight": "equal_weight"
                }
                
                # Pass weight constraints to optimizer if enabled
                kwargs = {}
                if objective_map[objective] in ['max_sharpe', 'min_volatility', 'max_return', 'risk_parity']:
                    kwargs['min_weight'] = min_weight if use_constraints else 0.0
                    kwargs['max_weight'] = max_weight if use_constraints else 1.0
                
                optimal_weights, basic_metrics = optimizer.optimize(objective_map[objective], **kwargs)
                
                # Store in session state for persistence across interactions
                st.session_state['optimization_complete'] = True
                st.session_state['data_handler'] = data_handler
                st.session_state['optimizer'] = optimizer
                st.session_state['optimal_weights'] = optimal_weights
                st.session_state['mean_returns'] = mean_returns
                st.session_state['cov_matrix'] = cov_matrix
                st.session_state['returns'] = returns
                st.session_state['prices'] = prices
                st.session_state['risk_free_rate'] = risk_free_rate
                st.session_state['objective'] = objective
                st.session_state['drift_threshold'] = drift_threshold
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
                if "No valid data" in str(e) or "No data returned" in str(e):
                    st.warning("**Possible causes:**")
                    st.markdown("""
                    - **Invalid ticker symbols**: Make sure tickers exist on Yahoo Finance
                    - **Internet connection**: Check your network connection
                    - **Market hours**: Some data may not be available immediately
                    - **Delisted stocks**: The ticker may no longer be traded
                    
                    **Try these working examples:**
                    - US Stocks: `AAPL,MSFT,GOOGL,AMZN`
                    - ETFs: `SPY,QQQ,GLD,TLT`
                    - Crypto: `BTC-USD,ETH-USD`
                    """)
                
                # Show the debug output if available
                with st.expander("🔍 Debug Information"):
                    st.code(str(e))
                    st.write("Check the terminal/console for detailed error messages.")
    
    # Display results if optimization has been completed (either just now or from session state)
    if st.session_state.get('optimization_complete', False):
        # Load from session state
        data_handler = st.session_state['data_handler']
        optimizer = st.session_state['optimizer']
        optimal_weights = st.session_state['optimal_weights']
        mean_returns = st.session_state['mean_returns']
        cov_matrix = st.session_state['cov_matrix']
        returns = st.session_state['returns']
        prices = st.session_state['prices']
        risk_free_rate = st.session_state['risk_free_rate']
        objective = st.session_state['objective']
        drift_threshold = st.session_state['drift_threshold']
        
        # Calculate all metrics
        all_metrics = PortfolioMetrics.get_all_metrics(
            optimal_weights, mean_returns, cov_matrix, 
            returns, risk_free_rate
        )
        
        # Display metrics in columns
        st.markdown(f"**Optimization Strategy:** {objective}")
        st.markdown("---")
        
        # Primary metrics with better styling
        st.markdown("---")
        st.subheader("📊 Key Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Expected Return",
                value=f"{all_metrics['Expected Return']:.2%}",
                help="Annualized expected return based on historical data"
            )
        
        with col2:
            st.metric(
                label="Volatility (Risk)",
                value=f"{all_metrics['Volatility']:.2%}",
                help="Annualized standard deviation of returns"
            )
        
        with col3:
            st.metric(
                label="Sharpe Ratio",
                value=f"{all_metrics['Sharpe Ratio']:.3f}",
                delta="Higher is better" if all_metrics['Sharpe Ratio'] > 1 else None,
                help="Risk-adjusted return (Return - Risk-free rate) / Volatility"
            )
        
        with col4:
            st.metric(
                label="Max Drawdown",
                value=f"{all_metrics['Maximum Drawdown']:.2%}",
                delta="Risk measure" if all_metrics['Maximum Drawdown'] < -0.1 else None,
                delta_color="inverse",
                help="Maximum peak-to-trough decline"
            )
        
        # Secondary metrics
        st.markdown("---")
        st.subheader("📈 Advanced Risk Metrics")
        
        # Add metrics explanation expander
        with st.expander("📖 Understanding Portfolio Metrics"):
            metrics_help = PortfolioHelp.get_metrics_explanation()
            
            for metric_name, metric_info in metrics_help.items():
                st.markdown(f"**{metric_name}**")
                st.markdown(f"*{metric_info['description']}*")
                st.latex(metric_info['formula'])
                st.markdown(f"**Interpretation**: {metric_info['interpretation']}")
                st.markdown(f"**Example**: {metric_info['example']}")
                st.markdown("---")
        
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric(
                label="Sortino Ratio",
                value=f"{all_metrics['Sortino Ratio']:.3f}",
                help="Downside risk-adjusted return"
            )
        
        with col6:
            st.metric(
                label="Calmar Ratio",
                value=f"{all_metrics['Calmar Ratio']:.3f}",
                help="Return / Maximum Drawdown"
            )
        
        with col7:
            st.metric(
                label="VaR (95%)",
                value=f"{all_metrics['VaR (95%)']:.2%}",
                help="Value at Risk - potential loss at 95% confidence"
            )
        
        with col8:
            st.metric(
                label="CVaR (95%)",
                value=f"{all_metrics['CVaR (95%)']:.2%}",
                help="Conditional VaR - expected loss beyond VaR"
            )
        
        # Portfolio weights
        st.markdown("---")
        st.subheader("💼 Portfolio Allocation")
        
        weights_df = pd.DataFrame({
            'Asset': data_handler.tickers,
            'Weight': optimal_weights,
            'Weight (%)': optimal_weights * 100
        }).sort_values('Weight', ascending=False)
        
        # Filter out zero weights for cleaner display
        weights_df_display = weights_df[weights_df['Weight'] > 0.001].copy()
        
        # Show summary info
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Total Holdings", f"{len(data_handler.tickers)}")
        with col_info2:
            st.metric("Allocated Assets", f"{len(weights_df_display)}")
        with col_info3:
            st.metric("Largest Position", f"{optimal_weights.max()*100:.1f}%")
        
        st.markdown("")
        
        # Visual allocation first (full width)
        st.markdown("**📊 Visual Allocation**")
        visualizer = PortfolioVisualizer()
        
        # Pass the filtered weights and tickers for visualization
        display_mask = optimal_weights > 0.001
        display_weights = optimal_weights[display_mask]
        display_tickers = [t for t, m in zip(data_handler.tickers, display_mask) if m]
        
        fig = visualizer.plot_weights(
            display_weights, 
            display_tickers,
            title=f"{objective}",
            interactive=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table and summary below
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**📋 Detailed Allocation**")
            st.dataframe(
                weights_df_display.style.format({
                    'Weight': '{:.4f}',
                    'Weight (%)': '{:.2f}%'
                }).background_gradient(subset=['Weight (%)'], cmap='Blues'),
                hide_index=True,
                use_container_width=True,
                height=min(350, len(weights_df_display) * 35 + 38)
            )
        
        with col2:
            st.subheader("📈 Portfolio Summary")
            
            # Total assets with meaningful allocation
            total_assets = len(weights_df_display)
            st.metric(
                label="Total Assets", 
                value=str(total_assets),
                help="Number of assets with >0.1% allocation"
            )
            
            # Largest position
            st.metric(
                label="Largest Position", 
                value=f"{weights_df_display.iloc[0]['Asset']}", 
                delta=f"{weights_df_display.iloc[0]['Weight (%)']:.1f}%"
            )
            
            # Top 3 concentration
            top3_concentration = weights_df_display.head(3)['Weight (%)'].sum()
            st.metric(
                label="Top 3 Concentration", 
                value=f"{top3_concentration:.1f}%",
                help="Combined weight of three largest positions"
            )
            
            # Diversification score (using all weights, not just displayed)
            herfindahl = (optimal_weights ** 2).sum()
            diversification_score = (1 - herfindahl) * 100
            
            # Color indicator based on score
            if diversification_score >= 70:
                score_emoji = "🟢"
            elif diversification_score >= 50:
                score_emoji = "🟡"
            else:
                score_emoji = "🔴"
            
            st.metric(
                label="Diversification Score", 
                value=f"{score_emoji} {diversification_score:.0f}/100",
                help="Higher = more diversified. Based on Herfindahl-Hirschman Index. 🟢 70+, 🟡 50-70, 🔴 <50"
            )
        
        with col_info3:
            # Portfolio Classification based on risk/return profile
            expected_return = all_metrics['Expected Return']
            volatility = all_metrics['Volatility']
            
            # Classification logic
            if volatility < 0.06:  # Very low risk
                if expected_return < 0.04:
                    portfolio_type = "🛡️ Ultra Conservative"
                    type_color = "#4CAF50"
                    description = "Very low risk, capital preservation focus"
                else:
                    portfolio_type = "💎 Income Focus"
                    type_color = "#2196F3"
                    description = "Low risk with income generation"
            elif volatility < 0.10:  # Low-moderate risk
                if expected_return < 0.07:
                    portfolio_type = "🏦 Conservative"
                    type_color = "#8BC34A"
                    description = "Low risk, stable returns"
                else:
                    portfolio_type = "⚖️ Balanced"
                    type_color = "#FFC107"
                    description = "Moderate risk-return balance"
            elif volatility < 0.15:  # Moderate risk
                if expected_return < 0.10:
                    portfolio_type = "📈 Growth & Income"
                    type_color = "#FF9800"
                    description = "Moderate growth with some stability"
                else:
                    portfolio_type = "🚀 Growth"
                    type_color = "#FF5722"
                    description = "Higher returns, moderate risk"
            else:  # High risk
                if expected_return > 0.12:
                    portfolio_type = "⚡ Aggressive Growth"
                    type_color = "#F44336"
                    description = "High risk, high return potential"
                else:
                    portfolio_type = "⚠️ High Volatility"
                    type_color = "#9C27B0"
                    description = "High risk without proportional return"
            
            st.metric(
                label="Portfolio Type",
                value=portfolio_type,
                help=f"{description} | Return: {expected_return:.1%}, Risk: {volatility:.1%}"
            )
            st.markdown(f"<p style='font-size: 0.8em; color: gray; margin-top: -10px;'>{description}</p>", 
                       unsafe_allow_html=True)
        
        # AI Insights and Recommendations
        st.markdown("---")
        st.subheader("🤖 AI Insights & Recommendations")
        
        # Add AI Insights guide
        with st.expander("📖 Understanding AI Insights & Health Score"):
            ai_guide = PortfolioHelp.get_ai_insights_guide()
            st.markdown(ai_guide['content'])
        
        with st.spinner("Analyzing portfolio with AI..."):
            # Generate comprehensive AI insights
            ai_insights = AIInsights.analyze_portfolio(
                weights=optimal_weights,
                tickers=tickers,
                metrics=all_metrics,
                returns=returns,
                mean_returns=mean_returns,
                cov_matrix=cov_matrix,
                strategy=objective
            )
            
            # Calculate portfolio health score
            health_score, health_grade = AIInsights.get_portfolio_health_score(
                ai_insights, all_metrics, n_assets=len(tickers)
            )
            
            # Display health score prominently
            col_health1, col_health2, col_health3 = st.columns([1, 2, 1])
            
            with col_health2:
                # Determine color based on score
                if health_score >= 80:
                    score_color = "#4CAF50"  # Green
                    score_emoji = "🌟"
                elif health_score >= 60:
                    score_color = "#FFC107"  # Yellow
                    score_emoji = "⭐"
                else:
                    score_color = "#FF5722"  # Red
                    score_emoji = "⚠️"
                
                st.markdown(
                    f"<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {score_color}22, {score_color}11); border-radius: 15px; border: 2px solid {score_color};'>"
                    f"<h2 style='color: {score_color}; margin: 0;'>{score_emoji} Portfolio Health Score</h2>"
                    f"<h1 style='color: {score_color}; font-size: 3.5em; margin: 10px 0;'>{health_score}</h1>"
                    f"<h3 style='color: {score_color}; margin: 0;'>{health_grade}</h3>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            st.markdown("")
            
            # Display insights in organized sections
            if ai_insights['strengths']:
                with st.expander(f"💪 Portfolio Strengths ({len(ai_insights['strengths'])} identified)", expanded=True):
                    for strength in ai_insights['strengths']:
                        st.markdown(strength)
                        st.markdown("")
            
            if ai_insights['opportunities']:
                with st.expander(f"✨ Opportunities ({len(ai_insights['opportunities'])} identified)", expanded=True):
                    for opportunity in ai_insights['opportunities']:
                        st.markdown(opportunity)
                        st.markdown("")
            
            if ai_insights['recommendations']:
                with st.expander(f"💡 Recommendations ({len(ai_insights['recommendations'])} identified)", expanded=True):
                    for rec in ai_insights['recommendations']:
                        st.markdown(rec)
                        st.markdown("")
            
            if ai_insights['risk_alerts']:
                with st.expander(f"⚠️ Risk Alerts ({len(ai_insights['risk_alerts'])} identified)", expanded=True):
                    st.warning("Review these risk factors carefully before investing:")
                    for alert in ai_insights['risk_alerts']:
                        st.markdown(alert)
                        st.markdown("")
            
            if ai_insights['weaknesses']:
                with st.expander(f"🔧 Areas for Improvement ({len(ai_insights['weaknesses'])} identified)", expanded=False):
                    for weakness in ai_insights['weaknesses']:
                        st.markdown(weakness)
                        st.markdown("")
            
            # Generate and display action items
            st.markdown("---")
            st.markdown("### 📋 Prioritized Action Items")
            
            # Display by priority
            has_actions = False
            
            # High Priority - Risk Alerts
            if ai_insights.get('risk_alerts'):
                has_actions = True
                st.markdown("#### 🔴 High Priority - Address Risk Concerns")
                for i, alert in enumerate(ai_insights['risk_alerts'][:3], 1):
                    st.markdown(f"{i}. {alert}")
                st.markdown("")
            
            # Medium Priority - Weaknesses
            if ai_insights.get('weaknesses'):
                has_actions = True
                st.markdown("#### 🟡 Medium Priority - Improve Weaknesses")
                for i, weakness in enumerate(ai_insights['weaknesses'][:2], 1):
                    st.markdown(f"{i}. {weakness}")
                st.markdown("")
            
            # Low Priority - Recommendations
            if ai_insights.get('recommendations'):
                has_actions = True
                st.markdown("#### 🟢 Consider for Optimization")
                for i, rec in enumerate(ai_insights['recommendations'][:3], 1):
                    st.markdown(f"{i}. {rec}")
                st.markdown("")
            
            if not has_actions:
                st.success("🎉 No critical action items - your portfolio is well-optimized!")
            
            # Show improvement plan for scores below 70
            if health_score < 70:
                st.markdown("---")
                st.markdown("### 🎯 Roadmap to Grade A/B")
                
                improvement_plan = AIInsights.generate_improvement_plan(
                    ai_insights, all_metrics, health_score, health_grade,
                    n_assets=len(tickers),
                    constraints_enabled=use_constraints,
                    min_weight=min_weight,
                    max_weight=max_weight
                )
                
                col_plan1, col_plan2, col_plan3 = st.columns(3)
                
                with col_plan1:
                    st.metric(
                        "Current Grade",
                        health_grade.split()[0],
                        delta=f"{health_score} points"
                    )
                
                with col_plan2:
                    st.metric(
                        "Grade B Target",
                        "70 points",
                        delta=f"+{improvement_plan['points_needed_for_b']} needed",
                        delta_color="inverse"
                    )
                
                with col_plan3:
                    st.metric(
                        "Grade A Target",
                        "80 points",
                        delta=f"+{improvement_plan['points_needed_for_a']} needed",
                        delta_color="inverse"
                    )
                
                # Show achievability assessment
                if improvement_plan['confidence'] == 'High':
                    st.success(f"✅ {improvement_plan['summary']} | Potential gain: +{improvement_plan['total_potential_gain']} points")
                else:
                    st.warning(f"⚠️ {improvement_plan['summary']}")
                
                st.info(f"⏱️ **Timeframe**: {improvement_plan['timeframe']}")
                
                # Priority Actions
                if improvement_plan['priority_actions']:
                    st.markdown("#### 🔴 Priority Actions (Highest Impact)")
                    for action in improvement_plan['priority_actions']:
                        with st.expander(action.split('\n')[0], expanded=True):
                            st.markdown(action)
                
                # Quick Wins
                if improvement_plan['quick_wins']:
                    st.markdown("#### ⚡ Quick Wins (Easy Improvements)")
                    for win in improvement_plan['quick_wins']:
                        with st.expander(win.split('\n')[0]):
                            st.markdown(win)
                
                # Long-term Improvements
                if improvement_plan['long_term_improvements']:
                    st.markdown("#### 📅 Long-Term Improvements")
                    for improvement in improvement_plan['long_term_improvements']:
                        with st.expander(improvement.split('\n')[0]):
                            st.markdown(improvement)
                
                st.markdown("---")
                st.info(
                    "💡 **Pro Tip**: Start with Priority Actions for maximum impact. "
                    "Quick Wins can often boost your score by 10-20 points in a single rebalance!"
                )
            
            st.info(
                "💡 **How to Use AI Insights**: These recommendations are based on modern portfolio theory, "
                "risk metrics, and diversification analysis. Use them to refine your portfolio strategy, "
                "but always consider your personal financial situation, goals, and risk tolerance."
            )
        
        # Strategy Comparison
        st.markdown("---")
        st.subheader("⚖️ Strategy Comparison")
        
        st.markdown("""
        **Compare Multiple Optimization Strategies**  
        See how different approaches would allocate your portfolio and their expected outcomes.
        """)
        
        compare_strategies = st.checkbox("Enable strategy comparison", value=False, key="compare_strat")
        
        if compare_strategies:
            with st.spinner("Comparing all strategies..."):
                strategies_to_compare = {
                    "Maximum Sharpe Ratio": "max_sharpe",
                    "Minimum Volatility": "min_volatility",
                    "Risk Parity": "risk_parity",
                    "Equal Weight": "equal_weight"
                }
                
                comparison_results = {}
                
                for strategy_name, strategy_code in strategies_to_compare.items():
                    try:
                        kwargs = {}
                        if strategy_code in ['max_sharpe', 'min_volatility', 'risk_parity']:
                            kwargs['min_weight'] = min_weight if use_constraints else 0.0
                            kwargs['max_weight'] = max_weight if use_constraints else 1.0
                        
                        weights, metrics = optimizer.optimize(strategy_code, **kwargs)
                        
                        # Calculate full metrics
                        full_metrics = PortfolioMetrics.get_all_metrics(
                            weights, mean_returns, cov_matrix, returns, risk_free_rate
                        )
                        
                        comparison_results[strategy_name] = {
                            'weights': weights,
                            'metrics': full_metrics
                        }
                    except Exception as e:
                        st.warning(f"Could not optimize {strategy_name}: {str(e)}")
                
                # Create comparison table
                comparison_data = []
                for strategy_name, result in comparison_results.items():
                    m = result['metrics']
                    comparison_data.append({
                        'Strategy': strategy_name,
                        'Expected Return': m['Expected Return'],
                        'Volatility': m['Volatility'],
                        'Sharpe Ratio': m['Sharpe Ratio'],
                        'Sortino Ratio': m['Sortino Ratio'],
                        'Max Drawdown': m['Maximum Drawdown'],
                        'VaR (95%)': m['VaR (95%)'],
                        'Allocated Assets': np.sum(result['weights'] > 0.001)
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                
                # Sort by Sharpe Ratio descending for better display
                comparison_df = comparison_df.sort_values('Sharpe Ratio', ascending=False).reset_index(drop=True)
                
                # Highlight your current strategy
                def highlight_current(row):
                    if row['Strategy'] == objective:
                        return ['background-color: #e3f2fd'] * len(row)
                    return [''] * len(row)
                
                st.markdown("**📊 Performance Comparison**")
                
                # Use st.dataframe without complex styling to avoid display issues
                st.dataframe(
                    comparison_df.style.format({
                        'Expected Return': '{:.2%}',
                        'Volatility': '{:.2%}',
                        'Sharpe Ratio': '{:.3f}',
                        'Sortino Ratio': '{:.3f}',
                        'Max Drawdown': '{:.2%}',
                        'VaR (95%)': '{:.2%}',
                        'Allocated Assets': '{:.0f}'
                    }).background_gradient(
                        subset=['Sharpe Ratio'], cmap='RdYlGn', vmin=0, vmax=2
                    ),
                    hide_index=True, 
                    use_container_width=True
                )
                st.caption(f"🔵 Your current strategy: **{objective}** (Sharpe: {comparison_df[comparison_df['Strategy'] == objective]['Sharpe Ratio'].values[0]:.3f})")
                
                # Add strategy comparison guide
                with st.expander("📖 How to Compare Strategies"):
                    comparison_guide = PortfolioHelp.get_strategy_comparison_guide()
                    st.markdown(comparison_guide['content'])
                
                # Allocation comparison chart
                st.markdown("**📊 Allocation Comparison**")
                
                # Create allocation comparison visualization
                import plotly.graph_objects as go
                
                fig_alloc_compare = go.Figure()
                
                # Only show assets that are allocated in at least one strategy
                all_allocated_assets = set()
                for result in comparison_results.values():
                    allocated = [data_handler.tickers[i] for i, w in enumerate(result['weights']) if w > 0.001]
                    all_allocated_assets.update(allocated)
                
                all_allocated_assets = sorted(list(all_allocated_assets))
                
                for strategy_name, result in comparison_results.items():
                    weights_dict = {ticker: weight for ticker, weight in zip(data_handler.tickers, result['weights'])}
                    strategy_weights = [weights_dict.get(ticker, 0) * 100 for ticker in all_allocated_assets]
                    
                    fig_alloc_compare.add_trace(go.Bar(
                        name=strategy_name,
                        x=all_allocated_assets,
                        y=strategy_weights,
                        text=[f"{w:.1f}%" if w > 0 else "" for w in strategy_weights],
                        textposition='auto'
                    ))
                
                fig_alloc_compare.update_layout(
                    barmode='group',
                    title="Weight Allocation by Strategy",
                    xaxis_title="Asset",
                    yaxis_title="Weight (%)",
                    template="plotly_white",
                    height=400
                )
                
                st.plotly_chart(fig_alloc_compare, use_container_width=True)
                
                # Risk-Return scatter
                st.markdown("**📈 Risk-Return Profile**")
                
                fig_risk_return = go.Figure()
                
                for strategy_name, result in comparison_results.items():
                    m = result['metrics']
                    is_current = (strategy_name == objective)
                    
                    fig_risk_return.add_trace(go.Scatter(
                        x=[m['Volatility'] * 100],
                        y=[m['Expected Return'] * 100],
                        mode='markers+text',
                        name=strategy_name,
                        text=[strategy_name],
                        textposition='top center',
                        marker=dict(
                            size=15 if is_current else 12,
                            symbol='star' if is_current else 'circle',
                            line=dict(width=2, color='DarkSlateGrey' if is_current else 'white')
                        )
                    ))
                
                fig_risk_return.update_layout(
                    title="Strategy Risk-Return Comparison",
                    xaxis_title="Volatility (Risk) %",
                    yaxis_title="Expected Return %",
                    template="plotly_white",
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig_risk_return, use_container_width=True)
                
                st.info("💡 **How to Use**: Look for the strategy with the best balance of return and risk for your goals. Your current strategy is marked with a star ⭐")
        
        # Efficient Frontier
        st.markdown("---")
        st.subheader("📉 Efficient Frontier Analysis")
        
        with st.spinner("Generating efficient frontier..."):
            ef_returns, ef_vols, ef_sharpes = optimizer.generate_efficient_frontier(n_portfolios=50)
            
            # Get other optimal points for comparison
            max_sharpe_weights, _ = optimizer.optimize_max_sharpe()
            min_vol_weights, _ = optimizer.optimize_min_volatility()
            
            optimal_points = {
            objective: (
            PortfolioMetrics.portfolio_return(optimal_weights, mean_returns),
            PortfolioMetrics.portfolio_volatility(optimal_weights, cov_matrix)
            ),
            'Max Sharpe': (
            PortfolioMetrics.portfolio_return(max_sharpe_weights, mean_returns),
            PortfolioMetrics.portfolio_volatility(max_sharpe_weights, cov_matrix)
            ),
            'Min Volatility': (
            PortfolioMetrics.portfolio_return(min_vol_weights, mean_returns),
            PortfolioMetrics.portfolio_volatility(min_vol_weights, cov_matrix)
            )
            }
            
            # Remove duplicates
            if objective in ['Maximum Sharpe Ratio', 'Max Sharpe']:
                optimal_points = {k: v for k, v in optimal_points.items() if k != 'Max Sharpe' or k == objective}
            elif objective == 'Minimum Volatility':
                optimal_points = {k: v for k, v in optimal_points.items() if k != 'Min Volatility' or k == objective}
            
            fig_ef = visualizer.plot_efficient_frontier(
                ef_returns, ef_vols, ef_sharpes,
                optimal_points=optimal_points,
                show_cml=True,
                risk_free_rate=risk_free_rate,
            interactive=True
            )
            st.plotly_chart(fig_ef, use_container_width=True)
            
            # Add interpretation
            with st.expander("ℹ️ Understanding the Efficient Frontier"):
                st.markdown("""
                **What is the Efficient Frontier?**
                - The curve shows optimal portfolios offering the highest expected return for each level of risk
                - Points below the curve are sub-optimal (can achieve better return for same risk)
                - The **Capital Market Line (CML)** shows portfolios combining the risk-free asset with the optimal risky portfolio
                
                **Key Points:**
                - 🌟 **Max Sharpe**: Best risk-adjusted returns (highest Sharpe ratio)
                - 🛡️ **Min Volatility**: Lowest risk portfolio
                - 📍 **Your Portfolio**: Currently selected optimization strategy
                
                **Color Legend:** Darker colors indicate higher Sharpe ratios
                """)
            
            # Correlation Matrix
            with st.expander("🔗 Asset Correlation Matrix", expanded=False):
                st.markdown("**Understanding Correlations:**")
                st.markdown("- Values close to **+1**: Assets move together (high correlation)")
                st.markdown("- Values close to **-1**: Assets move opposite (negative correlation)")  
                st.markdown("- Values close to **0**: Assets move independently (low correlation)")
                st.markdown("- **Diversification tip**: Mix low-correlated assets to reduce portfolio risk")
                st.markdown("---")
                corr_matrix = data_handler.get_correlation_matrix()
                fig_corr = visualizer.plot_correlation_matrix(corr_matrix, interactive=True)
                st.plotly_chart(fig_corr, use_container_width=True)
            
            # Cumulative Returns
            with st.expander("📊 Cumulative Returns Over Time", expanded=False):
                st.markdown("**Portfolio Performance vs Individual Assets**")
                st.markdown("Compare how your optimized portfolio would have performed against individual assets")
                st.markdown("---")
                fig_cum = visualizer.plot_cumulative_returns(
                    returns, 
                    weights=optimal_weights,
                    interactive=True
                )
                st.plotly_chart(fig_cum, use_container_width=True)
            
            # Monte Carlo Simulation
            st.markdown("---")
            st.subheader("🎯 Monte Carlo Forecast")
            
            # Add Monte Carlo guide
            with st.expander("📖 Understanding Monte Carlo Simulation"):
                mc_guide = PortfolioHelp.get_monte_carlo_guide()
                st.markdown(mc_guide['content'])
            
            st.markdown("""
            **Future Portfolio Projections**  
            See probability distributions of future portfolio values based on historical risk/return characteristics.
            """)
            
            mc_simulator = MonteCarloSimulator(mean_returns, cov_matrix)
            
            # Input parameters
            col1, col2, col3 = st.columns(3)
            with col1:
                mc_initial = st.number_input("Initial Investment ($)", value=100000, step=10000, min_value=1000, key="mc_initial")
            with col2:
                mc_years = st.selectbox("Time Horizon", [1, 3, 5, 10, 15, 20, 30], index=2, key="mc_years")
            with col3:
                mc_contribution = st.number_input("Annual Contribution ($)", value=0, step=1000, min_value=0, key="mc_contrib")
            
            run_mc = st.button("🎲 Run Monte Carlo Simulation", use_container_width=True, type="primary", key="run_mc")
            
            if run_mc:
                with st.spinner(f"Running 10,000 simulations over {mc_years} years..."):
                    mc_result = mc_simulator.simulate_portfolio(
                        optimal_weights,
                        mc_initial,
                        mc_years,
                        n_simulations=10000,
                        annual_contribution=mc_contribution
                    )
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("**📊 Simulation Results**")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Expected Value", f"${mc_result['expected_value']:,.0f}")
                    with col2:
                        st.metric("Median Value", f"${mc_result['percentiles']['50th']:,.0f}")
                    with col3:
                        growth_rate = ((mc_result['expected_value'] / mc_initial) ** (1/mc_years) - 1)
                        st.metric("Avg Annual Growth", f"{growth_rate:.2%}")
                    with col4:
                        prob_gain = (1 - mc_result['prob_loss'])
                        st.metric("Probability of Gain", f"{prob_gain:.1%}")
                    
                    # Percentile table
                    st.markdown("**📈 Outcome Probabilities**")
                    percentile_df = pd.DataFrame({
                        'Confidence Level': ['10% Chance', '25% Chance', '50% Chance (Median)', '75% Chance', '90% Chance'],
                        'Portfolio Value': [
                            f"${mc_result['percentiles']['90th']:,.0f}",
                            f"${mc_result['percentiles']['75th']:,.0f}",
                            f"${mc_result['percentiles']['50th']:,.0f}",
                            f"${mc_result['percentiles']['25th']:,.0f}",
                            f"${mc_result['percentiles']['10th']:,.0f}"
                        ],
                        'Interpretation': [
                            'Best case - only 10% chance to exceed',
                            'Optimistic - 25% chance to exceed',
                            'Typical outcome',
                            'Conservative - 75% chance to exceed',
                            'Worst case - 90% chance to exceed'
                        ]
                    })
                    st.dataframe(percentile_df, hide_index=True, use_container_width=True)
                    
                    # Distribution chart
                    st.markdown("**📊 Distribution of Final Values**")
                    import plotly.graph_objects as go
                    import plotly.express as px
                    
                    fig_dist = go.Figure()
                    
                    # Histogram
                    fig_dist.add_trace(go.Histogram(
                        x=mc_result['final_values'],
                        nbinsx=50,
                        name='Frequency',
                        marker_color='#636EFA',
                        opacity=0.7
                    ))
                    
                    # Add percentile lines
                    fig_dist.add_vline(x=mc_result['percentiles']['10th'], line_dash="dash", line_color="red", 
                                      annotation_text="10th %ile", annotation_position="top")
                    fig_dist.add_vline(x=mc_result['percentiles']['50th'], line_dash="solid", line_color="green", 
                                      annotation_text="Median", annotation_position="top")
                    fig_dist.add_vline(x=mc_result['percentiles']['90th'], line_dash="dash", line_color="blue", 
                                      annotation_text="90th %ile", annotation_position="top")
                    
                    fig_dist.update_layout(
                        title=f"Distribution of Portfolio Values After {mc_years} Years",
                        xaxis_title="Portfolio Value ($)",
                        yaxis_title="Frequency",
                        showlegend=False,
                        template="plotly_white"
                    )
                    
                    st.plotly_chart(fig_dist, use_container_width=True)
                    
                    # Sample paths chart
                    st.markdown("**📈 Sample Portfolio Growth Paths**")
                    
                    fig_paths = go.Figure()
                    
                    # Plot sample paths (show 100 random paths)
                    sample_indices = np.random.choice(len(mc_result['paths']), 100, replace=False)
                    years_array = np.arange(0, mc_years + 1)
                    
                    for idx in sample_indices:
                        fig_paths.add_trace(go.Scatter(
                            x=years_array,
                            y=mc_result['paths'][idx],
                            mode='lines',
                            line=dict(width=0.5, color='lightblue'),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                    
                    # Add percentile paths
                    percentile_paths = {
                        '10th': np.percentile(mc_result['paths'], 10, axis=0),
                        '50th': np.percentile(mc_result['paths'], 50, axis=0),
                        '90th': np.percentile(mc_result['paths'], 90, axis=0)
                    }
                    
                    fig_paths.add_trace(go.Scatter(
                        x=years_array, y=percentile_paths['90th'],
                        mode='lines', name='90th Percentile',
                        line=dict(width=3, color='green')
                    ))
                    fig_paths.add_trace(go.Scatter(
                        x=years_array, y=percentile_paths['50th'],
                        mode='lines', name='Median',
                        line=dict(width=3, color='orange')
                    ))
                    fig_paths.add_trace(go.Scatter(
                        x=years_array, y=percentile_paths['10th'],
                        mode='lines', name='10th Percentile',
                        line=dict(width=3, color='red')
                    ))
                    
                    fig_paths.update_layout(
                        title=f"Portfolio Growth Projections ({mc_years} Years)",
                        xaxis_title="Years",
                        yaxis_title="Portfolio Value ($)",
                        template="plotly_white",
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig_paths, use_container_width=True)
                    
                    # Risk metrics
                    st.markdown("**⚠️ Risk Metrics**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Value at Risk (95%)", f"${mc_result['var_95']:,.0f}",
                                 help="95% confidence that portfolio will be worth at least this much")
                    with col2:
                        st.metric("Conditional VaR (95%)", f"${mc_result['cvar_95']:,.0f}",
                                 help="Expected value in worst 5% of scenarios")
                    with col3:
                        potential_loss = mc_initial - mc_result['var_95']
                        st.metric("Max Expected Loss (95%)", f"${potential_loss:,.0f}",
                                 help="Maximum expected loss with 95% confidence")
                    
                    st.info(f"💡 **Insight**: There's a 5% chance your portfolio could be worth less than ${mc_result['var_95']:,.0f} after {mc_years} years.")
            
            # Rebalancing Analysis
            st.markdown("---")
            st.subheader("🔄 Rebalancing Analysis")
            
            # Add rebalancing guide
            with st.expander("📖 Portfolio Rebalancing Guide"):
                rebalancing_guide = PortfolioHelp.get_rebalancing_guide()
                st.markdown(rebalancing_guide['content'])
            
            # Create tabs for different rebalancing modes
            rebal_tab1, rebal_tab2 = st.tabs(["📊 Actual Portfolio", "🎲 Simulate Drift"])
            
            # Tab 1: Actual Portfolio Rebalancing
            with rebal_tab1:
                st.markdown("""
                **Track Your Actual Holdings**  
                Enter your current positions to see real rebalancing recommendations based on live market prices.
                """)
                
                # Get assets that have non-zero optimal weights
                assets_in_portfolio = [ticker for ticker, weight in zip(data_handler.tickers, optimal_weights) if weight > 0.0001]
                
                if len(assets_in_portfolio) == 0:
                    st.warning("No assets in optimal portfolio. Run optimization first.")
                else:
                    st.markdown("**💼 Enter Your Current Holdings**")
                    st.info(f"ℹ️ Showing {len(assets_in_portfolio)} asset(s) from your optimal portfolio: {', '.join(assets_in_portfolio)}. Assets with 0% allocation are not shown.")
                    
                    # Create input form for actual holdings
                    holdings_data = {}
                    
                    # Use columns for compact layout
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Asset**")
                        for ticker in assets_in_portfolio:
                            st.markdown(f"`{ticker}`")
                    
                    with col2:
                        st.markdown("**Shares Owned**")
                        for ticker in assets_in_portfolio:
                            shares = st.number_input(
                                f"Shares of {ticker}",
                                min_value=0.0,
                                value=0.0,
                                step=1.0,
                                key=f"shares_{ticker}",
                                label_visibility="collapsed"
                            )
                            if ticker not in holdings_data:
                                holdings_data[ticker] = {}
                            holdings_data[ticker]['shares'] = shares
                    
                    with col3:
                        st.markdown("**Purchase Price**")
                        for ticker in assets_in_portfolio:
                            purchase_price = st.number_input(
                                f"Purchase price of {ticker}",
                                min_value=0.0,
                                value=0.0,
                                step=0.01,
                                key=f"purchase_{ticker}",
                                label_visibility="collapsed"
                            )
                            holdings_data[ticker]['purchase_price'] = purchase_price
                    
                    # Calculate rebalancing button
                    if st.button("📊 Calculate Rebalancing Needs", use_container_width=True, type="primary"):
                        # Get current market prices
                        current_prices_series = prices.iloc[-1]
                        
                        # Calculate current portfolio value and positions
                        total_value = 0
                        position_details = []
                        
                        for ticker in assets_in_portfolio:
                            shares = holdings_data[ticker]['shares']
                            purchase_price = holdings_data[ticker]['purchase_price']
                            current_price = current_prices_series[ticker]
                            
                            current_value = shares * current_price
                            cost_basis = shares * purchase_price
                            unrealized_pl = current_value - cost_basis
                            unrealized_pl_pct = (unrealized_pl / cost_basis * 100) if cost_basis > 0 else 0
                            
                            total_value += current_value
                            
                            position_details.append({
                                'ticker': ticker,
                                'shares': shares,
                                'purchase_price': purchase_price,
                                'current_price': current_price,
                                'cost_basis': cost_basis,
                                'current_value': current_value,
                                'unrealized_pl': unrealized_pl,
                                'unrealized_pl_pct': unrealized_pl_pct
                            })
                        
                        if total_value == 0:
                            st.warning("⚠️ Please enter your holdings (shares owned must be greater than 0)")
                        else:
                            st.markdown("---")
                            
                            # Display current portfolio summary
                            st.markdown("**📈 Current Portfolio Summary**")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Portfolio Value", f"${total_value:,.2f}")
                            with col2:
                                total_cost = sum(p['cost_basis'] for p in position_details)
                                st.metric("Total Cost Basis", f"${total_cost:,.2f}")
                            with col3:
                                total_pl = total_value - total_cost
                                st.metric("Total Unrealized P/L", f"${total_pl:,.2f}", 
                                         delta=f"{(total_pl/total_cost*100):.2f}%" if total_cost > 0 else "0%")
                            with col4:
                                st.metric("Drift Threshold", f"{drift_threshold*100:.0f}%")
                            
                            st.markdown("---")
                            
                            # Show detailed positions
                            st.markdown("**💼 Current Positions**")
                            positions_df = pd.DataFrame([{
                                'Asset': p['ticker'],
                                'Shares': p['shares'],
                                'Purchase Price': f"${p['purchase_price']:.2f}",
                                'Current Price': f"${p['current_price']:.2f}",
                                'Cost Basis': p['cost_basis'],
                                'Market Value': p['current_value'],
                                'Current Weight': p['current_value'] / total_value,
                                'Target Weight': optimal_weights[data_handler.tickers.index(p['ticker'])],
                                'Unrealized P/L': p['unrealized_pl'],
                                'P/L %': p['unrealized_pl_pct']
                            } for p in position_details])
                            
                            st.dataframe(
                                positions_df.style.format({
                                    'Shares': '{:.2f}',
                                    'Cost Basis': '${:,.2f}',
                                    'Market Value': '${:,.2f}',
                                    'Current Weight': '{:.2%}',
                                    'Target Weight': '{:.2%}',
                                    'Unrealized P/L': '${:,.2f}',
                                    'P/L %': '{:.2f}%'
                                }).background_gradient(subset=['P/L %'], cmap='RdYlGn'),
                                hide_index=True,
                                use_container_width=True
                            )
                            
                            # Calculate drift and rebalancing needs
                            st.markdown("---")
                            st.markdown("**🎯 Rebalancing Analysis**")
                            
                            current_values = np.array([p['current_value'] for p in position_details])
                            current_weights = current_values / total_value
                            target_weights = np.array([optimal_weights[data_handler.tickers.index(p['ticker'])] for p in position_details])
                            
                            drifts = current_weights - target_weights
                            max_drift = np.max(np.abs(drifts))
                            
                            # Check if rebalancing is needed
                            needs_rebalancing = max_drift > drift_threshold
                            
                            if needs_rebalancing:
                                st.error(f"⚠️ **REBALANCING RECOMMENDED** - Maximum drift: {max_drift*100:.2f}%")
                                
                                # Calculate target values and trades needed
                                target_values = target_weights * total_value
                                value_adjustments = target_values - current_values
                                current_prices_array = np.array([p['current_price'] for p in position_details])
                                shares_to_trade = value_adjustments / current_prices_array
                                
                                # Create trades dataframe
                                trades_data = []
                                for i, p in enumerate(position_details):
                                    shares_trade = shares_to_trade[i]
                                    value_trade = value_adjustments[i]
                                    
                                    if abs(shares_trade) > 0.01:  # Only show meaningful trades
                                        action = 'BUY' if shares_trade > 0 else 'SELL'
                                        
                                        # Calculate tax implications for sells
                                        tax_note = ""
                                        if action == 'SELL':
                                            shares_to_sell = abs(shares_trade)
                                            gain_per_share = p['current_price'] - p['purchase_price']
                                            capital_gain = gain_per_share * shares_to_sell
                                            tax_note = f"${capital_gain:,.2f} gain" if capital_gain > 0 else f"${abs(capital_gain):,.2f} loss"
                                        
                                        trades_data.append({
                                            'Asset': p['ticker'],
                                            'Action': '🟢 ' + action if action == 'BUY' else '🔴 ' + action,
                                            'Shares to Trade': abs(shares_trade),
                                            'Value': abs(value_trade),
                                            'Current Weight': current_weights[i],
                                            'Target Weight': target_weights[i],
                                            'Drift': drifts[i],
                                            'Tax Impact': tax_note
                                        })
                                
                                if trades_data:
                                    st.markdown("**💼 Recommended Trades**")
                                    trades_df = pd.DataFrame(trades_data)
                                    
                                    st.dataframe(
                                        trades_df.style.format({
                                            'Shares to Trade': '{:.2f}',
                                            'Value': '${:,.2f}',
                                            'Current Weight': '{:.2%}',
                                            'Target Weight': '{:.2%}',
                                            'Drift': '{:.2%}'
                                        }).background_gradient(subset=['Drift'], cmap='RdYlGn', vmin=-0.1, vmax=0.1),
                                        hide_index=True,
                                        use_container_width=True
                                    )
                                    
                                    # Summary
                                    total_buy = sum(t['Value'] for t in trades_data if 'BUY' in t['Action'])
                                    total_sell = sum(t['Value'] for t in trades_data if 'SELL' in t['Action'])
                                    net_cash_flow = total_sell - total_buy  # Positive = cash released, Negative = cash needed
                                    
                                    col1, col2, col3, col4 = st.columns(4)
                                    with col1:
                                        st.metric("Total to Buy", f"${total_buy:,.2f}")
                                    with col2:
                                        st.metric("Total to Sell", f"${total_sell:,.2f}")
                                    with col3:
                                        cash_flow_label = "Cash Released" if net_cash_flow > 0 else "Cash Needed"
                                        st.metric(cash_flow_label, f"${abs(net_cash_flow):,.2f}")
                                    with col4:
                                        st.metric("Number of Trades", len(trades_data))
                                    
                                    st.info("💡 **Tax Tip**: Consider tax-loss harvesting opportunities and hold periods for long-term capital gains treatment")
                                
                            else:
                                st.success(f"✅ **NO REBALANCING NEEDED** - Maximum drift: {max_drift*100:.2f}% (within {drift_threshold*100:.0f}% threshold)")
                                
                                # Still show drift details
                                drift_df = pd.DataFrame({
                                    'Asset': [p['ticker'] for p in position_details],
                                    'Current Weight': current_weights,
                                    'Target Weight': target_weights,
                                    'Drift': drifts
                                })
                                
                                st.dataframe(
                                    drift_df.style.format({
                                        'Current Weight': '{:.2%}',
                                        'Target Weight': '{:.2%}',
                                        'Drift': '{:.2%}'
                                    }).background_gradient(subset=['Drift'], cmap='RdYlGn', vmin=-0.05, vmax=0.05),
                                    hide_index=True,
                                    use_container_width=True
                                )
            
            # Tab 2: Simulate Portfolio Drift (existing functionality)
            with rebal_tab2:
                st.markdown("""
                **Simulate Portfolio Drift**  
                See how your portfolio might drift over time as asset prices change and what rebalancing trades would be needed.
                """)
                
                # Input controls
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    initial_investment = st.number_input("Initial Portfolio Value ($)", value=100000, step=10000, min_value=1000)
                
                with col2:
                    st.metric("Drift Threshold", f"{drift_threshold*100:.0f}%")
                
                # Button outside columns for better visibility
                simulate_drift = st.button("🎲 Simulate Portfolio Drift", use_container_width=True, type="primary")
                
                if simulate_drift:
                    st.markdown("---")
                    
                    with st.spinner("Simulating market movements..."):
                        # Simulate random price changes (-10% to +20%)
                        np.random.seed()  # Different results each time
                        price_changes = np.random.uniform(0.9, 1.2, len(data_handler.tickers))
                        current_prices = prices.iloc[-1].values * price_changes
                        
                        # Calculate current values
                        initial_values = optimal_weights * initial_investment
                        current_values = initial_values * price_changes
                        
                        # Show price changes
                        st.markdown("**📊 Simulated Price Changes**")
                        price_change_df = pd.DataFrame({
                            'Asset': data_handler.tickers,
                            'Price Change': (price_changes - 1) * 100,
                            'Impact': ['📈 Up' if pc > 1 else '📉 Down' for pc in price_changes]
                        }).sort_values('Price Change', ascending=False)
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.dataframe(
                                price_change_df.style.format({'Price Change': '{:.2f}%'})
                                .background_gradient(subset=['Price Change'], cmap='RdYlGn'),
                                hide_index=True,
                                use_container_width=True
                            )
                        
                        with col2:
                            # Create rebalancer
                            rebalancer = PortfolioRebalancer(
                                optimal_weights, 
                                data_handler.tickers,
                                drift_threshold
                            )
                            
                            # Check for drift
                            monitoring = rebalancer.monitor_portfolio(current_values)
                            
                            # Display status prominently
                            if monitoring['Needs Rebalancing']:
                                st.error("⚠️ **REBALANCING REQUIRED**")
                                st.metric("Maximum Drift", f"{monitoring['Max Drift']*100:.2f}%", 
                                         delta=f"Threshold: {drift_threshold*100:.0f}%", delta_color="inverse")
                            else:
                                st.success("✅ **WITHIN THRESHOLD**")
                                st.metric("Maximum Drift", f"{monitoring['Max Drift']*100:.2f}%", 
                                         delta=f"Under {drift_threshold*100:.0f}% threshold", delta_color="normal")
                            
                            if monitoring['Needs Rebalancing']:
                                st.markdown("---")
                                st.markdown("**🚨 Drift Alerts**")
                                
                                # Show alerts in a formatted way
                                if monitoring['Alerts']:
                                    alert_data = []
                                    for alert in monitoring['Alerts']:
                                        alert_data.append({
                                            'Asset': alert['Ticker'],
                                            'Status': '🔴 ' + alert['Status'],
                                            'Current': f"{alert['Current Weight']:.2%}",
                                            'Target': f"{alert['Target Weight']:.2%}",
                                            'Drift': f"{alert['Drift %']:.1f}%"
                                        })
                                    
                                    alert_df = pd.DataFrame(alert_data)
                                    st.dataframe(alert_df, hide_index=True, use_container_width=True)
                                
                                    st.markdown("---")
                                    st.markdown("**💼 Recommended Trades**")
                                
                                    # Calculate rebalancing trades
                                    trades = rebalancer.calculate_rebalancing_trades(current_values, current_prices)
                                    
                                    display_trades = trades[trades['Action'] != 'HOLD'].copy()
                                    
                                    if not display_trades.empty:
                                        # Add icons for actions
                                        display_trades['Action'] = display_trades['Action'].map({
                                            'BUY': '🟢 BUY',
                                            'SELL': '🔴 SELL'
                                        })
                                        
                                        st.dataframe(
                                            display_trades[['Ticker', 'Action', 'Shares to Trade', 
                                                           'Value to Trade', 'Current Weight', 'Target Weight']].style.format({
                                                'Shares to Trade': '{:.2f}',
                                                'Value to Trade': '${:,.2f}',
                                                'Current Weight': '{:.2%}',
                                                'Target Weight': '{:.2%}'
                                            }).background_gradient(subset=['Value to Trade'], cmap='coolwarm'),
                                            hide_index=True,
                                            use_container_width=True
                                        )
                                        
                                        # Summary metrics
                                        st.markdown("---")
                                        st.markdown("**📊 Rebalancing Summary**")
                                        summary = rebalancer.get_rebalancing_summary(trades)
                                        
                                        col1, col2, col3, col4 = st.columns(4)
                                        
                                        with col1:
                                            st.metric(label="Total Buy Value", value=f"${summary['Total Buy Value']:,.0f}")
                                        
                                        with col2:
                                            st.metric(label="Total Sell Value", value=f"${summary['Total Sell Value']:,.0f}")
                                        
                                        with col3:
                                            st.metric(label="Portfolio Turnover", value=f"{summary['Turnover']:.2%}")
                                        
                                        with col4:
                                            st.metric(label="Trades Required", value=f"{summary['Number of Buys'] + summary['Number of Sells']}")
                                        
                                        st.info("💡 **Tip**: Consider transaction costs when rebalancing. Small drifts may not be worth trading.")
                                    else:
                                        st.info("No trades needed - minor adjustments only")
                            else:
                                st.success("✓ Portfolio is within acceptable drift threshold. No rebalancing needed.")
                            
                            # Show current weights (only for assets with non-zero target allocation)
                            current_weights_df = pd.DataFrame({
                                'Asset': data_handler.tickers,
                                'Current Weight': rebalancer.calculate_current_weights(current_values),
                                'Target Weight': optimal_weights,
                                'Drift': rebalancer.calculate_current_weights(current_values) - optimal_weights
                            })
                            
                            # Filter to show only assets that are part of the optimal portfolio
                            current_weights_df = current_weights_df[current_weights_df['Target Weight'] > 0.0001]
                            
                            if not current_weights_df.empty:
                                st.markdown("---")
                                st.markdown("**📊 Current Portfolio Weights**")
                                st.dataframe(
                                    current_weights_df.style.format({
                                        'Current Weight': '{:.2%}',
                                    'Target Weight': '{:.2%}',
                                    'Drift': '{:.2%}'
                                }).background_gradient(subset=['Drift'], cmap='RdYlGn', vmin=-0.1, vmax=0.1),
                                hide_index=True,
                                use_container_width=True
                            )
    
    # Show welcome message only if no optimization has been run
    else:
        # Welcome message with better formatting
        st.markdown("")  # Add spacing
        st.markdown("## 👋 Welcome to Portfolio Optimization Engine")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### How to Get Started
            
            1. **Select Your Portfolio Holdings** 📝
            - Enter portfolio holdings in the sidebar (comma-separated)
            - Examples: VTI, BND, SCHD, SCHG, VIG, VXUS
            
            2. **Configure Parameters** ⚙️
            - Choose historical data period (6-60 months)
            - Set risk-free rate (default: 2%)
            - Select optimization strategy
            - Set rebalancing drift threshold
            
            3. **Run Optimization** 🚀
            - Click the "Run Optimization" button
            - Wait for data fetching and calculations
            - Explore interactive results and charts
            
            ---
            
            ### Features You'll Get
            
            ✅ **Optimization Strategies**: 5 different approaches (Sharpe, Min Vol, Risk Parity, etc.)  
            ✅ **Performance Metrics**: 8+ comprehensive metrics including Sharpe, Sortino, Calmar ratios  
            ✅ **Visual Analytics**: Interactive charts for efficient frontier, allocations, correlations  
            ✅ **Rebalancing Tools**: Monitor drift and get trade recommendations  
            ✅ **Risk Analysis**: VaR, CVaR, Maximum Drawdown calculations  
            """)
        
        with col2:
            st.markdown("### 📊 Quick Tips")
            st.info("""
            **Asset Selection**
            - Minimum 2 assets
            - Mix different asset classes
            - Consider correlations
            """)
            
            st.success("""
            **Data Period**
            - Longer = More data
            - 12-24 months typical
            - Consider market cycles
            """)
            
            st.warning("""
            **Optimization Strategy**
            - Max Sharpe: Best risk-adj returns
            - Min Vol: Lowest risk
            - Risk Parity: Balanced risk
            """)
        
        st.markdown("")  # Add spacing
        st.markdown("### 💼 Sample Portfolio Holdings")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            **📊 U.S. Equity ETFs**
            - VTI (Total Market)
            - SCHD (Dividend)
            - SCHG (Growth)
            - VIG (Dividend Growth)
            - VOO (S&P 500)
            """)
        
        with col2:
            st.markdown("""
            **🏦 Fixed Income**
            - BND (Total Bond)
            - AGG (Aggregate Bond)
            - TLT (Treasury Bonds)
            - LQD (Corp Bonds)
            - VCIT (Int. Corp)
            """)
        
        with col3:
            st.markdown("""
            **🌍 International**
            - VXUS (Ex-US Total)
            - VEA (Developed)
            - VWO (Emerging)
            - IXUS (Ex-US Total)
            - IEMG (Emerging)
            """)
        
        with col4:
            st.markdown("""
            **🎯 Sector/Specialty**
            - VNQ (Real Estate)
            - GLD (Gold)
            - DBC (Commodities)
            - VGT (Technology)
            - VHT (Healthcare)
            """)
        
        st.markdown("---")
        st.markdown("👈 **Ready? Configure your portfolio in the sidebar and click 'Run Optimization'!**")


if __name__ == "__main__":
    main()
