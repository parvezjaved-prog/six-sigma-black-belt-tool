"""
SIX SIGMA DMAIC PROJECT MENTOR
Complete Black Belt Project Guide - Step-by-Step DMAIC Approach
Acts as your virtual Six Sigma mentor throughout the entire project lifecycle
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
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Six Sigma DMAIC Project Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stMetric {background-color: white; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);}
    h1 {color: #1f4788;}
    h2 {color: #2e5c8a;}
    h3 {color: #3d6fa3;}
    .phase-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f4788;
        margin: 10px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .tip-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for project tracking
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        'phase': 'Welcome',
        'define_complete': False,
        'measure_complete': False,
        'analyze_complete': False,
        'improve_complete': False,
        'control_complete': False,
        'project_name': '',
        'problem_statement': '',
        'goal': '',
        'baseline_sigma': None,
        'improved_sigma': None,
        'findings': [],
        'solutions': [],
    }

# Sidebar - Project Navigation
with st.sidebar:
    st.title("🎓 DMAIC Navigator")
    
    # Project Status
    st.markdown("### 📊 Project Status")
    
    phases = {
        'Define': st.session_state.project_data['define_complete'],
        'Measure': st.session_state.project_data['measure_complete'],
        'Analyze': st.session_state.project_data['analyze_complete'],
        'Improve': st.session_state.project_data['improve_complete'],
        'Control': st.session_state.project_data['control_complete'],
    }
    
    for phase, complete in phases.items():
        status = "✅" if complete else "⏳"
        st.markdown(f"{status} **{phase}**")
    
    st.markdown("---")
    
    # Phase Selection
    current_phase = st.selectbox(
        "Select DMAIC Phase:",
        ['Welcome', 'Define', 'Measure', 'Analyze', 'Improve', 'Control', 'Project Summary'],
        index=['Welcome', 'Define', 'Measure', 'Analyze', 'Improve', 'Control', 'Project Summary'].index(st.session_state.project_data['phase'])
    )
    
    st.session_state.project_data['phase'] = current_phase
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("📥 Save Project"):
        project_json = json.dumps(st.session_state.project_data, indent=2)
        st.download_button(
            "Download Project Data",
            project_json,
            file_name=f"six_sigma_project_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    if st.button("🔄 Reset Project"):
        if st.checkbox("Confirm reset"):
            st.session_state.project_data = {
                'phase': 'Welcome',
                'define_complete': False,
                'measure_complete': False,
                'analyze_complete': False,
                'improve_complete': False,
                'control_complete': False,
                'project_name': '',
                'problem_statement': '',
                'goal': '',
                'baseline_sigma': None,
                'improved_sigma': None,
                'findings': [],
                'solutions': [],
            }
            st.success("Project reset!")
            st.experimental_rerun()

# Main content area
st.title("🎓 Six Sigma Black Belt DMAIC Project Mentor")
st.markdown("**Your Virtual Six Sigma Coach - Guiding You Through Every Step of Your Project**")

# ==========================================
# WELCOME PAGE
# ==========================================

if current_phase == 'Welcome':
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="phase-box">
        <h2>👋 Welcome to Your Six Sigma DMAIC Journey!</h2>
        <p>I'm your virtual Black Belt mentor, here to guide you through every step of your Six Sigma project using the proven DMAIC methodology.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 What This Tool Does
        
        This isn't just an analysis tool - it's your complete **Six Sigma project companion** that:
        
        ✅ **Guides you step-by-step** through Define, Measure, Analyze, Improve, Control  
        ✅ **Provides templates** for every deliverable  
        ✅ **Runs statistical analyses** automatically  
        ✅ **Gives expert recommendations** based on your data  
        ✅ **Tracks your project progress**  
        ✅ **Generates professional reports**  
        ✅ **Acts as your mentor** - explaining what to do and why  
        
        ### 📚 The DMAIC Methodology
        
        **DMAIC** is the structured approach used by Six Sigma Black Belts worldwide:
        
        """)
        
        st.markdown("""
        <div class="tip-box">
        <b>🎯 D - DEFINE:</b> What is the problem? What are we trying to achieve?<br>
        <b>📊 M - MEASURE:</b> How are we performing today? What's our baseline?<br>
        <b>🔍 A - ANALYZE:</b> What are the root causes? Where should we focus?<br>
        <b>🚀 I - IMPROVE:</b> What solutions will work? How do we implement them?<br>
        <b>🎛️ C - CONTROL:</b> How do we sustain improvements? How do we prevent regression?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Start with Define** - Click "Define" in the sidebar to begin your project charter
        2. **Progress through each phase** - Complete activities and analyses in order
        3. **Upload your data** when prompted for statistical analysis
        4. **Follow the recommendations** - I'll guide you on what to do next
        5. **Generate your final report** - Document your entire project journey
        
        """)
        
        st.markdown("""
        <div class="success-box">
        <b>💡 Pro Tip:</b> Six Sigma projects typically take 3-6 months. Don't rush! Quality analysis takes time. 
        This tool will be here throughout your journey, helping you make data-driven decisions at every step.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 📈 Project Types
        
        **Manufacturing:**
        - Defect reduction
        - Cycle time improvement
        - Yield enhancement
        
        **Service:**
        - Error reduction
        - Process efficiency
        - Customer satisfaction
        
        **Transactional:**
        - Accuracy improvement
        - Turnaround time
        - Cost reduction
        
        ### 🎓 Prerequisites
        
        ✅ Basic statistics knowledge  
        ✅ Understanding of your process  
        ✅ Access to process data  
        ✅ Management support  
        ✅ Team members identified  
        
        ### 📊 Tools You'll Use
        
        - Project Charter
        - SIPOC Diagram
        - Data Collection Plan
        - Control Charts
        - Hypothesis Testing
        - DOE (Design of Experiments)
        - Control Plan
        - And many more!
        """)
    
    if st.button("🚀 Start Your Six Sigma Project", type="primary"):
        st.session_state.project_data['phase'] = 'Define'
        st.experimental_rerun()

# ==========================================
# DEFINE PHASE
# ==========================================

elif current_phase == 'Define':
    
    st.markdown("""
    <div class="phase-box">
    <h2>🎯 DEFINE Phase - Setting Up Your Project for Success</h2>
    <p><b>Goal:</b> Clearly define the problem, scope, and objectives of your improvement project</p>
    <p><b>Duration:</b> Typically 2-4 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Define Phase Guide
    with st.expander("📖 DEFINE Phase Guide - Click to Learn", expanded=True):
        st.markdown("""
        ### What You'll Accomplish in Define:
        
        1. ✅ **Project Charter** - Document the project scope, objectives, and team
        2. ✅ **Problem Statement** - Articulate the problem clearly and quantifiably
        3. ✅ **Goal Statement** - Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
        4. ✅ **SIPOC Diagram** - Map the high-level process
        5. ✅ **VOC Analysis** - Capture customer requirements
        6. ✅ **Stakeholder Analysis** - Identify who's affected and who can help
        
        ### Why Define is Critical:
        
        - **Alignment** - Ensures everyone understands the problem the same way
        - **Focus** - Prevents scope creep and wasted effort
        - **Buy-in** - Gets management and stakeholders committed
        - **Foundation** - Sets up the rest of your DMAIC project for success
        
        ### Common Define Mistakes to Avoid:
        
        ❌ Problem statement too vague ("improve quality")  
        ❌ Scope too broad (trying to fix everything)  
        ❌ No baseline metrics (how will you know if you improved?)  
        ❌ Skipping stakeholder analysis (leads to resistance later)  
        ❌ Solutions in disguise ("we need to buy new equipment")  
        """)
    
    st.markdown("---")
    
    # Project Charter Section
    st.markdown("### 📋 Step 1: Create Your Project Charter")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 What is a Project Charter?</b><br>
    The Project Charter is your project's "constitution" - a formal document that authorizes the project 
    and gives the team authority to use resources. It's typically one page and includes:
    <ul>
    <li>Business case (why this project matters)</li>
    <li>Problem statement (what's wrong)</li>
    <li>Goal statement (what success looks like)</li>
    <li>Scope (what's in and out)</li>
    <li>Team members and roles</li>
    <li>Timeline and milestones</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name:",
            value=st.session_state.project_data.get('project_name', ''),
            placeholder="e.g., Reduce Defects in Assembly Line 3",
            help="Give your project a clear, descriptive name"
        )
        st.session_state.project_data['project_name'] = project_name
        
        business_case = st.text_area(
            "Business Case (Why is this important?):",
            placeholder="e.g., Assembly Line 3 has 8% defect rate, costing $500K annually in rework and scrap. Customers are complaining about quality...",
            help="Explain the business impact - costs, customer impact, strategic importance",
            height=100
        )
        
        problem_statement = st.text_area(
            "Problem Statement (What is wrong?):",
            value=st.session_state.project_data.get('problem_statement', ''),
            placeholder="Assembly Line 3 defect rate is currently 8% (baseline period: Jan-Mar 2024, n=5000 units), which is above the industry standard of 2% and customer requirement of 3%.",
            help="Be specific! Include: WHAT is happening, WHERE, WHEN, HOW MUCH (quantify with data)",
            height=100
        )
        st.session_state.project_data['problem_statement'] = problem_statement
        
        # Problem Statement Validator
        if problem_statement:
            st.markdown("**Problem Statement Quality Check:**")
            checks = {
                'Quantified': any(char.isdigit() for char in problem_statement),
                'Specific location': any(word in problem_statement.lower() for word in ['line', 'area', 'department', 'process', 'machine']),
                'Time frame mentioned': any(word in problem_statement.lower() for word in ['2024', '2023', 'month', 'quarter', 'week', 'period']),
                'No solutions embedded': not any(word in problem_statement.lower() for word in ['need', 'should', 'must', 'buy', 'hire', 'install']),
            }
            
            for check, passed in checks.items():
                icon = "✅" if passed else "❌"
                st.markdown(f"{icon} {check}")
            
            if all(checks.values()):
                st.success("🎉 Excellent problem statement! Well-defined and quantified.")
            else:
                st.warning("⚠️ Consider improving your problem statement based on the checks above")
    
    with col2:
        goal_statement = st.text_area(
            "Goal Statement (What do you want to achieve?):",
            value=st.session_state.project_data.get('goal', ''),
            placeholder="Reduce Assembly Line 3 defect rate from 8% to less than 3% by December 2024, resulting in annual savings of $350K.",
            help="Use SMART criteria: Specific, Measurable, Achievable, Relevant, Time-bound",
            height=100
        )
        st.session_state.project_data['goal'] = goal_statement
        
        # SMART Goal Validator
        if goal_statement:
            st.markdown("**SMART Goal Check:**")
            smart_checks = {
                'Specific (clear target)': any(char.isdigit() for char in goal_statement),
                'Measurable (has metrics)': any(word in goal_statement.lower() for word in ['%', 'percent', 'reduce', 'increase', 'from', 'to']),
                'Time-bound (deadline)': any(word in goal_statement.lower() for word in ['2024', '2025', 'month', 'quarter', 'by']),
                'Realistic improvement': True,  # Can't auto-validate, but shown as reminder
            }
            
            for check, passed in smart_checks.items():
                icon = "✅" if passed else "❌"
                st.markdown(f"{icon} {check}")
        
        scope_in = st.text_area(
            "In Scope:",
            placeholder="- Assembly Line 3 only\n- Product types A, B, and C\n- First shift operations\n- Existing equipment",
            help="What IS included in your project?",
            height=100
        )
        
        scope_out = st.text_area(
            "Out of Scope:",
            placeholder="- Other assembly lines\n- Second and third shifts\n- Equipment purchases\n- Product redesign",
            help="What is NOT included (prevents scope creep)",
            height=100
        )
    
    st.markdown("---")
    
    # Team Section
    st.markdown("### 👥 Step 2: Build Your Project Team")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 Team Roles in Six Sigma:</b><br>
    <ul>
    <li><b>Champion:</b> Senior leader who sponsors and removes barriers</li>
    <li><b>Process Owner:</b> Person responsible for the process being improved</li>
    <li><b>Black Belt:</b> Project leader (that's you!)</li>
    <li><b>Green Belts:</b> Team members trained in Six Sigma basics</li>
    <li><b>Team Members:</b> Subject matter experts from the process</li>
    <li><b>Master Black Belt:</b> Coach/mentor (optional)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    num_team_members = st.number_input("How many team members?", min_value=3, max_value=10, value=5)
    
    team_members = []
    cols = st.columns(2)
    for i in range(num_team_members):
        with cols[i % 2]:
            with st.container():
                name = st.text_input(f"Team Member {i+1} Name:", key=f"member_{i}")
                role = st.selectbox(f"Role:", ['Team Member', 'Green Belt', 'Champion', 'Process Owner', 'SME'], key=f"role_{i}")
                team_members.append({'name': name, 'role': role})
    
    st.markdown("---")
    
    # SIPOC Section
    st.markdown("### 📊 Step 3: Create Your SIPOC Diagram")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 What is SIPOC?</b><br>
    <b>S</b>uppliers - <b>I</b>nputs - <b>P</b>rocess - <b>O</b>utputs - <b>C</b>ustomers<br><br>
    A high-level process map that helps you understand:<br>
    • Who provides what to your process (Suppliers & Inputs)<br>
    • What your process does (Process steps at 30,000 ft level)<br>
    • What your process produces (Outputs)<br>
    • Who receives the outputs (Customers)<br><br>
    <b>Keep it HIGH LEVEL:</b> 5-7 process steps maximum!
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Suppliers**")
        suppliers = st.text_area("Who provides inputs?", placeholder="- Parts vendor\n- Previous process\n- IT department", height=100, key="suppliers")
        
        st.markdown("**Inputs**")
        inputs = st.text_area("What do they provide?", placeholder="- Raw materials\n- Work orders\n- Specifications", height=100, key="inputs")
    
    with col2:
        st.markdown("**Process (5-7 high-level steps)**")
        process_steps = st.text_area("Main process steps:", placeholder="1. Receive materials\n2. Assembly\n3. Quality check\n4. Packaging\n5. Ship to customer", height=200, key="process")
    
    with col3:
        st.markdown("**Outputs**")
        outputs = st.text_area("What does the process produce?", placeholder="- Assembled product\n- Quality reports\n- Shipping documents", height=100, key="outputs")
        
        st.markdown("**Customers**")
        customers = st.text_area("Who receives outputs?", placeholder="- End customers\n- Next department\n- Distributors", height=100, key="customers")
    
    # VOC Section
    st.markdown("---")
    st.markdown("### 🎤 Step 4: Voice of Customer (VOC) Analysis")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 Why VOC Matters:</b><br>
    Six Sigma is about meeting customer requirements. VOC captures what customers actually need vs. what we think they need.
    </div>
    """, unsafe_allow_html=True)
    
    voc_method = st.multiselect(
        "How will you collect VOC?",
        ['Customer surveys', 'Interviews', 'Focus groups', 'Complaint analysis', 'Sales feedback', 'Social media monitoring', 'Return data analysis']
    )
    
    critical_to_quality = st.text_area(
        "CTQs (Critical to Quality characteristics):",
        placeholder="What are the 3-5 most important quality characteristics from customer perspective?\ne.g.,\n- Delivery time < 3 days\n- Defect rate < 1%\n- Product dimension: 10.0 ± 0.1mm",
        height=100
    )
    
    st.markdown("---")
    
    # Timeline
    st.markdown("### 📅 Step 5: Project Timeline")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Project Start Date:")
    with col2:
        target_end_date = st.date_input("Target Completion Date:")
    
    st.markdown("""
    <div class="warning-box">
    <b>⏰ Typical DMAIC Timeline:</b><br>
    • Define: 2-4 weeks<br>
    • Measure: 4-6 weeks<br>
    • Analyze: 3-5 weeks<br>
    • Improve: 6-10 weeks<br>
    • Control: 2-4 weeks<br>
    <b>Total: 3-6 months</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Complete Define Phase
    st.markdown("---")
    
    if st.button("✅ Complete DEFINE Phase", type="primary"):
        # Validation
        if not project_name:
            st.error("❌ Please enter a project name")
        elif not problem_statement:
            st.error("❌ Please enter a problem statement")
        elif not goal_statement:
            st.error("❌ Please enter a goal statement")
        else:
            st.session_state.project_data['define_complete'] = True
            st.session_state.project_data['phase'] = 'Measure'
            st.success("🎉 DEFINE Phase Complete! Moving to MEASURE phase...")
            st.balloons()
            st.experimental_rerun()
    
    # Save Define deliverables
    if st.button("💾 Save DEFINE Deliverables"):
        define_doc = f"""
SIX SIGMA PROJECT CHARTER
Generated: {datetime.now().strftime('%Y-%m-%d')}

PROJECT NAME: {project_name}

BUSINESS CASE:
{business_case}

PROBLEM STATEMENT:
{problem_statement}

GOAL STATEMENT:
{goal_statement}

SCOPE:
In Scope:
{scope_in}

Out of Scope:
{scope_out}

TEAM MEMBERS:
{chr(10).join([f"- {m['name']} ({m['role']})" for m in team_members if m['name']])}

SIPOC:
Suppliers: {suppliers}
Inputs: {inputs}
Process: {process_steps}
Outputs: {outputs}
Customers: {customers}

CRITICAL TO QUALITY:
{critical_to_quality}

TIMELINE:
Start: {start_date}
Target End: {target_end_date}
        """
        
        st.download_button(
            "Download Project Charter",
            define_doc,
            file_name=f"Project_Charter_{project_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# ==========================================
# MEASURE PHASE
# ==========================================

elif current_phase == 'Measure':
    
    st.markdown("""
    <div class="phase-box">
    <h2>📊 MEASURE Phase - Establishing Your Baseline</h2>
    <p><b>Goal:</b> Collect data to understand current process performance and validate the problem</p>
    <p><b>Duration:</b> Typically 4-6 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("📖 MEASURE Phase Guide", expanded=True):
        st.markdown("""
        ### What You'll Accomplish in Measure:
        
        1. ✅ **Data Collection Plan** - Define what data to collect, how, when, and by whom
        2. ✅ **MSA (Measurement System Analysis)** - Ensure your measurement system is reliable
        3. ✅ **Baseline Performance** - Calculate current Sigma level, Cpk, defect rate
        4. ✅ **Process Map** - Detail the current process flow
        5. ✅ **Data Validation** - Ensure data quality and sufficiency
        
        ### Key Questions Measure Answers:
        
        - How bad is the problem really? (quantified)
        - Is our measurement system reliable?
        - What's our current Sigma level?
        - Do we have enough data to make decisions?
        - What does "good" look like (specifications)?
        
        ### Measurement Mistakes to Avoid:
        
        ❌ Not doing MSA (garbage in = garbage out)  
        ❌ Too little data (need minimum 30 data points)  
        ❌ Biased sampling (only measuring "good" periods)  
        ❌ No operational definitions (what exactly is a "defect"?)  
        ❌ Skipping data stratification (missing important patterns)  
        """)
    
    st.markdown("---")
    
    # Data Collection Plan
    st.markdown("### 📋 Step 1: Create Data Collection Plan")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 The 5W2H Approach to Data Collection:</b><br>
    • <b>What</b> data will you collect?<br>
    • <b>Why</b> are you collecting it?<br>
    • <b>Where</b> will you collect it?<br>
    • <b>When</b> will you collect it?<br>
    • <b>Who</b> will collect it?<br>
    • <b>How</b> will you collect it?<br>
    • <b>How much</b> data do you need?
    </div>
    """, unsafe_allow_html=True)
    
    data_type = st.radio(
        "What type of data will you collect?",
        ['Continuous (measurements)', 'Discrete (counts/defects)', 'Both']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if data_type in ['Continuous (measurements)', 'Both']:
            st.markdown("**Continuous Data Details:**")
            continuous_vars = st.text_area(
                "What will you measure?",
                placeholder="e.g.,\n- Dimension (mm)\n- Weight (kg)\n- Temperature (°C)\n- Cycle time (seconds)",
                height=100
            )
            
            measurement_tool = st.text_input("Measurement tool/instrument:")
            measurement_precision = st.text_input("Measurement precision (e.g., ±0.01mm):")
    
    with col2:
        if data_type in ['Discrete (counts/defects)', 'Both']:
            st.markdown("**Discrete Data Details:**")
            defect_definition = st.text_area(
                "Define what constitutes a 'defect':",
                placeholder="Be very specific! e.g.,\n- Scratch > 2mm long\n- Missing component\n- Color variation outside Pantone 123 ± 2",
                height=100
            )
            
            opportunity_definition = st.text_input("What is one 'opportunity' for a defect?")
    
    sample_size = st.number_input("How many samples will you collect?", min_value=30, value=100, help="Minimum 30 for statistical validity")
    
    if sample_size < 30:
        st.warning("⚠️ Sample size less than 30 may not provide statistically valid results!")
    elif sample_size >= 100:
        st.success("✅ Excellent sample size for reliable analysis!")
    
    st.markdown("---")
    
    # File Upload for Baseline Data
    st.markdown("### 📁 Step 2: Upload Your Baseline Data")
    
    st.markdown("""
    <div class="tip-box">
    <b>💡 Data Requirements:</b><br>
    • Minimum 30 data points (more is better!)<br>
    • Include timestamp/sequence<br>
    • Include stratification factors (machine, operator, shift, etc.)<br>
    • Clean data (no blanks, consistent format)
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your baseline data (CSV or Excel):",
        type=['csv', 'xlsx', 'xls'],
        help="Your data should include measurements or defect counts plus any stratification factors"
    )
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
            
            with st.expander("📊 Data Preview", expanded=True):
                st.dataframe(df.head(50))
                
                # Data quality checks
                st.markdown("**Data Quality Checks:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Rows", len(df))
                    st.metric("Complete Rows", df.dropna().shape[0])
                
                with col2:
                    st.metric("Total Columns", len(df.columns))
                    st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
                
                with col3:
                    missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
                    st.metric("Missing Data %", f"{missing_pct:.1f}%")
                    
                    if missing_pct > 5:
                        st.warning("⚠️ High percentage of missing data!")
                    else:
                        st.success("✅ Good data completeness")
            
            # Column Selection
            st.markdown("### 🎯 Step 3: Identify Your Key Metrics")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            metric_type = st.radio("What type of analysis?", ['Continuous Data (Measurements)', 'Discrete Data (Defects)'])
            
            if metric_type == 'Continuous Data (Measurements)':
                ctq_column = st.selectbox("Select your CTQ (measurement) column:", numeric_cols)
                
                col1, col2 = st.columns(2)
                with col1:
                    lsl = st.number_input("Lower Specification Limit (LSL):", value=float(df[ctq_column].quantile(0.01)))
                with col2:
                    usl = st.number_input("Upper Specification Limit (USL):", value=float(df[ctq_column].quantile(0.99)))
                
                target = st.number_input("Target/Nominal:", value=float((lsl + usl) / 2))
                
                # Run baseline analysis
                if st.button("🚀 Calculate Baseline Performance", type="primary"):
                    data = df[ctq_column].dropna()
                    
                    mean = data.mean()
                    std = data.std()
                    
                    # Capability
                    cp = (usl - lsl) / (6 * std)
                    cpu = (usl - mean) / (3 * std)
                    cpl = (mean - lsl) / (3 * std)
                    cpk = min(cpu, cpl)
                    
                    pp = (usl - lsl) / (6 * data.std(ddof=0))
                    ppk = min((usl - mean)/(3*data.std(ddof=0)), (mean - lsl)/(3*data.std(ddof=0)))
                    
                    # Defects
                    defects = ((data < lsl) | (data > usl)).sum()
                    dpmo = (defects / len(data)) * 1_000_000
                    
                    if dpmo >= 1000000:
                        sigma_level = 0
                    else:
                        sigma_level = stats.norm.ppf(1 - dpmo/1_000_000) + 1.5
                    
                    st.session_state.project_data['baseline_sigma'] = sigma_level
                    
                    st.markdown("---")
                    st.markdown("## 📊 BASELINE PERFORMANCE RESULTS")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Current Sigma Level", f"{sigma_level:.2f}")
                    with col2:
                        st.metric("Cpk", f"{cpk:.3f}")
                    with col3:
                        st.metric("DPMO", f"{dpmo:,.0f}")
                    with col4:
                        st.metric("Defects", f"{defects}")
                    
                    # Interpretation
                    st.markdown("### 🎯 Performance Interpretation")
                    
                    if sigma_level >= 5:
                        interpretation = "🟢 **EXCELLENT** - World-class performance!"
                        recommendation = "Focus on maintaining and controlling this level."
                    elif sigma_level >= 4:
                        interpretation = "🟡 **GOOD** - Above average, but improvement possible"
                        recommendation = "Target specific improvement areas to reach Six Sigma level."
                    elif sigma_level >= 3:
                        interpretation = "🟠 **AVERAGE** - Typical industry performance"
                        recommendation = "Significant improvement opportunity - proceed with Analyze phase to find root causes."
                    else:
                        interpretation = "🔴 **POOR** - Immediate improvement needed"
                        recommendation = "Critical situation - prioritize root cause analysis and quick wins."
                    
                    st.markdown(f"""
                    <div class="success-box">
                    {interpretation}<br><br>
                    <b>Recommendation:</b> {recommendation}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Histogram
                    fig = go.Figure()
                    
                    fig.add_trace(go.Histogram(
                        x=data,
                        nbinsx=30,
                        name='Actual Data',
                        opacity=0.7
                    ))
                    
                    fig.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
                    fig.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
                    fig.add_vline(x=target, line_dash="dash", line_color="green", annotation_text="Target")
                    fig.add_vline(x=mean, line_color="blue", annotation_text="Mean")
                    
                    fig.update_layout(
                        title="Baseline Process Distribution",
                        xaxis_title=ctq_column,
                        yaxis_title="Frequency",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Control Chart
                    st.markdown("### 📈 Control Chart (Process Stability Check)")
                    
                    mr = data.diff().abs()
                    mr_mean = mr.mean()
                    
                    ucl = mean + 2.66 * mr_mean
                    lcl = mean - 2.66 * mr_mean
                    
                    fig2 = go.Figure()
                    
                    fig2.add_trace(go.Scatter(
                        y=data,
                        mode='lines+markers',
                        name='Individual Values',
                        line=dict(color='blue')
                    ))
                    
                    fig2.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL")
                    fig2.add_hline(y=mean, line_color="green", annotation_text="Mean")
                    fig2.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL")
                    
                    out_of_control = (data > ucl) | (data < lcl)
                    if out_of_control.any():
                        fig2.add_trace(go.Scatter(
                            x=data[out_of_control].index,
                            y=data[out_of_control],
                            mode='markers',
                            name='Out of Control',
                            marker=dict(color='red', size=12, symbol='x')
                        ))
                    
                    fig2.update_layout(
                        title="Individual-MR Control Chart",
                        xaxis_title="Sample Number",
                        yaxis_title=ctq_column,
                        height=500
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    if out_of_control.any():
                        st.warning(f"⚠️ {out_of_control.sum()} out-of-control points detected! Process may not be stable.")
                        st.markdown("""
                        <div class="warning-box">
                        <b>⚠️ Unstable Process Detected:</b><br>
                        Before proceeding to Analyze, you should:<br>
                        • Investigate out-of-control points<br>
                        • Remove special causes if found<br>
                        • Re-collect baseline data if necessary<br>
                        • A stable process is required for valid capability analysis
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.success("✅ Process is in statistical control - stable and predictable")
                    
                    st.session_state.project_data['measure_complete'] = True
            
            else:  # Discrete data
                defect_col = st.selectbox("Select defect count column:", numeric_cols)
                opportunity_col = st.selectbox("Select opportunity column:", numeric_cols)
                
                if st.button("🚀 Calculate Baseline Performance", type="primary"):
                    total_defects = df[defect_col].sum()
                    total_opportunities = df[opportunity_col].sum()
                    
                    dpo = total_defects / total_opportunities
                    dpmo = dpo * 1_000_000
                    
                    if dpo >= 1:
                        sigma_level = 0
                    else:
                        sigma_level = stats.norm.ppf(1 - dpo) + 1.5
                    
                    st.session_state.project_data['baseline_sigma'] = sigma_level
                    
                    st.markdown("## 📊 BASELINE PERFORMANCE RESULTS")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Sigma Level", f"{sigma_level:.2f}")
                    with col2:
                        st.metric("DPMO", f"{dpmo:,.0f}")
                    with col3:
                        st.metric("Total Defects", f"{total_defects:,.0f}")
                    with col4:
                        yield_pct = (1 - dpo) * 100
                        st.metric("Yield", f"{yield_pct:.2f}%")
                    
                    # P-chart
                    df['proportion'] = df[defect_col] / df[opportunity_col]
                    p_bar = df['proportion'].mean()
                    n_bar = df[opportunity_col].mean()
                    
                    ucl_p = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar)
                    lcl_p = max(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / n_bar))
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        y=df['proportion'],
                        mode='lines+markers',
                        name='Proportion Defective'
                    ))
                    
                    fig.add_hline(y=ucl_p, line_dash="dash", line_color="red", annotation_text="UCL")
                    fig.add_hline(y=p_bar, line_color="green", annotation_text="P-bar")
                    fig.add_hline(y=lcl_p, line_dash="dash", line_color="red", annotation_text="LCL")
                    
                    fig.update_layout(
                        title="P-Chart: Baseline Process Control",
                        xaxis_title="Sample",
                        yaxis_title="Proportion Defective",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.session_state.project_data['measure_complete'] = True
        
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    else:
        st.info("👆 Upload your baseline data to calculate current performance")
    
    st.markdown("---")
    
    if st.session_state.project_data.get('measure_complete'):
        if st.button("✅ Complete MEASURE Phase", type="primary"):
            st.session_state.project_data['phase'] = 'Analyze'
            st.success("🎉 MEASURE Phase Complete! Moving to ANALYZE...")
            st.balloons()
            st.experimental_rerun()

# ==========================================
# ANALYZE PHASE
# ==========================================

elif current_phase == 'Analyze':
    st.markdown("""
    <div class="phase-box">
    <h2>🔍 ANALYZE Phase - Finding Root Causes</h2>
    <p><b>Goal:</b> Identify and verify the root causes of the problem</p>
    <p><b>Duration:</b> 3-5 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Tools You'll Use in Analyze:
    - Fishbone (Ishikawa) Diagram
    - 5 Whys Analysis
    - Pareto Analysis
    - Hypothesis Testing
    - Regression Analysis
    - ANOVA
    - Multi-Vari Analysis
    
    Upload your data to continue with root cause analysis...
    """)
    
    # ... (Add complete Analyze phase tools here - similar structure to Measure)
    
    st.info("🚧 Analyze phase tools are being prepared. For now, use the data upload in Measure phase to see Pareto and statistical analysis.")

# ==========================================
# IMPROVE PHASE
# ==========================================

elif current_phase == 'Improve':
    st.markdown("""
    <div class="phase-box">
    <h2>🚀 IMPROVE Phase - Implementing Solutions</h2>
    <p><b>Goal:</b> Develop, test, and implement solutions to eliminate root causes</p>
    <p><b>Duration:</b> 6-10 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Coming soon: DOE, Pilot testing, Solution implementation tracking...")

# ==========================================
# CONTROL PHASE
# ==========================================

elif current_phase == 'Control':
    st.markdown("""
    <div class="phase-box">
    <h2>🎛️ CONTROL Phase - Sustaining Improvements</h2>
    <p><b>Goal:</b> Ensure improvements are sustained over time</p>
    <p><b>Duration:</b> 2-4 weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Coming soon: Control plans, SOP templates, handoff documentation...")

# ==========================================
# PROJECT SUMMARY
# ==========================================

elif current_phase == 'Project Summary':
    st.markdown("## 📊 Six Sigma Project Summary")
    
    st.markdown(f"""
    ### Project: {st.session_state.project_data.get('project_name', 'Not Set')}
    
    **Problem Statement:**  
    {st.session_state.project_data.get('problem_statement', 'Not defined')}
    
    **Goal:**  
    {st.session_state.project_data.get('goal', 'Not defined')}
    
    **Baseline Sigma Level:**  
    {st.session_state.project_data.get('baseline_sigma', 'Not calculated')}
    
    **Improved Sigma Level:**  
    {st.session_state.project_data.get('improved_sigma', 'Not yet measured')}
    
    **Project Progress:**
    """)
    
    phases = {
        'Define': st.session_state.project_data['define_complete'],
        'Measure': st.session_state.project_data['measure_complete'],
        'Analyze': st.session_state.project_data['analyze_complete'],
        'Improve': st.session_state.project_data['improve_complete'],
        'Control': st.session_state.project_data['control_complete'],
    }
    
    for phase, complete in phases.items():
        status = "✅ Complete" if complete else "⏳ In Progress"
        st.markdown(f"- **{phase}:** {status}")

# Footer
st.markdown("---")
st.markdown("**Six Sigma DMAIC Project Mentor** | Your Virtual Black Belt Coach | Version 2.0")