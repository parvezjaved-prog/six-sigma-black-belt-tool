"""
═══════════════════════════════════════════════════════════════════════════════
    COMPLETE SIX SIGMA BLACK BELT PROJECT SYSTEM
    
    End-to-End DMAIC Project Management with:
    - Detailed result interpretations
    - Automated project planning with timelines
    - FMEA, Risk Analysis, Cost-Benefit
    - What-if scenario calculations
    - Industry best practices and recommendations
    - Complete documentation from Charter to Handoff
    
    Version 4.0 - Complete Professional System
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import statsmodels.api as sm
from datetime import datetime, timedelta
import json
from io import BytesIO
import base64

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Complete Six Sigma DMAIC System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# STYLING
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .interpretation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .recommendation-box {
        background: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .error-box {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .timeline-item {
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .phase-complete {
        background: #d4edda;
        border-left-color: #28a745;
    }
    
    .phase-current {
        background: #fff3cd;
        border-left-color: #ffc107;
    }
    
    .phase-upcoming {
        background: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .next-step {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: bold;
    }
    
    h1, h2, h3 {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE - Complete Project Data
# ═══════════════════════════════════════════════════════════════════════════════

if 'project' not in st.session_state:
    st.session_state.project = {
        # Project Metadata
        'name': '',
        'type': '',  # Manufacturing, Service, Transactional
        'created_date': datetime.now(),
        'start_date': None,
        'target_end_date': None,
        'actual_end_date': None,
        'status': 'Not Started',  # Not Started, In Progress, Completed
        'current_phase': 'Define',
        
        # Team
        'champion': '',
        'black_belt': '',
        'process_owner': '',
        'team_members': [],
        
        # Define Phase
        'define': {
            'complete': False,
            'completion_date': None,
            'business_case': '',
            'problem_statement': '',
            'goal_statement': '',
            'scope_in': '',
            'scope_out': '',
            'sipoc': {},
            'voc': [],
            'ctqs': [],
            'stakeholders': []
        },
        
        # Measure Phase
        'measure': {
            'complete': False,
            'completion_date': None,
            'data_collection_plan': {},
            'msa_complete': False,
            'msa_results': {},
            'baseline_data': None,
            'baseline_sigma': None,
            'baseline_dpmo': None,
            'baseline_cpk': None,
            'process_stable': None,
            'process_normal': None
        },
        
        # Analyze Phase
        'analyze': {
            'complete': False,
            'completion_date': None,
            'fishbone': {},
            'five_whys': [],
            'root_causes_identified': [],
            'root_causes_verified': [],
            'hypothesis_tests': [],
            'regression_results': {},
            'critical_xs': []
        },
        
        # Improve Phase
        'improve': {
            'complete': False,
            'completion_date': None,
            'brainstormed_solutions': [],
            'selected_solutions': [],
            'fmea': [],
            'doe_plan': {},
            'doe_results': {},
            'pilot_plan': {},
            'pilot_results': {},
            'cost_benefit': {},
            'implementation_plan': [],
            'improved_sigma': None,
            'improved_dpmo': None,
            'improved_cpk': None
        },
        
        # Control Phase
        'control': {
            'complete': False,
            'completion_date': None,
            'control_plan': {},
            'sop_updated': False,
            'training_complete': False,
            'monitoring_system': {},
            'response_plan': {},
            'handoff_complete': False,
            'final_sigma': None,
            'sustained_sigma': None
        },
        
        # Overall Metrics
        'financial_impact': {
            'hard_savings': 0,
            'soft_savings': 0,
            'cost_avoidance': 0,
            'total_benefit': 0,
            'investment': 0,
            'roi': 0,
            'payback_months': 0
        },
        
        # Milestones & Timeline
        'milestones': [],
        'timeline': {},
        
        # Recommendations & Next Steps
        'current_recommendations': [],
        'next_steps': [],
        
        # Documentation
        'documents_generated': [],
        'charts_created': []
    }

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS - Detailed Interpretations
# ═══════════════════════════════════════════════════════════════════════════════

def interpret_sigma_level(sigma, dpmo):
    """Provide detailed interpretation of Sigma level"""
    
    if sigma >= 6:
        level = "World Class"
        color = "🟢"
        benchmark = "Achieved by less than 1% of companies globally"
        quality = "99.99966% yield - virtually defect-free"
        examples = "Aviation safety, pharmaceutical manufacturing"
        action = "Focus on maintaining this exceptional level and sharing best practices"
        business_impact = "Premium pricing capability, industry leadership, minimal quality costs"
        
    elif sigma >= 5:
        level = "Excellent"
        color = "🟢"
        benchmark = "Top 5% of companies - industry leading performance"
        quality = "99.9767% yield - 233 defects per million"
        examples = "Top automotive manufacturers, leading hospitals"
        action = "Sustain current performance and target 6 Sigma for critical processes"
        business_impact = "Strong competitive advantage, high customer loyalty, low cost of quality"
        
    elif sigma >= 4:
        level = "Good"
        color = "🟡"
        benchmark = "Better than average - top quartile performance"
        quality = "99.379% yield - 6,210 defects per million"
        examples = "Most modern manufacturing, good service operations"
        action = "Continue improvement efforts, focus on critical CTQs to reach 5 Sigma"
        business_impact = "Competitive position maintained, moderate quality costs"
        
    elif sigma >= 3:
        level = "Average"
        color = "🟠"
        benchmark = "Typical industry performance - middle 50%"
        quality = "93.32% yield - 66,807 defects per million"
        examples = "Traditional manufacturing, typical service industries"
        action = "Significant improvement opportunity - prioritize DMAIC projects"
        business_impact = "High quality costs (15-20% of sales), customer complaints common"
        
    elif sigma >= 2:
        level = "Poor"
        color = "🔴"
        benchmark = "Below industry average - bottom quartile"
        quality = "69.15% yield - 308,538 defects per million"
        examples = "Struggling operations, high rework environments"
        action = "URGENT - Immediate improvement required. Start with quick wins."
        business_impact = "Very high quality costs (25-40% of sales), customer defection risk"
        
    else:
        level = "Critical"
        color = "⛔"
        benchmark = "Non-competitive - survival threatened"
        quality = f"{(1-dpmo/1000000)*100:.1f}% yield - {dpmo:,.0f} defects per million"
        examples = "Crisis situations requiring immediate intervention"
        action = "CRISIS MODE - Senior leadership attention required immediately"
        business_impact = "Business viability at risk, major customer loss likely"
    
    return {
        'level': level,
        'color': color,
        'benchmark': benchmark,
        'quality': quality,
        'examples': examples,
        'action': action,
        'business_impact': business_impact,
        'sigma': sigma,
        'dpmo': dpmo
    }

def interpret_cpk(cpk, cp):
    """Detailed Cpk interpretation with recommendations"""
    
    if cpk >= 2.0:
        rating = "Excellent - Six Sigma Capable"
        color = "🟢"
        meaning = "Process comfortably meets specifications with significant margin"
        defect_rate = "< 3.4 PPM - Virtually defect-free"
        action = "Monitor and maintain. Focus resources on other processes."
        business_value = "Premium quality capability, potential for tighter specs or cost reduction"
        
    elif cpk >= 1.67:
        rating = "Very Good - Highly Capable"
        color = "🟢"
        meaning = "Process consistently meets requirements with good margin"
        defect_rate = "< 0.6 PPM expected"
        action = "Continue monitoring. Consider process optimization for cost reduction."
        business_value = "Reliable quality, low inspection needs, customer confidence high"
        
    elif cpk >= 1.33:
        rating = "Good - Capable"
        color = "🟡"
        meaning = "Process meets requirements but has limited margin"
        defect_rate = "< 63 PPM expected"
        action = "Maintain current performance. Reduce variation if possible."
        business_value = "Acceptable quality, some inspection may be needed"
        
    elif cpk >= 1.0:
        rating = "Marginal - Barely Capable"
        color = "🟠"
        meaning = "Process just meets specifications - high risk of defects"
        defect_rate = "2,700 PPM expected (0.27%)"
        action = "Improvement needed. Increase monitoring, consider centering process."
        business_value = "High quality costs, customer complaints likely, rework common"
        
    else:
        rating = "Not Capable"
        color = "🔴"
        meaning = "Process cannot consistently meet specifications"
        defect_rate = "> 2,700 PPM - Significant defects expected"
        action = "URGENT: Process improvement required. Consider 100% inspection until improved."
        business_value = "Very high costs, customer satisfaction at risk, may need to halt production"
    
    centering_issue = abs(cp - cpk) > 0.2
    centering_advice = ""
    
    if centering_issue:
        if cp > cpk:
            centering_advice = "⚠️ Process is off-center. Centering the process could improve Cpk significantly without reducing variation."
        else:
            centering_advice = "✅ Process is well-centered. Focus on reducing variation (improving Cp) to improve capability."
    
    return {
        'rating': rating,
        'color': color,
        'meaning': meaning,
        'defect_rate': defect_rate,
        'action': action,
        'business_value': business_value,
        'centering_issue': centering_issue,
        'centering_advice': centering_advice,
        'cpk': cpk,
        'cp': cp
    }

def interpret_control_chart(data, ucl, lcl, mean, out_of_control_points):
    """Detailed control chart interpretation"""
    
    total_points = len(data)
    ooc_count = len(out_of_control_points) if isinstance(out_of_control_points, (list, pd.Index)) else out_of_control_points
    
    if ooc_count == 0:
        status = "In Statistical Control"
        color = "🟢"
        meaning = "Process shows only common cause variation - predictable and stable"
        action = "Process is stable. Can proceed with capability analysis and improvement."
        investigation = "No special causes detected. Continue routine monitoring."
        
    elif ooc_count <= total_points * 0.05:  # Less than 5%
        status = "Mostly Stable with Few Exceptions"
        color = "🟡"
        meaning = f"{ooc_count} out-of-control point(s) detected - investigate but process is largely stable"
        action = "Investigate the out-of-control points. If assignable cause found, remove and recalculate limits."
        investigation = f"Review the {ooc_count} exceptional point(s). Look for: operator changes, material lot changes, equipment issues, measurement errors."
        
    else:
        status = "Out of Control"
        color = "🔴"
        meaning = f"{ooc_count} out-of-control points - process is unstable and unpredictable"
        action = "STOP capability analysis. Focus on achieving statistical control first."
        investigation = "Systematic investigation required. Process capability cannot be assessed until stability is achieved."
    
    # Check for runs and patterns (Western Electric Rules)
    runs_detected = check_western_electric_rules(data, mean, ucl, lcl)
    
    return {
        'status': status,
        'color': color,
        'meaning': meaning,
        'action': action,
        'investigation': investigation,
        'ooc_count': ooc_count,
        'total_points': total_points,
        'runs_detected': runs_detected
    }

def check_western_electric_rules(data, mean, ucl, lcl):
    """Check for patterns using Western Electric Rules"""
    
    sigma = (ucl - mean) / 3
    zone_a_upper = mean + 2*sigma
    zone_a_lower = mean - 2*sigma
    zone_b_upper = mean + sigma
    zone_b_lower = mean - sigma
    
    violations = []
    
    # Rule 1: One point beyond 3 sigma (already checked)
    
    # Rule 2: 2 out of 3 consecutive points in Zone A or beyond
    for i in range(len(data) - 2):
        window = data[i:i+3]
        beyond_zone_a = sum((window > zone_a_upper) | (window < zone_a_lower))
        if beyond_zone_a >= 2:
            violations.append(f"Rule 2 violation at point {i+3}: 2 of 3 points beyond 2-sigma")
    
    # Rule 3: 4 out of 5 consecutive points in Zone B or beyond (same side)
    for i in range(len(data) - 4):
        window = data[i:i+5]
        beyond_zone_b_upper = sum(window > zone_b_upper)
        beyond_zone_b_lower = sum(window < zone_b_lower)
        if beyond_zone_b_upper >= 4 or beyond_zone_b_lower >= 4:
            violations.append(f"Rule 3 violation at point {i+5}: 4 of 5 points beyond 1-sigma (same side)")
    
    # Rule 4: 8 consecutive points on same side of mean
    for i in range(len(data) - 7):
        window = data[i:i+8]
        if all(window > mean) or all(window < mean):
            violations.append(f"Rule 4 violation at point {i+8}: 8 consecutive points on same side of mean")
    
    return violations

def calculate_what_if_scenarios(current_sigma, current_dpmo, target_sigma):
    """Calculate what-if improvement scenarios"""
    
    target_dpmo = (1 - stats.norm.cdf(target_sigma - 1.5)) * 1000000
    
    improvement_pct = ((current_dpmo - target_dpmo) / current_dpmo) * 100
    
    # Estimate financial impact (industry averages)
    cost_of_poor_quality_current = current_dpmo / 10000  # Rough estimate: $100 per 1M opportunities
    cost_of_poor_quality_target = target_dpmo / 10000
    savings_per_million = cost_of_poor_quality_current - cost_of_poor_quality_target
    
    # Timeline estimation (industry standard)
    sigma_improvement = target_sigma - current_sigma
    
    if sigma_improvement <= 0.5:
        timeline = "2-3 months"
        effort = "Low - Quick wins, basic improvements"
        difficulty = "Easy"
    elif sigma_improvement <= 1.0:
        timeline = "3-6 months"
        effort = "Medium - Standard DMAIC project"
        difficulty = "Moderate"
    elif sigma_improvement <= 1.5:
        timeline = "6-12 months"
        effort = "High - Major process redesign likely needed"
        difficulty = "Challenging"
    else:
        timeline = "12-18 months"
        effort = "Very High - Fundamental changes required"
        difficulty = "Very Challenging"
    
    return {
        'current_sigma': current_sigma,
        'target_sigma': target_sigma,
        'current_dpmo': current_dpmo,
        'target_dpmo': target_dpmo,
        'improvement_pct': improvement_pct,
        'estimated_timeline': timeline,
        'effort_level': effort,
        'difficulty': difficulty,
        'savings_per_million_opportunities': savings_per_million
    }

def generate_project_timeline(project_type='Manufacturing'):
    """Generate detailed project timeline with milestones"""
    
    today = datetime.now()
    
    # Industry-standard DMAIC timelines
    timelines = {
        'Manufacturing': {
            'Define': 3,  # weeks
            'Measure': 5,
            'Analyze': 4,
            'Improve': 8,
            'Control': 2
        },
        'Service': {
            'Define': 2,
            'Measure': 6,
            'Analyze': 5,
            'Improve': 10,
            'Control': 3
        },
        'Transactional': {
            'Define': 2,
            'Measure': 4,
            'Analyze': 4,
            'Improve': 6,
            'Control': 2
        }
    }
    
    phases = timelines.get(project_type, timelines['Manufacturing'])
    
    milestones = []
    current_date = today
    
    for phase, weeks in phases.items():
        start_date = current_date
        end_date = current_date + timedelta(weeks=weeks)
        
        # Phase-specific milestones
        if phase == 'Define':
            phase_milestones = [
                {'task': 'Project Charter Approved', 'week': 1},
                {'task': 'Team Kickoff Meeting', 'week': 1},
                {'task': 'SIPOC Completed', 'week': 2},
                {'task': 'VOC Analysis Done', 'week': 2},
                {'task': 'Define Tollgate Review', 'week': 3}
            ]
        elif phase == 'Measure':
            phase_milestones = [
                {'task': 'Data Collection Plan Finalized', 'week': 1},
                {'task': 'MSA Completed', 'week': 2},
                {'task': 'Baseline Data Collected', 'week': 3},
                {'task': 'Process Capability Calculated', 'week': 4},
                {'task': 'Measure Tollgate Review', 'week': weeks}
            ]
        elif phase == 'Analyze':
            phase_milestones = [
                {'task': 'Fishbone Diagram Completed', 'week': 1},
                {'task': 'Data Analysis Done', 'week': 2},
                {'task': 'Root Causes Identified', 'week': 3},
                {'task': 'Root Causes Verified (Statistical)', 'week': 4},
                {'task': 'Analyze Tollgate Review', 'week': weeks}
            ]
        elif phase == 'Improve':
            phase_milestones = [
                {'task': 'Solution Brainstorming', 'week': 1},
                {'task': 'FMEA Completed', 'week': 2},
                {'task': 'DOE/Pilot Started', 'week': 3},
                {'task': 'Solutions Implemented', 'week': 6},
                {'task': 'Results Validated', 'week': 7},
                {'task': 'Improve Tollgate Review', 'week': weeks}
            ]
        else:  # Control
            phase_milestones = [
                {'task': 'Control Plan Created', 'week': 1},
                {'task': 'SOPs Updated', 'week': 1},
                {'task': 'Training Completed', 'week': 2},
                {'task': 'Process Handoff', 'week': 2},
                {'task': 'Final Project Review', 'week': 2}
            ]
        
        for milestone in phase_milestones:
            milestone_date = start_date + timedelta(weeks=milestone['week'])
            milestones.append({
                'phase': phase,
                'task': milestone['task'],
                'date': milestone_date,
                'week_in_phase': milestone['week'],
                'status': 'Completed' if milestone_date < today else 'Upcoming'
            })
        
        milestones.append({
            'phase': phase,
            'task': f'{phase} Phase Complete',
            'date': end_date,
            'week_in_phase': weeks,
            'status': 'Completed' if end_date < today else 'Upcoming',
            'is_phase_end': True
        })
        
        current_date = end_date
    
    return {
        'total_weeks': sum(phases.values()),
        'total_months': sum(phases.values()) / 4,
        'end_date': current_date,
        'phases': phases,
        'milestones': milestones
    }

def generate_fmea_template():
    """Generate FMEA (Failure Mode and Effects Analysis) template"""
    
    fmea_template = pd.DataFrame({
        'Process Step': ['', '', '', '', ''],
        'Potential Failure Mode': ['', '', '', '', ''],
        'Potential Effects': ['', '', '', '', ''],
        'Severity (1-10)': [0, 0, 0, 0, 0],
        'Potential Causes': ['', '', '', '', ''],
        'Occurrence (1-10)': [0, 0, 0, 0, 0],
        'Current Controls': ['', '', '', '', ''],
        'Detection (1-10)': [0, 0, 0, 0, 0],
        'RPN': [0, 0, 0, 0, 0],
        'Recommended Actions': ['', '', '', '', ''],
        'Responsibility': ['', '', '', '', ''],
        'Target Date': ['', '', '', '', '']
    })
    
    guidance = """
    **FMEA Guidance:**
    
    **Severity (S):** Impact of failure if it occurs
    - 10: Hazardous without warning
    - 9: Hazardous with warning
    - 8: Very high (product/service unusable)
    - 7: High (major disruption)
    - 6: Moderate (some customers dissatisfied)
    - 5: Low (minor disruption)
    - 4: Very low (minor inconvenience)
    - 3-1: Minimal to none
    
    **Occurrence (O):** Likelihood of failure happening
    - 10: Almost certain (>1 in 2)
    - 9: Very high (1 in 3)
    - 8: High (1 in 8)
    - 7: Moderate (1 in 20)
    - 6: Low (1 in 80)
    - 5: Rare (1 in 400)
    - 4-1: Very rare to nearly impossible
    
    **Detection (D):** Ability to detect before reaching customer
    - 10: Cannot detect
    - 9: Very remote chance
    - 8: Remote chance
    - 7: Low chance
    - 6: Moderate chance
    - 5: Good chance
    - 4-1: Almost certain to very high chance
    
    **RPN = S × O × D**
    - RPN > 200: Immediate action required
    - RPN 100-200: High priority
    - RPN < 100: Monitor
    """
    
    return fmea_template, guidance

def calculate_cost_benefit_analysis(current_performance, improved_performance, volume_per_year):
    """Detailed cost-benefit analysis"""
    
    # Current costs
    current_defect_rate = current_performance['dpmo'] / 1000000
    current_defects_per_year = volume_per_year * current_defect_rate
    
    # Improved costs
    improved_defect_rate = improved_performance['dpmo'] / 1000000
    improved_defects_per_year = volume_per_year * improved_defect_rate
    
    # Defects avoided
    defects_avoided = current_defects_per_year - improved_defects_per_year
    
    # Cost assumptions (industry averages - user should customize)
    cost_per_defect = {
        'scrap': 50,  # Average cost to scrap defective unit
        'rework': 30,  # Average cost to rework
        'warranty': 100,  # Average warranty cost per defect
        'customer_satisfaction': 200,  # Lost customer value
        'inspection': 5  # Inspection cost per unit
    }
    
    # Calculate savings
    scrap_savings = defects_avoided * cost_per_defect['scrap'] * 0.3  # 30% scrap
    rework_savings = defects_avoided * cost_per_defect['rework'] * 0.6  # 60% rework
    warranty_savings = defects_avoided * cost_per_defect['warranty'] * 0.1  # 10% reach customer
    
    total_annual_savings = scrap_savings + rework_savings + warranty_savings
    
    # Implementation costs (estimates)
    project_costs = {
        'black_belt_time': 40000,  # 6 months @ ~80K/year
        'team_time': 20000,  # Part-time team members
        'training': 5000,
        'equipment_tools': 10000,
        'consulting': 0,  # If external help needed
        'implementation': 15000
    }
    
    total_investment = sum(project_costs.values())
    
    # ROI calculations
    roi = ((total_annual_savings - total_investment) / total_investment) * 100
    payback_months = (total_investment / total_annual_savings) * 12 if total_annual_savings > 0 else 999
    
    # 5-year NPV (assuming 10% discount rate)
    discount_rate = 0.10
    npv = sum([total_annual_savings / ((1 + discount_rate) ** year) for year in range(1, 6)]) - total_investment
    
    return {
        'current_defects_per_year': current_defects_per_year,
        'improved_defects_per_year': improved_defects_per_year,
        'defects_avoided': defects_avoided,
        'scrap_savings': scrap_savings,
        'rework_savings': rework_savings,
        'warranty_savings': warranty_savings,
        'total_annual_savings': total_annual_savings,
        'project_costs': project_costs,
        'total_investment': total_investment,
        'roi_percent': roi,
        'payback_months': payback_months,
        'npv_5_year': npv,
        'interpretation': interpret_financial_results(roi, payback_months, npv)
    }

def interpret_financial_results(roi, payback_months, npv):
    """Interpret financial metrics"""
    
    if roi >= 300:
        roi_rating = "Outstanding"
        roi_meaning = "Exceptional return - project should be fast-tracked"
    elif roi >= 200:
        roi_rating = "Excellent"
        roi_meaning = "Very strong business case - high priority"
    elif roi >= 100:
        roi_rating = "Very Good"
        roi_meaning = "Solid business case - proceed with confidence"
    elif roi >= 50:
        roi_rating = "Good"
        roi_meaning = "Acceptable return - typical for Six Sigma projects"
    elif roi >= 0:
        roi_rating = "Marginal"
        roi_meaning = "Positive but low return - consider if strategic value exists"
    else:
        roi_rating = "Negative"
        roi_meaning = "Project may not be financially viable - reconsider scope or approach"
    
    if payback_months <= 6:
        payback_rating = "Very Fast"
    elif payback_months <= 12:
        payback_rating = "Fast"
    elif payback_months <= 24:
        payback_rating = "Moderate"
    else:
        payback_rating = "Slow"
    
    if npv > 100000:
        npv_rating = "Highly Positive"
    elif npv > 0:
        npv_rating = "Positive"
    else:
        npv_rating = "Negative"
    
    return {
        'roi_rating': roi_rating,
        'roi_meaning': roi_meaning,
        'payback_rating': payback_rating,
        'npv_rating': npv_rating,
        'overall_recommendation': 'APPROVED - Strong Business Case' if roi >= 100 and payback_months <= 12 
                                 else 'CONDITIONAL APPROVAL - Review strategic value' if roi >= 50 
                                 else 'NOT RECOMMENDED - Weak financial case'
    }

def generate_control_plan_template():
    """Generate Control Plan template"""
    
    control_plan = pd.DataFrame({
        'Process Step': ['', '', '', '', ''],
        'CTQ Characteristic': ['', '', '', '', ''],
        'Specification/Target': ['', '', '', '', ''],
        'Measurement Method': ['', '', '', '', ''],
        'Sample Size': ['', '', '', '', ''],
        'Frequency': ['', '', '', '', ''],
        'Who Measures': ['', '', '', '', ''],
        'Where Recorded': ['', '', '', '', ''],
        'Control Method': ['', '', '', '', ''],
        'Out-of-Control Action Plan': ['', '', '', '', ''],
        'Responsible Person': ['', '', '', '', '']
    })
    
    guidance = """
    **Control Plan Guidance:**
    
    **Control Methods:**
    - SPC (Statistical Process Control) with control charts
    - Mistake-proofing (Poka-yoke)
    - Standard operating procedures (SOPs)
    - Visual controls
    - Automated monitoring
    - Audits and checks
    
    **Frequency Guidelines:**
    - Critical characteristics: Every unit or continuous
    - Important characteristics: Hourly or per batch
    - Standard characteristics: Daily or per shift
    - Less critical: Weekly or monthly
    
    **Out-of-Control Actions:**
    - Stop process immediately
    - Contain affected product
    - Notify supervisor
    - Investigate root cause
    - Implement corrective action
    - Verify effectiveness
    - Resume production
    """
    
    return control_plan, guidance

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

# Sidebar
with st.sidebar:
    st.title("🎯 DMAIC Project System")
    
    # Project selector
    if st.session_state.project['name']:
        st.success(f"**Project:** {st.session_state.project['name']}")
        st.info(f"**Status:** {st.session_state.project['status']}")
        st.info(f"**Phase:** {st.session_state.project['current_phase']}")
    else:
        st.warning("No active project")
    
    st.markdown("---")
    
    # Navigation
    page = st.selectbox(
        "Navigate to:",
        ['🏠 Dashboard', '📋 Define', '📊 Measure', '🔍 Analyze', '🚀 Improve', '🎛️ Control', 
         '📈 Project Analytics', '📄 Generate Reports']
    )
    
    st.markdown("---")
    
    # Quick stats
    if st.session_state.project['measure']['baseline_sigma']:
        st.metric("Baseline Sigma", f"{st.session_state.project['measure']['baseline_sigma']:.2f}")
    
    if st.session_state.project['improve']['improved_sigma']:
        st.metric("Current Sigma", f"{st.session_state.project['improve']['improved_sigma']:.2f}")
    
    if st.session_state.project['financial_impact']['total_benefit'] > 0:
        st.metric("Est. Annual Savings", f"${st.session_state.project['financial_impact']['total_benefit']:,.0f}")

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════════════════

if page == '🏠 Dashboard':
    
    st.title("🎯 Six Sigma DMAIC Project Dashboard")
    
    # Check if project exists
    if not st.session_state.project['name']:
        st.markdown("""
        <div class="interpretation-box">
        <h2 style="color: white;">Welcome to Your Six Sigma Project System!</h2>
        <p style="font-size: 1.1em;">Let's create your first DMAIC project with complete guidance from charter to handoff.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Create New Project")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name:", placeholder="e.g., Reduce Assembly Defects on Line 3")
            project_type = st.selectbox("Project Type:", ['Manufacturing', 'Service', 'Transactional'])
            champion = st.text_input("Champion (Executive Sponsor):")
            
        with col2:
            black_belt = st.text_input("Black Belt (Project Leader):")
            process_owner = st.text_input("Process Owner:")
        
        if st.button("Create Project", type="primary"):
            if project_name and black_belt:
                st.session_state.project['name'] = project_name
                st.session_state.project['type'] = project_type
                st.session_state.project['champion'] = champion
                st.session_state.project['black_belt'] = black_belt
                st.session_state.project['process_owner'] = process_owner
                st.session_state.project['status'] = 'In Progress'
                st.session_state.project['start_date'] = datetime.now()
                
                # Generate timeline
                timeline = generate_project_timeline(project_type)
                st.session_state.project['timeline'] = timeline
                st.session_state.project['target_end_date'] = timeline['end_date']
                st.session_state.project['milestones'] = timeline['milestones']
                
                st.success("✅ Project created successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill in Project Name and Black Belt at minimum")
    
    else:
        # Existing project dashboard
        st.markdown(f"""
        <div class="metric-card">
        <h2>{st.session_state.project['name']}</h2>
        <p><b>Type:</b> {st.session_state.project['type']} | <b>Black Belt:</b> {st.session_state.project['black_belt']}</p>
        <p><b>Started:</b> {st.session_state.project['start_date'].strftime('%Y-%m-%d')} | 
        <b>Target End:</b> {st.session_state.project['target_end_date'].strftime('%Y-%m-%d') if st.session_state.project['target_end_date'] else 'Not set'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # DMAIC Progress
        st.markdown("### 📊 DMAIC Phase Progress")
        
        phases = ['Define', 'Measure', 'Analyze', 'Improve', 'Control']
        progress_pct = [
            100 if st.session_state.project['define']['complete'] else 50 if st.session_state.project['current_phase'] == 'Define' else 0,
            100 if st.session_state.project['measure']['complete'] else 50 if st.session_state.project['current_phase'] == 'Measure' else 0,
            100 if st.session_state.project['analyze']['complete'] else 50 if st.session_state.project['current_phase'] == 'Analyze' else 0,
            100 if st.session_state.project['improve']['complete'] else 50 if st.session_state.project['current_phase'] == 'Improve' else 0,
            100 if st.session_state.project['control']['complete'] else 50 if st.session_state.project['current_phase'] == 'Control' else 0,
        ]
        
        fig = go.Figure()
        
        colors_dmaic = ['#667eea' if p == 100 else '#ffc107' if p == 50 else '#e0e0e0' for p in progress_pct]
        
        fig.add_trace(go.Bar(
            x=phases,
            y=progress_pct,
            marker_color=colors_dmaic,
            text=[f"{p}%" for p in progress_pct],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="DMAIC Phase Completion",
            yaxis_title="Progress %",
            yaxis=dict(range=[0, 120]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Project Timeline
        st.markdown("### 📅 Project Timeline & Milestones")
        
        if st.session_state.project.get('milestones'):
            df_milestones = pd.DataFrame(st.session_state.project['milestones'])
            
            # Upcoming milestones
            upcoming = df_milestones[df_milestones['status'] == 'Upcoming'].head(5)
            
            if not upcoming.empty:
                st.markdown("#### 🎯 Next 5 Milestones")
                for _, milestone in upcoming.iterrows():
                    days_until = (milestone['date'] - datetime.now()).days
                    st.markdown(f"""
                    <div class="timeline-item phase-upcoming">
                    <b>{milestone['task']}</b> ({milestone['phase']})<br>
                    <small>Due: {milestone['date'].strftime('%Y-%m-%d')} ({days_until} days from now)</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Current Recommendations
        st.markdown("### 💡 Current Recommendations")
        
        current_phase = st.session_state.project['current_phase']
        
        if current_phase == 'Define':
            recommendations = [
                "Complete Project Charter with clear problem and goal statements",
                "Create SIPOC diagram to understand process boundaries",
                "Conduct Voice of Customer (VOC) analysis",
                "Identify Critical to Quality (CTQ) characteristics",
                "Get Champion approval before moving to Measure"
            ]
        elif current_phase == 'Measure':
            recommendations = [
                "Develop detailed Data Collection Plan",
                "Conduct Measurement System Analysis (Gage R&R)",
                "Collect baseline data (minimum 30 data points)",
                "Calculate current Sigma level and process capability",
                "Verify process is in statistical control"
            ]
        elif current_phase == 'Analyze':
            recommendations = [
                "Create Fishbone diagram to identify potential causes",
                "Use 5 Whys to drill down to root causes",
                "Perform statistical analysis (hypothesis tests, ANOVA, regression)",
                "Verify root causes with data (not assumptions)",
                "Prioritize critical X's that drive Y"
            ]
        elif current_phase == 'Improve':
            recommendations = [
                "Brainstorm solutions with team",
                "Complete FMEA to assess risks",
                "Design experiments (DOE) to optimize solutions",
                "Run pilot to validate improvements",
                "Measure improved Sigma level and calculate ROI"
            ]
        else:  # Control
            recommendations = [
                "Create Control Plan for critical CTQs",
                "Update Standard Operating Procedures (SOPs)",
                "Train process owners and operators",
                "Set up ongoing monitoring system",
                "Complete project handoff and documentation"
            ]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-box">
            <b>Step {i}:</b> {rec}
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Upload Data for Analysis", use_container_width=True):
                st.session_state.project['current_phase'] = 'Measure'
                st.rerun()
        
        with col2:
            if st.button("📋 View Complete Timeline", use_container_width=True):
                st.info("Navigate to Project Analytics to see complete timeline")
        
        with col3:
            if st.button("📄 Generate Report", use_container_width=True):
                st.info("Navigate to Generate Reports section")

# ═══════════════════════════════════════════════════════════════════════════════
# MEASURE PHASE - ENHANCED WITH DETAILED INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════════════════════

elif page == '📊 Measure':
    
    st.title("📊 MEASURE Phase - Establish Baseline Performance")
    
    st.markdown("""
    <div class="interpretation-box">
    <h3 style="color: white;">Measure Phase Objectives</h3>
    <ul style="color: white; font-size: 1.1em;">
    <li>Validate measurement system reliability (MSA/Gage R&R)</li>
    <li>Collect baseline data to understand current performance</li>
    <li>Calculate current Sigma level and process capability</li>
    <li>Verify process stability</li>
    <li>Document current state</li>
    </ul>
    <p style="color: white;"><b>Expected Duration:</b> 4-6 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    st.markdown("### 📁 Upload Baseline Data")
    
    uploaded_file = st.file_uploader(
        "Upload your baseline process data (CSV or Excel):",
        type=['csv', 'xlsx'],
        help="Minimum 30 data points recommended. Include timestamps and any stratification factors (machine, operator, shift, etc.)"
    )
    
    if uploaded_file:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        with st.expander("📊 Data Preview & Quality Check"):
            st.dataframe(df.head(50))
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric("Complete Rows", df.dropna().shape[0])
            missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
            col4.metric("Missing %", f"{missing_pct:.1f}%")
            
            if missing_pct > 5:
                st.warning("⚠️ More than 5% missing data - consider data quality improvement")
        
        # Data type selection
        st.markdown("---")
        st.markdown("### 🎯 Select Analysis Type")
        
        analysis_type = st.radio(
            "What type of data do you have?",
            ['Continuous (Measurements)', 'Discrete (Defect Counts)'],
            help="Continuous: dimensions, time, temperature, etc. | Discrete: defects, errors, pass/fail"
        )
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # CONTINUOUS DATA ANALYSIS
        if analysis_type == 'Continuous (Measurements)':
            
            st.markdown("### 📏 Continuous Data Analysis Setup")
            
            col1, col2 = st.columns(2)
            
            with col1:
                ctq_col = st.selectbox("Select CTQ (measurement) column:", numeric_cols)
                lsl = st.number_input("Lower Specification Limit (LSL):", value=float(df[ctq_col].quantile(0.01)))
                target = st.number_input("Target/Nominal:", value=float(df[ctq_col].mean()))
            
            with col2:
                st.write("")  # Spacing
                usl = st.number_input("Upper Specification Limit (USL):", value=float(df[ctq_col].quantile(0.99)))
                annual_volume = st.number_input("Annual Production Volume:", value=100000, step=10000)
            
            if st.button("🚀 Run Complete Baseline Analysis", type="primary"):
                
                data = df[ctq_col].dropna()
                
                # Calculate all metrics
                mean = data.mean()
                std = data.std()
                
                cp = (usl - lsl) / (6 * std)
                cpu = (usl - mean) / (3 * std)
                cpl = (mean - lsl) / (3 * std)
                cpk = min(cpu, cpl)
                
                pp = (usl - lsl) / (6 * data.std(ddof=0))
                ppk = min((usl - mean)/(3*data.std(ddof=0)), (mean - lsl)/(3*data.std(ddof=0)))
                
                defects = ((data < lsl) | (data > usl)).sum()
                dpmo = (defects / len(data)) * 1_000_000
                sigma_level = (1 - stats.norm.cdf(dpmo / 1_000_000)) if dpmo < 1_000_000 else 0
                sigma_level = stats.norm.ppf(1 - dpmo/1_000_000) + 1.5 if dpmo < 933193 else 0
                
                # Store in session
                st.session_state.project['measure']['baseline_sigma'] = sigma_level
                st.session_state.project['measure']['baseline_dpmo'] = dpmo
                st.session_state.project['measure']['baseline_cpk'] = cpk
                st.session_state.project['measure']['baseline_data'] = df
                
                # ═══════════════════════════════════════════════════════════════
                # DETAILED RESULTS WITH INTERPRETATIONS
                # ═══════════════════════════════════════════════════════════════
                
                st.markdown("---")
                st.markdown("## 📊 BASELINE PERFORMANCE ANALYSIS RESULTS")
                
                # Key Metrics
                st.markdown("### 🎯 Key Performance Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Sigma Level", f"{sigma_level:.2f}")
                col2.metric("DPMO", f"{dpmo:,.0f}")
                col3.metric("Cpk", f"{cpk:.3f}")
                col4.metric("Yield", f"{(1-dpmo/1000000)*100:.3f}%")
                
                # DETAILED SIGMA INTERPRETATION
                st.markdown("---")
                st.markdown("### 📈 Sigma Level Interpretation")
                
                sigma_interp = interpret_sigma_level(sigma_level, dpmo)
                
                st.markdown(f"""
                <div class="interpretation-box">
                <h3 style="color: white;">{sigma_interp['color']} {sigma_interp['level']} Performance</h3>
                <p style="font-size: 1.1em; color: white;"><b>Your Quality Level:</b> {sigma_interp['quality']}</p>
                <p style="color: white;"><b>Industry Benchmark:</b> {sigma_interp['benchmark']}</p>
                <p style="color: white;"><b>Comparable Examples:</b> {sigma_interp['examples']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="recommendation-box">
                <h4>💡 Recommended Action</h4>
                <p><b>{sigma_interp['action']}</b></p>
                <p><b>Business Impact:</b> {sigma_interp['business_impact']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # DETAILED CPK INTERPRETATION
                st.markdown("---")
                st.markdown("### 🎯 Process Capability (Cpk) Interpretation")
                
                cpk_interp = interpret_cpk(cpk, cp)
                
                st.markdown(f"""
                <div class="metric-card">
                <h4>{cpk_interp['color']} {cpk_interp['rating']}</h4>
                <p><b>What this means:</b> {cpk_interp['meaning']}</p>
                <p><b>Expected defect rate:</b> {cpk_interp['defect_rate']}</p>
                <p><b>Business value:</b> {cpk_interp['business_value']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="recommendation-box">
                <h4>🎯 Action Required</h4>
                <p>{cpk_interp['action']}</p>
                {f'<p><b>Process Centering:</b> {cpk_interp["centering_advice"]}</p>' if cpk_interp['centering_advice'] else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Additional capability metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Cp (Potential)", f"{cp:.3f}", 
                           help="What the process COULD achieve if perfectly centered")
                col2.metric("Pp (Long-term)", f"{pp:.3f}",
                           help="Long-term performance capability")
                col3.metric("Ppk (Long-term actual)", f"{ppk:.3f}",
                           help="Long-term actual capability")
                
                # WHAT-IF SCENARIOS
                st.markdown("---")
                st.markdown("### 🔮 What-If Improvement Scenarios")
                
                st.markdown("""
                <div class="tip-box">
                <p>See what different Sigma levels would mean for your process and business</p>
                </div>
                """, unsafe_allow_html=True)
                
                target_sigma = st.slider("Target Sigma Level:", 
                                        min_value=max(2.0, sigma_level), 
                                        max_value=6.0, 
                                        value=min(sigma_level + 1, 6.0),
                                        step=0.5)
                
                scenario = calculate_what_if_scenarios(sigma_level, dpmo, target_sigma)
                
                st.markdown(f"""
                <div class="success-box">
                <h4>📊 Improvement Scenario: {scenario['current_sigma']:.2f}σ → {scenario['target_sigma']:.2f}σ</h4>
                <p><b>DPMO Reduction:</b> {scenario['current_dpmo']:,.0f} → {scenario['target_dpmo']:,.0f} 
                   ({scenario['improvement_pct']:.1f}% improvement)</p>
                <p><b>Estimated Timeline:</b> {scenario['estimated_timeline']}</p>
                <p><b>Effort Required:</b> {scenario['effort_level']}</p>
                <p><b>Difficulty Level:</b> {scenario['difficulty']}</p>
                <p><b>Estimated Savings:</b> ${scenario['savings_per_million_opportunities']*annual_volume/1000000:,.0f} per year</p>
                </div>
                """, unsafe_allow_html=True)
                
                # COST-BENEFIT ANALYSIS
                st.markdown("---")
                st.markdown("### 💰 Financial Impact Analysis")
                
                current_perf = {'dpmo': dpmo, 'sigma': sigma_level}
                improved_perf = {'dpmo': scenario['target_dpmo'], 'sigma': target_sigma}
                
                cost_benefit = calculate_cost_benefit_analysis(current_perf, improved_perf, annual_volume)
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Annual Savings", f"${cost_benefit['total_annual_savings']:,.0f}")
                col2.metric("ROI", f"{cost_benefit['roi_percent']:.0f}%")
                col3.metric("Payback Period", f"{cost_benefit['payback_months']:.1f} months")
                col4.metric("5-Year NPV", f"${cost_benefit['npv_5_year']:,.0f}")
                
                st.markdown(f"""
                <div class="interpretation-box">
                <h4 style="color: white;">Financial Recommendation</h4>
                <p style="color: white; font-size: 1.1em;"><b>{cost_benefit['interpretation']['overall_recommendation']}</b></p>
                <p style="color: white;">{cost_benefit['interpretation']['roi_meaning']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed breakdown
                with st.expander("📊 View Detailed Financial Breakdown"):
                    st.markdown("#### Annual Savings Breakdown")
                    savings_df = pd.DataFrame({
                        'Category': ['Scrap Reduction', 'Rework Reduction', 'Warranty Reduction'],
                        'Annual Savings': [
                            cost_benefit['scrap_savings'],
                            cost_benefit['rework_savings'],
                            cost_benefit['warranty_savings']
                        ]
                    })
                    st.dataframe(savings_df.style.format({'Annual Savings': '${:,.0f}'}))
                    
                    st.markdown("#### Project Investment")
                    cost_df = pd.DataFrame(list(cost_benefit['project_costs'].items()), 
                                          columns=['Item', 'Cost'])
                    st.dataframe(cost_df.style.format({'Cost': '${:,.0f}'}))
                
                # PROCESS STABILITY CHECK
                st.markdown("---")
                st.markdown("### 📉 Process Stability Analysis (Control Chart)")
                
                mr = data.diff().abs()
                mr_mean = mr.mean()
                ucl = mean + 2.66 * mr_mean
                lcl = mean - 2.66 * mr_mean
                
                out_of_control = (data > ucl) | (data < lcl)
                
                # Control chart interpretation
                control_interp = interpret_control_chart(data, ucl, lcl, mean, out_of_control)
                
                st.markdown(f"""
                <div class="metric-card">
                <h4>{control_interp['color']} Process Status: {control_interp['status']}</h4>
                <p><b>What this means:</b> {control_interp['meaning']}</p>
                <p><b>Out-of-control points:</b> {control_interp['ooc_count']} out of {control_interp['total_points']} 
                   ({control_interp['ooc_count']/control_interp['total_points']*100:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="recommendation-box">
                <h4>🔍 Investigation Required</h4>
                <p>{control_interp['investigation']}</p>
                <p><b>Next Step:</b> {control_interp['action']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Plot control chart
                fig_control = go.Figure()
                
                fig_control.add_trace(go.Scatter(
                    y=data,
                    mode='lines+markers',
                    name='Individual Values',
                    line=dict(color='blue'),
                    marker=dict(size=6)
                ))
                
                fig_control.add_hline(y=ucl, line_dash="dash", line_color="red", 
                                     annotation_text="UCL", annotation_position="right")
                fig_control.add_hline(y=mean, line_color="green", 
                                     annotation_text="Mean", annotation_position="right")
                fig_control.add_hline(y=lcl, line_dash="dash", line_color="red", 
                                     annotation_text="LCL", annotation_position="right")
                
                if out_of_control.any():
                    fig_control.add_trace(go.Scatter(
                        x=data[out_of_control].index,
                        y=data[out_of_control],
                        mode='markers',
                        name='Out of Control',
                        marker=dict(color='red', size=12, symbol='x', line=dict(width=2, color='darkred'))
                    ))
                
                fig_control.update_layout(
                    title="I-MR Control Chart (Individual Values)",
                    xaxis_title="Sample Number",
                    yaxis_title=ctq_col,
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_control, use_container_width=True)
                
                # Western Electric Rules violations
                if control_interp['runs_detected']:
                    st.markdown("#### ⚠️ Additional Pattern Violations Detected")
                    for violation in control_interp['runs_detected']:
                        st.warning(violation)
                
                # CAPABILITY HISTOGRAM
                st.markdown("---")
                st.markdown("### 📊 Process Distribution vs Specifications")
                
                fig_hist = go.Figure()
                
                # Histogram
                fig_hist.add_trace(go.Histogram(
                    x=data,
                    nbinsx=40,
                    name='Actual Data',
                    opacity=0.7,
                    marker_color='lightblue'
                ))
                
                # Normal distribution overlay
                x_range = np.linspace(data.min(), data.max(), 200)
                y_normal = stats.norm.pdf(x_range, mean, std) * len(data) * (data.max() - data.min()) / 40
                
                fig_hist.add_trace(go.Scatter(
                    x=x_range,
                    y=y_normal,
                    mode='lines',
                    name='Normal Distribution',
                    line=dict(color='red', width=2)
                ))
                
                # Spec limits
                fig_hist.add_vline(x=lsl, line_dash="dash", line_color="red", line_width=3,
                                  annotation_text="LSL", annotation_position="top")
                fig_hist.add_vline(x=usl, line_dash="dash", line_color="red", line_width=3,
                                  annotation_text="USL", annotation_position="top")
                fig_hist.add_vline(x=target, line_dash="dash", line_color="green", line_width=2,
                                  annotation_text="Target", annotation_position="top")
                fig_hist.add_vline(x=mean, line_color="blue", line_width=2,
                                  annotation_text="Mean", annotation_position="bottom")
                
                fig_hist.update_layout(
                    title="Process Distribution vs Specification Limits",
                    xaxis_title=ctq_col,
                    yaxis_title="Frequency",
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # NORMALITY ASSESSMENT
                st.markdown("---")
                st.markdown("### 📈 Normality Assessment")
                
                st.markdown("""
                <div class="tip-box">
                <p><b>Why Normality Matters:</b> Process capability calculations assume normal distribution. 
                If data is non-normal, capability indices may be misleading.</p>
                </div>
                """, unsafe_allow_html=True)
                
                normality_results = check_normality(data)
                
                col1, col2, col3 = st.columns(3)
                
                anderson_pass = "✅ Pass" if normality_results['anderson_normal'] else "❌ Fail"
                col1.metric("Anderson-Darling Test", anderson_pass)
                col1.caption(f"Statistic: {normality_results['anderson_stat']:.3f}")
                
                if normality_results['shapiro_p']:
                    shapiro_pass = "✅ Pass" if normality_results['shapiro_normal'] else "❌ Fail"
                    col2.metric("Shapiro-Wilk Test", shapiro_pass)
                    col2.caption(f"p-value: {normality_results['shapiro_p']:.4f}")
                
                ks_pass = "✅ Pass" if normality_results['ks_normal'] else "❌ Fail"
                col3.metric("Kolmogorov-Smirnov Test", ks_pass)
                col3.caption(f"p-value: {normality_results['ks_p']:.4f}")
                
                if normality_results['anderson_normal']:
                    st.markdown("""
                    <div class="success-box">
                    <p><b>✅ Data appears normally distributed</b></p>
                    <p>Process capability calculations (Cp, Cpk) are valid and reliable.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                    <p><b>⚠️ Data may not be normally distributed</b></p>
                    <p><b>Recommendations:</b></p>
                    <ul>
                    <li>Consider data transformation (log, Box-Cox)</li>
                    <li>Use non-parametric capability analysis</li>
                    <li>Investigate why distribution is non-normal (mixture of populations? Truncated data?)</li>
                    <li>Capability indices may underestimate or overestimate true capability</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Probability plot
                fig_qq = go.Figure()
                
                (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm")
                
                fig_qq.add_trace(go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    name='Sample Data',
                    marker=dict(color='blue', size=6)
                ))
                
                fig_qq.add_trace(go.Scatter(
                    x=osm,
                    y=slope * osm + intercept,
                    mode='lines',
                    name='Normal Distribution',
                    line=dict(color='red', width=2)
                ))
                
                fig_qq.update_layout(
                    title=f"Normal Probability Plot (R² = {r**2:.4f})",
                    xaxis_title="Theoretical Quantiles",
                    yaxis_title="Sample Quantiles",
                    height=500
                )
                
                st.plotly_chart(fig_qq, use_container_width=True)
                
                st.info(f"**R² = {r**2:.4f}** | Closer to 1.0 indicates better fit to normal distribution")
                
                # NEXT STEPS
                st.markdown("---")
                st.markdown("### ✅ Measure Phase Next Steps")
                
                next_steps = [
                    {
                        'step': '1. Document Baseline Results',
                        'action': 'Save all charts and metrics for your project documentation',
                        'status': 'ready'
                    },
                    {
                        'step': '2. Complete Measurement System Analysis (MSA)',
                        'action': 'Conduct Gage R&R study to ensure measurement reliability',
                        'status': 'needed' if not st.session_state.project['measure'].get('msa_complete') else 'done'
                    },
                    {
                        'step': '3. Address Process Stability Issues',
                        'action': 'Investigate and remove special causes if process is out of control',
                        'status': 'critical' if not control_interp['status'] == 'In Statistical Control' else 'done'
                    },
                    {
                        'step': '4. Tollgate Review with Champion',
                        'action': 'Present baseline findings and get approval to proceed to Analyze',
                        'status': 'ready'
                    },
                    {
                        'step': '5. Proceed to Analyze Phase',
                        'action': 'Begin root cause analysis to identify critical Xs driving Y',
                        'status': 'ready'
                    }
                ]
                
                for step_info in next_steps:
                    if step_info['status'] == 'critical':
                        box_class = 'error-box'
                        icon = '🔴'
                    elif step_info['status'] == 'needed':
                        box_class = 'warning-box'
                        icon = '🟡'
                    elif step_info['status'] == 'done':
                        box_class = 'success-box'
                        icon = '✅'
                    else:
                        box_class = 'recommendation-box'
                        icon = '▶️'
                    
                    st.markdown(f"""
                    <div class="{box_class}">
                    <p><b>{icon} {step_info['step']}</b></p>
                    <p>{step_info['action']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Save progress
                if st.button("✅ Mark Measure Phase as Complete", type="primary"):
                    st.session_state.project['measure']['complete'] = True
                    st.session_state.project['measure']['completion_date'] = datetime.now()
                    st.session_state.project['current_phase'] = 'Analyze'
                    st.success("🎉 Measure Phase marked complete! Moving to Analyze phase...")
                    st.balloons()

# Due to length limits, I'll break here. This is a comprehensive start.

# Would you like me to:
# 1. Continue with Analyze, Improve, and Control phases with same detail level?
# 2. Add the complete FMEA, DOE, and other tools?
# 3. Create the report generation system?