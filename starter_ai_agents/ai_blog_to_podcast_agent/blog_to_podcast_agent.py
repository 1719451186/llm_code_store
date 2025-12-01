import os

import streamlit as st
from elevenlabs import ElevenLabs
from firecrawl import FirecrawlApp
from openai import OpenAI

# Streamlit Setup
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")

# API Keys (Runtime Input)
st.sidebar.header("🔑 API Keys")
# 这里使用OpenAI的API可能会造成费用生成，不知道可以不可以换成硅基流动的api，这样可以使用硅基流动的便宜的api
siliconflow_key = st.sidebar.text_input("Siliconflow API Key", type="password")
# openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
elevenlabs_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_key = st.sidebar.text_input("Firecrawl API Key", type="password")


# Blog URL Input
url = st.text_input("Enter Blog URL:", "")

# Generate Button
if st.button("🎙️ Generate Podcast", disabled=not all([siliconflow_key, elevenlabs_key, firecrawl_key])):
    if not url.strip():
        st.warning("Please enter a blog URL")
    else:
        with st.spinner("Scraping blog and generating podcast..."):
            try:
                os.environ["FIRECRAWL_API_KEY"] = firecrawl_key

                firecrawl_app = FirecrawlApp(api_key=firecrawl_key)
                scrape_result = firecrawl_app.scrape(
                    url,
                    formats=["markdown"],
                    wait_for=30000,
                    timeout=60000,
                )

                blog_markdown = getattr(scrape_result, "markdown", None)
                if not blog_markdown and isinstance(scrape_result, dict):
                    blog_markdown = scrape_result.get("markdown")

                if not blog_markdown:
                    st.error("Failed to scrape blog content. Please verify the URL.")
                    st.stop()

                client = OpenAI(
                    api_key=siliconflow_key,
                    base_url="https://api.siliconflow.cn/v1",
                )

                completion = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3",
                    messages=[
                        {
                            "role": "system",
                            "content": "You write concise, engaging podcast scripts based on blog articles. Keep responses under 2000 characters.",
                        },
                        {
                            "role": "user",
                            "content": f"Blog URL: {url}\n\nContent:\n{blog_markdown}",
                        },
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )

                summary = completion.choices[0].message.content
                
                if summary:
                    # Initialize ElevenLabs client and generate audio
                    tts_client = ElevenLabs(api_key=elevenlabs_key)
                    
                    # Generate audio using text_to_speech.convert
                    audio_generator = tts_client.text_to_speech.convert(
                        text=summary,
                        voice_id="JBFqnCBsd6RMkjVDRZzb",
                        model_id="eleven_multilingual_v2"
                    )
                    
                    # Collect audio chunks if it's a generator
                    audio_chunks = []
                    for chunk in audio_generator:
                        if chunk:
                            audio_chunks.append(chunk)
                    audio_bytes = b"".join(audio_chunks)
                    
                    # Display audio
                    st.success("Podcast generated! 🎧")
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # Download button
                    st.download_button(
                        "Download Podcast",
                        audio_bytes,
                        "podcast.mp3",
                        "audio/mp3"
                    )
                    
                    # Show summary
                    with st.expander("📄 Podcast Summary"):
                        st.write(summary)
                else:
                    st.error("Failed to generate summary")
                    
            except Exception as e:
                st.error(f"Error: {e}")
