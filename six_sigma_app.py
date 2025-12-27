"""
═══════════════════════════════════════════════════════════════════════════════
    COMPLETE SIX SIGMA AUTO-ANALYZER
    
    Automatic Detection & Analysis System:
    1. Upload data → System detects type automatically
    2. Auto-generates project charter and timeline
    3. Runs complete DMAIC analysis automatically
    4. Provides detailed interpretations and recommendations
    5. Creates complete project documentation
    
    Zero manual configuration needed - just upload and go!
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import anderson, shapiro
import statsmodels.api as sm
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Six Sigma Auto-Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    
    .hero-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    .interpretation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
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
    
    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        background: white;
        margin: 20px 0;
    }
    
    .step-box {
        background: white;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS - AUTO DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def auto_detect_data_type(df):
    """Automatically detect if data is discrete (defects) or continuous (measurements)"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Look for defect-related keywords
    defect_keywords = ['defect', 'error', 'fail', 'reject', 'rework', 'scrap', 'ng', 'bad']
    opportunity_keywords = ['opportunity', 'sample', 'unit', 'total', 'inspected']
    
    defect_cols = [col for col in df.columns if any(kw in col.lower() for kw in defect_keywords)]
    opportunity_cols = [col for col in df.columns if any(kw in col.lower() for kw in opportunity_keywords)]
    
    if defect_cols and opportunity_cols:
        return {
            'type': 'discrete',
            'defect_col': defect_cols[0],
            'opportunity_col': opportunity_cols[0],
            'confidence': 'high'
        }
    elif defect_cols:
        return {
            'type': 'discrete',
            'defect_col': defect_cols[0],
            'opportunity_col': None,
            'confidence': 'medium'
        }
    else:
        # Assume continuous if no defect keywords
        # Pick the column with most variation as the CTQ
        if numeric_cols:
            variances = {col: df[col].var() for col in numeric_cols}
            ctq_col = max(variances, key=variances.get)
            
            return {
                'type': 'continuous',
                'ctq_col': ctq_col,
                'confidence': 'medium'
            }
    
    return {
        'type': 'unknown',
        'confidence': 'low'
    }

def auto_detect_specifications(data):
    """Automatically estimate specification limits from data"""
    
    mean = data.mean()
    std = data.std()
    
    # Use 6-sigma range as initial spec limits
    lsl = mean - 3 * std
    usl = mean + 3 * std
    
    # Round to reasonable precision
    precision = len(str(std).split('.')[-1]) if '.' in str(std) else 0
    
    lsl = round(lsl, precision)
    usl = round(usl, precision)
    target = round(mean, precision)
    
    return lsl, usl, target

def interpret_sigma_level(sigma, dpmo):
    """Detailed interpretation of Sigma level"""
    
    if sigma >= 6:
        return {
            'level': 'World Class',
            'color': '🟢',
            'quality': f'99.99966% yield - {dpmo:.1f} DPMO',
            'benchmark': 'Top 0.1% of companies globally',
            'examples': 'Aviation safety, pharmaceutical critical processes',
            'action': 'Maintain excellence. Share best practices across organization.',
            'business_impact': 'Premium pricing power, industry leadership, minimal quality costs',
            'recommendation': 'Focus on sustaining performance and knowledge transfer'
        }
    elif sigma >= 5:
        return {
            'level': 'Excellent',
            'color': '🟢',
            'quality': f'99.98% yield - {dpmo:.0f} DPMO',
            'benchmark': 'Top 5% - Industry leading',
            'examples': 'Top automotive, leading hospitals, best-in-class manufacturing',
            'action': 'Sustain and target 6 Sigma for critical processes',
            'business_impact': 'Strong competitive advantage, high customer loyalty',
            'recommendation': 'Continue current practices. Document and standardize.'
        }
    elif sigma >= 4:
        return {
            'level': 'Good',
            'color': '🟡',
            'quality': f'99.38% yield - {dpmo:.0f} DPMO',
            'benchmark': 'Above average - Top quartile',
            'examples': 'Modern manufacturing, good service operations',
            'action': 'Good foundation. Focus improvement on critical CTQs to reach 5 Sigma.',
            'business_impact': 'Competitive, moderate quality costs (5-10% of sales)',
            'recommendation': 'Identify top 3 improvement opportunities. Launch DMAIC projects.'
        }
    elif sigma >= 3:
        return {
            'level': 'Average',
            'color': '🟠',
            'quality': f'93.3% yield - {dpmo:.0f} DPMO',
            'benchmark': 'Typical industry performance',
            'examples': 'Traditional manufacturing, typical service industries',
            'action': 'SIGNIFICANT IMPROVEMENT OPPORTUNITY. Start DMAIC projects immediately.',
            'business_impact': 'High quality costs (15-25% of sales), customer complaints common',
            'recommendation': 'URGENT: Launch 3-5 improvement projects. Quick wins needed.'
        }
    elif sigma >= 2:
        return {
            'level': 'Poor',
            'color': '🔴',
            'quality': f'69.1% yield - {dpmo:.0f} DPMO',
            'benchmark': 'Below average - Bottom quartile',
            'examples': 'Struggling operations, high rework environments',
            'action': 'CRITICAL SITUATION. Immediate executive intervention required.',
            'business_impact': 'Very high costs (30-40% of sales), customer defection risk',
            'recommendation': 'CRISIS MODE: Daily management review. Emergency improvement team.'
        }
    else:
        return {
            'level': 'Critical',
            'color': '⛔',
            'quality': f'{(1-dpmo/1000000)*100:.1f}% yield - {dpmo:.0f} DPMO',
            'benchmark': 'Non-competitive - Survival threatened',
            'examples': 'Operations in crisis',
            'action': 'EMERGENCY: Business viability at risk. Immediate action required.',
            'business_impact': 'Unsustainable. Major customer loss imminent.',
            'recommendation': 'STOP and fix immediately. Consider process shutdown until stable.'
        }

def interpret_cpk(cpk, cp):
    """Detailed Cpk interpretation"""
    
    if cpk >= 2.0:
        return {
            'rating': 'Excellent - Six Sigma Capable',
            'color': '🟢',
            'meaning': 'Process exceeds requirements with large safety margin',
            'defect_rate': '< 3.4 PPM - Virtually defect-free',
            'action': 'Monitor periodically. Consider process optimization for cost reduction.',
            'business_value': 'Premium quality. Potential for spec tightening or cost reduction.'
        }
    elif cpk >= 1.67:
        return {
            'rating': 'Very Good - Five Sigma Capable',
            'color': '🟢',
            'meaning': 'Process consistently meets requirements',
            'defect_rate': '< 0.6 PPM expected',
            'action': 'Maintain current performance. Reduce inspection frequency.',
            'business_value': 'Excellent quality. Low inspection costs justified.'
        }
    elif cpk >= 1.33:
        return {
            'rating': 'Good - Capable',
            'color': '🟡',
            'meaning': 'Process meets requirements but limited margin',
            'defect_rate': '< 63 PPM expected',
            'action': 'Adequate. Monitor regularly. Variation reduction would improve margin.',
            'business_value': 'Acceptable quality. Some inspection still recommended.'
        }
    elif cpk >= 1.0:
        return {
            'rating': 'Marginal - Barely Capable',
            'color': '🟠',
            'meaning': 'Process barely meets specifications',
            'defect_rate': '~2,700 PPM (0.27%)',
            'action': 'IMPROVEMENT NEEDED. Increase monitoring. Center process if possible.',
            'business_value': 'High risk. Customer complaints likely. Improvement urgent.'
        }
    else:
        return {
            'rating': 'Not Capable',
            'color': '🔴',
            'meaning': 'Process cannot consistently meet specifications',
            'defect_rate': f'> 2,700 PPM - High defect rate',
            'action': 'CRITICAL: 100% inspection required. Process improvement mandatory.',
            'business_value': 'Unsustainable. Major quality costs. Customer dissatisfaction.'
        }

def generate_auto_timeline(project_type='Manufacturing'):
    """Generate automatic project timeline"""
    
    phases = {
        'Manufacturing': {'Define': 3, 'Measure': 5, 'Analyze': 4, 'Improve': 8, 'Control': 2},
        'Service': {'Define': 2, 'Measure': 6, 'Analyze': 5, 'Improve': 10, 'Control': 3},
        'Transactional': {'Define': 2, 'Measure': 4, 'Analyze': 4, 'Improve': 6, 'Control': 2}
    }
    
    timeline = phases.get(project_type, phases['Manufacturing'])
    total_weeks = sum(timeline.values())
    
    return {
        'phases': timeline,
        'total_weeks': total_weeks,
        'total_months': round(total_weeks / 4, 1),
        'end_date': datetime.now() + timedelta(weeks=total_weeks)
    }

def calculate_financial_impact(current_dpmo, target_dpmo, annual_volume):
    """Calculate financial impact of improvement"""
    
    # Industry average costs
    cost_per_defect = 75  # Average of scrap, rework, warranty
    
    current_defects = annual_volume * (current_dpmo / 1_000_000)
    target_defects = annual_volume * (target_dpmo / 1_000_000)
    defects_avoided = current_defects - target_defects
    
    annual_savings = defects_avoided * cost_per_defect
    
    # Project investment (typical)
    project_investment = 50000  # Black Belt time + resources
    
    roi = ((annual_savings - project_investment) / project_investment) * 100 if project_investment > 0 else 0
    payback_months = (project_investment / annual_savings * 12) if annual_savings > 0 else 999
    
    return {
        'annual_savings': annual_savings,
        'defects_avoided': defects_avoided,
        'investment': project_investment,
        'roi': roi,
        'payback_months': payback_months
    }

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

# Hero Section
st.markdown("""
<div class="hero-box">
<h1 style="color: white; margin: 0; font-size: 3em;">🎯 Six Sigma Auto-Analyzer</h1>
<p style="font-size: 1.3em; margin-top: 15px;">
Upload your data → Get complete DMAIC analysis automatically
</p>
<p style="font-size: 1.1em; opacity: 0.9;">
No configuration needed • Automatic detection • Detailed interpretations • Full project plan
</p>
</div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("## 📁 Step 1: Upload Your Data")

st.markdown("""
<div class="upload-zone">
<h3>📊 Drop your Excel or CSV file here</h3>
<p>Supported formats: CSV, XLS, XLSX</p>
<p><b>The system will automatically:</b></p>
<ul style="list-style: none; padding: 0;">
<li>✅ Detect if you have defect data or measurement data</li>
<li>✅ Identify the right columns to analyze</li>
<li>✅ Calculate current Sigma level</li>
<li>✅ Generate complete project charter and timeline</li>
<li>✅ Provide detailed recommendations</li>
</ul>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your data file",
    type=['csv', 'xlsx', 'xls'],
    help="Upload Excel or CSV file with your process data"
)

if uploaded_file is not None:
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DATA LOADING
    # ═══════════════════════════════════════════════════════════════════════════
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        
        with st.expander("📊 View Raw Data"):
            st.dataframe(df.head(100))
        
        # ═══════════════════════════════════════════════════════════════════════
        # AUTO DETECTION
        # ═══════════════════════════════════════════════════════════════════════
        
        st.markdown("---")
        st.markdown("## 🤖 Step 2: Automatic Analysis")
        
        with st.spinner("🔍 Analyzing your data..."):
            detection = auto_detect_data_type(df)
        
        st.markdown(f"""
        <div class="success-box">
        <h3>✅ Data Type Detected: {detection['type'].upper()}</h3>
        <p><b>Confidence:</b> {detection['confidence'].upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════════════
        # CONTINUOUS DATA ANALYSIS
        # ═══════════════════════════════════════════════════════════════════════
        
        if detection['type'] == 'continuous':
            
            ctq_col = detection['ctq_col']
            data = df[ctq_col].dropna()
            
            st.info(f"📏 **Analyzing:** {ctq_col} ({len(data)} data points)")
            
            # Auto-detect specifications
            lsl_auto, usl_auto, target_auto = auto_detect_specifications(data)
            
            st.markdown("### 🎯 Specification Limits")
            st.markdown("""
            <div class="recommendation-box">
            <p>The system has auto-detected specification limits based on your data distribution.</p>
            <p><b>You can adjust these if you know your actual specifications:</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                lsl = st.number_input("Lower Spec Limit (LSL)", value=float(lsl_auto), format="%.4f")
            with col2:
                usl = st.number_input("Upper Spec Limit (USL)", value=float(usl_auto), format="%.4f")
            with col3:
                target = st.number_input("Target", value=float(target_auto), format="%.4f")
            
            # Calculate metrics
            mean = data.mean()
            std = data.std()
            
            cp = (usl - lsl) / (6 * std)
            cpu = (usl - mean) / (3 * std)
            cpl = (mean - lsl) / (3 * std)
            cpk = min(cpu, cpl)
            
            defects = ((data < lsl) | (data > usl)).sum()
            dpmo = (defects / len(data)) * 1_000_000
            
            if dpmo >= 933193:
                sigma_level = 0
            else:
                sigma_level = stats.norm.ppf(1 - dpmo/1_000_000) + 1.5
            
            # ═══════════════════════════════════════════════════════════════════
            # RESULTS WITH DETAILED INTERPRETATIONS
            # ═══════════════════════════════════════════════════════════════════
            
            st.markdown("---")
            st.markdown("## 📊 COMPLETE ANALYSIS RESULTS")
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Sigma Level", f"{sigma_level:.2f}")
            col2.metric("DPMO", f"{dpmo:,.0f}")
            col3.metric("Cpk", f"{cpk:.3f}")
            col4.metric("Yield", f"{(1-dpmo/1000000)*100:.2f}%")
            
            # Sigma Interpretation
            sigma_interp = interpret_sigma_level(sigma_level, dpmo)
            
            st.markdown(f"""
            <div class="interpretation-box">
            <h2 style="color: white;">{sigma_interp['color']} Performance Level: {sigma_interp['level']}</h2>
            <h3 style="color: white;">Current Quality: {sigma_interp['quality']}</h3>
            <p style="font-size: 1.1em; color: white;"><b>Industry Benchmark:</b> {sigma_interp['benchmark']}</p>
            <p style="color: white;"><b>Comparable to:</b> {sigma_interp['examples']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="color: white;"><b>Business Impact:</b> {sigma_interp['business_impact']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="recommendation-box">
            <h3>💡 Recommended Action</h3>
            <p><b>{sigma_interp['action']}</b></p>
            <p><i>{sigma_interp['recommendation']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cpk Interpretation
            cpk_interp = interpret_cpk(cpk, cp)
            
            st.markdown("### 🎯 Process Capability Assessment")
            
            st.markdown(f"""
            <div class="metric-card">
            <h3>{cpk_interp['color']} {cpk_interp['rating']}</h3>
            <p><b>What this means:</b> {cpk_interp['meaning']}</p>
            <p><b>Expected defect rate:</b> {cpk_interp['defect_rate']}</p>
            <p><b>Business impact:</b> {cpk_interp['business_value']}</p>
            <hr>
            <p><b>Action required:</b> {cpk_interp['action']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Financial Analysis
            st.markdown("---")
            st.markdown("### 💰 Financial Impact Analysis")
            
            annual_volume = st.number_input(
                "Annual Production Volume:",
                value=100000,
                step=10000,
                help="Enter your annual production volume to calculate financial impact"
            )
            
            target_sigma = st.slider(
                "Target Sigma Level (Improvement Goal):",
                min_value=float(max(sigma_level, 3.0)),
                max_value=6.0,
                value=float(min(sigma_level + 1, 6.0)),
                step=0.5
            )
            
            target_dpmo = (1 - stats.norm.cdf(target_sigma - 1.5)) * 1_000_000
            
            financials = calculate_financial_impact(dpmo, target_dpmo, annual_volume)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Annual Savings", f"${financials['annual_savings']:,.0f}")
            col2.metric("ROI", f"{financials['roi']:.0f}%")
            col3.metric("Payback Period", f"{financials['payback_months']:.1f} months")
            
            st.markdown(f"""
            <div class="success-box">
            <h4>📈 Improvement Scenario: {sigma_level:.1f}σ → {target_sigma:.1f}σ</h4>
            <p><b>Defects avoided annually:</b> {financials['defects_avoided']:,.0f}</p>
            <p><b>Annual cost savings:</b> ${financials['annual_savings']:,.0f}</p>
            <p><b>Project investment:</b> ${financials['investment']:,.0f}</p>
            <p><b>Return on Investment:</b> {financials['roi']:.0f}%</p>
            <p><b>Payback period:</b> {financials['payback_months']:.1f} months</p>
            </div>
            """, unsafe_allow_html=True)
            
            # AUTO-GENERATED PROJECT PLAN
            st.markdown("---")
            st.markdown("## 📋 AUTO-GENERATED PROJECT PLAN")
            
            timeline = generate_auto_timeline('Manufacturing')
            
            st.markdown(f"""
            <div class="interpretation-box">
            <h3 style="color: white;">🎯 Recommended DMAIC Project</h3>
            <p style="color: white; font-size: 1.2em;"><b>Project Name:</b> Improve {ctq_col} Process Capability</p>
            <p style="color: white;"><b>Goal:</b> Reduce DPMO from {dpmo:,.0f} to {target_dpmo:,.0f} ({target_sigma:.1f} Sigma)</p>
            <p style="color: white;"><b>Expected Timeline:</b> {timeline['total_weeks']} weeks ({timeline['total_months']} months)</p>
            <p style="color: white;"><b>Expected Savings:</b> ${financials['annual_savings']:,.0f} per year</p>
            <p style="color: white;"><b>ROI:</b> {financials['roi']:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Timeline breakdown
            st.markdown("### 📅 Project Timeline")
            
            current_date = datetime.now()
            for phase, weeks in timeline['phases'].items():
                end_date = current_date + timedelta(weeks=weeks)
                
                st.markdown(f"""
                <div class="step-box">
                <h4>{phase} Phase</h4>
                <p><b>Duration:</b> {weeks} weeks</p>
                <p><b>Start:</b> {current_date.strftime('%Y-%m-%d')} | <b>End:</b> {end_date.strftime('%Y-%m-%d')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                current_date = end_date
            
            # Charts
            st.markdown("---")
            st.markdown("### 📊 Process Visualization")
            
            # Histogram
            fig_hist = go.Figure()
            
            fig_hist.add_trace(go.Histogram(
                x=data,
                nbinsx=40,
                name='Actual Data',
                opacity=0.7,
                marker_color='lightblue'
            ))
            
            x_range = np.linspace(data.min(), data.max(), 200)
            y_normal = stats.norm.pdf(x_range, mean, std) * len(data) * (data.max() - data.min()) / 40
            
            fig_hist.add_trace(go.Scatter(
                x=x_range,
                y=y_normal,
                mode='lines',
                name='Normal Distribution',
                line=dict(color='red', width=2)
            ))
            
            fig_hist.add_vline(x=lsl, line_dash="dash", line_color="red", line_width=3,
                              annotation_text="LSL")
            fig_hist.add_vline(x=usl, line_dash="dash", line_color="red", line_width=3,
                              annotation_text="USL")
            fig_hist.add_vline(x=target, line_dash="dash", line_color="green", line_width=2,
                              annotation_text="Target")
            fig_hist.add_vline(x=mean, line_color="blue", line_width=2,
                              annotation_text="Mean")
            
            fig_hist.update_layout(
                title="Process Distribution vs Specification Limits",
                xaxis_title=ctq_col,
                yaxis_title="Frequency",
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Control Chart
            st.markdown("### 📈 Process Stability Check (Control Chart)")
            
            mr = data.diff().abs()
            mr_mean = mr.mean()
            ucl = mean + 2.66 * mr_mean
            lcl = mean - 2.66 * mr_mean
            
            out_of_control = (data > ucl) | (data < lcl)
            
            fig_control = go.Figure()
            
            fig_control.add_trace(go.Scatter(
                y=data,
                mode='lines+markers',
                name='Individual Values',
                line=dict(color='blue'),
                marker=dict(size=6)
            ))
            
            fig_control.add_hline(y=ucl, line_dash="dash", line_color="red", 
                                 annotation_text="UCL")
            fig_control.add_hline(y=mean, line_color="green", 
                                 annotation_text="Mean")
            fig_control.add_hline(y=lcl, line_dash="dash", line_color="red", 
                                 annotation_text="LCL")
            
            if out_of_control.any():
                fig_control.add_trace(go.Scatter(
                    x=data[out_of_control].index,
                    y=data[out_of_control],
                    mode='markers',
                    name='Out of Control',
                    marker=dict(color='red', size=12, symbol='x', line=dict(width=2))
                ))
            
            fig_control.update_layout(
                title="Individual-MR Control Chart",
                xaxis_title="Sample Number",
                yaxis_title=ctq_col,
                height=500
            )
            
            st.plotly_chart(fig_control, use_container_width=True)
            
            if out_of_control.any():
                st.markdown(f"""
                <div class="warning-box">
                <p><b>⚠️ {out_of_control.sum()} out-of-control points detected</b></p>
                <p>Process shows special cause variation. Investigation required before process improvement.</p>
                <p><b>Recommended action:</b> Identify and remove special causes, then recollect baseline data.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box">
                <p><b>✅ Process is in statistical control</b></p>
                <p>Only common cause variation present. Process is stable and predictable.</p>
                <p><b>Ready to proceed with process capability improvement.</b></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Next Steps
            st.markdown("---")
            st.markdown("## ✅ Recommended Next Steps")
            
            next_steps = [
                {
                    'step': '1. Get Management Approval',
                    'detail': f'Present business case: ${financials["annual_savings"]:,.0f} annual savings with {financials["roi"]:.0f}% ROI',
                    'timeline': 'Week 1'
                },
                {
                    'step': '2. Form Project Team',
                    'detail': 'Identify Black Belt, process owner, and team members (5-7 people recommended)',
                    'timeline': 'Week 1'
                },
                {
                    'step': '3. Launch Define Phase',
                    'detail': 'Create project charter, SIPOC diagram, and stakeholder analysis',
                    'timeline': 'Weeks 1-3'
                },
                {
                    'step': '4. Validate Measurement System',
                    'detail': 'Conduct Gage R&R study to ensure measurement reliability',
                    'timeline': 'Weeks 4-5'
                },
                {
                    'step': '5. Begin Root Cause Analysis',
                    'detail': 'Use Fishbone, 5 Whys, and statistical analysis to identify critical Xs',
                    'timeline': 'Weeks 6-9'
                }
            ]
            
            for step_info in next_steps:
                st.markdown(f"""
                <div class="recommendation-box">
                <h4>{step_info['step']}</h4>
                <p>{step_info['detail']}</p>
                <p><b>Timeline:</b> {step_info['timeline']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════════════════════════
        # DISCRETE DATA ANALYSIS
        # ═══════════════════════════════════════════════════════════════════════
        
        elif detection['type'] == 'discrete':
            
            defect_col = detection['defect_col']
            opportunity_col = detection.get('opportunity_col')
            
            if opportunity_col:
                st.info(f"📊 **Analyzing:** {defect_col} vs {opportunity_col}")
                
                total_defects = df[defect_col].sum()
                total_opportunities = df[opportunity_col].sum()
                
                dpo = total_defects / total_opportunities
                dpmo = dpo * 1_000_000
                
                if dpo >= 1:
                    sigma_level = 0
                else:
                    sigma_level = stats.norm.ppf(1 - dpo) + 1.5
                
                yield_pct = (1 - dpo) * 100
                
                # Results
                st.markdown("---")
                st.markdown("## 📊 DEFECT ANALYSIS RESULTS")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Sigma Level", f"{sigma_level:.2f}")
                col2.metric("DPMO", f"{dpmo:,.0f}")
                col3.metric("Total Defects", f"{total_defects:,.0f}")
                col4.metric("Yield", f"{yield_pct:.2f}%")
                
                # Interpretation
                sigma_interp = interpret_sigma_level(sigma_level, dpmo)
                
                st.markdown(f"""
                <div class="interpretation-box">
                <h2 style="color: white;">{sigma_interp['color']} Performance: {sigma_interp['level']}</h2>
                <h3 style="color: white;">{sigma_interp['quality']}</h3>
                <p style="font-size: 1.1em; color: white;"><b>Benchmark:</b> {sigma_interp['benchmark']}</p>
                <p style="color: white;"><b>Similar to:</b> {sigma_interp['examples']}</p>
                <hr style="border-color: rgba(255,255,255,0.3);">
                <p style="color: white;"><b>Business Impact:</b> {sigma_interp['business_impact']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="recommendation-box">
                <h3>💡 Required Action</h3>
                <p><b>{sigma_interp['action']}</b></p>
                <p>{sigma_interp['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # P-Chart
                st.markdown("### 📉 P-Chart (Proportion Defective)")
                
                df['proportion'] = df[defect_col] / df[opportunity_col]
                p_bar = df['proportion'].mean()
                n_bar = df[opportunity_col].mean()
                
                ucl_p = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar)
                lcl_p = max(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar))
                
                fig_pchart = go.Figure()
                
                fig_pchart.add_trace(go.Scatter(
                    y=df['proportion'],
                    mode='lines+markers',
                    name='Proportion Defective',
                    line=dict(color='blue')
                ))
                
                fig_pchart.add_hline(y=ucl_p, line_dash="dash", line_color="red", annotation_text="UCL")
                fig_pchart.add_hline(y=p_bar, line_color="green", annotation_text="Mean")
                fig_pchart.add_hline(y=lcl_p, line_dash="dash", line_color="red", annotation_text="LCL")
                
                out_of_control_p = (df['proportion'] > ucl_p) | (df['proportion'] < lcl_p)
                
                if out_of_control_p.any():
                    fig_pchart.add_trace(go.Scatter(
                        x=df[out_of_control_p].index,
                        y=df.loc[out_of_control_p, 'proportion'],
                        mode='markers',
                        name='Out of Control',
                        marker=dict(color='red', size=12, symbol='x')
                    ))
                
                fig_pchart.update_layout(
                    title="P-Chart: Process Control",
                    xaxis_title="Sample",
                    yaxis_title="Proportion Defective",
                    height=500
                )
                
                st.plotly_chart(fig_pchart, use_container_width=True)
                
                # Auto project plan for discrete
                st.markdown("---")
                st.markdown("## 📋 AUTO-GENERATED IMPROVEMENT PROJECT")
                
                annual_volume = st.number_input("Annual Volume:", value=1000000, step=100000)
                target_sigma = st.slider("Target Sigma:", min_value=float(max(sigma_level, 3)), max_value=6.0, value=float(min(sigma_level+1, 6)), step=0.5)
                
                target_dpmo_discrete = (1 - stats.norm.cdf(target_sigma - 1.5)) * 1_000_000
                financials_discrete = calculate_financial_impact(dpmo, target_dpmo_discrete, annual_volume)
                
                timeline_discrete = generate_auto_timeline('Manufacturing')
                
                st.markdown(f"""
                <div class="interpretation-box">
                <h3 style="color: white;">🎯 Defect Reduction Project</h3>
                <p style="color: white; font-size: 1.2em;"><b>Goal:</b> Reduce defect rate from {dpmo:,.0f} to {target_dpmo_discrete:,.0f} DPMO</p>
                <p style="color: white;"><b>Timeline:</b> {timeline_discrete['total_weeks']} weeks</p>
                <p style="color: white;"><b>Expected Savings:</b> ${financials_discrete['annual_savings']:,.0f}/year</p>
                <p style="color: white;"><b>ROI:</b> {financials_discrete['roi']:.0f}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.warning("⚠️ Could not automatically detect data type. Please ensure your data has clear column names (e.g., 'Defects', 'Opportunities', or measurement names)")
    
    except Exception as e:
        st.error(f"❌ Error analyzing data: {str(e)}")
        st.info("Please ensure your data is in the correct format (CSV or Excel with headers)")

else:
    # Landing page when no file uploaded
    st.markdown("## 🚀 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="step-box">
        <h3>1️⃣ Upload Data</h3>
        <p>Drop your Excel or CSV file</p>
        <p><b>No preparation needed!</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-box">
        <h3>2️⃣ Auto-Analysis</h3>
        <p>System detects data type</p>
        <p><b>Runs complete analysis</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-box">
        <h3>3️⃣ Get Results</h3>
        <p>Detailed interpretations</p>
        <p><b>Complete project plan</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📊 Sample Data Format")
    
    tab1, tab2 = st.tabs(["Continuous Data (Measurements)", "Discrete Data (Defects)"])
    
    with tab1:
        st.markdown("""
        **For measurement data (dimensions, time, weight, etc.):**
        
        | Sample | Measurement | Machine | Operator |
        |--------|-------------|---------|----------|
        | 1 | 10.2 | M1 | John |
        | 2 | 10.5 | M2 | Mary |
        | 3 | 10.1 | M1 | John |
        
        Just upload and the system handles the rest!
        """)
    
    with tab2:
        st.markdown("""
        **For defect data:**
        
        | Date | Defects | Opportunities | Machine |
        |------|---------|---------------|---------|
        | 2024-01-01 | 5 | 1000 | M1 |
        | 2024-01-02 | 3 | 1000 | M2 |
        | 2024-01-03 | 8 | 1000 | M1 |
        
        System auto-detects defect columns!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 20px;">
<p><b>Six Sigma Auto-Analyzer</b> | Complete DMAIC Analysis in Minutes</p>
<p>Upload → Analyze → Get Results | No Configuration Required</p>
</div>
""", unsafe_allow_html=True)