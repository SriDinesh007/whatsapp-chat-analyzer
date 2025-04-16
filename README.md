# WhatsApp Chat Analyzer

A Streamlit web app to analyze WhatsApp chat exports. Upload your `.txt` chat file and explore statistics like most active users, most common words, emojis, word cloud, and more!

## Features

- Total messages, media, links, words
- Monthly and weekly activity timelines
- Most active users 
- Word cloud generation
- Most common words
- Emoji analysis

## Live App
You can access the live version of the app here:  
[WhatsApp Chat Analyzer](https://whatsapp-chat-analyzer-ejzcardvureev42p8ibadu.streamlit.app/)

If the link is not working, copy and paste the following URL directly into your browser:

https://whatsapp-chat-analyzer-ejzcardvureev42p8ibadu.streamlit.app/

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/SriDinesh007/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2. (Optional) Create a Python Virtual Environment

To isolate the dependencies for this project, it's recommended to use a virtual environment:

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
# For macOS/Linux:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```


### 3. Install Requirements

Once your environment is set up, install all the required Python packages using:

```bash
pip install -r requirements.txt
```

### 4. Run the app locally

```bash
streamlit run app.py    
```

### 5. Upload Your WhatsApp Chat

Export your chat from WhatsApp and upload the `.txt` file using the **file uploader in the sidebar** of the app.
