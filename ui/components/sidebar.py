import streamlit as st


def sidebar():
    with st.sidebar:
        st.button("Refresh", type="primary", use_container_width=True)
        st.header("Disclaimer")
        st.caption(
            "The IGP Clone App is not affiliated with the Instituto de Geofísica del Peru (IGP) and was created for educational and informational purposes only. While efforts have been made to ensure the accuracy and reliability of the information provided, we do not guarantee its completeness or correctness. The use of this application is at your own risk, and we shall not be held responsible for any misuse, inaccuracies, or errors that may arise from its use."
        )
