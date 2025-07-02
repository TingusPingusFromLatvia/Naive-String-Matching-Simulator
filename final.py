import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def naive_string_matching_with_steps(text, pattern):
    """
    Naïve string matching algorithm that returns all steps for visualization
    """
    steps = []
    matches = []
    comparisons = 0
    
    n = len(text)
    m = len(pattern)
    
    for i in range(n - m + 1):
        step_comparisons = []
        current_match = True
        
        for j in range(m):
            comparisons += 1
            char_match = text[i + j] == pattern[j]
            step_comparisons.append({
                'text_pos': i + j,
                'pattern_pos': j,
                'text_char': text[i + j],
                'pattern_char': pattern[j],
                'match': char_match
            })
            
            if not char_match:
                current_match = False
                break
        
        steps.append({
            'start_pos': i,
            'comparisons': step_comparisons,
            'is_match': current_match and len(step_comparisons) == m,
            'total_comparisons': comparisons
        })
        
        if current_match and len(step_comparisons) == m:
            matches.append(i)
    
    return steps, matches, comparisons

def visualize_step(text, pattern, step, step_num):
    """
    Create a visual representation of the current step
    """
    st.subheader(f"Step {step_num + 1}: Checking position {step['start_pos']}")
    
    # Create text display with highlighting
    text_display = ""
    pattern_display = ""
    
    # Build the text display
    for i, char in enumerate(text):
        if any(comp['text_pos'] == i for comp in step['comparisons']):
            # This character is being compared
            comp = next(comp for comp in step['comparisons'] if comp['text_pos'] == i)
            if comp['match']:
                text_display += f"<span style='background-color: #90EE90; padding: 2px;'>{char}</span>"
            else:
                text_display += f"<span style='background-color: #FFB6C1; padding: 2px;'>{char}</span>"
        else:
            text_display += char
    
    # Build the pattern display with alignment
    pattern_position = step['start_pos']
    pattern_display = " " * pattern_position
    
    for j, char in enumerate(pattern):
        if j < len(step['comparisons']):
            comp = step['comparisons'][j]
            if comp['match']:
                pattern_display += f"<span style='background-color: #90EE90; padding: 2px;'>{char}</span>"
            else:
                pattern_display += f"<span style='background-color: #FFB6C1; padding: 2px;'>{char}</span>"
        else:
            pattern_display += char
    
    # Display
    st.markdown("*Text:*")
    st.markdown(f"<div style='font-family: monospace; font-size: 18px;'>{text_display}</div>", unsafe_allow_html=True)
    st.markdown("*Pattern:*")
    st.markdown(f"<div style='font-family: monospace; font-size: 18px;'>{pattern_display}</div>", unsafe_allow_html=True)
    
    # Show comparison details
    st.markdown("*Comparisons:*")
    for comp in step['comparisons']:
        status = "✅ Match" if comp['match'] else "❌ Mismatch"
        st.write(f"Text[{comp['text_pos']}] = '{comp['text_char']}' vs Pattern[{comp['pattern_pos']}] = '{comp['pattern_char']}' → {status}")
    
    if step['is_match']:
        st.success(f"✅ *MATCH FOUND* at position {step['start_pos']}!")
    else:
        st.info("❌ No match at this position, moving to next position.")
    
    st.write(f"*Total comparisons so far:* {step['total_comparisons']}")

def analyze_complexity(text_length, pattern_length):
    """
    Analyze and display complexity information
    """
    st.subheader("Complexity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("*Time Complexity:*")
        st.write("• Best Case: O(n) - pattern found at the beginning")
        st.write("• Average Case: O(n×m)")
        st.write("• Worst Case: O(n×m) - pattern not found or found at the end")
        st.write(f"• Current input: O({text_length} × {pattern_length}) = O({text_length * pattern_length})")
    
    with col2:
        st.markdown("*Space Complexity:*")
        st.write("• O(1) - constant extra space")
        st.markdown("*Characteristics:*")
        st.write("• Simple to implement")
        st.write("• No preprocessing required")
        st.write("• Can be inefficient for large inputs")

def generate_performance_chart():
    """
    Generate a performance comparison chart
    """
    st.subheader("Performance Visualization")
    
    # Generate data for different input sizes
    sizes = [10, 20, 50, 100, 200, 500]
    comparisons_best = sizes  # Best case: O(n)
    comparisons_worst = [n * 5 for n in sizes]  # Worst case with pattern length 5
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, comparisons_best, label='Best Case O(n)', marker='o', color='green')
    ax.plot(sizes, comparisons_worst, label='Worst Case O(n×m)', marker='s', color='red')
    ax.set_xlabel('Text Length')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Naïve String Matching: Best vs Worst Case Performance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Naïve String Matching Simulator", layout="wide")
    
    st.title("🔍 Naïve String Matching Algorithm Simulator")
    st.markdown("*Design and Analysis of Algorithms Project*")
    st.markdown("---")
    
    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    
    # Predefined examples
    examples = {
        "Custom": ("", ""),
        "Simple Example": ("ABAAABCDABABCABCABCDAB", "ABCAB"),
        "DNA Sequence": ("ATCGATCGATCGATCG", "GATC"),
        "Worst Case": ("AAAAAAAAAB", "AAAAB"),
        "Best Case": ("ABCDEFGHIJ", "ABC"),
        "No Match": ("HELLO WORLD", "XYZ")
    }
    
    selected_example = st.sidebar.selectbox("Choose an example:", list(examples.keys()))
    
    if selected_example == "Custom":
        text = st.sidebar.text_input("Enter text:", value="ABAAABCDABABCABCABCDAB")
        pattern = st.sidebar.text_input("Enter pattern:", value="ABCAB")
    else:
        text, pattern = examples[selected_example]
        st.sidebar.text_input("Text:", value=text, disabled=True)
        st.sidebar.text_input("Pattern:", value=pattern, disabled=True)
    
    if not text or not pattern:
        st.warning("Please enter both text and pattern.")
        return
    
    if len(pattern) > len(text):
        st.error("Pattern cannot be longer than text.")
        return
    
    # Run the algorithm
    steps, matches, total_comparisons = naive_string_matching_with_steps(text, pattern)
    
    # Display results summary
    st.header("Results Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Text Length", len(text))
    with col2:
        st.metric("Pattern Length", len(pattern))
    with col3:
        st.metric("Matches Found", len(matches))
    with col4:
        st.metric("Total Comparisons", total_comparisons)
    
    if matches:
        st.success(f"✅ Pattern found at positions: {matches}")
    else:
        st.info("❌ Pattern not found in the text.")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Step-by-Step Visualization", "Algorithm Code", "Complexity Analysis", "Performance Charts"])
    
    with tab1:
        st.header("Step-by-Step Execution")
        
        # Control buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            auto_play = st.button("▶ Auto Play All Steps")
        
        with col2:
            show_all = st.button("📋 Show All Steps")
        
        if auto_play:
            placeholder = st.empty()
            for i, step in enumerate(steps):
                with placeholder.container():
                    visualize_step(text, pattern, step, i)
                    st.markdown("---")
                time.sleep(2)  # Pause between steps
        
        elif show_all:
            for i, step in enumerate(steps):
                with st.expander(f"Step {i + 1}: Position {step['start_pos']} {'✅' if step['is_match'] else '❌'}"):
                    visualize_step(text, pattern, step, i)
        
        else:
            # Step selector
            if steps:
                step_num = st.slider("Select step to visualize:", 0, len(steps) - 1, 0)
                visualize_step(text, pattern, steps[step_num], step_num)
    
    with tab2:
        st.header("Algorithm Implementation")
        st.code('''
def naive_string_matching(text, pattern):
    """
    Naïve String Matching Algorithm
    Time Complexity: O(n × m) where n = len(text), m = len(pattern)
    Space Complexity: O(1)
    """
    matches = []
    n = len(text)
    m = len(pattern)
    
    # Check each possible position in text
    for i in range(n - m + 1):
        # Check if pattern matches at position i
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        
        # If we matched the entire pattern
        if j == m:
            matches.append(i)
    
    return matches

# Example usage
text = "ABAAABCDABABCABCABCDAB"
pattern = "ABCAB"
result = naive_string_matching(text, pattern)
print(f"Pattern found at positions: {result}")
        ''', language='python')
        
        st.markdown("*Algorithm Steps:*")
        st.markdown("""
        1. *Initialize*: Set up variables for text length (n) and pattern length (m)
        2. *Outer Loop*: For each position i from 0 to (n-m)
        3. *Inner Loop*: Compare pattern with text starting at position i
        4. *Character Comparison*: Match characters one by one
        5. *Record Match*: If all characters match, record the position
        6. *Continue*: Move to next position and repeat
        """)
    
    with tab3:
        analyze_complexity(len(text), len(pattern))
        
        # Comparison table
        st.subheader("Algorithm Comparison")
        comparison_data = {
            'Algorithm': ['Naïve', 'KMP', 'Boyer-Moore', 'Rabin-Karp'],
            'Time Complexity': ['O(n×m)', 'O(n+m)', 'O(n/m) best, O(n×m) worst', 'O(n+m) average'],
            'Space Complexity': ['O(1)', 'O(m)', 'O(m)', 'O(1)'],
            'Preprocessing': ['None', 'O(m)', 'O(m+σ)', 'O(m)'],
            'Best Use Case': ['Small patterns', 'General purpose', 'Large alphabets', 'Multiple patterns']
        }
        
        st.dataframe(pd.DataFrame(comparison_data))
    
    with tab4:
        generate_performance_chart()
        
        # Interactive performance calculator
        st.subheader("Performance Calculator")
        calc_col1, calc_col2 = st.columns(2)
        
        with calc_col1:
            calc_text_len = st.number_input("Text Length:", min_value=1, max_value=10000, value=100)
            calc_pattern_len = st.number_input("Pattern Length:", min_value=1, max_value=100, value=5)
        
        with calc_col2:
            best_case = calc_text_len
            worst_case = calc_text_len * calc_pattern_len
            st.metric("Best Case Comparisons", best_case)
            st.metric("Worst Case Comparisons", worst_case)
            st.metric("Efficiency Ratio", f"{worst_case/best_case:.1f}x")

if __name__ == "__main__":
    main()