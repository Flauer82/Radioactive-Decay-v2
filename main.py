import streamlit as st
import radioactivedecay as rd
import matplotlib.pyplot as plt
from io import BytesIO

def create_decay_plot(isotope_str, figsize=(20, 16)):
    try:
        # Create initial nuclide
        initial_nuclide = rd.Nuclide(isotope_str)
        
        # Create a new figure with the desired size first
        plt.figure(figsize=figsize)
        
        # Plot decay chain
        fig, ax = initial_nuclide.plot(label_pos=0.66)
        
        # Adjust layout
        plt.tight_layout(pad=3.0)
        
        # Convert plot to PNG image with high resolution
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        plt.close('all')  # Close all figures to free memory
        buf.seek(0)
        
        return buf
    except Exception as e:
        st.error(f"Error: {str(e)}")
        plt.close('all')  # Ensure figures are closed even if there's an error
        return None

def create_evolution_plot(isotope_str, figsize=(20, 10)):
    try:
        # Create inventory
        inv = rd.Inventory({isotope_str: 1.0})
        
        # Create new figure with desired size
        plt.figure(figsize=figsize)
        
        # Create time evolution plot
        fig, ax = inv.plot(1000, 'd', 
                          xscale='log', 
                          yscale='log', 
                          xmin=1, 
                          ymin=1e-8)
        
        # Adjust layout
        plt.tight_layout(pad=2.0)
        
        # Convert to PNG with high resolution
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        plt.close('all')  # Close all figures to free memory
        buf.seek(0)
        
        return buf
    except Exception as e:
        st.error(f"Error: {str(e)}")
        plt.close('all')  # Ensure figures are closed even if there's an error
        return None

def main():
    st.title("Radioactive Decay Chain Visualizer")
    
    # Add description
    st.write("""
    Enter an isotope to visualize its decay chain. The graph shows:
    - Each isotope in the decay chain with its half-life
    - Decay modes connecting parent to daughter nuclides
    - Branching ratios for each decay mode
    """)
    
    # Add input fields
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        isotope = st.text_input("Enter isotope (e.g., U-238, Th-232):", "U-238")
    
    with col2:
        chain_button = st.button("Generate Decay Chain", type="primary")
    
    with col3:
        evolution_button = st.button("Show Decay Evolution", type="secondary")
    
    # Create containers for plots
    chain_container = st.container()
    evolution_container = st.container()
    
    if chain_button and isotope:
        with st.spinner('Generating decay chain...'):
            plot_data = create_decay_plot(isotope)
            if plot_data:
                with chain_container:
                    st.image(plot_data, use_column_width=True)
    
    if evolution_button and isotope:
        with st.spinner('Generating decay evolution plot...'):
            evolution_data = create_evolution_plot(isotope)
            if evolution_data:
                with evolution_container:
                    st.write("### Decay Evolution Over Time")
                    st.image(evolution_data, use_column_width=True)
    
    # Add helpful information
    with st.expander("Usage Tips"):
        st.write("""
        - Enter the isotope in the format 'Element-Mass' (e.g., U-238, Th-232)
        - Click 'Generate Decay Chain' to see the decay pathways
        - Click 'Show Decay Evolution' to see how the amounts of each isotope change over time
        - The decay chain diagram shows all possible decay paths
        - The evolution graph uses logarithmic scales to show changes over time
        
        Try these examples:
        - U-238: Uranium series
        - Th-232: Thorium series
        - Ra-226: Radium decay
        - Rn-222: Radon decay chain
        - Mo-99: Medical isotope
        
        The time evolution graph shows:
        - X-axis: Time in days (logarithmic scale)
        - Y-axis: Relative amounts (logarithmic scale)
        - Different curves for each isotope in the decay chain
        """)

if __name__ == "__main__":
    main()