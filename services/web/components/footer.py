import streamlit as st


def render_footer():
    """푸터 렌더링"""
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### Edu Agents")
        st.markdown("AI-powered education platform")

    with col2:
        st.markdown("**Company**")
        st.markdown("About")
        st.markdown("Contact")
        st.markdown("Careers")

    with col3:
        st.markdown("**Resources**")
        st.markdown("Blog")
        st.markdown("Documentation")
        st.markdown("Support")

    with col4:
        st.markdown("**Legal**")
        st.markdown("Privacy Policy")
        st.markdown("Terms of Service")
        st.markdown("Cookie Policy")

    st.markdown("---")

    st.markdown(
        "<p style='text-align: center; color: #888;'>© 2025 Edu Agents</p>",
        unsafe_allow_html=True,
    )
