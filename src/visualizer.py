"""
Visualization Module
Creates charts and plots for portfolio analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class PortfolioVisualizer:
    """
    Handles all visualization for portfolio optimization.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the visualizer.
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
    
    @staticmethod
    def plot_efficient_frontier(returns: np.ndarray, volatilities: np.ndarray,
                               sharpe_ratios: np.ndarray, optimal_points: dict = None,
                               show_cml: bool = True, risk_free_rate: float = 0.02,
                               interactive: bool = False):
        """
        Plot the efficient frontier.
        
        Args:
            returns: Array of portfolio returns
            volatilities: Array of portfolio volatilities
            sharpe_ratios: Array of Sharpe ratios
            optimal_points: Dictionary of optimal portfolios to highlight
            show_cml: Whether to show Capital Market Line
            risk_free_rate: Risk-free rate for CML
            interactive: Use Plotly for interactive plot
        """
        if interactive:
            return PortfolioVisualizer._plot_efficient_frontier_plotly(
                returns, volatilities, sharpe_ratios, optimal_points, show_cml, risk_free_rate
            )
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Color points by Sharpe ratio
        scatter = ax.scatter(volatilities, returns, c=sharpe_ratios, cmap='viridis',
                           alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Volatility (Standard Deviation)', fontsize=12)
        ax.set_ylabel('Expected Return', fontsize=12)
        ax.set_title('Efficient Frontier', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Sharpe Ratio', fontsize=10)
        
        # Plot optimal points if provided
        if optimal_points:
            for name, (ret, vol) in optimal_points.items():
                ax.scatter(vol, ret, marker='*', s=500, edgecolors='black',
                          linewidth=2, label=name, zorder=5)
        
        # Plot Capital Market Line if requested
        if show_cml and optimal_points and 'Max Sharpe' in optimal_points:
            max_sharpe_ret, max_sharpe_vol = optimal_points['Max Sharpe']
            sharpe = (max_sharpe_ret - risk_free_rate) / max_sharpe_vol
            
            # CML from risk-free rate through max Sharpe portfolio
            x_cml = np.linspace(0, max(volatilities) * 1.2, 100)
            y_cml = risk_free_rate + sharpe * x_cml
            
            ax.plot(x_cml, y_cml, 'r--', linewidth=2, label='Capital Market Line')
            ax.scatter(0, risk_free_rate, marker='o', s=100, color='red',
                      edgecolors='black', linewidth=2, label='Risk-Free Rate', zorder=5)
        
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def _plot_efficient_frontier_plotly(returns: np.ndarray, volatilities: np.ndarray,
                                       sharpe_ratios: np.ndarray, optimal_points: dict = None,
                                       show_cml: bool = True, risk_free_rate: float = 0.02):
        """
        Plot interactive efficient frontier using Plotly.
        """
        fig = go.Figure()
        
        # Add efficient frontier
        fig.add_trace(go.Scatter(
            x=volatilities,
            y=returns,
            mode='markers',
            marker=dict(
                size=8,
                color=sharpe_ratios,
                colorscale='Viridis',
                showscale=False,  # Remove Sharpe Ratio colorbar to save space
                line=dict(width=0.5, color='black')
            ),
            text=[f'Return: {r:.2%}<br>Vol: {v:.2%}<br>Sharpe: {s:.3f}' 
                  for r, v, s in zip(returns, volatilities, sharpe_ratios)],
            hovertemplate='%{text}<extra></extra>',
            name='Portfolio Options',
            showlegend=True
        ))
        
        # Add optimal points
        if optimal_points:
            for name, (ret, vol) in optimal_points.items():
                fig.add_trace(go.Scatter(
                    x=[vol],
                    y=[ret],
                    mode='markers+text',
                    marker=dict(size=18, symbol='star', line=dict(width=2, color='black')),
                    name=name,
                    text=name,
                    textposition='top center',
                    textfont=dict(size=10, color='black'),
                    hovertemplate=f'{name}<br>Return: {ret:.2%}<br>Vol: {vol:.2%}<extra></extra>',
                    showlegend=True
                ))
        
        # Add CML
        if show_cml and optimal_points and 'Max Sharpe' in optimal_points:
            max_sharpe_ret, max_sharpe_vol = optimal_points['Max Sharpe']
            sharpe = (max_sharpe_ret - risk_free_rate) / max_sharpe_vol
            
            x_cml = np.linspace(0, max(volatilities) * 1.2, 100)
            y_cml = risk_free_rate + sharpe * x_cml
            
            fig.add_trace(go.Scatter(
                x=x_cml,
                y=y_cml,
                mode='lines',
                line=dict(dash='dash', color='red', width=2),
                name='Capital Market Line',
                showlegend=True
            ))
            
            fig.add_trace(go.Scatter(
                x=[0],
                y=[risk_free_rate],
                mode='markers',
                marker=dict(size=12, color='red', line=dict(width=2, color='black')),
                name='Risk-Free Rate',
                hovertemplate=f'Risk-Free Rate: {risk_free_rate:.2%}<extra></extra>',
                showlegend=True
            ))
        
        fig.update_layout(
            title={
                'text': 'Efficient Frontier',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#000000'}
            },
            xaxis_title='Volatility (Risk)',
            yaxis_title='Expected Return',
            hovermode='closest',
            template='plotly_white',
            height=600,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor="white",
                bordercolor="#333333",
                borderwidth=2,
                font=dict(size=12, color='#000000')
            ),
            margin=dict(l=80, r=120, t=80, b=80),
            font=dict(color='#000000')
        )
        
        return fig
    
    @staticmethod
    def plot_weights(weights: np.ndarray, tickers: List[str], title: str = "Portfolio Allocation",
                    interactive: bool = False):
        """
        Plot portfolio weights as a bar chart or pie chart.
        
        Args:
            weights: Portfolio weights
            tickers: Asset ticker symbols
            title: Chart title
            interactive: Use Plotly for interactive plot
        """
        if interactive:
            return PortfolioVisualizer._plot_weights_plotly(weights, tickers, title)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Bar chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(tickers)))
        bars = ax1.bar(tickers, weights * 100, color=colors, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Weight (%)', fontsize=12)
        ax1.set_title(f'{title} - Bar Chart', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
        
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Pie chart
        # Only show assets with weight > 0.5%
        display_weights = []
        display_tickers = []
        other_weight = 0
        
        for ticker, weight in zip(tickers, weights):
            if weight > 0.005:
                display_weights.append(weight)
                display_tickers.append(ticker)
            else:
                other_weight += weight
        
        if other_weight > 0:
            display_weights.append(other_weight)
            display_tickers.append('Other')
        
        wedges, texts, autotexts = ax2.pie(
            display_weights,
            labels=display_tickers,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(display_weights)]
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax2.set_title(f'{title} - Pie Chart', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def _plot_weights_plotly(weights: np.ndarray, tickers: List[str], title: str = "Portfolio Allocation"):
        """
        Plot interactive portfolio weights using Plotly.
        """
        # Filter out very small weights for cleaner display
        significant_mask = weights > 0.001
        display_weights = weights[significant_mask]
        display_tickers = [t for t, m in zip(tickers, significant_mask) if m]
        
        # Create subplots with better spacing
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Allocation by Weight', 'Portfolio Distribution'),
            specs=[[{"type": "bar"}, {"type": "pie"}]],
            horizontal_spacing=0.15
        )
        
        # Color scheme
        colors = px.colors.qualitative.Set3[:len(display_tickers)]
        
        # Bar chart - sorted by weight
        sorted_indices = np.argsort(display_weights)[::-1]
        sorted_weights = display_weights[sorted_indices]
        sorted_tickers = [display_tickers[i] for i in sorted_indices]
        sorted_colors = [colors[i] for i in sorted_indices]
        
        fig.add_trace(
            go.Bar(
                x=sorted_tickers,
                y=sorted_weights * 100,
                text=[f'{w*100:.1f}%' for w in sorted_weights],
                textposition='outside',
                marker=dict(
                    color=sorted_colors,
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{x}</b><br>Weight: %{y:.2f}%<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Pie chart with better styling
        fig.add_trace(
            go.Pie(
                labels=display_tickers,
                values=display_weights,
                textinfo='label+percent',
                textposition='auto',
                marker=dict(
                    colors=colors,
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>Weight: %{value:.2%}<br>Value: %{percent}<extra></extra>',
                hole=0.3  # Donut chart for modern look
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_xaxes(title_text="Asset", row=1, col=1, tickangle=-45)
        fig.update_yaxes(title_text="Weight (%)", row=1, col=1)
        
        fig.update_layout(
            title_text=f"<b>{title}</b>",
            title_font_size=16,
            showlegend=False,
            height=450,
            margin=dict(t=80, b=60, l=60, r=60)
        )
        
        return fig
    
    @staticmethod
    def plot_correlation_matrix(corr_matrix: pd.DataFrame, interactive: bool = False):
        """
        Plot correlation matrix as a heatmap.
        
        Args:
            corr_matrix: Correlation matrix
            interactive: Use Plotly for interactive plot
        """
        if interactive:
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title='Asset Correlation Matrix',
                xaxis_title='Asset',
                yaxis_title='Asset',
                height=600,
                width=700
            )
            
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title('Asset Correlation Matrix', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_returns_distribution(returns: pd.DataFrame, interactive: bool = False):
        """
        Plot distribution of returns for each asset.
        
        Args:
            returns: DataFrame of asset returns
            interactive: Use Plotly for interactive plot
        """
        if interactive:
            fig = go.Figure()
            
            for column in returns.columns:
                fig.add_trace(go.Histogram(
                    x=returns[column],
                    name=column,
                    opacity=0.7,
                    nbinsx=50
                ))
            
            fig.update_layout(
                title='Distribution of Asset Returns',
                xaxis_title='Return',
                yaxis_title='Frequency',
                barmode='overlay',
                height=500
            )
            
            return fig
        
        n_assets = len(returns.columns)
        n_cols = min(3, n_assets)
        n_rows = (n_assets + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        
        if n_assets == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if n_assets > n_cols else axes
        
        for idx, column in enumerate(returns.columns):
            ax = axes[idx] if n_assets > 1 else axes[0]
            
            ax.hist(returns[column], bins=50, alpha=0.7, edgecolor='black')
            ax.axvline(returns[column].mean(), color='red', linestyle='--',
                      linewidth=2, label=f'Mean: {returns[column].mean():.4f}')
            ax.set_xlabel('Return', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.set_title(f'{column} Return Distribution', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for idx in range(n_assets, len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_cumulative_returns(returns: pd.DataFrame, weights: Optional[np.ndarray] = None,
                               interactive: bool = False):
        """
        Plot cumulative returns over time.
        
        Args:
            returns: DataFrame of asset returns
            weights: Optional portfolio weights to also plot portfolio returns
            interactive: Use Plotly for interactive plot
        """
        cumulative = (1 + returns).cumprod()
        
        if interactive:
            fig = go.Figure()
            
            for column in cumulative.columns:
                fig.add_trace(go.Scatter(
                    x=cumulative.index,
                    y=cumulative[column],
                    mode='lines',
                    name=column
                ))
            
            if weights is not None:
                portfolio_returns = (returns * weights).sum(axis=1)
                portfolio_cumulative = (1 + portfolio_returns).cumprod()
                
                fig.add_trace(go.Scatter(
                    x=portfolio_cumulative.index,
                    y=portfolio_cumulative,
                    mode='lines',
                    name='Portfolio',
                    line=dict(width=3, dash='dash')
                ))
            
            fig.update_layout(
                title='Cumulative Returns',
                xaxis_title='Date',
                yaxis_title='Cumulative Return',
                hovermode='x unified',
                height=600
            )
            
            return fig
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        for column in cumulative.columns:
            ax.plot(cumulative.index, cumulative[column], label=column, linewidth=2)
        
        if weights is not None:
            portfolio_returns = (returns * weights).sum(axis=1)
            portfolio_cumulative = (1 + portfolio_returns).cumprod()
            ax.plot(portfolio_cumulative.index, portfolio_cumulative, 
                   label='Portfolio', linewidth=3, linestyle='--', color='black')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Cumulative Return', fontsize=12)
        ax.set_title('Cumulative Returns Over Time', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def save_figure(fig, filename: str, dpi: int = 300):
        """
        Save figure to file.
        
        Args:
            fig: Matplotlib figure or Plotly figure
            filename: Output filename
            dpi: Resolution for matplotlib figures
        """
        if hasattr(fig, 'write_html'):
            # Plotly figure
            if filename.endswith('.html'):
                fig.write_html(filename)
            else:
                fig.write_image(filename)
        else:
            # Matplotlib figure
            fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        
        print(f"Figure saved to {filename}")
