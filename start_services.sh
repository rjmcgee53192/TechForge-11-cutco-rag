#!/bin/bash
# Start the LiteLLM proxy in the background
echo "Starting LiteLLM proxy on port 4000..."
litellm --config litellm_config.yaml --port 4000 &
PROXY_PID=$!

# Wait for proxy to initialize
sleep 3

# Start the Streamlit application
echo "Starting Streamlit UI..."
streamlit run src/app_streamlit.py

# Cleanup: Kill the proxy when streamlit exits
kill $PROXY_PID
