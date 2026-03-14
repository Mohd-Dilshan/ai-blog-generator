import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

TONE_PROMPTS = {
    "professional": "Write in a professional, formal tone suitable for business audiences. Use industry-appropriate language and maintain a polished, authoritative voice.",
    "casual": "Write in a friendly, conversational tone as if talking to a friend. Use everyday language, contractions, and a warm, approachable voice.",
    "technical": "Write in a technical, detailed tone suitable for experts. Include specific terminology, data-driven insights, and in-depth explanations.",
    "creative": "Write in a creative, engaging tone with vivid descriptions. Use storytelling elements, metaphors, and an imaginative approach.",
    "persuasive": "Write in a persuasive, compelling tone aimed at convincing readers. Use strong arguments, emotional appeals, and clear calls to action."
}


def generate_blog_content(topic: str, tone: str, word_count: int) -> dict:
    """Generate blog content using Groq API with Llama 3.3 70B."""
    
    tone_instruction = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])
    
    prompt = f"""You are an expert blog writer and SEO specialist. Generate a comprehensive blog post about the following topic.

Topic: {topic}

Requirements:
1. {tone_instruction}
2. The blog should be approximately {word_count} words.
3. Include a compelling introduction that hooks the reader.
4. Use clear headings and subheadings (format with ## for main sections, ### for subsections).
5. Include practical examples, tips, or actionable advice where relevant.
6. End with a strong conclusion that summarizes key points.

Please generate the blog content now. Do not include the title in the body - I will request that separately."""

    seo_prompt = f"""Based on the blog topic "{topic}", generate SEO metadata in the following exact format:

TITLE: [An engaging, SEO-optimized title under 60 characters]
META_DESCRIPTION: [A compelling meta description between 150-160 characters that includes the main keyword]
KEYWORDS: [5-7 relevant keywords separated by commas]

Only output in the exact format above, nothing else."""

    try:
        # Generate main blog content
        content_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert blog writer who creates engaging, well-structured content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        blog_content = content_response.choices[0].message.content
        
        # Generate SEO metadata
        seo_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SEO expert. Provide metadata in the exact format requested."
                },
                {
                    "role": "user",
                    "content": seo_prompt
                }
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        seo_content = seo_response.choices[0].message.content
        
        # Parse SEO metadata
        title = ""
        meta_description = ""
        keywords = ""
        
        for line in seo_content.split("\n"):
            line = line.strip()
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
            elif line.startswith("META_DESCRIPTION:"):
                meta_description = line.replace("META_DESCRIPTION:", "").strip()
            elif line.startswith("KEYWORDS:"):
                keywords = line.replace("KEYWORDS:", "").strip()
        
        return {
            "success": True,
            "title": title,
            "meta_description": meta_description,
            "keywords": keywords,
            "content": blog_content,
            "topic": topic,
            "tone": tone.capitalize(),
            "word_count": len(blog_content.split())
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.route("/")
def index():
    """Render the main input form."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generate blog content based on user input."""
    topic = request.form.get("topic", "").strip()
    tone = request.form.get("tone", "professional")
    word_count = int(request.form.get("word_count", 500))
    
    if not topic:
        return render_template("index.html", error="Please enter a topic for your blog.")
    
    if word_count < 300:
        word_count = 300
    elif word_count > 2000:
        word_count = 2000
    
    result = generate_blog_content(topic, tone, word_count)
    
    if result["success"]:
        return render_template("result.html", **result)
    else:
        return render_template("index.html", error=f"Error generating content: {result['error']}")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint for generating blog content (JSON response)."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    topic = data.get("topic", "").strip()
    tone = data.get("tone", "professional")
    word_count = int(data.get("word_count", 500))
    
    if not topic:
        return jsonify({"success": False, "error": "Topic is required"}), 400
    
    word_count = max(300, min(2000, word_count))
    
    result = generate_blog_content(topic, tone, word_count)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
