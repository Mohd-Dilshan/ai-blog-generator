---
title: AI Blog Generator
emoji: ✍️
colorFrom: indigo
colorTo: cyan
sdk: docker
pinned: false
license: mit
---

# AI Blog Generator

An AI-powered blog generator that creates high-quality, SEO-optimized blog posts instantly using Groq API and Llama 3.3 70B.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Topic-Based Generation**: Enter any topic and get a complete blog post
- **Multiple Writing Tones**: Choose from Professional, Casual, Technical, Creative, or Persuasive
- **Word Count Control**: Slider from 300-2000 words
- **SEO Optimization**: Automatically generates:
  - SEO-friendly title
  - Meta description (150-160 characters)
  - Relevant keywords
- **Copy Functionality**: One-click copy for all generated content
- **Markdown Support**: View and copy raw markdown format
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Python, Flask
- **AI Model**: Groq API with Llama 3.3 70B Versatile
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Docker (Hugging Face Spaces)

## Quick Start

### Prerequisites

- Python 3.11+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-blog-generator.git
   cd ai-blog-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:7860
   ```

### Docker Development

```bash
# Build the image
docker build -t ai-blog-generator .

# Run the container
docker run -p 7860:7860 -e GROQ_API_KEY=your_api_key ai-blog-generator
```

## Deployment to Hugging Face Spaces

1. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces)
   - Select "Docker" as the SDK
   - Choose a name for your Space

2. **Push your code**
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push space main
   ```

3. **Add your API key**
   - Go to Space Settings > Repository Secrets
   - Add `GROQ_API_KEY` with your Groq API key

4. **Your app will be live** at `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## API Endpoints

### Web Interface
- `GET /` - Main form page
- `POST /generate` - Generate blog (form submission)

### JSON API
- `POST /api/generate` - Generate blog (JSON request/response)

**Request Body:**
```json
{
  "topic": "10 Tips for Productive Remote Work",
  "tone": "professional",
  "word_count": 800
}
```

**Response:**
```json
{
  "success": true,
  "title": "SEO Optimized Title",
  "meta_description": "Compelling meta description...",
  "keywords": "keyword1, keyword2, keyword3",
  "content": "Generated blog content...",
  "topic": "Original topic",
  "tone": "Professional",
  "word_count": 823
}
```

## Project Structure

```
ai-blog-generator/
├── app.py                 # Flask application
├── templates/
│   ├── index.html         # Input form
│   └── result.html        # Generated blog display
├── static/
│   └── css/
│       └── style.css      # Custom styles
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Environment variables template
└── README.md              # Documentation
```

## Writing Tones

| Tone | Description |
|------|-------------|
| **Professional** | Formal, business-appropriate language with an authoritative voice |
| **Casual** | Friendly, conversational tone with everyday language |
| **Technical** | Detailed, expert-level content with specific terminology |
| **Creative** | Engaging, vivid descriptions with storytelling elements |
| **Persuasive** | Compelling arguments with emotional appeals and CTAs |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `PORT` | Server port (default: 7860) | No |

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Groq](https://groq.com/) for ultra-fast LLM inference
- [Meta](https://ai.meta.com/) for the Llama 3.3 model
- [Hugging Face](https://huggingface.co/) for hosting
