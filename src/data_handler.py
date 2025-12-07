"""
Data Handler Module
Handles fetching and preprocessing of historical asset price data.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Tuple, Optional


class DataHandler:
    """
    Fetches and processes historical price data for portfolio optimization.
    """
    
    def __init__(self, tickers: List[str], period_months: int = 12, risk_free_rate: float = 0.02):
        """
        Initialize the DataHandler.
        
        Args:
            tickers: List of asset ticker symbols
            period_months: Historical data period in months (6-60)
            risk_free_rate: Annual risk-free rate for Sharpe ratio calculation
        """
        self.tickers = tickers
        self.period_months = max(6, min(60, period_months))  # Constrain to 6-60 months
        self.risk_free_rate = risk_free_rate
        self.prices = None
        self.returns = None
        self.mean_returns = None
        self.cov_matrix = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical price data from Yahoo Finance.
        
        Returns:
            DataFrame with adjusted close prices
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.period_months * 30)
        
        print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        try:
            # Download data
            raw_data = yf.download(
                self.tickers,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            # Handle empty data
            if raw_data.empty:
                print("Warning: No data returned from yfinance")
                raise ValueError("No data returned from yfinance. Check your internet connection and ticker symbols.")
            
            print(f"Raw data shape: {raw_data.shape}")
            print(f"Raw data columns: {raw_data.columns.tolist()}")
            
            # Extract 'Adj Close' prices, handling different return structures
            if len(self.tickers) == 1:
                # Single ticker case
                if isinstance(raw_data.columns, pd.MultiIndex):
                    # MultiIndex format: (metric, ticker)
                    try:
                        data = raw_data.xs('Adj Close', axis=1, level=0)
                        data = pd.DataFrame(data.values, index=raw_data.index, columns=self.tickers)
                    except KeyError:
                        # Try 'Close' if 'Adj Close' not available
                        try:
                            data = raw_data.xs('Close', axis=1, level=0)
                            data = pd.DataFrame(data.values, index=raw_data.index, columns=self.tickers)
                        except KeyError:
                            # Use first available price column
                            data = pd.DataFrame(raw_data.iloc[:, 0].values, index=raw_data.index, columns=self.tickers)
                elif 'Adj Close' in raw_data.columns:
                    # Simple format with 'Adj Close' column
                    data = pd.DataFrame(raw_data['Adj Close'].values, index=raw_data.index, columns=self.tickers)
                elif 'Close' in raw_data.columns:
                    # Fallback to 'Close' if 'Adj Close' not available
                    data = pd.DataFrame(raw_data['Close'].values, index=raw_data.index, columns=self.tickers)
                else:
                    # Fallback: use first numeric column
                    numeric_cols = raw_data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        data = pd.DataFrame(raw_data[numeric_cols[0]].values, index=raw_data.index, columns=self.tickers)
                    else:
                        print(f"Error: No numeric columns found in data")
                        raise ValueError("No price data found in downloaded data")
            else:
                # Multiple tickers case
                if isinstance(raw_data.columns, pd.MultiIndex):
                    # MultiIndex format: (metric, ticker)
                    try:
                        data = raw_data.xs('Adj Close', axis=1, level=0)
                    except KeyError:
                        # Try 'Close' if 'Adj Close' not available
                        try:
                            data = raw_data.xs('Close', axis=1, level=0)
                        except KeyError:
                            # Try alternative column structure
                            available_metrics = list(set([col[0] for col in raw_data.columns]))
                            print(f"Available metrics: {available_metrics}")
                            if 'Adj Close' in available_metrics:
                                data = raw_data[[col for col in raw_data.columns if col[0] == 'Adj Close']]
                                data.columns = [col[1] if isinstance(col, tuple) else col for col in data.columns]
                            elif 'Close' in available_metrics:
                                data = raw_data[[col for col in raw_data.columns if col[0] == 'Close']]
                                data.columns = [col[1] if isinstance(col, tuple) else col for col in data.columns]
                            else:
                                # Use first available metric
                                first_metric = available_metrics[0]
                                data = raw_data[[col for col in raw_data.columns if col[0] == first_metric]]
                                data.columns = [col[1] if isinstance(col, tuple) else col for col in data.columns]
                                print(f"Using '{first_metric}' prices instead of 'Adj Close'")
                else:
                    # Simple format - assume it's already price data
                    data = raw_data
            
            print(f"Extracted data shape: {data.shape}")
            
            # Drop any columns with all NaN values
            data = data.dropna(axis=1, how='all')
            
            # Forward fill then backward fill any remaining NaN values
            data = data.ffill().bfill()
            
            # Drop any rows that are still all NaN
            data = data.dropna(how='all')
            
            # Update tickers list to only include successfully downloaded tickers
            self.tickers = list(data.columns)
            self.prices = data
            
            if len(self.tickers) == 0 or data.empty:
                raise ValueError("No valid data retrieved for any of the provided tickers. Please check ticker symbols.")
            
            print(f"Successfully fetched data for {len(self.tickers)} assets: {', '.join(self.tickers)}")
            print(f"Final data shape: {data.shape}")
            
            return data
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise
    
    def calculate_returns(self) -> pd.DataFrame:
        """
        Calculate daily returns from price data.
        
        Returns:
            DataFrame with daily returns
        """
        if self.prices is None:
            self.fetch_data()
        
        self.returns = self.prices.pct_change().dropna()
        return self.returns
    
    def calculate_mean_returns(self, annualize: bool = True) -> pd.Series:
        """
        Calculate mean returns for each asset.
        
        Args:
            annualize: If True, annualize the returns (assuming 252 trading days)
        
        Returns:
            Series with mean returns for each asset
        """
        if self.returns is None:
            self.calculate_returns()
        
        mean_returns = self.returns.mean()
        
        if annualize:
            mean_returns = mean_returns * 252
        
        self.mean_returns = mean_returns
        return mean_returns
    
    def calculate_cov_matrix(self, annualize: bool = True) -> pd.DataFrame:
        """
        Calculate covariance matrix of returns.
        
        Args:
            annualize: If True, annualize the covariance (assuming 252 trading days)
        
        Returns:
            Covariance matrix
        """
        if self.returns is None:
            self.calculate_returns()
        
        cov_matrix = self.returns.cov()
        
        if annualize:
            cov_matrix = cov_matrix * 252
        
        self.cov_matrix = cov_matrix
        return cov_matrix
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Calculate correlation matrix of returns.
        
        Returns:
            Correlation matrix
        """
        if self.returns is None:
            self.calculate_returns()
        
        return self.returns.corr()
    
    def prepare_optimization_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for portfolio optimization.
        
        Returns:
            Tuple of (mean_returns, cov_matrix) as numpy arrays
        """
        mean_returns = self.calculate_mean_returns(annualize=True)
        cov_matrix = self.calculate_cov_matrix(annualize=True)
        
        return mean_returns.values, cov_matrix.values
    
    def get_asset_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for each asset.
        
        Returns:
            DataFrame with statistics for each asset
        """
        if self.returns is None:
            self.calculate_returns()
        
        stats = pd.DataFrame({
            'Mean Return (Annual)': self.calculate_mean_returns(annualize=True),
            'Volatility (Annual)': self.returns.std() * np.sqrt(252),
            'Sharpe Ratio': (self.calculate_mean_returns(annualize=True) - self.risk_free_rate) / 
                           (self.returns.std() * np.sqrt(252)),
            'Min': self.returns.min(),
            'Max': self.returns.max(),
            'Skewness': self.returns.skew(),
            'Kurtosis': self.returns.kurtosis()
        })
        
        return stats
    
    def get_price_history(self) -> pd.DataFrame:
        """
        Get the raw price history.
        
        Returns:
            DataFrame with historical prices
        """
        if self.prices is None:
            self.fetch_data()
        
        return self.prices
    
    @staticmethod
    def validate_tickers(tickers: List[str]) -> List[str]:
        """
        Validate that tickers exist and can be downloaded.
        
        Args:
            tickers: List of ticker symbols to validate
        
        Returns:
            List of valid tickers
        """
        valid_tickers = []
        
        for ticker in tickers:
            try:
                data = yf.Ticker(ticker)
                hist = data.history(period="5d")
                
                if not hist.empty:
                    valid_tickers.append(ticker)
                else:
                    print(f"Warning: No data available for {ticker}")
            except:
                print(f"Warning: Could not validate {ticker}")
        
        return valid_tickers
