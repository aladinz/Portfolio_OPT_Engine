"""
Comprehensive Help System for Portfolio Optimization Engine
Provides educational content about Modern Portfolio Theory and optimization strategies
"""

class PortfolioHelp:
    """Educational content and help documentation for portfolio optimization"""
    
    @staticmethod
    def get_mpt_overview():
        """Modern Portfolio Theory overview"""
        return {
            'title': '📚 Modern Portfolio Theory (MPT)',
            'content': """
**Modern Portfolio Theory** was introduced by Harry Markowitz in 1952 and revolutionized investment management.

### Core Principles:

1. **Risk-Return Tradeoff**: Higher returns come with higher risk. MPT helps find the optimal balance.

2. **Diversification**: "Don't put all eggs in one basket." By combining assets with different risk profiles, 
   you can reduce overall portfolio risk without sacrificing expected returns.

3. **Efficient Frontier**: The set of optimal portfolios offering the highest expected return for each 
   level of risk, or the lowest risk for each level of return.

4. **Portfolio vs. Individual Assets**: What matters is how an asset contributes to overall portfolio 
   risk and return, not just its individual characteristics.

### Key Metrics:

- **Expected Return**: The weighted average of asset returns based on portfolio allocation
- **Volatility (Standard Deviation)**: Measure of portfolio risk - how much returns fluctuate
- **Sharpe Ratio**: Risk-adjusted return metric (Return - Risk-Free Rate) / Volatility
- **Correlation**: How assets move together - low correlation provides better diversification

### Why It Matters:

MPT provides a mathematical framework for constructing portfolios that maximize returns for a given 
level of risk, or minimize risk for a target return. This engine implements these principles with 
multiple optimization strategies.
            """,
            'reference': 'Markowitz, H. (1952). "Portfolio Selection". Journal of Finance.'
        }
    
    @staticmethod
    def get_strategy_explanation(strategy: str):
        """Get detailed explanation of optimization strategies"""
        strategies = {
            'max_sharpe': {
                'title': '🎯 Maximum Sharpe Ratio',
                'description': 'Finds the portfolio with the best risk-adjusted returns',
                'how_it_works': """
**Objective**: Maximize (Return - Risk-Free Rate) / Volatility

This strategy finds the portfolio that gives you the most return per unit of risk taken.

**Best For**:
- Investors seeking optimal risk-adjusted returns
- Long-term growth portfolios
- When you want the "most bang for your buck"

**Considerations**:
- May concentrate in assets with highest Sharpe ratios
- Use constraints (8-20% per asset) to ensure diversification
- Sensitive to estimation errors in expected returns

**Example**: If stocks have 10% return with 15% volatility (Sharpe=0.6) and a balanced portfolio 
has 8% return with 10% volatility (Sharpe=0.7), Max Sharpe chooses the balanced portfolio.
                """,
                'math': 'Sharpe Ratio = (E[R] - Rf) / σ',
                'tips': [
                    'Enable constraints to prevent over-concentration',
                    'Works best with 6-10 diversified assets',
                    'Review top holdings - ensure you\'re comfortable with allocations'
                ]
            },
            'min_volatility': {
                'title': '🛡️ Minimum Volatility',
                'description': 'Creates the most stable, least risky portfolio possible',
                'how_it_works': """
**Objective**: Minimize portfolio volatility (standard deviation)

This conservative strategy focuses solely on reducing risk, finding the portfolio with the 
smallest expected fluctuations.

**Best For**:
- Conservative investors near retirement
- Capital preservation goals
- Risk-averse investors
- Market uncertainty periods

**Considerations**:
- May sacrifice returns for stability
- Often heavily weights bonds and defensive assets
- Lower returns but smoother ride
- Useful for sleep-at-night portfolios

**Example**: Between a 100% stock portfolio (15% vol) and 60/40 stocks/bonds (9% vol), 
Min Vol chooses the latter or even more conservative.
                """,
                'math': 'Minimize: σ²portfolio = w\'Σw',
                'tips': [
                    'Expect lower returns than growth strategies',
                    'Great for reducing portfolio stress',
                    'Include bonds and low-volatility stocks'
                ]
            },
            'risk_parity': {
                'title': '⚖️ Risk Parity',
                'description': 'Equalizes risk contribution across all assets',
                'how_it_works': """
**Objective**: Each asset contributes equally to total portfolio risk

Instead of equal dollar weights, Risk Parity allocates so each holding contributes the same 
amount of risk to the portfolio.

**Best For**:
- True diversification seekers
- All-weather portfolios
- Reducing concentration risk
- Institutional-style allocation

**Considerations**:
- May overweight low-volatility assets (bonds)
- Provides robust diversification
- Less sensitive to return estimates
- Works well across market conditions

**Example**: If stocks are 3x more volatile than bonds, Risk Parity allocates ~3x more to bonds 
than stocks, so each contributes 50% of portfolio risk.

**Philosophy**: "Diversify by risk, not by dollars." Made famous by Ray Dalio's All Weather Portfolio.
                """,
                'math': 'RC_i = w_i × (Σw)_i / σ_portfolio, target: RC_i = 1/N for all i',
                'tips': [
                    'Best with constraints enabled (8-20%)',
                    'Works excellently with 8-10 assets',
                    'Provides consistent risk-adjusted returns',
                    'Less likely to concentrate than Max Sharpe'
                ]
            },
            'equal_weight': {
                'title': '⚖️ Equal Weight',
                'description': 'Simple 1/N allocation across all holdings',
                'how_it_works': """
**Objective**: Allocate equal percentage to each asset

The simplest strategy - divide your portfolio equally. With 10 assets, each gets 10%.

**Best For**:
- Simple, easy-to-understand portfolios
- When you believe all assets are equally good
- Avoiding optimization estimation errors
- Passive "naive diversification"

**Considerations**:
- No optimization - ignores risk/return characteristics
- May not be efficient
- Easy to implement and rebalance
- Surprisingly competitive in practice

**Research Note**: Studies show equal weight often outperforms optimized portfolios due to 
estimation errors in optimization inputs. It's the "wisdom of simplicity."

**Example**: 5 assets? Each gets 20%. Simple as that.
                """,
                'math': 'w_i = 1/N for all assets',
                'tips': [
                    'Great starting point for new investors',
                    'Consider 5-8 well-chosen assets',
                    'Rebalance periodically to maintain equal weights',
                    'Add constraints if you want slight optimization'
                ]
            },
            'max_return': {
                'title': '🚀 Maximum Return',
                'description': 'Pursues highest possible returns (aggressive)',
                'how_it_works': """
**Objective**: Maximize expected portfolio return

This aggressive strategy allocates to maximize expected returns, potentially with high risk.

**Best For**:
- Aggressive growth investors
- Long time horizons (20+ years)
- High risk tolerance
- Speculative allocations

**Considerations**:
- Typically very high volatility
- May concentrate in few high-return assets
- Requires strong risk tolerance
- Best with volatility constraints enabled

**Warning**: Without constraints, often concentrates 100% in the single highest-return asset. 
Use volatility limits or position constraints.

**Example**: Will heavily favor growth stocks, emerging markets, or high-risk assets.
                """,
                'math': 'Maximize: E[R] = w\'μ',
                'tips': [
                    'ALWAYS use constraints (max 20-25% per asset)',
                    'Consider max volatility constraint',
                    'Only for very long-term goals',
                    'Review allocations carefully before implementing'
                ]
            }
        }
        
        return strategies.get(strategy.lower().replace(' ', '_'), {
            'title': strategy,
            'description': 'Strategy information not available',
            'how_it_works': 'Please refer to documentation.',
            'tips': []
        })
    
    @staticmethod
    def get_metrics_explanation():
        """Explain portfolio metrics"""
        return {
            'Expected Return': {
                'description': 'Weighted average of asset returns based on portfolio allocation',
                'formula': 'E[R] = Σ(w_i × r_i)',
                'interpretation': 'Higher is better. Typical range: 4-12% annually',
                'example': 'If 60% stocks (10% return) + 40% bonds (4% return) = 7.6% expected return'
            },
            'Volatility': {
                'description': 'Standard deviation of returns - measures portfolio risk/variability',
                'formula': 'σ = √(w\'Σw)',
                'interpretation': 'Lower = more stable. Stocks ~15%, Bonds ~5%, Balanced ~10%',
                'example': '10% volatility means returns typically within ±10% of average'
            },
            'Sharpe Ratio': {
                'description': 'Risk-adjusted return - return per unit of risk taken',
                'formula': '(E[R] - Rf) / σ',
                'interpretation': '>1.0 = Good, >1.5 = Excellent, >2.0 = Outstanding',
                'example': '8% return, 10% vol, 3% risk-free = Sharpe of 0.5'
            },
            'Sortino Ratio': {
                'description': 'Like Sharpe but only penalizes downside volatility',
                'formula': '(E[R] - Rf) / σ_downside',
                'interpretation': 'Better than Sharpe for asymmetric returns. Higher is better.',
                'example': 'Useful when returns have different up vs. down volatility'
            },
            'Maximum Drawdown': {
                'description': 'Largest peak-to-trough decline in portfolio value',
                'formula': 'Max(Peak_i - Trough_j) for all i < j',
                'interpretation': '-20% = moderate, -30% = significant, -40%+ = severe',
                'example': 'Portfolio drops from $100k to $70k = -30% drawdown'
            },
            'Value at Risk (VaR)': {
                'description': 'Maximum expected loss over time period at confidence level',
                'formula': 'Percentile of return distribution',
                'interpretation': '95% VaR of -5% = 5% chance of losing >5%',
                'example': 'Helps quantify tail risk and worst-case scenarios'
            },
            'Conditional VaR (CVaR)': {
                'description': 'Average loss when VaR threshold is exceeded',
                'formula': 'E[Loss | Loss > VaR]',
                'interpretation': 'Always worse than VaR. Shows severity of tail events.',
                'example': 'If VaR=-5% and CVaR=-8%, losses beyond 5% average 8%'
            },
            'Diversification Score': {
                'description': 'How evenly spread your investments are (Herfindahl-Hirschman Index)',
                'formula': '(1 - Σw_i²) × 100',
                'interpretation': '85+ = Excellent, 70-85 = Good, <70 = Concentrated',
                'example': '10 equal positions (10% each) = 90 score'
            }
        }
    
    @staticmethod
    def get_constraints_guide():
        """Guide to using portfolio constraints"""
        return {
            'title': '⚖️ Portfolio Constraints Guide',
            'content': """
### Why Use Constraints?

Without constraints, optimizers often concentrate heavily in 1-3 "optimal" assets. While 
mathematically correct, this creates dangerous concentration risk.

### Types of Constraints:

**1. Position Limits (Min/Max Weight)**
- **Max Weight**: Prevents over-concentration in single asset
- **Min Weight**: Ensures all holdings are meaningful contributors

**2. Suggested Settings:**

**For 3-5 Assets (Focused Portfolio):**
- Max: 25-30% per asset
- Min: 10-15% per asset
- Allows some concentration while limiting extreme positions

**For 6-7 Assets (Balanced Portfolio):**
- Max: 20-25% per asset
- Min: 8-12% per asset
- Good balance of optimization and diversification

**For 8-10 Assets (Diversified Portfolio):**
- Max: 15-20% per asset
- Min: 8-10% per asset
- Forces true diversification across all holdings

### Feasibility Check:

Constraints must be feasible: **Min Weight × Number of Assets ≤ 100%**

Example: 10 assets with 12% minimum = 120% (INFEASIBLE!)
         10 assets with 8% minimum = 80% (OK, 20% flexibility)

### Impact on Strategies:

- **Max Sharpe**: Constraints prevent it from picking only "best" 1-2 assets
- **Min Volatility**: Forces inclusion of some growth assets
- **Risk Parity**: Works best WITH constraints (8-20%)
- **Equal Weight**: Constraints have no effect (already equal)

### Best Practice:

✅ Always enable constraints for Max Sharpe and Min Volatility
✅ Use 8-20% range for 8-10 asset portfolios
✅ Adjust based on your concentration tolerance
            """
        }
    
    @staticmethod
    def get_monte_carlo_guide():
        """Explain Monte Carlo simulation"""
        return {
            'title': '🎲 Monte Carlo Simulation Guide',
            'content': """
### What is Monte Carlo Simulation?

A statistical technique that runs thousands of scenarios to project possible future outcomes 
for your portfolio.

### How It Works:

1. **Random Sampling**: Generates random returns based on your portfolio's historical 
   return and volatility patterns

2. **Multiple Scenarios**: Runs 10,000 different possible futures

3. **Statistical Analysis**: Analyzes the distribution of outcomes

### Key Outputs:

**Percentile Analysis:**
- **10th Percentile**: Pessimistic scenario (10% chance of worse outcome)
- **25th Percentile**: Below-average scenario
- **50th Percentile (Median)**: Most likely outcome
- **75th Percentile**: Above-average scenario
- **90th Percentile**: Optimistic scenario (10% chance of better outcome)

**Risk Metrics:**
- **95% Value at Risk (VaR)**: 5% chance of losing more than this amount
- **95% CVaR**: Average loss when worst 5% scenarios occur

### Use Cases:

✅ **Retirement Planning**: Will I have enough in 20 years?
✅ **Goal Setting**: What's realistic to expect?
✅ **Risk Assessment**: How bad could it get?
✅ **Strategy Comparison**: Which approach has better odds?

### Interpreting Results:

- **Wide Range** (10th to 90th): High uncertainty/volatility
- **Narrow Range**: More predictable outcomes
- **Negative 10th Percentile**: Significant downside risk

### Parameters:

- **Time Horizon**: 1-30 years (longer = more uncertainty)
- **Initial Investment**: Your starting capital
- **Annual Contribution**: Optional ongoing investments
- **Simulations**: 10,000 (provides statistical reliability)

### Limitations:

⚠️ **Assumes**: Normal distribution of returns (reality can differ)
⚠️ **Based on**: Historical patterns (past ≠ future)
⚠️ **Doesn't include**: Black swan events, regime changes

### Best Practice:

Use Monte Carlo for planning, but understand it shows possibilities, not certainties. 
Focus on the range of outcomes, not a single projection.
            """
        }
    
    @staticmethod
    def get_rebalancing_guide():
        """Guide to portfolio rebalancing"""
        return {
            'title': '🔄 Rebalancing Guide',
            'content': """
### What is Rebalancing?

Periodically adjusting your portfolio back to target allocations as asset values change.

### Why Rebalance?

1. **Maintain Risk Level**: Winning assets grow, increasing risk beyond target
2. **Buy Low, Sell High**: Forces disciplined contrarian behavior
3. **Preserve Strategy**: Keeps portfolio aligned with optimization

### Example:

**Start**: 60% Stocks ($60k), 40% Bonds ($40k)
**After 1 Year**: Stocks → $75k (71%), Bonds → $42k (29%)
**Rebalancing**: Sell $6k stocks, buy $6k bonds → Back to 60/40

### Rebalancing Methods:

**1. Time-Based (Calendar)**
- Quarterly: Every 3 months
- Semi-Annual: Every 6 months  
- Annual: Once per year

**Pros**: Simple, disciplined
**Cons**: May rebalance unnecessarily or miss needed adjustments

**2. Threshold-Based (Drift)**
- 5% Drift: Rebalance when any asset drifts ±5% from target
- 10% Drift: More tolerance (less frequent trades)

**Pros**: Only trades when needed
**Cons**: Requires monitoring

**3. Combination**
- Annual review + 10% threshold (most common)

### Rebalancing Frequency Recommendations:

**Tax-Advantaged Accounts (IRA, 401k):**
- Rebalance 2-4 times per year (no tax impact)
- Use 5% drift threshold

**Taxable Accounts:**
- Rebalance once annually (minimize capital gains taxes)
- Use new contributions to rebalance when possible
- Consider tax-loss harvesting

**High-Volatility Portfolios:**
- Check quarterly, rebalance at 8-10% drift

**Low-Volatility Portfolios:**
- Check semi-annually, rebalance at 10-15% drift

### Costs to Consider:

- **Trading Commissions**: Usually $0 with modern brokers
- **Bid-Ask Spreads**: Minimal for liquid ETFs
- **Taxes**: Capital gains in taxable accounts
- **Opportunity Cost**: Missing out on momentum

### Smart Rebalancing Tips:

✅ Use new contributions to rebalance (avoid selling)
✅ Rebalance across all accounts together (tax efficiency)
✅ Consider "rebalancing bands" (e.g., 8-12% instead of exactly 10%)
✅ Don't rebalance too frequently (let winners run)
✅ Annual rebalancing is sufficient for most investors

### When NOT to Rebalance:

❌ In a crash (wait for recovery)
❌ Just because one asset is up (need significant drift)
❌ Creating large taxable events unnecessarily
            """
        }
    
    @staticmethod
    def get_strategy_comparison_guide():
        """Guide to comparing strategies"""
        return {
            'title': '⚖️ Strategy Comparison Guide',
            'content': """
### How to Compare Strategies

The Strategy Comparison feature runs all 4 optimization approaches on your portfolio 
simultaneously, allowing you to see trade-offs.

### What to Look For:

**1. Return vs. Risk**
- Scatter plot shows risk-return positioning
- Higher and left = better (more return, less risk)

**2. Sharpe Ratio**
- Best measure of risk-adjusted performance
- Higher = better bang-for-buck

**3. Allocated Assets**
- How many of your holdings get meaningful weight
- More = better diversification

**4. Max Drawdown**
- Worst historical decline
- Lower (less negative) = less pain

### Typical Patterns:

**Maximum Sharpe Ratio:**
- Usually best Sharpe ratio (by definition)
- Moderate risk, good returns
- May concentrate in 5-7 assets

**Minimum Volatility:**
- Lowest risk/volatility
- Lowest returns
- Often concentrates in bonds

**Risk Parity:**
- Best diversification (uses all assets)
- Balanced risk-return
- Consistent across markets

**Equal Weight:**
- Simple, transparent
- Often surprisingly competitive
- Uses all assets equally

### Decision Framework:

**Choose Max Sharpe if:**
- You want optimal risk-adjusted returns
- You're comfortable with some concentration
- You trust the optimization

**Choose Min Volatility if:**
- You prioritize stability over returns
- You're conservative/near retirement
- You want to sleep well at night

**Choose Risk Parity if:**
- You want true diversification
- You believe in all-weather approaches
- You want robust performance

**Choose Equal Weight if:**
- You want simplicity
- You're skeptical of optimization
- You want to use all holdings

### Advanced Tip:

Compare Sharpe ratios - if they're within 0.1-0.2, strategies are similar. 
Choose based on diversification preference rather than small Sharpe differences.
            """
        }
    
    @staticmethod
    def get_ai_insights_guide():
        """Guide to understanding AI insights"""
        return {
            'title': '🤖 AI Insights Guide',
            'content': """
### What Are AI Insights?

Our AI analysis system evaluates your portfolio across multiple dimensions and provides 
actionable recommendations based on Modern Portfolio Theory principles.

### Portfolio Health Score (0-100)

**Components:**
- Diversification quality (adjusted for portfolio size)
- Risk-adjusted returns (Sharpe ratio)
- Volatility appropriateness
- Number of strengths vs. weaknesses
- Risk alerts and concerns

**Grading Scale:**
- **90-100 (A+)**: Excellent - Institutional quality
- **80-89 (A)**: Very Good - Strong fundamentals
- **70-79 (B)**: Good - Solid construction
- **60-69 (C)**: Fair - Room for improvement
- **50-59 (D)**: Needs work - Significant issues
- **0-49 (F)**: Poor - Requires restructuring

**Size-Adjusted Expectations:**
- 3-5 assets: More lenient (focused strategy accepted)
- 6-7 assets: Moderate expectations
- 8-10 assets: Highest standards

### Insight Categories:

**💪 Portfolio Strengths**
- What your portfolio does well
- Advantages to maintain
- Areas of excellence

**✨ Opportunities**
- Potential enhancements
- Areas for optimization
- Strategic considerations

**💡 Recommendations**
- Specific action items
- Improvement suggestions
- Optimization ideas

**⚠️ Risk Alerts**
- Critical concerns
- High-priority issues
- Red flags to address

**🔧 Areas for Improvement**
- Weaknesses to fix
- Underperforming aspects
- Efficiency gaps

### How to Use AI Insights:

1. **Start with Health Score**: Understand overall quality
2. **Address Risk Alerts**: Fix critical issues first
3. **Review Strengths**: Understand what's working
4. **Consider Recommendations**: Implement improvements
5. **Monitor Progress**: Reoptimize and check new score

### Roadmap to A/B Grade (if score < 70):

**Shows:**
- Points needed for B grade (70) and A grade (80)
- Potential point gains from each action
- Prioritized action list
- Realistic achievability assessment
- Estimated timeframe

**Action Priority Levels:**
- 🔴 **High Priority**: Most impactful (15-25 points)
- ⚡ **Quick Wins**: Easy improvements (5-15 points)
- 📅 **Long-term**: Structural changes (ongoing)

### Interpreting Recommendations:

**Context-Aware**: Recommendations adjust based on:
- Number of assets (3 vs 10)
- Whether constraints are enabled
- Current strategy selection
- Your specific metrics

**Specific Advice**: Tells you EXACTLY what to do:
- Which slider to adjust
- Which strategy to try
- How many assets to add
- What constraint values to use

### Best Practice:

✅ Don't aim for perfection (95+ rare even for institutions)
✅ Focus on getting to 70+ (B grade = solid portfolio)
✅ Address high-priority items first
✅ Reoptimize after making changes
✅ Understand tradeoffs (can't have high return AND low risk)
            """
        }
