import streamlit as st


def render_hero_section():
    """히어로 섹션 - 과정 추천"""
    st.markdown(
        """
        <div style="
            background: #f7a70d;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        ">
            <h2 style="color: #1a1a1a; margin-bottom: 0.5rem;">Find Your Perfect Learning Path</h2>
            <p style="color: #333333;">Discover AI-powered education tailored to your goals</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.selectbox("Study Level", ["Beginner", "Intermediate", "Advanced"], key="level")

    with col2:
        st.selectbox(
            "Interest Area",
            ["AI & Machine Learning", "Data Science", "Web Development", "Cloud Computing"],
            key="interest",
        )

    with col3:
        st.selectbox("Learning Style", ["Self-paced", "Instructor-led", "Hybrid"], key="style")

    with col4:
        st.button("Get Recommendations", type="primary", use_container_width=True)


def render_features_section():
    """서비스 특징 섹션"""
    st.markdown("---")
    st.markdown(
        "<h2 style='color: #1a1a1a;'>How We Support Your Learning</h2>",
        unsafe_allow_html=True,
    )

    features = [
        {"title": "Course Matching", "desc": "AI-powered course recommendations"},
        {"title": "Progress Tracking", "desc": "Monitor your learning journey"},
        {"title": "AI Tutoring", "desc": "Get personalized assistance"},
        {"title": "Resource Library", "desc": "Access curated materials"},
        {"title": "Community", "desc": "Connect with learners"},
        {"title": "Certifications", "desc": "Earn recognized credentials"},
    ]

    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="
                    background: #f5f5f5;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                    border-left: 4px solid #f7a70d;
                ">
                    <h4 style="color: #1a1a1a; margin: 0 0 0.5rem 0;">{feature['title']}</h4>
                    <p style="color: #666666; margin: 0;">{feature['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_testimonials_section():
    """학생 후기 섹션"""
    st.markdown("---")
    st.markdown(
        "<h2 style='color: #1a1a1a;'>Success Stories</h2>",
        unsafe_allow_html=True,
    )

    testimonials = [
        {
            "name": "Alice Kim",
            "role": "Data Scientist",
            "quote": "Edu Agents helped me transition into AI with personalized guidance.",
        },
        {
            "name": "James Park",
            "role": "ML Engineer",
            "quote": "The AI tutor feature accelerated my learning significantly.",
        },
        {
            "name": "Sarah Lee",
            "role": "Developer",
            "quote": "Best platform for structured learning with real-world projects.",
        },
    ]

    cols = st.columns(3)
    for i, t in enumerate(testimonials):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background: #ffffff;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    border: 1px solid #e0e0e0;
                    text-align: center;
                ">
                    <div style="
                        width: 60px;
                        height: 60px;
                        background: #f7a70d;
                        border-radius: 50%;
                        margin: 0 auto 1rem;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: #1a1a1a;
                        font-size: 1.5rem;
                        font-weight: bold;
                    ">{t['name'][0]}</div>
                    <p style="font-style: italic; color: #555555;">"{t['quote']}"</p>
                    <p style="font-weight: bold; margin: 0; color: #1a1a1a;">{t['name']}</p>
                    <p style="color: #888888; font-size: 0.9rem;">{t['role']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_partners_section():
    """파트너 섹션"""
    st.markdown("---")
    st.markdown(
        "<h2 style='color: #1a1a1a;'>Our Partners</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #666666;'>Trusted by leading organizations worldwide</p>",
        unsafe_allow_html=True,
    )

    partners = ["Google", "Microsoft", "AWS", "Meta", "OpenAI", "Anthropic"]
    cols = st.columns(6)
    for i, partner in enumerate(partners):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background: #f5f5f5;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    text-align: center;
                    font-weight: bold;
                    color: #333333;
                    border: 1px solid #e0e0e0;
                ">{partner}</div>
                """,
                unsafe_allow_html=True,
            )
