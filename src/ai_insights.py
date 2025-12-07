"""
AI-Powered Portfolio Insights and Recommendations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class AIInsights:
    """Generate intelligent portfolio insights and recommendations"""
    
    @staticmethod
    def analyze_portfolio(
        weights: np.ndarray,
        tickers: List[str],
        metrics: Dict,
        returns: pd.DataFrame,
        mean_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        strategy: str
    ) -> Dict:
        """
        Perform comprehensive AI analysis of portfolio
        
        Returns dict with insights, recommendations, and risk assessments
        """
        insights = {
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'risk_alerts': [],
            'opportunities': []
        }
        
        # Analyze diversification
        div_insights = AIInsights._analyze_diversification(weights, tickers, metrics)
        insights['strengths'].extend(div_insights.get('strengths', []))
        insights['recommendations'].extend(div_insights.get('recommendations', []))
        
        # Analyze risk profile
        risk_insights = AIInsights._analyze_risk_profile(metrics, returns)
        insights['strengths'].extend(risk_insights.get('strengths', []))
        insights['weaknesses'].extend(risk_insights.get('weaknesses', []))
        insights['risk_alerts'].extend(risk_insights.get('risk_alerts', []))
        
        # Analyze concentration
        conc_insights = AIInsights._analyze_concentration(weights, tickers)
        insights['recommendations'].extend(conc_insights.get('recommendations', []))
        insights['risk_alerts'].extend(conc_insights.get('risk_alerts', []))
        
        # Analyze correlations
        corr_insights = AIInsights._analyze_correlations(weights, tickers, returns)
        insights['strengths'].extend(corr_insights.get('strengths', []))
        insights['recommendations'].extend(corr_insights.get('recommendations', []))
        
        # Analyze strategy effectiveness
        strat_insights = AIInsights._analyze_strategy(strategy, metrics, weights)
        insights['recommendations'].extend(strat_insights.get('recommendations', []))
        insights['opportunities'].extend(strat_insights.get('opportunities', []))
        
        # Analyze return potential
        return_insights = AIInsights._analyze_returns(metrics, mean_returns, weights, tickers)
        insights['strengths'].extend(return_insights.get('strengths', []))
        insights['opportunities'].extend(return_insights.get('opportunities', []))
        insights['recommendations'].extend(return_insights.get('recommendations', []))
        
        return insights
    
    @staticmethod
    def _analyze_diversification(weights: np.ndarray, tickers: List[str], metrics: Dict) -> Dict:
        """Analyze portfolio diversification"""
        insights = {'strengths': [], 'recommendations': []}
        
        div_score = metrics.get('Diversification Score', 0)
        n_assets = len(tickers)
        
        # Adjust expectations based on number of assets
        if n_assets >= 8:
            # Well-diversified portfolio expectations
            if div_score >= 85:
                insights['strengths'].append(
                    f"🌟 **Excellent Diversification**: Your portfolio has a diversification score of {div_score:.0f}/100, "
                    f"indicating well-distributed risk across {n_assets} assets."
                )
            elif div_score >= 70:
                insights['strengths'].append(
                    f"✓ **Good Diversification**: Portfolio achieves a {div_score:.0f}/100 diversification score "
                    f"with balanced exposure across {n_assets} assets."
                )
            elif div_score >= 50:
                insights['recommendations'].append(
                    f"📊 **Improve Diversification**: Your score of {div_score:.0f}/100 with {n_assets} assets suggests some concentration. "
                    f"Consider adjusting constraints to spread risk more evenly across all holdings."
                )
            else:
                insights['recommendations'].append(
                    f"⚠️ **Concentration Risk**: Low diversification score ({div_score:.0f}/100) with {n_assets} assets. "
                    f"Enable or tighten weight constraints to improve risk distribution."
                )
        elif n_assets >= 6:
            # Balanced portfolio expectations (slightly lower thresholds)
            if div_score >= 75:
                insights['strengths'].append(
                    f"🌟 **Strong Diversification**: {div_score:.0f}/100 score with {n_assets} assets shows well-balanced risk exposure."
                )
            elif div_score >= 60:
                insights['strengths'].append(
                    f"✓ **Good Balance**: {div_score:.0f}/100 diversification with {n_assets} assets (balanced portfolio approach)."
                )
            elif div_score >= 40:
                insights['recommendations'].append(
                    f"📊 **Moderate Concentration**: {div_score:.0f}/100 with {n_assets} assets. Adjust constraints for better spread."
                )
            else:
                insights['recommendations'].append(
                    f"⚠️ **High Concentration**: {div_score:.0f}/100 indicates heavy weighting in few of your {n_assets} assets."
                )
        else:
            # Focused portfolio (3-5 assets) - more lenient expectations
            if div_score >= 65:
                insights['strengths'].append(
                    f"✓ **Well-Balanced Focused Portfolio**: {div_score:.0f}/100 score with {n_assets} assets shows good distribution "
                    f"for a concentrated strategy."
                )
            elif div_score >= 45:
                insights['strengths'].append(
                    f"✓ **Acceptable Focus**: {div_score:.0f}/100 with {n_assets} assets (focused portfolio - concentration is expected)."
                )
            elif div_score >= 25:
                insights['recommendations'].append(
                    f"📊 **Concentration in Focused Portfolio**: {div_score:.0f}/100 with {n_assets} assets. "
                    f"Consider balancing allocations or adding 1-2 more holdings."
                )
            else:
                insights['recommendations'].append(
                    f"⚠️ **Extreme Concentration**: {div_score:.0f}/100 suggests near-total weighting in 1-2 of your {n_assets} assets. "
                    f"Enable constraints or add more holdings for risk management."
                )
        
        return insights
    
    @staticmethod
    def _analyze_risk_profile(metrics: Dict, returns: pd.DataFrame) -> Dict:
        """Analyze risk characteristics"""
        insights = {'strengths': [], 'weaknesses': [], 'risk_alerts': []}
        
        volatility = metrics.get('Volatility', 0)
        sharpe = metrics.get('Sharpe Ratio', 0)
        max_dd = abs(metrics.get('Maximum Drawdown', 0))
        var_95 = abs(metrics.get('VaR (95%)', 0))
        
        # Volatility assessment
        if volatility < 0.08:
            insights['strengths'].append(
                f"🛡️ **Low Volatility**: Annual volatility of {volatility*100:.1f}% indicates a conservative, "
                f"stable portfolio suitable for risk-averse investors."
            )
        elif volatility < 0.15:
            insights['strengths'].append(
                f"⚖️ **Moderate Risk**: Volatility at {volatility*100:.1f}% represents a balanced risk level "
                f"appropriate for medium-term growth."
            )
        elif volatility < 0.25:
            insights['risk_alerts'].append(
                f"📈 **Elevated Volatility**: {volatility*100:.1f}% volatility suggests higher risk. "
                f"Expect larger price swings - suitable for growth-focused investors with longer horizons."
            )
        else:
            insights['risk_alerts'].append(
                f"⚠️ **High Volatility**: {volatility*100:.1f}% is significantly above market average. "
                f"This aggressive portfolio requires strong risk tolerance and long time horizon."
            )
        
        # Sharpe ratio assessment with educational context
        if sharpe > 1.5:
            insights['strengths'].append(
                f"⭐ **Excellent Risk-Adjusted Returns**: Sharpe ratio of {sharpe:.2f} indicates outstanding "
                f"return per unit of risk - well above the 1.0 benchmark. "
                f"**What this means**: You're earning {sharpe:.1f}x more return than risk-free investments per unit of risk. "
                f"Institutional portfolios typically target 1.0+."
            )
        elif sharpe > 1.0:
            insights['strengths'].append(
                f"✓ **Strong Risk Efficiency**: Sharpe ratio of {sharpe:.2f} shows good risk-adjusted performance. "
                f"**Interpretation**: For every 1% of volatility, you're gaining {sharpe:.2f}% excess return over risk-free rates. "
                f"This beats typical market efficiency."
            )
        elif sharpe > 0.5:
            insights['weaknesses'].append(
                f"📊 **Moderate Efficiency**: Sharpe ratio of {sharpe:.2f} is acceptable but could be improved. "
                f"**Why improve**: Higher Sharpe means getting more return without proportionally increasing risk. "
                f"Try better diversification, constraint adjustments, or alternative strategies."
            )
        else:
            insights['weaknesses'].append(
                f"⚠️ **Poor Risk Efficiency**: Low Sharpe ratio ({sharpe:.2f}) suggests returns don't adequately "
                f"compensate for risk taken. **Action needed**: You're experiencing significant volatility without "
                f"proportional returns. Consider Min Volatility or Risk Parity strategies for better balance."
            )
        
        # Drawdown assessment with investor context
        if max_dd > 0.30:
            insights['risk_alerts'].append(
                f"🔻 **Severe Drawdown Risk**: Historical maximum drawdown of {max_dd*100:.1f}% indicates "
                f"potential for significant temporary losses during market downturns. "
                f"**Real impact**: A $100k portfolio could drop to ${100000*(1-max_dd):.0f}. "
                f"**Action**: Ensure emergency funds are separate and you can avoid forced selling during downturns. "
                f"Consider adding defensive assets (bonds, low-volatility stocks)."
            )
        elif max_dd > 0.20:
            insights['risk_alerts'].append(
                f"📉 **Notable Drawdown**: {max_dd*100:.1f}% maximum drawdown is substantial. "
                f"**What this means**: During worst periods, your portfolio could decline by this amount before recovering. "
                f"**Investor psychology**: Ensure you can withstand seeing temporary losses of this magnitude without panic selling."
            )
        
        # VaR assessment with practical examples
        if var_95 > 0.05:
            insights['risk_alerts'].append(
                f"💰 **Value at Risk**: There's a 5% chance of losing more than {var_95*100:.1f}% in a single day. "
                f"**Practical example**: On a $100k portfolio, this means potential daily losses exceeding ${100000*var_95:.0f} "
                f"about once per month (1 in 20 trading days). "
                f"**Preparation**: Maintain adequate emergency reserves separate from this portfolio to avoid forced liquidation "
                f"during volatile periods."
            )
        
        return insights
    
    @staticmethod
    def _analyze_concentration(weights: np.ndarray, tickers: List[str]) -> Dict:
        """Analyze position concentration"""
        insights = {'recommendations': [], 'risk_alerts': []}
        
        max_weight = np.max(weights)
        min_weight = np.min(weights)
        top_3_weight = np.sum(sorted(weights, reverse=True)[:3])
        
        if max_weight > 0.40:
            insights['risk_alerts'].append(
                f"🎯 **High Concentration**: Largest position is {max_weight*100:.1f}% of portfolio. "
                f"**Risk impact**: Single asset dominance means portfolio success heavily depends on one holding's performance. "
                f"**Consider**: Even blue-chip stocks can decline 30-50% - ensure you're comfortable with this exposure."
            )
        elif max_weight > 0.25:
            insights['recommendations'].append(
                f"📍 **Notable Position**: Top holding at {max_weight*100:.1f}%. "
                f"**Diversification principle**: Modern Portfolio Theory suggests limiting single positions to 15-25% "
                f"to reduce unsystematic (company-specific) risk. Consider if this concentration aligns with your risk tolerance."
            )
        
        if top_3_weight > 0.60:
            insights['recommendations'].append(
                f"🔝 **Top-Heavy Portfolio**: Top 3 positions represent {top_3_weight*100:.1f}% of portfolio. "
                f"**Why diversify**: If these 3 assets underperform simultaneously (e.g., same sector correction), "
                f"your entire portfolio suffers. Broadening holdings reduces this correlation risk."
            )
        
        if min_weight < 0.02 and min_weight > 0:
            insights['recommendations'].append(
                f"💡 **Small Positions**: Smallest allocation is {min_weight*100:.1f}%. "
                f"**Portfolio efficiency**: Positions under 2-3% have minimal impact on overall performance "
                f"but add tracking complexity. **Consider**: Consolidating tiny positions into larger, more meaningful "
                f"allocations that can actually move the needle on portfolio returns."
            )
        
        return insights
    
    @staticmethod
    def _analyze_correlations(weights: np.ndarray, tickers: List[str], returns: pd.DataFrame) -> Dict:
        """Analyze correlation structure"""
        insights = {'strengths': [], 'recommendations': []}
        
        # Calculate weighted correlation
        corr_matrix = returns.corr()
        
        # Get average correlation between holdings
        n = min(len(weights), len(tickers), len(returns.columns))
        if n > 1:
            correlations = []
            for i in range(n - 1):  # Changed from range(n)
                for j in range(i + 1, n):
                    # Both i and j are guaranteed to be < n, which is <= len(weights)
                    if weights[i] > 0.01 and weights[j] > 0.01:  # Only consider meaningful positions
                        correlations.append(corr_matrix.iloc[i, j])
            
            if correlations:
                avg_corr = np.mean(correlations)
                
                if avg_corr < 0.3:
                    insights['strengths'].append(
                        f"🔀 **Low Correlation**: Average correlation of {avg_corr:.2f} indicates strong diversification benefits. "
                        f"Assets tend to move independently, reducing overall portfolio risk."
                    )
                elif avg_corr < 0.6:
                    insights['strengths'].append(
                        f"✓ **Moderate Correlation**: {avg_corr:.2f} average correlation provides reasonable diversification "
                        f"while maintaining coherent portfolio behavior."
                    )
                elif avg_corr < 0.8:
                    insights['recommendations'].append(
                        f"🔗 **High Correlation**: Assets show {avg_corr:.2f} average correlation. "
                        f"Consider adding uncorrelated assets (bonds, commodities, international) for better diversification."
                    )
                else:
                    insights['recommendations'].append(
                        f"⚠️ **Very High Correlation**: {avg_corr:.2f} suggests assets move together. "
                        f"Limited diversification benefit - add negatively correlated or uncorrelated assets."
                    )
        
        return insights
    
    @staticmethod
    def _analyze_strategy(strategy: str, metrics: Dict, weights: np.ndarray) -> Dict:
        """Analyze strategy appropriateness"""
        insights = {'recommendations': [], 'opportunities': []}
        
        sharpe = metrics.get('Sharpe Ratio', 0)
        volatility = metrics.get('Volatility', 0)
        expected_return = metrics.get('Expected Return', 0)
        
        if strategy == "Maximum Sharpe Ratio":
            if sharpe < 0.8:
                insights['recommendations'].append(
                    f"🎯 **Strategy Review**: Max Sharpe achieved {sharpe:.2f} ratio. "
                    f"Consider if constraints are too restrictive or if asset selection needs refinement."
                )
            else:
                insights['opportunities'].append(
                    f"✨ **Optimal Efficiency**: Max Sharpe strategy achieved {sharpe:.2f} ratio, "
                    f"representing the best risk-adjusted returns available from your assets."
                )
        
        elif strategy == "Minimum Volatility":
            insights['opportunities'].append(
                f"🛡️ **Defensive Position**: Min Volatility achieved {volatility*100:.1f}% risk - "
                f"ideal for capital preservation and reducing portfolio stress during market turmoil."
            )
            if expected_return < 0.05:
                insights['recommendations'].append(
                    f"📊 **Return Trade-off**: {expected_return*100:.1f}% expected return is conservative. "
                    f"If you can tolerate more risk, consider Max Sharpe for better growth potential."
                )
        
        elif strategy == "Risk Parity":
            insights['opportunities'].append(
                f"⚖️ **Balanced Risk**: Risk Parity equalizes risk contribution across assets, "
                f"providing robust diversification that performs well in various market conditions."
            )
        
        elif strategy == "Equal Weight":
            insights['recommendations'].append(
                f"💡 **Simple Approach**: Equal weighting is transparent but ignores risk-return optimization. "
                f"Try Max Sharpe or Risk Parity for potentially better risk-adjusted performance."
            )
        
        return insights
    
    @staticmethod
    def _analyze_returns(metrics: Dict, mean_returns: pd.Series, weights: np.ndarray, tickers: List[str]) -> Dict:
        """Analyze return characteristics"""
        insights = {'strengths': [], 'opportunities': [], 'recommendations': []}
        
        expected_return = metrics.get('Expected Return', 0)
        volatility = metrics.get('Volatility', 0)
        
        # Return level assessment
        if expected_return > 0.12:
            insights['strengths'].append(
                f"🚀 **Strong Growth Potential**: {expected_return*100:.1f}% expected annual return "
                f"positions portfolio for significant long-term wealth accumulation."
            )
        elif expected_return > 0.08:
            insights['strengths'].append(
                f"📈 **Solid Returns**: {expected_return*100:.1f}% expected return exceeds typical bond yields "
                f"while maintaining reasonable risk."
            )
        elif expected_return > 0.04:
            insights['opportunities'].append(
                f"💰 **Conservative Returns**: {expected_return*100:.1f}% return is modest. "
                f"If appropriate for your timeline, consider adding growth-oriented assets."
            )
        else:
            insights['recommendations'].append(
                f"📉 **Low Return Potential**: {expected_return*100:.1f}% may not meet long-term goals. "
                f"Review if portfolio is too conservative for your needs."
            )
        
        # Risk-return ratio
        return_to_risk = expected_return / volatility if volatility > 0 else 0
        if return_to_risk > 0.8:
            insights['strengths'].append(
                f"⭐ **Excellent Balance**: Return-to-risk ratio of {return_to_risk:.2f} shows strong "
                f"compensation for volatility undertaken."
            )
        
        # Identify top contributors
        # Ensure arrays match in size
        n = min(len(mean_returns), len(weights), len(tickers))
        if n > 0:
            # Handle both pandas Series and numpy arrays
            mean_ret_array = mean_returns.values if hasattr(mean_returns, 'values') else mean_returns
            weighted_returns = mean_ret_array[:n] * weights[:n]
            top_contributor_idx = np.argmax(weighted_returns)
            top_contributor = tickers[top_contributor_idx]
            contribution = weighted_returns[top_contributor_idx] / expected_return if expected_return > 0 else 0
            
            insights['opportunities'].append(
                f"🎯 **Top Performer**: {top_contributor} contributes approximately {contribution*100:.0f}% "
                f"of portfolio's expected return. Monitor this key position closely."
            )
        
        return insights
    
    @staticmethod
    def generate_action_items(insights: Dict) -> List[str]:
        """Generate prioritized action items from insights"""
        actions = []
        
        def extract_title(text: str) -> str:
            """Extract clean title from markdown-formatted insight text"""
            # Remove emoji at start (optional)
            import re
            text = re.sub(r'^[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]+\s*', '', text)
            
            # Extract text between ** markers
            if '**' in text:
                parts = text.split('**')
                if len(parts) >= 3:
                    return parts[1].strip()
                # Fallback: remove all ** and take first part
                text = text.replace('**', '')
            
            # Extract text before colon
            if ':' in text:
                return text.split(':')[0].strip()
            
            # Fallback: first 80 chars
            return text[:80].strip()
        
        # High priority - risk alerts
        if insights['risk_alerts']:
            actions.append("🔴 **High Priority - Address Risk Concerns:**")
            for alert in insights['risk_alerts'][:3]:  # Top 3 risks
                title = extract_title(alert)
                actions.append(f"  • {title}")
        
        # Medium priority - weaknesses
        if insights['weaknesses']:
            actions.append("🟡 **Medium Priority - Improve Weaknesses:**")
            for weakness in insights['weaknesses'][:2]:
                title = extract_title(weakness)
                actions.append(f"  • {title}")
        
        # Low priority - recommendations  
        if insights['recommendations']:
            actions.append("🟢 **Consider for Optimization:**")
            for rec in insights['recommendations'][:2]:
                title = extract_title(rec)
                actions.append(f"  • {title}")
        
        return actions
    
    @staticmethod
    def get_portfolio_health_score(insights: Dict, metrics: Dict, n_assets: int = 10) -> Tuple[int, str]:
        """
        Calculate overall portfolio health score (0-100)
        
        Args:
            insights: Dictionary of portfolio insights
            metrics: Portfolio metrics
            n_assets: Number of assets in portfolio
        
        Returns: (score, grade_label)
        """
        score = 50  # Start at neutral
        
        # Add points for strengths (max +40)
        score += min(len(insights['strengths']) * 8, 40)
        
        # Deduct points for weaknesses and risks (max -40)
        score -= min(len(insights['weaknesses']) * 6, 20)
        score -= min(len(insights['risk_alerts']) * 10, 20)
        
        # Adjust for key metrics
        sharpe = metrics.get('Sharpe Ratio', 0)
        if sharpe > 1.5:
            score += 15
        elif sharpe > 1.0:
            score += 10
        elif sharpe > 0.5:
            score += 3
        elif sharpe < 0.3:
            score -= 10
        
        # Diversification scoring adjusted for portfolio size
        div_score = metrics.get('Diversification Score', 0)
        
        if n_assets >= 8:
            # Well-diversified portfolio expectations
            if div_score >= 85:
                score += 12
            elif div_score >= 70:
                score += 6
            elif div_score >= 50:
                score += 0
            else:
                score -= 15
        elif n_assets >= 6:
            # Balanced portfolio expectations
            if div_score >= 75:
                score += 12
            elif div_score >= 60:
                score += 6
            elif div_score >= 40:
                score += 0
            else:
                score -= 10
        else:
            # Focused portfolio (3-5 assets)
            if div_score >= 65:
                score += 10
            elif div_score >= 45:
                score += 5
            elif div_score >= 25:
                score += 0
            else:
                score -= 8
        
        # Volatility check
        volatility = metrics.get('Volatility', 0)
        if volatility < 0.08:
            score += 5  # Low volatility bonus
        elif volatility > 0.25:
            score -= 8  # High volatility penalty
        
        # Return efficiency check
        expected_return = metrics.get('Expected Return', 0)
        if expected_return > 0.10:
            score += 5
        elif expected_return < 0.03:
            score -= 5
        
        # Cap between 0-100
        score = max(0, min(100, score))
        
        # Determine grade
        if score >= 90:
            grade = "A+ (Excellent)"
        elif score >= 80:
            grade = "A (Very Good)"
        elif score >= 70:
            grade = "B (Good)"
        elif score >= 60:
            grade = "C (Fair)"
        elif score >= 50:
            grade = "D (Needs Improvement)"
        else:
            grade = "F (Poor)"
        
        return score, grade
    
    @staticmethod
    def generate_improvement_plan(insights: Dict, metrics: Dict, current_score: int, current_grade: str, 
                                 n_assets: int = 0, constraints_enabled: bool = False, 
                                 min_weight: float = 0.0, max_weight: float = 1.0) -> Dict:
        """
        Generate specific improvement plan to reach Grade A or B
        
        Args:
            insights: AI insights dictionary
            metrics: Portfolio metrics
            current_score: Current health score
            current_grade: Current grade label
            n_assets: Number of assets in portfolio
            constraints_enabled: Whether constraints are currently enabled
            min_weight: Current minimum weight constraint
            max_weight: Current maximum weight constraint
        
        Returns dict with target scores and specific actionable steps
        """
        improvement_plan = {
            'current_score': current_score,
            'current_grade': current_grade,
            'target_b_score': 70,
            'target_a_score': 80,
            'points_needed_for_b': max(0, 70 - current_score),
            'points_needed_for_a': max(0, 80 - current_score),
            'priority_actions': [],
            'quick_wins': [],
            'long_term_improvements': []
        }
        
        sharpe = metrics.get('Sharpe Ratio', 0)
        div_score = metrics.get('Diversification Score', 0)
        volatility = metrics.get('Volatility', 0)
        expected_return = metrics.get('Expected Return', 0)
        max_dd = abs(metrics.get('Maximum Drawdown', 0))
        
        # Analyze what's holding the score back
        score_gaps = []
        
        # 1. Check Sharpe Ratio (potential: +15 to +25 points)
        if sharpe < 1.0:
            potential_gain = 10 if sharpe < 0.5 else 0
            if sharpe < 1.5:
                potential_gain += (15 if sharpe < 1.0 else 5)
            
            score_gaps.append({
                'issue': 'Low Sharpe Ratio',
                'current': sharpe,
                'potential_points': potential_gain,
                'priority': 1
            })
            
            if sharpe < 0.8:
                improvement_plan['priority_actions'].append(
                    f"🎯 **Improve Risk-Adjusted Returns (Sharpe Ratio)**: Current {sharpe:.2f} → Target 1.0+\n"
                    f"   • Switch to 'Maximum Sharpe Ratio' optimization strategy\n"
                    f"   • This alone could add up to {potential_gain} points to your score\n"
                    f"   • Enable weight constraints (8-20% per asset) for better diversification"
                )
            else:
                improvement_plan['long_term_improvements'].append(
                    f"📈 **Optimize Sharpe Ratio**: Move from {sharpe:.2f} to 1.2+ (potential +{potential_gain} points)\n"
                    f"   • Review asset selection - replace low performers\n"
                    f"   • Consider adding uncorrelated assets (bonds, gold, international)"
                )
        
        # 2. Check Diversification (potential: +10 to +25 points)
        if div_score < 85:
            potential_gain = 15 if div_score < 50 else (10 if div_score < 70 else 5)
            potential_gain += 10  # Max possible from diversification
            
            score_gaps.append({
                'issue': 'Poor Diversification',
                'current': div_score,
                'potential_points': potential_gain,
                'priority': 2 if div_score < 50 else 3
            })
            
            if div_score < 70:
                # Context-aware recommendations based on portfolio size and constraints
                if not constraints_enabled:
                    improvement_plan['priority_actions'].append(
                        f"📊 **Fix Concentration Issues**: Current {div_score:.0f}/100 → Target 85+\n"
                        f"   • Enable portfolio constraints in sidebar (Max: 20%, Min: 8%)\n"
                        f"   • This will force diversification across all {n_assets} assets\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
                elif n_assets < 5:
                    improvement_plan['priority_actions'].append(
                        f"📊 **Fix Concentration Issues**: Current {div_score:.0f}/100 → Target 70+\n"
                        f"   • You have {n_assets} assets (Focused portfolio - minimum 3 required)\n"
                        f"   • Consider adding 1-2 more holdings for better risk management\n"
                        f"   • Suggested: Add bonds (BND/AGG) or international (VXUS) for diversification\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
                elif n_assets < 6:
                    improvement_plan['quick_wins'].append(
                        f"📊 **Enhance Diversification**: Current {div_score:.0f}/100 → Target 75+\n"
                        f"   • You have {n_assets} assets (Focused portfolio - acceptable range)\n"
                        f"   • Optional: Add 1-3 more holdings to reach 6-8 assets for better spread\n"
                        f"   • Or adjust constraints: Lower max to 18% and raise min to 10%\n"
                        f"   • Current approach is valid for concentrated strategy"
                    )
                elif n_assets < 8:
                    improvement_plan['quick_wins'].append(
                        f"📊 **Optimize Diversification**: Current {div_score:.0f}/100 → Target 80+\n"
                        f"   • You have {n_assets} assets (Balanced portfolio)\n"
                        f"   • Add 1-3 more holdings to reach 8-10 assets for optimal diversification\n"
                        f"   • Add holdings from different asset classes (bonds, international, REITs)\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
                elif max_weight > 0.25:
                    improvement_plan['priority_actions'].append(
                        f"📊 **Fix Concentration Issues**: Current {div_score:.0f}/100 → Target 85+\n"
                        f"   • Constraints enabled but max weight ({max_weight*100:.0f}%) is too high\n"
                        f"   • Reduce max weight to 20% or lower to force better spread\n"
                        f"   • With {n_assets} assets, aim for max 15-20% per holding\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
                elif min_weight < 0.05:
                    improvement_plan['priority_actions'].append(
                        f"📊 **Fix Concentration Issues**: Current {div_score:.0f}/100 → Target 85+\n"
                        f"   • Constraints enabled but min weight ({min_weight*100:.0f}%) is too low\n"
                        f"   • Increase min weight to 8-10% to prevent tiny allocations\n"
                        f"   • This forces meaningful diversification across all {n_assets} holdings\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
                else:
                    improvement_plan['priority_actions'].append(
                        f"📊 **Fix Concentration Issues**: Current {div_score:.0f}/100 → Target 85+\n"
                        f"   • Constraints enabled ({min_weight*100:.0f}%-{max_weight*100:.0f}%) with {n_assets} assets\n"
                        f"   • Try 'Risk Parity' strategy for equal risk contribution\n"
                        f"   • Or switch to 'Equal Weight' (1/{n_assets} each = {100/n_assets:.1f}% each)\n"
                        f"   • Your current strategy may be concentrating despite constraints\n"
                        f"   • This could add {potential_gain} points to your health score"
                    )
            else:
                improvement_plan['quick_wins'].append(
                    f"🔄 **Fine-tune Diversification**: {div_score:.0f}/100 → 85+ (potential +{potential_gain} points)\n"
                    f"   • Adjust min weight constraint to 8-10% per asset\n"
                    f"   • Ensure all holdings contribute meaningfully"
                )
        
        # 3. Check Risk Alerts (potential: +10 each resolved)
        if insights['risk_alerts']:
            num_alerts = len(insights['risk_alerts'])
            potential_gain = num_alerts * 10
            
            score_gaps.append({
                'issue': 'Active Risk Alerts',
                'current': num_alerts,
                'potential_points': potential_gain,
                'priority': 1
            })
            
            improvement_plan['priority_actions'].append(
                f"⚠️ **Address {num_alerts} Risk Alert(s)**: (potential +{potential_gain} points)\n"
                f"   • High volatility ({volatility*100:.1f}%): Add bonds or defensive assets (BND, AGG, SGOV)\n"
                f"   • High drawdown ({max_dd*100:.1f}%): Try 'Minimum Volatility' or 'Risk Parity' strategy\n"
                f"   • Concentration risk: Enable weight constraints to limit single positions"
            )
        
        # 4. Check Weaknesses (potential: +6 each resolved)
        if insights['weaknesses']:
            num_weaknesses = len(insights['weaknesses'])
            potential_gain = num_weaknesses * 6
            
            score_gaps.append({
                'issue': 'Portfolio Weaknesses',
                'current': num_weaknesses,
                'potential_points': potential_gain,
                'priority': 2
            })
            
            improvement_plan['long_term_improvements'].append(
                f"🔧 **Resolve {num_weaknesses} Weakness(es)**: (potential +{potential_gain} points)\n"
                f"   • Poor risk efficiency: Optimize using better strategy\n"
                f"   • Review and replace underperforming assets\n"
                f"   • Consider professional portfolio review if issues persist"
            )
        
        # 5. Check if portfolio is too conservative
        if expected_return < 0.06 and volatility < 0.10:
            improvement_plan['quick_wins'].append(
                f"💰 **Boost Returns Without Excessive Risk**:\n"
                f"   • Current return {expected_return*100:.1f}% is very conservative\n"
                f"   • Add growth-oriented ETFs (VTI, VOO, SCHG) at 20-30% allocation\n"
                f"   • Target 7-9% expected return with moderate risk (10-12% volatility)"
            )
        
        # 6. Check if portfolio is too aggressive
        if volatility > 0.20 and sharpe < 0.8:
            improvement_plan['quick_wins'].append(
                f"🛡️ **Reduce Risk Without Sacrificing Returns**:\n"
                f"   • Volatility {volatility*100:.1f}% is high with poor Sharpe {sharpe:.2f}\n"
                f"   • Add 20-30% bonds (BND, AGG) or short-term Treasuries (SGOV)\n"
                f"   • Switch to 'Risk Parity' strategy for balanced risk distribution"
            )
        
        # Sort score gaps by priority and potential gain
        score_gaps.sort(key=lambda x: (x['priority'], -x['potential_points']))
        
        # Calculate realistic path to Grade B and A
        total_potential = sum(gap['potential_points'] for gap in score_gaps)
        
        improvement_plan['total_potential_gain'] = total_potential
        improvement_plan['realistic_max_score'] = min(100, current_score + total_potential)
        
        # Generate summary recommendation
        if improvement_plan['points_needed_for_b'] <= total_potential:
            improvement_plan['achievable_grade'] = 'A' if improvement_plan['points_needed_for_a'] <= total_potential else 'B'
            improvement_plan['confidence'] = 'High'
            improvement_plan['summary'] = f"Grade {improvement_plan['achievable_grade']} is achievable by implementing the recommended changes."
        else:
            improvement_plan['achievable_grade'] = current_grade
            improvement_plan['confidence'] = 'Low'
            improvement_plan['summary'] = "Significant portfolio restructuring needed. Consider working with a financial advisor."
        
        # Add estimated timeframe
        if improvement_plan['points_needed_for_b'] <= 15:
            improvement_plan['timeframe'] = "Quick wins available - Grade B achievable immediately with constraint adjustments"
        elif improvement_plan['points_needed_for_b'] <= 30:
            improvement_plan['timeframe'] = "Grade B achievable within 1-2 portfolio rebalances"
        else:
            improvement_plan['timeframe'] = "Grade B requires fundamental portfolio restructuring (3-6 months)"
        
        return improvement_plan
