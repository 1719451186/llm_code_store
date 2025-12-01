## 📰 ➡️ 🎙️ Blog to Podcast Agent
This is a Streamlit-based application that allows users to convert any blog post into a podcast. The app uses Siliconflow 提供的 OpenAI 兼容模型（默认 DeepSeek-V3，采用官方 `openai` SDK 调用）进行摘要，使用 Firecrawl 抓取网页内容，并使用 ElevenLabs API 生成音频。输入任意博客 URL，即可生成对应播客。

## Features

- **Blog Scraping**: Scrapes the full content of any public blog URL using Firecrawl API.

- **Summary Generation**: Creates an engaging and concise summary of the blog (within 2000 characters) using Siliconflow 的大模型（兼容 OpenAI Chat Completions 接口）。

- **Podcast Generation**: Converts the summary into an audio podcast using the ElevenLabs voice API.

- **API Key Integration**: Requires Siliconflow、Firecrawl、ElevenLabs API keys to function, entered securely via the sidebar.

## Setup

### Requirements 

1. **API Keys**:
    - **Siliconflow API Key**: 注册硅基流动账号即可获取，可直接填入侧边栏，或写入环境变量 `SILICONFLOW_API_KEY`。

    - **ElevenLabs API Key**: Get your ElevenLabs API key from ElevenLabs.

    - **Firecrawl API Key**: Get your Firecrawl API key from Firecrawl.

2. **Python 3.8+**: Ensure you have Python 3.8 or higher installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps
   cd ai_agent_tutorials/ai_blog_to_podcast_agent
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
### Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run blog_to_podcast_agent.py
   ```

2. In the app interface:
    - Enter your Siliconflow, ElevenLabs, and Firecrawl API keys in the sidebar.

    - Input the blog URL you want to convert.

    - Click "🎙️ Generate Podcast".

    - Listen to the generated podcast or download it.