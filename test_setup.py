"""
Quick test script to verify installation and basic functionality
"""

import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.data_handler import DataHandler
        from src.optimizer import PortfolioOptimizer
        from src.metrics import PortfolioMetrics
        from src.visualizer import PortfolioVisualizer
        from src.rebalancer import PortfolioRebalancer
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_dependencies():
    """Test that required packages are installed."""
    print("\nTesting dependencies...")
    required = ['numpy', 'pandas', 'scipy', 'matplotlib', 'yfinance', 'streamlit']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True

def test_basic_functionality():
    """Test basic functionality without fetching real data."""
    print("\nTesting basic functionality...")
    try:
        import numpy as np
        from src.optimizer import PortfolioOptimizer
        from src.metrics import PortfolioMetrics
        
        # Create synthetic data
        n_assets = 3
        mean_returns = np.array([0.10, 0.12, 0.08])
        cov_matrix = np.array([
            [0.04, 0.01, 0.01],
            [0.01, 0.06, 0.01],
            [0.01, 0.01, 0.03]
        ])
        
        # Test optimizer
        optimizer = PortfolioOptimizer(mean_returns, cov_matrix)
        weights, metrics = optimizer.optimize('max_sharpe')
        
        assert len(weights) == n_assets
        assert abs(sum(weights) - 1.0) < 1e-6
        assert all(w >= 0 for w in weights)
        
        print("✓ Optimizer working correctly")
        
        # Test metrics
        ret = PortfolioMetrics.portfolio_return(weights, mean_returns)
        vol = PortfolioMetrics.portfolio_volatility(weights, cov_matrix)
        sharpe = PortfolioMetrics.sharpe_ratio(weights, mean_returns, cov_matrix)
        
        assert 0 <= ret <= 1
        assert vol > 0
        assert isinstance(sharpe, float)
        
        print("✓ Metrics calculation working correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("PORTFOLIO OPTIMIZATION ENGINE - VERIFICATION TEST")
    print("="*60 + "\n")
    
    all_passed = True
    
    # Run tests
    all_passed &= test_dependencies()
    all_passed &= test_imports()
    all_passed &= test_basic_functionality()
    
    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now run:")
        print("  - python example.py        (for example run)")
        print("  - streamlit run app.py     (for dashboard)")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
