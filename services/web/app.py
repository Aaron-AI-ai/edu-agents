import streamlit as st

from components.header import render_header
from components.sections import (
    render_features_section,
    render_hero_section,
    render_partners_section,
    render_testimonials_section,
)
from components.footer import render_footer

st.set_page_config(
    page_title="Edu Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main():
    # Header
    render_header()

    # Main Sections
    render_hero_section()
    render_features_section()
    render_testimonials_section()
    render_partners_section()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
