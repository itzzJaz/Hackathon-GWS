import streamlit as st
import main as mn

st.set_page_config(layout="wide", page_title="Hourglass - Manager")

# Better at using CSS for designing the UI
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f5efe4 !important;
        font-family: 'Bookman Old Style', serif !important;
    }
    
    .custom-card {
        background: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 20px !important;
        padding: 32px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02), 0 12px 24px rgba(0, 0, 0, 0.03) !important;
    }
    
    .custom-title {
        font-size: 1.5rem !important;
        color: #141312 !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
        margin-bottom: 12px !important;
        font-family: 'Bookman Old Style', serif !important;
    }
    
    .custom-text {
        font-size: 0.95rem !important;
        color: #524d45 !important;
        line-height: 1.6 !important;
        margin-bottom: 16px !important;
        font-family: 'Bookman Old Style', serif !important;
    }

    .custom-label {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #141312 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-top: 12px !important;
        margin-bottom: 2px !important;
        font-family: 'Bookman Old Style', serif !important;
    }

    .custom-value {
        font-size: 0.95rem !important;
        color: #524d45 !important;
        margin-bottom: 12px !important;
        font-family: 'Bookman Old Style', serif !important;
    }

    .custom-divider {
        border: 0 !important;
        border-top: 1px solid rgba(0, 0, 0, 0.06) !important;
        margin: 16px 0 !important;
    }
    
    .badge {
        display: inline-block !important;
        padding: 4px 12px !important;
        background-color: #fdfbf7 !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 100px !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #8a7e6b !important;
        margin-bottom: 16px !important;
        font-family: 'Bookman Old Style', serif !important;
    }
</style>
""", unsafe_allow_html=True)

header_left, header_right = st.columns([3, 1])

with header_left:
    st.title("Events Dashboard")
    st.caption("A platform to organize and sync events at school.")

with header_right:
    st.write("##")
    with st.popover("Create Event", use_container_width=True):
        with st.form("create_event_form", clear_on_submit=True):
            new_name = st.text_input("Event Name")
            new_desc = st.text_area("Description")
            new_date = st.text_input("Date")
            new_venue = st.text_input("Venue")
            new_org = st.text_input("Organizer Name")
            new_parts = st.number_input("Expected Participants", min_value=0, step=1)
            new_pass = st.text_input("Password", type="password")
            
            if st.form_submit_button("Publish Event"):
                if new_name and new_pass:
                    res = mn.create_event(new_name, new_date, new_desc, new_venue, new_parts, new_org, new_pass)
                    if res:
                        st.success("Published successfully.")
                        st.rerun()
                    else:
                        st.error("Submission failed.")
                        
                else:
                    st.warning("Event Name and Security Key are required.")

st.divider()

events = mn.get_info() or []

if not events:
    st.info("No managed events scheduled at this moment.")
else:
    for start in range(0,len(events),3):
        cols=st.columns(3)

        for col, event in zip(cols,events[start:start + 3]):
            with col:
                event_id=event.get("id")
                name=event.get("name", "Untitled Event")
                desc=event.get("description", "No description available.")
                date=event.get("date","Not specified")
                venue=event.get("venue","Not specified")
                org=event.get("organizer_name","Unassigned")
                parts=event.get("participants",0)

                card_html = f"""
                <div class="custom-card">
                    <div class="badge">{org}</div>
                    <div class="custom-title">{name}</div>
                    <div class="custom-text">{desc}</div>
                    <div class="custom-divider"></div>
                    <div class="custom-label">Date</div>
                    <div class="custom-value">{date}</div>
                    <div class="custom-label">Venue</div>
                    <div class="custom-value">{venue}</div>
                    <div class="custom-divider"></div>
                    <div class="custom-label">Participants</div>
                    <div class="custom-value">{parts}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                with st.popover("Edit Fields", use_container_width=True):
                    field_to_edit = st.selectbox(
                        "Select field to update",
                        ["name", "date", "description", "venue", "participants", "organizer_name"],
                        key=f"field_{event_id}"
                    )
                    
                    if field_to_edit == "participants":
                        updated_value = st.number_input("New Value", min_value=0, step=1, value=int(parts), key=f"val_{event_id}")
                    elif field_to_edit == "description":
                        updated_value = st.text_area("New Value", value=desc, key=f"val_{event_id}")
                    else:
                        current_val = event.get(field_to_edit, "")
                        updated_value = st.text_input("New Value", value=str(current_val if current_val is not None else ""), key=f"val_{event_id}")
                        
                    edit_password = st.text_input("Enter Security Key", type="password", key=f"pass_{event_id}")
                    
                    if st.button("Save Changes", key=f"btn_{event_id}", use_container_width=True):
                        if edit_password:
                            edit_result = mn.edit(field_to_edit, updated_value, event_id, edit_password)
                            if edit_result == "Incorrect password":
                                st.error("Authentication failed: Incorrect password.")
                            elif edit_result is not None:
                                st.success("Updated successfully.")
                                st.rerun()
                            else:
                                st.error("Update execution error.")
                        else:
                            st.warning("Authentication required to complete action.")

                with st.popover("Delete Event", use_container_width=True):
                    delete_password = st.text_input(
                        "Enter Security Key", type="password", key=f"delete_pass_{event_id}"
                    )

                    if st.button("Delete Event", key=f"delete_btn_{event_id}", use_container_width=True):
                        if delete_password:
                            delete_result = mn.delete(event_id, delete_password)
                            if delete_result == "Incorrect password":
                                st.error("Authentication failed: Incorrect password.")
                            elif delete_result is not None:
                                st.success("Event deleted successfully.")
                                st.rerun()
                            else:
                                st.error("Delete execution error.")
                        else:
                            st.warning("Authentication required to complete action.")
