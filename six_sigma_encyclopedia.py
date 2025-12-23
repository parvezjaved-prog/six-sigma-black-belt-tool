"""
═══════════════════════════════════════════════════════════════════
    SIX SIGMA BLACK BELT COMPLETE ENCYCLOPEDIA & PROJECT MENTOR
    
    A Comprehensive DMAIC Guide with All Tools, Charts, and Methods
    Your Complete Six Sigma Reference and Virtual Mentor
    
    Version 3.0 - Complete Encyclopedia Edition
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import normaltest, shapiro, anderson, chi2_contingency, f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from datetime import datetime, timedelta
import json
from io import BytesIO
import base64

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Six Sigma Encyclopedia & DMAIC Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
    <style>
    /* Main styling */
    .main {background-color: #f5f7fa;}
    
    /* Metrics */
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1 {color: #1f4788; font-size: 2.5em; font-weight: 700;}
    h2 {color: #2e5c8a; font-size: 2em; font-weight: 600;}
    h3 {color: #3d6fa3; font-size: 1.5em; font-weight: 500;}
    
    /* Custom boxes */
    .phase-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .tip-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2196f3;
        margin: 15px 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 15px 0;
    }
    
    .success-box {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 15px 0;
    }
    
    .tool-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.2s;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Progress bar */
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        padding: 3px;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        height: 20px;
        border-radius: 8px;
        transition: width 0.3s;
    }
    
    /* Checklist */
    .checklist-item {
        padding: 10px;
        margin: 5px 0;
        background-color: white;
        border-radius: 5px;
        border-left: 3px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════

if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        # Navigation
        'current_phase': 'Home',
        'current_tool': None,
        
        # Project Info
        'project_name': '',
        'project_type': '',
        'start_date': datetime.now(),
        'target_date': datetime.now() + timedelta(days=180),
        
        # Define Phase
        'define_complete': False,
        'problem_statement': '',
        'goal_statement': '',
        'business_case': '',
        'scope_in': '',
        'scope_out': '',
        'team_members': [],
        'champion': '',
        'sipoc': {},
        'voc_data': [],
        'ctq_characteristics': [],
        
        # Measure Phase
        'measure_complete': False,
        'baseline_data': None,
        'measurement_system': {},
        'gage_rr_results': {},
        'baseline_sigma': None,
        'baseline_cpk': None,
        'baseline_dpmo': None,
        'process_stable': None,
        
        # Analyze Phase
        'analyze_complete': False,
        'root_causes': [],
        'hypothesis_tests': [],
        'regression_models': [],
        'fishbone_data': {},
        'five_whys': [],
        'pareto_data': {},
        
        # Improve Phase
        'improve_complete': False,
        'solutions': [],
        'doe_results': {},
        'pilot_results': {},
        'cost_benefit': {},
        'implementation_plan': [],
        
        # Control Phase
        'control_complete': False,
        'control_plan': {},
        'sop_created': False,
        'training_complete': False,
        'handoff_complete': False,
        'final_sigma': None,
        
        # Data Storage
        'uploaded_data': {},
        'analysis_results': {},
        'charts_generated': [],
    }

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def calculate_sigma_level(dpmo):
    """Calculate Sigma level from DPMO"""
    if dpmo >= 1000000:
        return 0
    elif dpmo <= 0:
        return 6
    else:
        return stats.norm.ppf(1 - dpmo/1000000) + 1.5

def calculate_dpmo_from_sigma(sigma):
    """Calculate DPMO from Sigma level"""
    return (1 - stats.norm.cdf(sigma - 1.5)) * 1000000

def calculate_process_capability(data, lsl, usl, target=None):
    """Calculate comprehensive process capability metrics"""
    mean = data.mean()
    std = data.std()
    
    # Short-term capability
    cp = (usl - lsl) / (6 * std)
    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    cpk = min(cpu, cpl)
    
    # Long-term capability
    pp = (usl - lsl) / (6 * data.std(ddof=0))
    ppu = (usl - mean) / (3 * data.std(ddof=0))
    ppl = (mean - lsl) / (3 * data.std(ddof=0))
    ppk = min(ppu, ppl)
    
    # Process performance
    defects = ((data < lsl) | (data > usl)).sum()
    dpmo = (defects / len(data)) * 1000000
    sigma_level = calculate_sigma_level(dpmo)
    
    # Centering
    if target:
        cpm = cp / np.sqrt(1 + ((mean - target) / std)**2)
    else:
        cpm = None
    
    return {
        'mean': mean,
        'std': std,
        'cp': cp,
        'cpu': cpu,
        'cpl': cpl,
        'cpk': cpk,
        'pp': pp,
        'ppu': ppu,
        'ppl': ppl,
        'ppk': ppk,
        'cpm': cpm,
        'defects': defects,
        'dpmo': dpmo,
        'sigma_level': sigma_level,
        'yield': (1 - dpmo/1000000) * 100
    }

def create_control_chart(data, chart_type='I-MR'):
    """Generate control charts"""
    if chart_type == 'I-MR':
        mean = data.mean()
        mr = data.diff().abs()
        mr_mean = mr.mean()
        
        ucl = mean + 2.66 * mr_mean
        lcl = mean - 2.66 * mr_mean
        
        ucl_mr = 3.267 * mr_mean
        
        return {
            'mean': mean,
            'ucl': ucl,
            'lcl': lcl,
            'mr_mean': mr_mean,
            'ucl_mr': ucl_mr,
            'moving_range': mr
        }

def check_normality(data):
    """Comprehensive normality testing"""
    # Anderson-Darling
    anderson_result = anderson(data)
    
    # Shapiro-Wilk (if sample size < 5000)
    if len(data) < 5000:
        shapiro_stat, shapiro_p = shapiro(data)
    else:
        shapiro_stat, shapiro_p = None, None
    
    # Kolmogorov-Smirnov
    ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
    
    return {
        'anderson_stat': anderson_result.statistic,
        'anderson_critical': anderson_result.critical_values[2],  # 5% level
        'anderson_normal': anderson_result.statistic < anderson_result.critical_values[2],
        'shapiro_stat': shapiro_stat,
        'shapiro_p': shapiro_p,
        'shapiro_normal': shapiro_p > 0.05 if shapiro_p else None,
        'ks_stat': ks_stat,
        'ks_p': ks_p,
        'ks_normal': ks_p > 0.05
    }

def generate_sigma_conversion_table():
    """Generate Sigma to DPMO conversion table"""
    sigma_levels = np.arange(1, 6.1, 0.1)
    dpmo_values = [calculate_dpmo_from_sigma(s) for s in sigma_levels]
    yield_values = [(1 - d/1000000) * 100 for d in dpmo_values]
    
    df = pd.DataFrame({
        'Sigma Level': sigma_levels,
        'DPMO': dpmo_values,
        'Yield %': yield_values
    })
    
    return df

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f4788/ffffff?text=Six+Sigma", use_container_width=True)
    
    st.title("🎓 Navigation")
    
    # Main sections
    main_section = st.radio(
        "Select Mode:",
        ['🏠 Home', '📚 Encyclopedia', '🎯 DMAIC Project', '🔧 Tools Library', '📊 Quick Analysis'],
        key='main_section'
    )
    
    st.markdown("---")
    
    # Project Progress (if in DMAIC mode)
    if main_section == '🎯 DMAIC Project':
        st.markdown("### 📈 Project Progress")
        
        phases_complete = [
            st.session_state.project_data['define_complete'],
            st.session_state.project_data['measure_complete'],
            st.session_state.project_data['analyze_complete'],
            st.session_state.project_data['improve_complete'],
            st.session_state.project_data['control_complete'],
        ]
        
        progress = sum(phases_complete) / 5 * 100
        
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <p style="text-align: center; margin-top: 5px;">{progress:.0f}% Complete</p>
        """, unsafe_allow_html=True)
        
        st.markdown("#### DMAIC Phases:")
        phases = ['Define', 'Measure', 'Analyze', 'Improve', 'Control']
        for i, phase in enumerate(phases):
            status = "✅" if phases_complete[i] else "⏳"
            st.markdown(f"{status} **{phase}**")
        
        st.markdown("---")
        
        # Quick project info
        if st.session_state.project_data['project_name']:
            st.markdown(f"**Project:** {st.session_state.project_data['project_name']}")
            if st.session_state.project_data['baseline_sigma']:
                st.metric("Baseline Sigma", f"{st.session_state.project_data['baseline_sigma']:.2f}")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True):
            st.session_state.save_project = True
    with col2:
        if st.button("📥 Load", use_container_width=True):
            st.session_state.load_project = True
    
    # Help
    with st.expander("❓ Help & Support"):
        st.markdown("""
        **Getting Started:**
        - 🏠 Home: Overview and introduction
        - 📚 Encyclopedia: Learn Six Sigma concepts
        - 🎯 DMAIC: Guided project workflow
        - 🔧 Tools: Individual analysis tools
        - 📊 Quick Analysis: Fast data analysis
        
        **Need Help?**
        - Each section has detailed guides
        - Hover over ⓘ icons for tooltips
        - Check the encyclopedia for definitions
        """)

# ═══════════════════════════════════════════════════════════════════
# MAIN CONTENT - HOME
# ═══════════════════════════════════════════════════════════════════

if main_section == '🏠 Home':
    
    # Hero section
    st.markdown("""
    <div class="phase-box">
    <h1 style="color: white; margin: 0;">🎓 Six Sigma Black Belt Complete Encyclopedia</h1>
    <p style="font-size: 1.2em; color: white; margin-top: 10px;">
    Your comprehensive guide to Six Sigma DMAIC methodology with all tools, charts, and statistical methods
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
        <h3>📚 Complete Encyclopedia</h3>
        <p>Comprehensive reference covering:</p>
        <ul>
        <li>All DMAIC phases</li>
        <li>Statistical methods</li>
        <li>Control charts (15+ types)</li>
        <li>Hypothesis testing</li>
        <li>Process capability</li>
        <li>DOE & regression</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
        <h3>🎯 DMAIC Project Guide</h3>
        <p>Step-by-step mentoring through:</p>
        <ul>
        <li>Define: Project charter & scope</li>
        <li>Measure: Baseline & MSA</li>
        <li>Analyze: Root cause analysis</li>
        <li>Improve: Solutions & DOE</li>
        <li>Control: Sustaining gains</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tool-card">
        <h3>🔧 Analysis Tools</h3>
        <p>Professional statistical tools:</p>
        <ul>
        <li>Automated analysis</li>
        <li>Interactive charts</li>
        <li>Statistical tests</li>
        <li>Capability studies</li>
        <li>Root cause tools</li>
        <li>Report generation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # What's included
    st.markdown("## 📦 What's Included in This Encyclopedia")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts & Graphs", "🧮 Statistical Methods", "🛠️ Quality Tools", "📋 Templates"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Control Charts
            - ✅ I-MR Chart (Individuals & Moving Range)
            - ✅ X̄-R Chart (Average & Range)
            - ✅ X̄-S Chart (Average & Standard Deviation)
            - ✅ P Chart (Proportion defective)
            - ✅ NP Chart (Number defective)
            - ✅ C Chart (Count of defects)
            - ✅ U Chart (Defects per unit)
            - ✅ EWMA Chart (Exponentially Weighted Moving Average)
            - ✅ CUSUM Chart (Cumulative Sum)
            - ✅ Pre-control Charts
            - ✅ Zone Charts
            
            ### Process Capability Charts
            - ✅ Histogram with Normal Curve
            - ✅ Probability Plots (Q-Q, P-P)
            - ✅ Capability Distribution
            - ✅ Process Capability Overview
            """)
        
        with col2:
            st.markdown("""
            ### Analysis Charts
            - ✅ Pareto Charts
            - ✅ Scatter Diagrams
            - ✅ Box Plots
            - ✅ Multi-Vari Charts
            - ✅ Time Series Plots
            - ✅ Regression Plots
            - ✅ Residual Plots
            - ✅ Main Effects Plots
            - ✅ Interaction Plots
            - ✅ Contour Plots (DOE)
            - ✅ Surface Response Plots
            - ✅ Correlation Matrices
            - ✅ Heat Maps
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Descriptive Statistics
            - ✅ Central Tendency (Mean, Median, Mode)
            - ✅ Dispersion (Range, Variance, Std Dev)
            - ✅ Distribution Shape (Skewness, Kurtosis)
            - ✅ Percentiles & Quartiles
            
            ### Hypothesis Testing
            - ✅ 1-Sample t-Test
            - ✅ 2-Sample t-Test
            - ✅ Paired t-Test
            - ✅ 1-Sample Proportion Test
            - ✅ 2-Sample Proportion Test
            - ✅ Chi-Square Test
            - ✅ F-Test for Variances
            - ✅ Mann-Whitney U Test
            - ✅ Kruskal-Wallis Test
            
            ### ANOVA
            - ✅ One-Way ANOVA
            - ✅ Two-Way ANOVA
            - ✅ Repeated Measures ANOVA
            - ✅ ANCOVA
            - ✅ MANOVA
            """)
        
        with col2:
            st.markdown("""
            ### Regression & Correlation
            - ✅ Simple Linear Regression
            - ✅ Multiple Regression
            - ✅ Polynomial Regression
            - ✅ Logistic Regression
            - ✅ Correlation Analysis
            - ✅ Partial Correlation
            
            ### Process Capability
            - ✅ Cp, Cpk (Short-term)
            - ✅ Pp, Ppk (Long-term)
            - ✅ Cpm (Taguchi Index)
            - ✅ Pp/Ppk Analysis
            - ✅ Sigma Level Calculation
            - ✅ DPMO Calculation
            
            ### Normality Tests
            - ✅ Anderson-Darling
            - ✅ Shapiro-Wilk
            - ✅ Kolmogorov-Smirnov
            - ✅ Ryan-Joiner
            - ✅ Probability Plots
            """)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Root Cause Analysis
            - ✅ Fishbone (Ishikawa) Diagram
            - ✅ 5 Whys Analysis
            - ✅ Fault Tree Analysis
            - ✅ Pareto Analysis
            - ✅ Scatter Diagrams
            - ✅ Multi-Vari Studies
            
            ### Process Mapping
            - ✅ SIPOC Diagram
            - ✅ Process Flow Charts
            - ✅ Value Stream Mapping
            - ✅ Spaghetti Diagrams
            - ✅ Swim Lane Diagrams
            
            ### Measurement System Analysis
            - ✅ Gage R&R (Crossed)
            - ✅ Gage R&R (Nested)
            - ✅ Attribute Agreement Analysis
            - ✅ Bias & Linearity Studies
            - ✅ Stability Analysis
            """)
        
        with col2:
            st.markdown("""
            ### Design of Experiments (DOE)
            - ✅ Full Factorial Designs
            - ✅ Fractional Factorial Designs
            - ✅ Response Surface Methodology
            - ✅ Taguchi Methods
            - ✅ Mixture Designs
            - ✅ Screening Designs
            
            ### Lean Tools
            - ✅ Value Stream Mapping
            - ✅ 5S Assessment
            - ✅ Kaizen Event Planning
            - ✅ Waste Analysis
            - ✅ Takt Time Calculation
            
            ### Risk Analysis
            - ✅ FMEA (Failure Mode & Effects Analysis)
            - ✅ Risk Priority Number (RPN)
            - ✅ Fault Tree Analysis
            - ✅ Monte Carlo Simulation
            """)
    
    with tab4:
        st.markdown("""
        ### Project Templates
        - ✅ Project Charter
        - ✅ SIPOC Diagram
        - ✅ Data Collection Plan
        - ✅ Measurement System Analysis Plan
        - ✅ Control Plan
        - ✅ Standard Operating Procedures (SOP)
        - ✅ Training Plan
        - ✅ Communication Plan
        - ✅ Cost-Benefit Analysis
        - ✅ Project Storyboard
        - ✅ Final Report Template
        - ✅ Handoff Checklist
        """)
    
    st.markdown("---")
    
    # Getting started
    st.markdown("## 🚀 Getting Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-box">
        <h4>📚 New to Six Sigma?</h4>
        <p>Start with the <b>Encyclopedia</b> section to learn fundamental concepts, terminology, and methodology.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Encyclopedia →", use_container_width=True):
            st.session_state.project_data['current_phase'] = 'Encyclopedia'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="tip-box">
        <h4>🎯 Starting a Project?</h4>
        <p>Use the <b>DMAIC Project</b> mode for step-by-step guidance through your improvement project.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start DMAIC Project →", use_container_width=True):
            st.session_state.project_data['current_phase'] = 'DMAIC'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="warning-box">
        <h4>📊 Need Quick Analysis?</h4>
        <p>Jump to <b>Quick Analysis</b> to upload data and get instant statistical insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Quick Analysis →", use_container_width=True):
            st.session_state.project_data['current_phase'] = 'Quick Analysis'
            st.rerun()
    
    st.markdown("---")
    
    # Sigma level reference
    st.markdown("## 📊 Quick Reference: Sigma Levels")
    
    sigma_table = pd.DataFrame({
        'Sigma Level': [6, 5, 4, 3, 2, 1],
        'DPMO': [3.4, 233, 6210, 66807, 308538, 690000],
        'Yield %': [99.99966, 99.9767, 99.379, 93.32, 69.15, 31.00],
        'Quality Level': ['World Class', 'Excellent', 'Good', 'Average', 'Poor', 'Non-competitive'],
        'Example': [
            'Aviation safety',
            'Top manufacturing',
            'Most manufacturing',
            'Typical business',
            'Service industries',
            'Unacceptable'
        ]
    })
    
    st.dataframe(sigma_table, use_container_width=True, hide_index=True)
    
    # Chart showing sigma levels
    fig = go.Figure()
    
    sigma_levels = list(range(1, 7))
    dpmo_values = [690000, 308538, 66807, 6210, 233, 3.4]
    colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997', '#17a2b8']
    
    fig.add_trace(go.Bar(
        x=sigma_levels,
        y=dpmo_values,
        marker_color=colors,
        text=[f'{d:,.0f}' for d in dpmo_values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Sigma Level vs DPMO (Defects Per Million Opportunities)",
        xaxis_title="Sigma Level",
        yaxis_title="DPMO (log scale)",
        yaxis_type="log",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA SECTION
# ═══════════════════════════════════════════════════════════════════

elif main_section == '📚 Encyclopedia':
    
    st.title("📚 Six Sigma Complete Encyclopedia")
    
    st.markdown("""
    <div class="tip-box">
    <h3>🎓 Your Complete Six Sigma Reference</h3>
    <p>Comprehensive coverage of Six Sigma methodology, tools, and techniques. 
    Each topic includes definitions, examples, when to use, and how to interpret results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Encyclopedia navigation
    encyclopedia_section = st.selectbox(
        "Select Topic:",
        [
            '📖 Fundamentals',
            '📊 DMAIC Methodology',
            '📈 Control Charts',
            '🧮 Statistical Methods',
            '📉 Process Capability',
            '🔍 Root Cause Analysis',
            '🧪 Design of Experiments (DOE)',
            '📏 Measurement System Analysis',
            '🎯 Hypothesis Testing',
            '📐 Regression & Correlation',
            '🛠️ Quality Tools',
            '📋 Glossary & Formulas'
        ]
    )
    
    # ═══════════════════════════════════════════════════════════════
    # FUNDAMENTALS
    # ═══════════════════════════════════════════════════════════════
    
    if encyclopedia_section == '📖 Fundamentals':
        
        st.markdown("## 📖 Six Sigma Fundamentals")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "What is Six Sigma?",
            "History & Evolution",
            "Key Concepts",
            "Belts & Roles",
            "Benefits & Applications"
        ])
        
        with tab1:
            st.markdown("""
            ### What is Six Sigma?
            
            **Six Sigma** is a data-driven methodology and set of tools for process improvement. 
            It seeks to improve the quality of process outputs by identifying and removing the causes 
            of defects and minimizing variability in manufacturing and business processes.
            
            #### Key Principles:
            
            1. **Focus on the Customer**
               - Understand customer requirements (CTQs - Critical to Quality)
               - Measure performance against customer expectations
               - Deliver value that meets or exceeds requirements
            
            2. **Data-Driven Decisions**
               - Measure and analyze actual performance data
               - Use statistical methods to validate decisions
               - Eliminate opinions and assumptions
            
            3. **Process Focus**
               - Understand and improve processes, not just outcomes
               - Map and analyze process flows
               - Identify root causes, not symptoms
            
            4. **Proactive Management**
               - Prevent defects rather than detect them
               - Build quality into processes
               - Anticipate and mitigate risks
            
            5. **Collaboration**
               - Cross-functional teams
               - Stakeholder engagement
               - Sharing best practices
            
            6. **Continuous Improvement**
               - Strive for perfection (while recognizing it's a journey)
               - Sustain gains and raise the bar
               - Culture of excellence
            
            #### What Does "Six Sigma" Mean?
            
            Sigma (σ) is a Greek letter representing standard deviation in statistics. 
            In Six Sigma:
            
            - **1 Sigma** = 691,000 defects per million opportunities (DPMO)
            - **2 Sigma** = 308,000 DPMO
            - **3 Sigma** = 66,800 DPMO ← Most businesses operate here
            - **4 Sigma** = 6,210 DPMO
            - **5 Sigma** = 233 DPMO
            - **6 Sigma** = 3.4 DPMO ← The goal!
            
            A Six Sigma process produces only **3.4 defects per million opportunities** - 
            virtually defect-free performance (99.99966% quality level).
            """)
            
            # Visual representation
            st.markdown("#### Visual Representation of Sigma Levels")
            
            fig = go.Figure()
            
            # Normal distribution
            x = np.linspace(-6, 6, 1000)
            y = stats.norm.pdf(x, 0, 1)
            
            fig.add_trace(go.Scatter(
                x=x, y=y,
                fill='tozeroy',
                name='Process Distribution',
                line=dict(color='blue', width=2)
            ))
            
            # Add specification limits for different sigma levels
            for sigma in [3, 4, 5, 6]:
                fig.add_vline(x=sigma, line_dash="dash", 
                             annotation_text=f"{sigma}σ",
                             line_color='red')
                fig.add_vline(x=-sigma, line_dash="dash", 
                             line_color='red')
            
            fig.update_layout(
                title="Process Distribution and Sigma Levels",
                xaxis_title="Standard Deviations from Mean",
                yaxis_title="Probability Density",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            st.markdown("""
            ### History & Evolution of Six Sigma
            
            #### 1980s: Birth at Motorola
            - **1986**: Engineer Bill Smith develops Six Sigma methodology at Motorola
            - **1987**: Motorola CEO Bob Galvin champions Six Sigma company-wide
            - **1988**: Motorola wins Malcolm Baldrige National Quality Award
            - Six Sigma helps Motorola save $16 billion over 11 years
            
            #### 1990s: Popularization
            - **1995**: GE CEO Jack Welch adopts Six Sigma
            - GE reports $12 billion in savings by 1998
            - Larry Bossidy brings it to Allied Signal
            - Methodology spreads across Fortune 500 companies
            
            #### 2000s: Expansion Beyond Manufacturing
            - Six Sigma enters service industries
            - Healthcare, finance, government adopt the methodology
            - Integration with Lean (Lean Six Sigma)
            - Software and IT adopt adapted versions
            
            #### 2010s-Present: Modern Applications
            - Integration with Agile and DevOps
            - Data Science and Machine Learning applications
            - Industry 4.0 and IoT integration
            - Sustainability and green initiatives
            
            #### Key Figures in Six Sigma History
            
            | Person | Role | Contribution |
            |--------|------|--------------|
            | **Bill Smith** | Engineer, Motorola | Created the methodology |
            | **Bob Galvin** | CEO, Motorola | Championed adoption |
            | **Mikel Harry** | Motorola Engineer | Developed training program |
            | **Jack Welch** | CEO, GE | Popularized globally |
            | **Michael George** | Consultant | Lean Six Sigma integration |
            
            #### Evolution of the Methodology
            
            **Original Six Sigma (1980s)**
            - Focus: Manufacturing defect reduction
            - Tools: Statistical Process Control, DOE
            - Structure: Belt system (Green, Black, Master Black)
            
            **Six Sigma + (1990s-2000s)**
            - DMAIC framework standardized
            - Design for Six Sigma (DFSS) created
            - Service applications developed
            
            **Lean Six Sigma (2000s)**
            - Integration with Toyota Production System
            - Speed + Quality focus
            - Value stream mapping added
            
            **Modern Six Sigma (2010s-Present)**
            - Big Data analytics
            - Machine learning integration
            - Real-time process monitoring
            - Cloud-based collaboration tools
            """)
        
        with tab3:
            st.markdown("""
            ### Key Six Sigma Concepts
            
            #### 1. Variation
            
            **Variation** is the enemy of quality. All processes have variation:
            
            - **Common Cause Variation**: Natural, inherent to the process
              - Example: Slight differences in raw materials
              - Solution: Process redesign
            
            - **Special Cause Variation**: Assignable, unusual events
              - Example: Machine breakdown, untrained operator
              - Solution: Identify and eliminate the cause
            
            #### 2. Critical to Quality (CTQ)
            
            CTQs are the key measurable characteristics whose performance standards must be met.
            
            **CTQ Tree Example:**
            ```
            Customer Need: "Fast delivery"
                ├─ Order processing time < 2 hours
                ├─ Picking accuracy > 99.5%
                └─ Shipping time < 24 hours
            ```
            
            #### 3. Defects, Defectives, and Opportunities
            
            - **Defect**: Any instance where a requirement is not met
            - **Defective**: A unit that contains one or more defects
            - **Opportunity**: A chance for a defect to occur
            
            **Example:**
            - Product has 5 inspection points (5 opportunities)
            - 3 defects found across 100 units
            - DPMO = (3 / (100 × 5)) × 1,000,000 = 6,000 DPMO
            
            #### 4. Process Capability
            
            Measures how well a process meets specifications:
            
            - **Cp**: Potential capability (if perfectly centered)
              - Cp = (USL - LSL) / (6σ)
            
            - **Cpk**: Actual capability (accounts for centering)
              - Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]
            
            **Interpretation:**
            - Cpk < 1.0: Process not capable
            - Cpk = 1.33: Minimum acceptable
            - Cpk ≥ 1.67: Good capability
            - Cpk ≥ 2.0: Excellent (Six Sigma level)
            
            #### 5. Y = f(X) Relationship
            
            The fundamental Six Sigma equation:
            
            **Y = f(X₁, X₂, X₃, ..., Xₙ)**
            
            Where:
            - **Y** = Output (dependent variable, CTQ)
            - **X** = Inputs (independent variables, process factors)
            - **f** = Function (the relationship/process)
            
            **Goal**: Identify critical Xs that drive Y
            
            #### 6. The 1.5 Sigma Shift
            
            Six Sigma assumes processes drift ±1.5σ over time:
            
            - Short-term capability (Cpk) assumes no drift
            - Long-term performance (Ppk) accounts for drift
            - 4.5σ short-term = 3σ long-term (≈ 66,800 DPMO)
            - 6σ short-term = 4.5σ long-term (≈ 3.4 DPMO)
            
            #### 7. Hidden Factory
            
            The "Hidden Factory" represents:
            - Rework and corrections
            - Inspection and sorting
            - Expediting and firefighting
            - Waste that's accepted as "normal"
            
            **Six Sigma exposes and eliminates the hidden factory**
            """)
            
            # Interactive Cp/Cpk calculator
            st.markdown("#### 🧮 Interactive Capability Calculator")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                process_mean = st.number_input("Process Mean (μ):", value=10.0, step=0.1)
            with col2:
                process_std = st.number_input("Process Std Dev (σ):", value=0.5, min_value=0.01, step=0.1)
            with col3:
                st.write("")  # Spacer
            
            col1, col2, col3 = st.columns(3)
            with col1:
                calc_lsl = st.number_input("LSL:", value=8.0, step=0.1)
            with col2:
                calc_usl = st.number_input("USL:", value=12.0, step=0.1)
            with col3:
                st.write("")  # Spacer
            
            # Calculate
            calc_cp = (calc_usl - calc_lsl) / (6 * process_std)
            calc_cpu = (calc_usl - process_mean) / (3 * process_std)
            calc_cpl = (process_mean - calc_lsl) / (3 * process_std)
            calc_cpk = min(calc_cpu, calc_cpl)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Cp", f"{calc_cp:.3f}")
            col2.metric("Cpk", f"{calc_cpk:.3f}")
            col3.metric("Cpu", f"{calc_cpu:.3f}")
            col4.metric("Cpl", f"{calc_cpl:.3f}")
            
            # Visual
            fig = go.Figure()
            
            x = np.linspace(calc_lsl - 2, calc_usl + 2, 500)
            y_dist = stats.norm.pdf(x, process_mean, process_std)
            
            fig.add_trace(go.Scatter(x=x, y=y_dist, fill='tozeroy', name='Process'))
            fig.add_vline(x=calc_lsl, line_dash="dash", line_color="red", annotation_text="LSL")
            fig.add_vline(x=calc_usl, line_dash="dash", line_color="red", annotation_text="USL")
            fig.add_vline(x=process_mean, line_color="green", annotation_text="Mean")
            
            fig.update_layout(
                title="Process Distribution vs Specifications",
                xaxis_title="Value",
                yaxis_title="Density",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("""
            ### Six Sigma Belts & Roles
            
            The Six Sigma organizational structure uses a martial arts belt ranking system:
            
            #### 🥇 Executive Leadership
            
            **Champion (Senior Leader)**
            - **Role**: Executive sponsor, removes barriers
            - **Responsibilities:**
              - Select projects aligned with strategy
              - Allocate resources
              - Remove organizational obstacles
              - Review project progress
            - **Time Commitment**: 5-10% (oversight role)
            
            **Deployment Leader**
            - **Role**: Oversees Six Sigma program
            - **Responsibilities:**
              - Program strategy and planning
              - Resource allocation
              - Training coordination
              - Metrics and reporting
            
            #### 🥋 Master Black Belt (MBB)
            
            - **Training**: 4+ weeks, deep statistical expertise
            - **Experience**: Several successful Black Belt projects
            - **Role**: Six Sigma expert, coach, mentor
            - **Responsibilities:**
              - Train and mentor Black Belts and Green Belts
              - Provide advanced statistical support
              - Develop new tools and methods
              - Lead complex, strategic projects
            - **Typical Ratio**: 1 MBB per 30 Black Belts
            - **Time Commitment**: 100% dedicated
            
            #### 🥋 Black Belt (BB)
            
            - **Training**: 4 weeks (typically spread over 4 months)
            - **Certification**: Complete 2+ successful projects
            - **Role**: Full-time improvement professional
            - **Responsibilities:**
              - Lead major DMAIC projects
              - Mentor Green Belts
              - Advanced statistical analysis
              - Change management
            - **Project Scope**: $250K+ impact, 4-6 months
            - **Typical Ratio**: 1% of workforce
            - **Time Commitment**: 100% dedicated to projects
            
            **Required Skills:**
            - Advanced statistics (hypothesis testing, regression, DOE)
            - Project management
            - Change management
            - Team leadership
            - Presentation and influence
            
            #### 🟢 Green Belt (GB)
            
            - **Training**: 2 weeks
            - **Certification**: Complete 1+ successful project
            - **Role**: Part-time improvement while maintaining regular job
            - **Responsibilities:**
              - Lead smaller projects (often within own area)
              - Support Black Belt projects as team member
              - Basic statistical analysis
              - Process improvement
            - **Project Scope**: $50-100K impact, 2-4 months
            - **Typical Ratio**: 5% of workforce
            - **Time Commitment**: 20-50% while keeping day job
            
            **Required Skills:**
            - Basic statistics (control charts, capability, hypothesis tests)
            - Problem solving
            - Process mapping
            - Team participation
            
            #### 🟡 Yellow Belt (YB)
            
            - **Training**: 2-3 days
            - **Role**: Awareness and support
            - **Responsibilities:**
              - Understand Six Sigma basics
              - Participate in projects as team member
              - Small improvements in own work area
            - **Typical Ratio**: 20-30% of workforce
            - **Time Commitment**: Minimal, as needed
            
            #### 🔵 White Belt
            
            - **Training**: 4-8 hours
            - **Role**: Basic awareness
            - **Responsibilities:**
              - Understand Six Sigma terminology
              - Support improvement culture
            - **Typical Ratio**: All employees
            
            #### 👥 Team Member Roles
            
            **Process Owner**
            - Responsible for the process being improved
            - Provides resources and access
            - Implements and sustains changes
            
            **Subject Matter Expert (SME)**
            - Deep process knowledge
            - Technical expertise
            - Historical context
            
            **Team Member**
            - Active participation
            - Data collection
            - Implementation support
            
            #### 📊 Typical Organization Structure
            
            ```
            CEO
            └── Deployment Champion
                ├── Master Black Belt (Coach/Mentor)
                │   ├── Black Belt (Full-time project leader)
                │   │   ├── Green Belt (Part-time project leader)
                │   │   │   ├── Yellow Belt (Team member)
                │   │   │   └── White Belt (Aware participant)
                │   │   └── Team Members (SMEs, Process Owners)
                │   └── Black Belt
                └── Master Black Belt
            ```
            
            #### 🎓 Certification Bodies
            
            - **ASQ (American Society for Quality)**: Most recognized globally
            - **IASSC (International Association for Six Sigma Certification)**
            - **Council for Six Sigma Certification (CSSC)**
            - Company-specific programs (GE, Motorola, etc.)
            
            #### 💰 Career Impact
            
            **Salary Premiums (US Market, approximate):**
            - Green Belt: +$5,000-10,000
            - Black Belt: +$15,000-25,000
            - Master Black Belt: +$30,000-50,000
            
            **Career Paths:**
            - Operational excellence roles
            - Quality management
            - Process engineering
            - Plant/operations management
            - Consulting
            """)
        
        with tab5:
            st.markdown("""
            ### Benefits & Applications of Six Sigma
            
            #### 💰 Financial Benefits
            
            **Documented Savings:**
            - **Motorola**: $16 billion (1987-1997)
            - **General Electric**: $12 billion in first 3 years
            - **Honeywell**: $3.5 billion over 5 years
            - **Ford**: $1 billion annually
            
            **Typical ROI:**
            - Black Belt project: $150-500K average savings
            - Investment: $50-100K (training, time, resources)
            - **ROI: 3:1 to 10:1** in Year 1
            
            #### 🏭 Industry Applications
            
            **Manufacturing**
            - ✅ Defect reduction
            - ✅ Yield improvement
            - ✅ Cycle time reduction
            - ✅ Scrap/rework reduction
            - ✅ Equipment reliability (OEE)
            - **Example**: Reduce defect rate from 3% to 0.5%, saving $2M annually
            
            **Healthcare**
            - ✅ Reduce medication errors
            - ✅ Improve patient wait times
            - ✅ Increase bed utilization
            - ✅ Reduce infection rates
            - ✅ Streamline billing processes
            - **Example**: Reduce ER wait time from 4 hours to 90 minutes
            
            **Financial Services**
            - ✅ Loan processing time
            - ✅ Transaction accuracy
            - ✅ Call center performance
            - ✅ Fraud detection
            - ✅ Customer onboarding
            - **Example**: Reduce loan approval time from 30 days to 5 days
            
            **IT/Software**
            - ✅ Defect density reduction
            - ✅ Deployment reliability
            - ✅ Incident resolution time
            - ✅ System availability
            - ✅ Development cycle time
            - **Example**: Improve system uptime from 95% to 99.9%
            
            **Supply Chain/Logistics**
            - ✅ On-time delivery
            - ✅ Inventory accuracy
            - ✅ Order fulfillment speed
            - ✅ Shipping damage reduction
            - ✅ Warehouse efficiency
            - **Example**: Increase on-time delivery from 85% to 98%
            
            **Customer Service**
            - ✅ Call handling time
            - ✅ First call resolution
            - ✅ Customer satisfaction
            - ✅ Complaint reduction
            - ✅ Service level achievement
            - **Example**: Increase first-call resolution from 60% to 90%
            
            #### 📈 Business Benefits
            
            **Quantitative Benefits:**
            - ✅ Cost reduction (20-50% typical)
            - ✅ Defect reduction (50-90%)
            - ✅ Cycle time improvement (30-60%)
            - ✅ Capacity increase (15-30%)
            - ✅ Revenue growth (improved quality → customer satisfaction → sales)
            
            **Qualitative Benefits:**
            - ✅ Customer satisfaction improvement
            - ✅ Employee engagement
            - ✅ Data-driven culture
            - ✅ Competitive advantage
            - ✅ Organizational learning
            - ✅ Change management capability
            
            #### 🎯 When to Use Six Sigma
            
            **Best Fit:**
            - ✅ Chronic, recurring problems
            - ✅ High-volume, repeatable processes
            - ✅ Data is available or can be collected
            - ✅ Problem cause is unknown
            - ✅ Solution requires validation
            - ✅ Process is stable but needs improvement
            
            **Poor Fit:**
            - ❌ One-time or rare issues
            - ❌ Obvious solutions (just fix it!)
            - ❌ No data available and can't collect
            - ❌ Urgent crisis (use rapid response first)
            - ❌ Problem is strategic, not operational
            
            #### ⚠️ Common Challenges
            
            **Implementation Challenges:**
            1. **Lack of Leadership Support**
               - Solution: Executive training, visible sponsorship
            
            2. **Poor Project Selection**
               - Solution: Align with strategy, use selection criteria
            
            3. **Insufficient Training**
               - Solution: Invest in proper certification programs
            
            4. **Resistance to Change**
               - Solution: Change management, communication, quick wins
            
            5. **Data Quality Issues**
               - Solution: MSA, data collection systems
            
            6. **Not Sustaining Improvements**
               - Solution: Control plans, audits, standard work
            
            7. **Treating it as a Program, Not Culture**
               - Solution: Long-term commitment, integration with operations
            
            #### 🌟 Success Factors
            
            **Critical Success Factors:**
            1. **Top Management Commitment** (most important!)
            2. Project alignment with business strategy
            3. Proper training and certification
            4. Effective project selection
            5. Dedicated resources (time, budget, people)
            6. Data-driven decision culture
            7. Recognition and rewards
            8. Integration with existing systems
            9. Sustainability focus (Control phase)
            10. Communication and knowledge sharing
            
            #### 📊 Measuring Six Sigma Success
            
            **Program Metrics:**
            - Number of certified belts
            - Projects completed
            - Financial impact (verified savings)
            - Sigma level improvement
            - Customer satisfaction scores
            - Employee engagement
            - Cycle time reductions
            - Defect rate reductions
            
            **Leading vs Lagging Indicators:**
            - **Leading**: Training completion, projects launched, team meetings
            - **Lagging**: Savings achieved, Sigma levels, customer complaints
            """)
    
    # ═══════════════════════════════════════════════════════════════
    # DMAIC METHODOLOGY
    # ═══════════════════════════════════════════════════════════════
    
    elif encyclopedia_section == '📊 DMAIC Methodology':
        
        st.markdown("## 📊 DMAIC Methodology - Complete Guide")
        
        st.markdown("""
        <div class="phase-box">
        <h3 style="color: white;">The DMAIC Framework</h3>
        <p style="color: white; font-size: 1.1em;">
        DMAIC (Define-Measure-Analyze-Improve-Control) is the core Six Sigma methodology 
        for improving existing processes. Each phase has specific objectives, tools, and deliverables.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # DMAIC Phase selector
        dmaic_phase = st.selectbox(
            "Select DMAIC Phase to Learn:",
            ['📋 DMAIC Overview', '🎯 Define', '📊 Measure', '🔍 Analyze', '🚀 Improve', '🎛️ Control']
        )
        
        if dmaic_phase == '📋 DMAIC Overview':
            
            st.markdown("""
            ### What is DMAIC?
            
            **DMAIC** is a systematic, data-driven methodology for improving existing processes, products, or services.
            It provides a structured approach to problem-solving that ensures improvements are based on facts, not assumptions.
            
            #### Why DMAIC?
            
            - ✅ **Structured**: Step-by-step framework prevents skipping important steps
            - ✅ **Data-Driven**: Decisions based on evidence, not opinions
            - ✅ **Repeatable**: Can be applied to any process improvement
            - ✅ **Comprehensive**: Addresses root causes, not symptoms
            - ✅ **Sustainable**: Control phase ensures gains don't erode
            
            #### The Five Phases Explained
            """)
            
            # Create visual DMAIC roadmap
            fig = go.Figure()
            
            phases = ['Define', 'Measure', 'Analyze', 'Improve', 'Control']
            colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            
            for i, (phase, color) in enumerate(zip(phases, colors)):
                fig.add_trace(go.Scatter(
                    x=[i], y=[1],
                    mode='markers+text',
                    marker=dict(size=80, color=color),
                    text=phase,
                    textposition='middle center',
                    textfont=dict(size=14, color='white', family='Arial Black'),
                    showlegend=False
                ))
                
                if i < len(phases) - 1:
                    fig.add_annotation(
                        x=i+0.5, y=1,
                        text='→',
                        showarrow=False,
                        font=dict(size=30, color='gray')
                    )
            
            fig.update_layout(
                title="The DMAIC Roadmap",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 4.5]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 1.5]),
                height=200,
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed phase breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="tool-card">
                <h4>🎯 1. DEFINE</h4>
                <p><b>Goal:</b> Clearly define the problem and project scope</p>
                <p><b>Duration:</b> 2-4 weeks</p>
                <p><b>Key Question:</b> "What is the problem and why does it matter?"</p>
                <p><b>Key Tools:</b></p>
                <ul>
                <li>Project Charter</li>
                <li>SIPOC Diagram</li>
                <li>Voice of Customer (VOC)</li>
                <li>Stakeholder Analysis</li>
                </ul>
                <p><b>Deliverables:</b></p>
                <ul>
                <li>Problem statement</li>
                <li>Goal statement</li>
                <li>Project scope</li>
                <li>Team charter</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="tool-card">
                <h4>🔍 3. ANALYZE</h4>
                <p><b>Goal:</b> Identify and verify root causes</p>
                <p><b>Duration:</b> 3-5 weeks</p>
                <p><b>Key Question:</b> "Why is this happening?"</p>
                <p><b>Key Tools:</b></p>
                <ul>
                <li>Fishbone Diagram</li>
                <li>5 Whys</li>
                <li>Hypothesis Testing</li>
                <li>Regression Analysis</li>
                <li>ANOVA</li>
                </ul>
                <p><b>Deliverables:</b></p>
                <ul>
                <li>Verified root causes</li>
                <li>Statistical proof</li>
                <li>Critical X's identified</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="tool-card">
                <h4>🎛️ 5. CONTROL</h4>
                <p><b>Goal:</b> Sustain the improvements</p>
                <p><b>Duration:</b> 2-4 weeks (plus ongoing monitoring)</p>
                <p><b>Key Question:</b> "How do we maintain the gains?"</p>
                <p><b>Key Tools:</b></p>
                <ul>
                <li>Control Plan</li>
                <li>Standard Operating Procedures</li>
                <li>Control Charts</li>
                <li>Audits and Reviews</li>
                </ul>
                <p><b>Deliverables:</b></p>
                <ul>
                <li>Control plan</li>
                <li>Updated SOPs</li>
                <li>Training materials</li>
                <li>Handoff documentation</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="tool-card">
                <h4>📊 2. MEASURE</h4>
                <p><b>Goal:</b> Establish baseline performance and validate measurement system</p>
                <p><b>Duration:</b> 4-6 weeks</p>
                <p><b>Key Question:</b> "How are we performing today?"</p>
                <p><b>Key Tools:</b></p>
                <ul>
                <li>Data Collection Plan</li>
                <li>Measurement System Analysis (MSA)</li>
                <li>Process Capability</li>
                <li>Control Charts</li>
                </ul>
                <p><b>Deliverables:</b></p>
                <ul>
                <li>Baseline Sigma level</li>
                <li>Process capability (Cpk)</li>
                <li>MSA results</li>
                <li>Current state map</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="tool-card">
                <h4>🚀 4. IMPROVE</h4>
                <p><b>Goal:</b> Develop and implement solutions</p>
                <p><b>Duration:</b> 6-10 weeks</p>
                <p><b>Key Question:</b> "What changes will eliminate root causes?"</p>
                <p><b>Key Tools:</b></p>
                <ul>
                <li>Brainstorming</li>
                <li>Design of Experiments (DOE)</li>
                <li>Pilot Testing</li>
                <li>Cost-Benefit Analysis</li>
                <li>FMEA</li>
                </ul>
                <p><b>Deliverables:</b></p>
                <ul>
                <li>Implemented solutions</li>
                <li>Pilot results</li>
                <li>New Sigma level</li>
                <li>Validated improvements</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # DMAIC Timeline
            st.markdown("### 📅 Typical DMAIC Project Timeline")
            
            timeline_data = pd.DataFrame({
                'Phase': ['Define', 'Measure', 'Analyze', 'Improve', 'Control'],
                'Start': [0, 3, 7, 10, 16],
                'Duration': [3, 4, 3, 6, 2],
                'Weeks': ['0-3', '3-7', '7-10', '10-16', '16-18']
            })
            
            fig = go.Figure()
            
            colors_timeline = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            
            for i, row in timeline_data.iterrows():
                fig.add_trace(go.Bar(
                    name=row['Phase'],
                    x=[row['Duration']],
                    y=[row['Phase']],
                    orientation='h',
                    marker=dict(color=colors_timeline[i]),
                    text=f"{row['Weeks']} weeks",
                    textposition='inside',
                    showlegend=False
                ))
            
            fig.update_layout(
                title="DMAIC Project Timeline (Typical 18-24 weeks)",
                xaxis_title="Weeks",
                yaxis_title="",
                barmode='stack',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="warning-box">
            <b>⏰ Timeline Note:</b><br>
            The above is a typical timeline. Actual duration varies based on:
            <ul>
            <li>Project complexity</li>
            <li>Data availability</li>
            <li>Team resources</li>
            <li>Organizational factors</li>
            </ul>
            Some projects finish in 3 months, others take 6+ months.
            </div>
            """, unsafe_allow_html=True)
            
            # Common Mistakes
            st.markdown("### ⚠️ Common DMAIC Mistakes to Avoid")
            
            mistakes_data = {
                'Define': [
                    "Skipping Define to 'save time'",
                    "Problem statement too vague",
                    "Scope too broad ('boil the ocean')",
                    "Solutions embedded in problem statement",
                    "No baseline metrics defined"
                ],
                'Measure': [
                    "Skipping Measurement System Analysis",
                    "Insufficient data (n < 30)",
                    "Not checking process stability",
                    "Measuring symptoms instead of root causes",
                    "Accepting data without validation"
                ],
                'Analyze': [
                    "Jumping to solutions without analysis",
                    "Confusing correlation with causation",
                    "Not validating root causes statistically",
                    "Analysis paralysis (over-analyzing)",
                    "Ignoring process knowledge"
                ],
                'Improve': [
                    "Implementing without piloting",
                    "No cost-benefit analysis",
                    "Not considering risks (FMEA)",
                    "Solution doesn't address root cause",
                    "Changing multiple things at once"
                ],
                'Control': [
                    "No control plan created",
                    "Not documenting changes in SOPs",
                    "Insufficient training",
                    "No ongoing monitoring",
                    "Declaring victory too early"
                ]
            }
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs(['Define', 'Measure', 'Analyze', 'Improve', 'Control'])
            
            for tab, (phase, mistakes) in zip([tab1, tab2, tab3, tab4, tab5], mistakes_data.items()):
                with tab:
                    for mistake in mistakes:
                        st.markdown(f"❌ {mistake}")

# This is PART 1 of the complete encyclopedia. The code is getting very long.

# Would you like me to:
# 1. Continue with the remaining sections (Control Charts, Statistical Methods, etc.)?
# 2. Create this as a multi-page app (separate files for each section)?
# 3. Deploy what we have so far and add sections incrementally?