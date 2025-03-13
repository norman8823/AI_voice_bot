import requests
import os
import jwt
from datetime import datetime, timedelta
import streamlit as st

# Load environment variables
dotenv.load_dotenv()


# Call ID to retrieve
call_ids = [
    "a7e95587-8023-4823-882f-528414dee193",
    "1d6e6aed-2841-4062-ad6f-853aac109663",
    "19246cfb-23f6-4460-b69c-0ec0e69f7e39",
    "d799c7a2-399f-4ac2-9927-13da85f4936d",
    "a41a8404-6850-48a6-ba45-655fb9dc3945"

]


def get_call_data(call_id):
    # Get credentials from environment variables
    org_id = os.getenv("ORG_ID")
    private_key = os.getenv("VAPI_AUTH_TOKEN")
    
    # Generate JWT payload
    payload = {
        "orgId": org_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    # Create JWT token
    token = jwt.encode(payload, private_key, algorithm="HS256")
    
    # Set request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Make API request
    response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
    
    # Handle response
    if response.status_code == 200:
        print("Success!")
        return(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        st.error(f"Error: {response.status_code}")
        st.error(response.text)

st.title("AI agent Logs")
# Select the Callid
selected_call_id = st.selectbox("Select the Call ID", call_ids)

if selected_call_id:
#make API request with selected call ID
    call_data = get_call_data(selected_call_id)
    if call_data:
        st.subheader("Call Metrics")
        st.json({
            "Call ID": call_data["id"],
            "Type": call_data["type"],
            "Started at": call_data["startedAt"],
            "Ended at": call_data["endedAt"],
            "Ended reason": call_data["endedReason"],
    
        })

        st.divider()
        st.subheader("Summary")
        st.write(call_data['analysis']['summary'])

        st.subheader("Topics")
        for topic in call_data['analysis']['structuredData']['topics']:
            st.write(f"- {topic}")
        
        st.subheader(f"Success Evaluation: {call_data['analysis']['successEvaluation']}")

        st.divider()

        st.subheader("Transcript")
        st.text_area("Transcript", call_data['transcript'], height=400)

        st.divider()
        st.subheader("Recordings")
        st.markdown(f"[Recording URL]({call_data['recordingUrl']})")

