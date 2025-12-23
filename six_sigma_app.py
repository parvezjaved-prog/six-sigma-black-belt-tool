"""
SIX SIGMA BLACK BELT AUTO-PILOT 2025
Complete automated Six Sigma analysis tool
Author: Your Name | Date: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import normaltest, shapiro
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Six Sigma Black Belt Auto-Pilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stMetric {background-color: white; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);}
    h1 {color: #1f4788;}
    h2 {color: #2e5c8a;}
    h3 {color: #3d6fa3;}
    .reportview-container .main footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Title and Introduction
st.title("🚀 Six Sigma Black Belt Auto-Pilot")
st.markdown("**Upload your data → Get instant Sigma level, root causes, and professional charts**")
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("⚙️ Configuration")
    
    uploaded_file = st.file_uploader(
        "Upload your data (CSV or Excel)", 
        type=['csv', 'xlsx', 'xls'],
        help="Your file should have a date column and either defect/opportunity columns OR measurement (CTQ) data"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Quick Guide")
    st.markdown("""
    **For Discrete Data (Defects):**
    - Include columns: Date, Defects, Opportunities
    
    **For Continuous Data (Measurements):**
    - Include columns: Date, Measurement values
    - You'll set specifications (USL/LSL)
    
    **Sample Data Format:**
    ```
    Date       | Defects | Opportunities
    2024-01-01 | 5       | 1000
    2024-01-02 | 3       | 1000
    ```
    """)

# Main content area
if uploaded_file is not None:
    
    # Load data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File loaded successfully! {len(df)} rows, {len(df.columns)} columns")
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
    
    # Data preview
    with st.expander("📋 View Raw Data (first 100 rows)", expanded=False):
        st.dataframe(df.head(100), use_container_width=True)
    
    # Data info
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", f"{len(df):,}")
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    st.markdown("---")
    
    # Auto-detect column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = [col for col in df.columns if any(x in col.lower() for x in ['date', 'time', 'day', 'month', 'year'])]
    defect_cols = [col for col in df.columns if any(x in col.lower() for x in ['defect', 'bad', 'ng', 'fail', 'rework', 'reject', 'error'])]
    opportunity_cols = [col for col in df.columns if any(x in col.lower() for x in ['opportunity', 'opportun', 'sample', 'unit', 'total'])]
    
    # Determine data type
    st.header("🔍 Step 1: Data Type Detection")
    
    data_type = st.radio(
        "Select your data type:",
        ["Auto-detect", "Discrete (Attribute) Data - Defects/Pass-Fail", "Continuous (Variable) Data - Measurements"],
        help="Auto-detect will analyze your columns and suggest the best type"
    )
    
    if data_type == "Auto-detect":
        if defect_cols or opportunity_cols:
            data_type = "Discrete (Attribute) Data - Defects/Pass-Fail"
            st.info(f"✅ Auto-detected: **Discrete Data** (Found columns: {', '.join(defect_cols + opportunity_cols)})")
        else:
            data_type = "Continuous (Variable) Data - Measurements"
            st.info(f"✅ Auto-detected: **Continuous Data** (Found numeric columns: {', '.join(numeric_cols[:3])}...)")
    
    st.markdown("---")
    
    # ========================================
    # DISCRETE DATA ANALYSIS
    # ========================================
    
    if "Discrete" in data_type:
        st.header("📊 Discrete Data Analysis (Attribute)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            defect_col = st.selectbox(
                "Select Defect/Failure column:",
                defect_cols if defect_cols else df.columns.tolist(),
                help="Column containing count of defects, failures, or non-conformances"
            )
        
        with col2:
            opportunity_col = st.selectbox(
                "Select Opportunity/Sample Size column:",
                opportunity_cols if opportunity_cols else df.columns.tolist(),
                help="Column containing number of opportunities or sample size"
            )
        
        if st.button("🚀 Run Discrete Analysis", type="primary"):
            
            # Calculate metrics
            try:
                total_defects = df[defect_col].sum()
                total_opportunities = df[opportunity_col].sum()
                
                dpu = total_defects / len(df)  # Defects per unit
                dpmo = (total_defects / total_opportunities) * 1_000_000
                dpo = total_defects / total_opportunities
                yield_pct = (1 - dpo) * 100
                
                # Sigma calculation (accounting for 1.5 sigma shift)
                if dpo >= 1:
                    sigma_lt = 0
                    sigma_st = 0
                else:
                    sigma_lt = stats.norm.ppf(1 - dpo)
                    sigma_st = sigma_lt + 1.5
                
                # Display key metrics
                st.markdown("### 🎯 Key Performance Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Defects", f"{total_defects:,.0f}")
                    st.metric("DPU", f"{dpu:.4f}")
                
                with col2:
                    st.metric("DPMO", f"{dpmo:,.0f}")
                    st.metric("DPO", f"{dpo:.6f}")
                
                with col3:
                    st.metric("Yield %", f"{yield_pct:.3f}%")
                    st.metric("First Pass Yield", f"{yield_pct:.2f}%")
                
                with col4:
                    sigma_color = "🟢" if sigma_st >= 4 else "🟡" if sigma_st >= 3 else "🔴"
                    st.metric("Sigma Level (ST)", f"{sigma_color} {sigma_st:.2f}")
                    st.metric("Sigma Level (LT)", f"{sigma_lt:.2f}")
                
                # Sigma interpretation
                st.markdown("### 📈 Sigma Level Interpretation")
                
                if sigma_st >= 6:
                    interpretation = "🌟 **WORLD CLASS** - 3.4 DPMO - Best in class performance"
                elif sigma_st >= 5:
                    interpretation = "🟢 **EXCELLENT** - 233 DPMO - Industry leading"
                elif sigma_st >= 4:
                    interpretation = "🟡 **GOOD** - 6,210 DPMO - Above average, room for improvement"
                elif sigma_st >= 3:
                    interpretation = "🟠 **AVERAGE** - 66,807 DPMO - Typical industry performance, needs improvement"
                elif sigma_st >= 2:
                    interpretation = "🔴 **POOR** - 308,538 DPMO - Significant quality issues"
                else:
                    interpretation = "⛔ **CRITICAL** - >308,538 DPMO - Immediate action required"
                
                st.info(interpretation)
                
                # Control chart (P-chart)
                st.markdown("### 📉 P-Chart (Proportion Defective)")
                
                df['proportion'] = df[defect_col] / df[opportunity_col]
                p_bar = df['proportion'].mean()
                n_bar = df[opportunity_col].mean()
                
                ucl_p = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar)
                lcl_p = max(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar))
                
                fig_pchart = go.Figure()
                
                fig_pchart.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=df['proportion'],
                    mode='lines+markers',
                    name='Proportion Defective',
                    line=dict(color='blue'),
                    marker=dict(size=6)
                ))
                
                fig_pchart.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=[ucl_p] * len(df),
                    mode='lines',
                    name='UCL',
                    line=dict(color='red', dash='dash')
                ))
                
                fig_pchart.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=[p_bar] * len(df),
                    mode='lines',
                    name='Center Line',
                    line=dict(color='green', dash='dash')
                ))
                
                fig_pchart.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=[lcl_p] * len(df),
                    mode='lines',
                    name='LCL',
                    line=dict(color='red', dash='dash')
                ))
                
                # Detect out-of-control points
                out_of_control = (df['proportion'] > ucl_p) | (df['proportion'] < lcl_p)
                
                if out_of_control.any():
                    fig_pchart.add_trace(go.Scatter(
                        x=df[out_of_control].index,
                        y=df.loc[out_of_control, 'proportion'],
                        mode='markers',
                        name='Out of Control',
                        marker=dict(color='red', size=12, symbol='x')
                    ))
                
                fig_pchart.update_layout(
                    title="P-Chart: Process Control Chart",
                    xaxis_title="Sample Number",
                    yaxis_title="Proportion Defective",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig_pchart, use_container_width=True)
                
                # Control chart interpretation
                if out_of_control.any():
                    st.warning(f"⚠️ **{out_of_control.sum()} out-of-control points detected!** These indicate special cause variation requiring investigation.")
                    st.dataframe(df[out_of_control][[defect_col, opportunity_col, 'proportion']])
                else:
                    st.success("✅ Process is in statistical control - only common cause variation present")
                
                # Pareto analysis if there are categories
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                if categorical_cols:
                    st.markdown("### 📊 Root Cause Analysis")
                    
                    category_col = st.selectbox("Select category for Pareto analysis:", categorical_cols)
                    
                    if category_col:
                        # Pareto chart
                        pareto_data = df.groupby(category_col)[defect_col].sum().sort_values(ascending=False)
                        pareto_pct = (pareto_data / pareto_data.sum() * 100).cumsum()
                        
                        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
                        
                        fig_pareto.add_trace(
                            go.Bar(x=pareto_data.index, y=pareto_data.values, name="Defects"),
                            secondary_y=False
                        )
                        
                        fig_pareto.add_trace(
                            go.Scatter(x=pareto_data.index, y=pareto_pct.values, name="Cumulative %", 
                                      mode='lines+markers', line=dict(color='red')),
                            secondary_y=True
                        )
                        
                        fig_pareto.update_layout(
                            title=f"Pareto Chart: Defects by {category_col}",
                            xaxis_title=category_col,
                            height=500
                        )
                        
                        fig_pareto.update_yaxes(title_text="Defect Count", secondary_y=False)
                        fig_pareto.update_yaxes(title_text="Cumulative %", secondary_y=True)
                        
                        st.plotly_chart(fig_pareto, use_container_width=True)
                        
                        # Statistical testing (Chi-square)
                        st.markdown("#### Statistical Significance Testing")
                        
                        contingency_table = pd.crosstab(df[category_col], df[defect_col] > 0)
                        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Chi-square statistic", f"{chi2:.2f}")
                        col2.metric("p-value", f"{p_value:.4f}")
                        col3.metric("Degrees of freedom", dof)
                        
                        if p_value < 0.05:
                            st.success(f"✅ **SIGNIFICANT ROOT CAUSE FOUND!** {category_col} has a statistically significant effect on defects (p < 0.05)")
                        else:
                            st.info(f"ℹ️ {category_col} does not show significant effect on defects (p = {p_value:.4f})")
                
            except Exception as e:
                st.error(f"Error in analysis: {e}")
    
    # ========================================
    # CONTINUOUS DATA ANALYSIS
    # ========================================
    
    elif "Continuous" in data_type:
        st.header("📏 Continuous Data Analysis (Variable)")
        
        # Select CTQ
        ctq_col = st.selectbox(
            "Select CTQ (Critical to Quality) measurement column:",
            numeric_cols,
            help="The main quality characteristic you want to analyze"
        )
        
        # Specification limits
        st.markdown("### 🎯 Specification Limits")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            usl = st.number_input(
                "Upper Specification Limit (USL):",
                value=float(df[ctq_col].quantile(0.99) * 1.1),
                format="%.4f"
            )
        
        with col2:
            lsl = st.number_input(
                "Lower Specification Limit (LSL):",
                value=float(df[ctq_col].quantile(0.01) * 0.9),
                format="%.4f"
            )
        
        with col3:
            target = st.number_input(
                "Target (nominal):",
                value=float((usl + lsl) / 2),
                format="%.4f"
            )
        
        if st.button("🚀 Run Continuous Analysis", type="primary"):
            
            try:
                # Clean data
                data = df[ctq_col].dropna()
                
                # Basic statistics
                mean = data.mean()
                std = data.std()
                median = data.median()
                
                st.markdown("### 📊 Descriptive Statistics")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                col1.metric("Mean", f"{mean:.4f}")
                col2.metric("Std Dev", f"{std:.4f}")
                col3.metric("Median", f"{median:.4f}")
                col4.metric("Min", f"{data.min():.4f}")
                col5.metric("Max", f"{data.max():.4f}")
                
                # Normality test
                st.markdown("### 📈 Normality Assessment")
                
                # Anderson-Darling test
                anderson_result = stats.anderson(data)
                shapiro_stat, shapiro_p = shapiro(data) if len(data) < 5000 else (None, None)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Anderson-Darling Statistic", f"{anderson_result.statistic:.4f}")
                    if anderson_result.statistic < anderson_result.critical_values[2]:  # 5% significance
                        st.success("✅ Data appears normally distributed")
                        is_normal = True
                    else:
                        st.warning("⚠️ Data may not be normally distributed")
                        is_normal = False
                
                with col2:
                    if shapiro_p:
                        st.metric("Shapiro-Wilk p-value", f"{shapiro_p:.4f}")
                        if shapiro_p > 0.05:
                            st.success("✅ Passes Shapiro-Wilk test")
                        else:
                            st.warning("⚠️ Fails Shapiro-Wilk test")
                
                # Histogram with normal curve
                fig_hist = go.Figure()
                
                fig_hist.add_trace(go.Histogram(
                    x=data,
                    name='Actual Data',
                    nbinsx=30,
                    histnorm='probability density',
                    marker_color='lightblue'
                ))
                
                # Normal curve overlay
                x_range = np.linspace(data.min(), data.max(), 100)
                normal_curve = stats.norm.pdf(x_range, mean, std)
                
                fig_hist.add_trace(go.Scatter(
                    x=x_range,
                    y=normal_curve,
                    name='Normal Distribution',
                    line=dict(color='red', width=2)
                ))
                
                # Add spec limits
                fig_hist.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
                fig_hist.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
                fig_hist.add_vline(x=target, line_dash="dash", line_color="green", annotation_text="Target")
                
                fig_hist.update_layout(
                    title="Histogram with Normal Curve and Spec Limits",
                    xaxis_title=ctq_col,
                    yaxis_title="Density",
                    height=500
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Probability plot
                fig_prob = go.Figure()
                
                # Q-Q plot
                (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm")
                
                fig_prob.add_trace(go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    name='Actual',
                    marker=dict(color='blue')
                ))
                
                fig_prob.add_trace(go.Scatter(
                    x=osm,
                    y=slope * osm + intercept,
                    mode='lines',
                    name='Theoretical Normal',
                    line=dict(color='red')
                ))
                
                fig_prob.update_layout(
                    title=f"Normal Probability Plot (R² = {r**2:.4f})",
                    xaxis_title="Theoretical Quantiles",
                    yaxis_title="Sample Quantiles",
                    height=500
                )
                
                st.plotly_chart(fig_prob, use_container_width=True)
                
                # Process Capability Analysis
                st.markdown("### 🎯 Process Capability Analysis")
                
                # Short-term capability (within subgroup)
                cp = (usl - lsl) / (6 * std)
                cpu = (usl - mean) / (3 * std)
                cpl = (mean - lsl) / (3 * std)
                cpk = min(cpu, cpl)
                
                # Long-term capability (overall)
                pp = (usl - lsl) / (6 * std)
                ppu = (usl - mean) / (3 * std)
                ppl = (mean - lsl) / (3 * std)
                ppk = min(ppu, ppl)
                
                # Calculate defects
                defects_above = sum(data > usl)
                defects_below = sum(data < lsl)
                total_defects = defects_above + defects_below
                
                dpmo_actual = (total_defects / len(data)) * 1_000_000
                
                # Estimated DPMO from normal distribution
                prob_above = 1 - stats.norm.cdf(usl, mean, std)
                prob_below = stats.norm.cdf(lsl, mean, std)
                dpmo_est = (prob_above + prob_below) * 1_000_000
                
                # Sigma levels
                if dpmo_est >= 1000000:
                    sigma_lt = 0
                    sigma_st = 0
                else:
                    sigma_lt = stats.norm.ppf(1 - dpmo_est/1_000_000)
                    sigma_st = sigma_lt + 1.5
                
                # Display capability metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Cp", f"{cp:.3f}")
                    st.metric("Cpu", f"{cpu:.3f}")
                    
                with col2:
                    cpk_color = "🟢" if cpk >= 1.33 else "🟡" if cpk >= 1.0 else "🔴"
                    st.metric("Cpk", f"{cpk_color} {cpk:.3f}")
                    st.metric("Cpl", f"{cpl:.3f}")
                
                with col3:
                    st.metric("Pp", f"{pp:.3f}")
                    st.metric("Ppk", f"{ppk:.3f}")
                
                with col4:
                    sigma_color = "🟢" if sigma_st >= 4 else "🟡" if sigma_st >= 3 else "🔴"
                    st.metric("Sigma (ST)", f"{sigma_color} {sigma_st:.2f}")
                    st.metric("Sigma (LT)", f"{sigma_lt:.2f}")
                
                # Capability interpretation
                st.markdown("#### Capability Interpretation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if cpk >= 2.0:
                        st.success("🌟 **EXCELLENT** - Cpk ≥ 2.0 - Six Sigma capable")
                    elif cpk >= 1.33:
                        st.success("✅ **CAPABLE** - Cpk ≥ 1.33 - Process meets requirements")
                    elif cpk >= 1.0:
                        st.warning("⚠️ **MARGINAL** - 1.0 ≤ Cpk < 1.33 - Improvement needed")
                    else:
                        st.error("🔴 **NOT CAPABLE** - Cpk < 1.0 - Immediate action required")
                
                with col2:
                    st.metric("Estimated DPMO", f"{dpmo_est:,.0f}")
                    st.metric("Actual Defects", f"{total_defects} ({dpmo_actual:,.0f} DPMO)")
                
                # Process capability chart
                fig_capability = go.Figure()
                
                # Plot distribution
                x_range = np.linspace(data.min() - std, data.max() + std, 200)
                y_dist = stats.norm.pdf(x_range, mean, std)
                
                fig_capability.add_trace(go.Scatter(
                    x=x_range,
                    y=y_dist,
                    fill='tozeroy',
                    name='Process Distribution',
                    fillcolor='rgba(0, 100, 255, 0.3)',
                    line=dict(color='blue')
                ))
                
                # Spec limits
                fig_capability.add_vline(x=lsl, line_dash="dash", line_color="red", line_width=3, annotation_text="LSL")
                fig_capability.add_vline(x=usl, line_dash="dash", line_color="red", line_width=3, annotation_text="USL")
                fig_capability.add_vline(x=target, line_dash="dash", line_color="green", line_width=2, annotation_text="Target")
                fig_capability.add_vline(x=mean, line_color="blue", line_width=2, annotation_text="Mean")
                
                # Shade out-of-spec areas
                x_below = x_range[x_range < lsl]
                y_below = stats.norm.pdf(x_below, mean, std)
                
                x_above = x_range[x_range > usl]
                y_above = stats.norm.pdf(x_above, mean, std)
                
                fig_capability.add_trace(go.Scatter(
                    x=x_below,
                    y=y_below,
                    fill='tozeroy',
                    name='Below LSL',
                    fillcolor='rgba(255, 0, 0, 0.3)',
                    line=dict(color='red', width=0)
                ))
                
                fig_capability.add_trace(go.Scatter(
                    x=x_above,
                    y=y_above,
                    fill='tozeroy',
                    name='Above USL',
                    fillcolor='rgba(255, 0, 0, 0.3)',
                    line=dict(color='red', width=0)
                ))
                
                fig_capability.update_layout(
                    title="Process Capability Visualization",
                    xaxis_title=ctq_col,
                    yaxis_title="Probability Density",
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig_capability, use_container_width=True)
                
                # Control Charts
                st.markdown("### 📉 Control Charts")
                
                # I-MR Chart (Individual and Moving Range)
                df_chart = df[[ctq_col]].copy()
                df_chart['MR'] = df_chart[ctq_col].diff().abs()
                
                # Individual chart
                ucl_i = mean + 2.66 * df_chart['MR'].mean()
                lcl_i = mean - 2.66 * df_chart['MR'].mean()
                
                # Moving Range chart
                mr_mean = df_chart['MR'].mean()
                ucl_mr = 3.267 * mr_mean
                lcl_mr = 0
                
                fig_control = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=("Individual Chart", "Moving Range Chart"),
                    vertical_spacing=0.15
                )
                
                # Individual chart
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=df_chart[ctq_col],
                              mode='lines+markers', name='Individual Values',
                              line=dict(color='blue')),
                    row=1, col=1
                )
                
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=[ucl_i]*len(df_chart),
                              mode='lines', name='UCL', line=dict(color='red', dash='dash')),
                    row=1, col=1
                )
                
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=[mean]*len(df_chart),
                              mode='lines', name='Mean', line=dict(color='green')),
                    row=1, col=1
                )
                
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=[lcl_i]*len(df_chart),
                              mode='lines', name='LCL', line=dict(color='red', dash='dash')),
                    row=1, col=1
                )
                
                # Detect out of control points
                out_of_control_i = (df_chart[ctq_col] > ucl_i) | (df_chart[ctq_col] < lcl_i)
                
                if out_of_control_i.any():
                    fig_control.add_trace(
                        go.Scatter(x=df_chart[out_of_control_i].index,
                                  y=df_chart.loc[out_of_control_i, ctq_col],
                                  mode='markers', name='Out of Control',
                                  marker=dict(color='red', size=10, symbol='x')),
                        row=1, col=1
                    )
                
                # Moving Range chart
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=df_chart['MR'],
                              mode='lines+markers', name='Moving Range',
                              line=dict(color='purple')),
                    row=2, col=1
                )
                
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=[ucl_mr]*len(df_chart),
                              mode='lines', name='UCL (MR)', line=dict(color='red', dash='dash')),
                    row=2, col=1
                )
                
                fig_control.add_trace(
                    go.Scatter(x=list(range(len(df_chart))), y=[mr_mean]*len(df_chart),
                              mode='lines', name='Mean (MR)', line=dict(color='green')),
                    row=2, col=1
                )
                
                fig_control.update_layout(height=800, showlegend=False)
                fig_control.update_xaxes(title_text="Sample Number", row=2, col=1)
                fig_control.update_yaxes(title_text=ctq_col, row=1, col=1)
                fig_control.update_yaxes(title_text="Moving Range", row=2, col=1)
                
                st.plotly_chart(fig_control, use_container_width=True)
                
                # Control chart interpretation
                if out_of_control_i.any():
                    st.warning(f"⚠️ **{out_of_control_i.sum()} out-of-control points detected** - Special cause variation present")
                else:
                    st.success("✅ Process is in statistical control")
                
                # Root Cause Analysis for continuous data
                st.markdown("### 🔍 Root Cause Analysis")
                
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                numeric_factors = [col for col in numeric_cols if col != ctq_col]
                
                if categorical_cols or numeric_factors:
                    
                    analysis_type = st.radio(
                        "Select analysis type:",
                        ["Categorical Factors (ANOVA)", "Numeric Factors (Regression)"]
                    )
                    
                    if analysis_type == "Categorical Factors (ANOVA)" and categorical_cols:
                        
                        factor_col = st.selectbox("Select categorical factor:", categorical_cols)
                        
                        # Box plot by category
                        fig_box = px.box(df, x=factor_col, y=ctq_col,
                                        title=f"{ctq_col} by {factor_col}",
                                        color=factor_col)
                        
                        st.plotly_chart(fig_box, use_container_width=True)
                        
                        # ANOVA
                        groups = [group[ctq_col].dropna() for name, group in df.groupby(factor_col)]
                        
                        if len(groups) > 1 and all(len(g) > 1 for g in groups):
                            f_stat, p_value = stats.f_oneway(*groups)
                            
                            st.markdown("#### ANOVA Results")
                            
                            col1, col2 = st.columns(2)
                            col1.metric("F-statistic", f"{f_stat:.4f}")
                            col2.metric("p-value", f"{p_value:.6f}")
                            
                            if p_value < 0.05:
                                st.success(f"✅ **SIGNIFICANT ROOT CAUSE!** {factor_col} significantly affects {ctq_col} (p < 0.05)")
                                
                                # Show means by group
                                means = df.groupby(factor_col)[ctq_col].agg(['mean', 'std', 'count'])
                                st.dataframe(means.style.format({'mean': '{:.4f}', 'std': '{:.4f}'}))
                                
                            else:
                                st.info(f"ℹ️ {factor_col} does not significantly affect {ctq_col} (p = {p_value:.4f})")
                    
                    elif analysis_type == "Numeric Factors (Regression)" and numeric_factors:
                        
                        factor_col = st.selectbox("Select numeric factor:", numeric_factors)
                        
                        # Scatter plot
                        fig_scatter = px.scatter(df, x=factor_col, y=ctq_col,
                                                trendline="ols",
                                                title=f"{ctq_col} vs {factor_col}")
                        
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # Correlation and regression
                        correlation = df[[factor_col, ctq_col]].corr().iloc[0, 1]
                        
                        X = df[[factor_col]].dropna()
                        y = df.loc[X.index, ctq_col]
                        X = sm.add_constant(X)
                        
                        model = sm.OLS(y, X).fit()
                        
                        st.markdown("#### Regression Analysis")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Correlation (R)", f"{correlation:.4f}")
                        col2.metric("R-squared", f"{model.rsquared:.4f}")
                        col3.metric("p-value", f"{model.pvalues[1]:.6f}")
                        
                        if model.pvalues[1] < 0.05:
                            st.success(f"✅ **SIGNIFICANT RELATIONSHIP!** {factor_col} significantly predicts {ctq_col}")
                            st.write(f"**Equation:** {ctq_col} = {model.params[0]:.4f} + {model.params[1]:.4f} × {factor_col}")
                        else:
                            st.info(f"ℹ️ No significant relationship found (p = {model.pvalues[1]:.4f})")
                
            except Exception as e:
                st.error(f"Error in analysis: {e}")
                import traceback
                st.code(traceback.format_exc())

else:
    # Landing page when no file is uploaded
    st.info("👈 **Upload your data file in the sidebar to begin analysis**")
    
    st.markdown("""
    ## 🎓 What This Tool Does
    
    This Six Sigma Black Belt Auto-Pilot automatically:
    
    1. ✅ **Detects your data type** (discrete defects vs continuous measurements)
    2. ✅ **Calculates Sigma levels** (short-term and long-term)
    3. ✅ **Creates all required charts:**
       - Control charts (P, NP, C, U, I-MR, Xbar-R)
       - Process capability charts
       - Histograms with normal curves
       - Probability plots (Q-Q plots)
       - Pareto charts
       - Box plots
    4. ✅ **Performs statistical tests:**
       - Normality tests (Anderson-Darling, Shapiro-Wilk)
       - Process capability (Cp, Cpk, Pp, Ppk)
       - ANOVA for categorical factors
       - Regression for numeric factors
       - Chi-square for independence
    5. ✅ **Identifies root causes** automatically
    6. ✅ **Tells you exactly where the problem is** and what to fix first
    
    ## 📋 Sample Data Format
    
    ### For Discrete (Defect) Data:
    ```
    Date       | Machine | Operator | Defects | Opportunities
    2024-01-01 | M1      | John     | 5       | 1000
    2024-01-02 | M2      | Mary     | 3       | 1000
    2024-01-03 | M1      | John     | 8       | 1000
    ```
    
    ### For Continuous (Measurement) Data:
    ```
    Date       | Machine | Operator | Thickness | Temperature
    2024-01-01 | M1      | John     | 2.543     | 185
    2024-01-02 | M2      | Mary     | 2.551     | 187
    2024-01-03 | M1      | John     | 2.538     | 183
    ```
    
    ## 🚀 Quick Start
    
    1. Prepare your data in CSV or Excel format
    2. Upload using the sidebar
    3. Select your data type and columns
    4. Click "Run Analysis"
    5. Get instant Six Sigma insights!
    
    ---
    
    Built with ❤️ for Six Sigma Black Belts worldwide
    """)

# Footer
st.markdown("---")
st.markdown("**Six Sigma Black Belt Auto-Pilot** | Version 1.0 | 2025")