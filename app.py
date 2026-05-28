import streamlit as st
import time
import sys
import os
import io
from contextlib import redirect_stdout

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

from src.regular import RegularValidator
from src.livre_contexto import ContextFreeValidator
from src.recursiva import RecursiveValidator
from src.testes import run_tests
from src.bonus_regex import compare_regex_vs_dfa

st.set_page_config(page_title="Formal Validator", page_icon="⚙️", layout="wide")

st.title("⚙️ Formal Language Validator")
st.markdown("### 3-Level Hierarchy ($LR \subsetneq LLC \subsetneq R$)")

if 'lr_val' not in st.session_state:
    st.session_state.lr_val = RegularValidator()
    st.session_state.llc_val = ContextFreeValidator()
    st.session_state.r_val = RecursiveValidator()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Regular (DFA)", 
    "Context-Free (PDA)", 
    "Recursive (TM)", 
    "🧪 Test Suite", 
    "⚡ DFA vs Regex"
])

def render_tester(validator, default_text, tab_name, description):
    st.markdown(f"### **{tab_name} Validator**")
    st.info(description)
    
    input_str = st.text_input(f"Enter string to test:", value=default_text, key=tab_name)
    
    if st.button(f"Validate {tab_name}", type="primary"):
        f = io.StringIO()
        with redirect_stdout(f):
            start_time = time.perf_counter()
            is_accepted, steps = validator.recognize(input_str, verbose=True)
            end_time = time.perf_counter()
        
        calc_time = (end_time - start_time) * 1000
        
        if is_accepted:
            st.success(f"✅ **ACCEPTED** in {steps} steps! (Execution time: {calc_time:.4f} ms)")
        else:
            st.error(f"❌ **REJECTED** at step {steps}. (Execution time: {calc_time:.4f} ms)")
            
        with st.expander("View Execution Steps", expanded=True):
            st.code(f.getvalue(), language="text")

with tab1:
    render_tester(
        st.session_state.lr_val, 
        "LOGIN AUTH REQUEST LOGOUT", 
        "LR",
        "Regex logic: Begins with LOGIN, then AUTH, zero or more REQUEST, ends with LOGOUT."
    )

with tab2:
    render_tester(
        st.session_state.llc_val, 
        "BEGIN BEGIN END END", 
        "LLC",
        "Stack logic: Nested transaction blocks. Every BEGIN needs a matching END."
    )

with tab3:
    render_tester(
        st.session_state.r_val, 
        "OPEN COMMIT CLOSE", 
        "R",
        "Turing Machine logic: Balanced trio of events (OPEN^n COMMIT^n CLOSE^n)."
    )

with tab4:
    st.markdown("### 🧪 Automated Test Suite")
    st.info("Reads the .txt files in the `testes/` folder and validates all strings automatically.")
    
    if st.button("Run All Tests 🚀", type="primary"):
        test_dir = os.path.join(project_root, 'testes')
        
        f = io.StringIO()
        with redirect_stdout(f):
            run_tests(os.path.join(test_dir, 'testes_regular.txt'), st.session_state.lr_val, "Regular Language (DFA)")
            run_tests(os.path.join(test_dir, 'testes_livre_contexto.txt'), st.session_state.llc_val, "Context-Free (PDA)")
            run_tests(os.path.join(test_dir, 'testes_recursiva.txt'), st.session_state.r_val, "Recursive (Turing Machine)")
        
        st.code(f.getvalue(), language="text")

with tab5:
    st.markdown("### ⚡ Performance Comparison: Manual DFA vs Python `re`")
    st.info("Demonstrates why standard library tools are faster (compiled in C), but manual automata are mathematically traceable.")
    
    regex_input = st.text_input("Enter a sequence of logs to stress-test:", value="LOGIN AUTH REQUEST REQUEST REQUEST REQUEST LOGOUT", key="regex_input")
    
    if st.button("Compare Execution", type="primary"):
        f = io.StringIO()
        with redirect_stdout(f):
            compare_regex_vs_dfa(regex_input)
        
        st.code(f.getvalue(), language="text")
