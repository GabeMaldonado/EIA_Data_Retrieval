mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"egmaldonado10@gmail.com.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
maxUploadSize=1028\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml