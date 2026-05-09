import streamlit as st

def render_header():
    # Premium Dark Mode Header - Fixed at Top
    banner_html = """
    <div style="position: fixed; top: 0; left: 0; right: 0; z-index: 99999; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
        <div style="background-color: #111; padding: 4px 20px; font-size: 12px; color: #888; display: flex; align-items: center; border-bottom: 1px solid #333; flex-wrap: wrap;">
            <i class="fa-solid fa-flag-usa" style="color: #b31942; margin-right: 8px;"></i>
            <span>An official website of the NexusRAG Hackathon Government Division</span>
        </div>
        <div style="background-color: #1E1E1E; padding: 15px 20px; color: white; border-bottom: 1px solid #333; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <h1 style="margin: 0; font-size: clamp(18px, 4vw, 24px); font-family: 'Arial', sans-serif; color: #FAFAFA; white-space: nowrap;">
                <i class="fa-solid fa-building-columns" style="margin-right: 10px; color: #FF9800;"></i> NexusRAG Platform
            </h1>
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                <a href="/" target="_self" style="color: #FAFAFA; text-decoration: none; font-weight: bold; font-family: 'Arial', sans-serif; font-size: 16px; transition: color 0.2s;" onmouseover="this.style.color='#FF9800'" onmouseout="this.style.color='#FAFAFA'">
                    <i class="fa-solid fa-house" style="margin-right: 6px; color: #FF9800;"></i>Home
                </a>
                <a href="/Dataset" target="_self" style="color: #FAFAFA; text-decoration: none; font-weight: bold; font-family: 'Arial', sans-serif; font-size: 16px; transition: color 0.2s;" onmouseover="this.style.color='#FF9800'" onmouseout="this.style.color='#FAFAFA'">
                    <i class="fa-solid fa-database" style="margin-right: 6px; color: #FF9800;"></i>Dataset
                </a>
                <a href="/Workflow" target="_self" style="color: #FAFAFA; text-decoration: none; font-weight: bold; font-family: 'Arial', sans-serif; font-size: 16px; transition: color 0.2s;" onmouseover="this.style.color='#FF9800'" onmouseout="this.style.color='#FAFAFA'">
                    <i class="fa-solid fa-diagram-project" style="margin-right: 6px; color: #FF9800;"></i>Workflow
                </a>
            </div>
        </div>
    </div>
    <div style="height: 90px;"></div> <!-- Spacer to prevent content overlap -->
    """
    st.markdown(banner_html, unsafe_allow_html=True)

def render_footer():
    # Premium Dark Mode Footer
    footer_html = """
    <div style="background-color: #111; padding: 30px 20px; margin-top: 50px; border-top: 1px solid #333; color: #888; font-family: 'Arial', sans-serif; font-size: 14px;">
        <div style="display: flex; justify-content: space-between; max-width: 1200px; margin: 0 auto; flex-wrap: wrap; gap: 20px;">
            <div>
                <strong style="color: #FFF;">NexusRAG Platform</strong><br>
                NexusRAG Hackathon Division<br>
                TigerGraph Integration
            </div>
            <div>
                <a href="#" style="color: #FF9800; text-decoration: none; margin-right: 15px;">Privacy Policy</a>
                <a href="#" style="color: #FF9800; text-decoration: none; margin-right: 15px;">Accessibility</a>
                <a href="https://github.com/tigergraph/graphrag" style="color: #FF9800; text-decoration: none;">GitHub Repository</a>
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
