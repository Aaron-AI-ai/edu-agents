import streamlit as st


def render_header():
    """상단 헤더 및 네비게이션 렌더링"""
    # 글로벌 CSS 스타일 (TopUniversities 색상 컨셉)
    st.markdown(
        """
        <style>
        /* 글로벌 색상 변수 */
        :root {
            --primary-gold: #f7a70d;
            --primary-dark: #1a1a1a;
            --text-dark: #333333;
            --text-gray: #666666;
            --bg-white: #ffffff;
            --bg-gray: #f5f5f5;
            --border-gray: #e0e0e0;
        }

        /* 버튼 스타일 오버라이드 */
        .stButton > button {
            background-color: #f7a70d !important;
            color: #1a1a1a !important;
            border: none !important;
            font-weight: 600 !important;
        }
        .stButton > button:hover {
            background-color: #e69600 !important;
        }

        /* 선택박스 스타일 */
        .stSelectbox > div > div {
            border-color: #e0e0e0 !important;
        }

        /* 링크 색상 */
        a {
            color: #f7a70d !important;
        }
        a:hover {
            color: #e69600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 헤더
    col1, col2, col3 = st.columns([2, 6, 2])

    with col1:
        st.markdown(
            "<h3 style='color: #1a1a1a; margin: 0;'>Edu Agents</h3>",
            unsafe_allow_html=True,
        )

    with col2:
        # 네비게이션 메뉴
        menu_cols = st.columns(5)
        menu_items = ["Rankings", "Discover", "Events", "Prepare", "About"]
        for i, item in enumerate(menu_items):
            with menu_cols[i]:
                st.markdown(
                    f"<p style='color: #333; font-weight: 500; cursor: pointer; margin: 0;'>{item}</p>",
                    unsafe_allow_html=True,
                )

    with col3:
        st.text_input("", placeholder="Search...", label_visibility="collapsed")

    st.markdown("---")
