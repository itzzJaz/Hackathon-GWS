
import streamlit as st
import main as mn

st.set_page_config(layout="wide", page_title="Events")

st.title("Events")
st.caption("Discover events, activities and opportunities.")
st.divider()

# Get event data
info = mn.get_info() or []

if not info:
    st.info("No events available right now.")

else:
    # Three cards per row
    for start in range(0, len(info), 3):
        cols = st.columns(3)

        for col, event in zip(cols, info[start:start + 3]):
            with col:

                with st.container(border=True):

                    # Event name at the top
                    st.subheader(event.get("name", "Untitled Event"))

                    # Description
                    st.write(
                        event.get("description", "No description available.")
                    )

                    st.divider()

                    # Date and venue
                    st.markdown("**Date**")
                    st.write(event.get("date", "Not specified"))

                    st.markdown("**Venue**")
                    st.write(event.get("venue", "Not specified"))

                    st.divider()

                    # Organizer and participants
                    st.markdown("**Organizer**")
                    st.write(event.get("organizer_name", "Not specified"))

                    st.markdown("**Participants**")
                    st.write(event.get("participants", 0))

