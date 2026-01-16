"""
Smart Cultural Storyteller - Main Application (Simple UI)
AI-powered storytelling platform for cultural preservation
"""

import gradio as gr
import os
from story_generator import StoryGenerator
from audio_generator import AudioGenerator
from image_generator import ImageGenerator
from typing import Tuple, List, Optional

class SmartCulturalStoryteller:
    def __init__(self):
        """Initialize the storytelling application"""
        self.story_gen = StoryGenerator()
        self.audio_gen = AudioGenerator()
        self.image_gen = ImageGenerator()
        
        # Track generated files for cleanup
        self.temp_files = []
    
    def generate_complete_story(
        self, 
        topic: str, 
        culture: str, 
        story_type: str,
        ai_provider: str = "auto",
        language: str = "en",
        art_style: str = "digital art",
        voice_speed: str = "normal",
        voice_type: str = "default",
        generate_audio: bool = True,
        generate_images: bool = True
    ) -> Tuple[str, str, str, List, str]:
        """
        Generate a complete story with text, audio, and visuals
        
        Returns:
            Tuple of (title, story_content, audio_path, image_paths, status_message)
        """
        
        try:
            # Clean up previous files
            self._cleanup_previous_files()
            
            # Generate topic-specific image first (instant preview)
            topic_image = None
            if topic.strip():
                topic_image = self.image_gen.generate_topic_image(topic, culture, art_style)
                if topic_image:
                    self.temp_files.append(topic_image)
            
            # Generate story
            story_data = self.story_gen.generate_story(topic, culture, story_type, ai_provider, language)
            
            if "error" in story_data:
                return "", story_data["content"], None, [], f"Error: {story_data['error']}"
            
            title = story_data["title"]
            content = story_data["content"]
            scenes = story_data["scenes"]
            
            audio_path = None
            image_paths = []
            
            # Generate audio narration
            if generate_audio and content:
                audio_path = self.audio_gen.generate_audio(content, language, voice_speed=voice_speed, voice_type=voice_type)
                if audio_path:
                    self.temp_files.append(audio_path)
            
            # Generate scene images
            if generate_images and scenes:
                scene_images = self.image_gen.generate_scene_images(scenes, culture, topic, art_style, ai_provider)
                self.temp_files.extend([path for path in scene_images if path])
                
                # Combine topic image with scene images
                if topic_image:
                    image_paths = [topic_image] + scene_images
                else:
                    image_paths = scene_images
            else:
                # If no scene images requested, still show topic image
                image_paths = [topic_image] if topic_image else []
            
            status = f"✅ Story generated successfully! Created {len(scenes)} scenes"
            if audio_path:
                status += " with audio narration"
            if image_paths:
                status += f" and {len([p for p in image_paths if p])} images"
            
            return title, content, audio_path, image_paths, status
            
        except Exception as e:
            return "", f"Error generating story: {str(e)}", None, [], f"❌ Error: {str(e)}"
    
    def get_story_suggestions(self, culture: str) -> List[str]:
        """Get story topic suggestions for selected culture"""
        return self.story_gen.get_story_suggestions(culture)
    
    def regenerate_audio_from_edited_story(self, story_content: str, language: str, voice_speed: str = 'normal', voice_type: str = 'default') -> Tuple[Optional[str], str]:
        """
        Regenerate audio from edited story content with voice options
        
        Args:
            story_content: The edited story content
            language: Language for audio generation
            voice_speed: Voice speed option
            voice_type: Voice type/accent option
            
        Returns:
            Tuple of (audio_path, status_message)
        """
        
        try:
            if not story_content.strip():
                return None, "❌ No story content to generate audio from!"
            
            # Clean up previous audio files
            self._cleanup_previous_files()
            
            # Generate new audio with selected voice
            audio_path = self.audio_gen.generate_audio(story_content, language, voice_speed=voice_speed, voice_type=voice_type)
            
            if audio_path:
                self.temp_files.append(audio_path)
                voice_desc = self.audio_gen.get_voice_options().get(voice_type, voice_type)
                speed_desc = self.audio_gen.get_voice_speed_options().get(voice_speed, voice_speed)
                return audio_path, f"✅ Audio regenerated with {voice_desc} at {speed_desc}!"
            else:
                return None, "❌ Failed to generate audio. Please try again."
                
        except Exception as e:
            return None, f"❌ Error generating audio: {str(e)}"
    
    def regenerate_images_from_edited_story(self, story_content: str, culture: str, topic: str, art_style: str, ai_provider: str) -> Tuple[List, str]:
        """
        Regenerate images from edited story content
        
        Args:
            story_content: The edited story content
            culture: Cultural context
            topic: Original topic
            art_style: Art style for images
            ai_provider: AI provider to use
            
        Returns:
            Tuple of (image_paths, status_message)
        """
        
        try:
            if not story_content.strip():
                return [], "❌ No story content to generate images from!"
            
            # Extract key scenes from the edited story
            scenes = self._extract_scenes_from_story(story_content, topic)
            
            if not scenes:
                return [], "❌ Could not extract scenes from the story content!"
            
            # Generate images for the extracted scenes
            image_paths = self.image_gen.generate_scene_images(scenes, culture, topic, art_style, ai_provider)
            self.temp_files.extend([path for path in image_paths if path])
            
            valid_images = len([p for p in image_paths if p])
            return image_paths, f"✅ Generated {valid_images} images from your edited story!"
            
        except Exception as e:
            return [], f"❌ Error generating images: {str(e)}"
    
    def save_story_to_file(self, title: str, content: str) -> str:
        """
        Save the story to a text file
        
        Args:
            title: Story title
            content: Story content
            
        Returns:
            Status message
        """
        
        try:
            if not content.strip():
                return "❌ No story content to save!"
            
            # Create filename from title
            import re
            import datetime
            
            safe_title = re.sub(r'[^\w\s-]', '', title.strip())
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            
            if not safe_title:
                safe_title = "story"
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.txt"
            
            # Save story to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                f.write("="*50 + "\n\n")
                f.write(content)
                f.write(f"\n\n" + "="*50)
                f.write(f"\nSaved on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return f"✅ Story saved successfully as '{filename}'!"
            
        except Exception as e:
            return f"❌ Error saving story: {str(e)}"
    
    def _extract_scenes_from_story(self, story_content: str, topic: str) -> List[str]:
        """
        Extract visual scenes from story content for image generation
        
        Args:
            story_content: The story text
            topic: Original topic for context
            
        Returns:
            List of scene descriptions
        """
        
        # Split story into paragraphs
        paragraphs = [p.strip() for p in story_content.split('\n\n') if p.strip()]
        
        scenes = []
        
        # Extract key visual moments from paragraphs
        for i, paragraph in enumerate(paragraphs[:5]):  # Limit to 5 scenes
            if len(paragraph) > 50:  # Only substantial paragraphs
                # Create scene description
                scene_desc = f"Scene from story about {topic}: {paragraph[:100]}..."
                scenes.append(scene_desc)
        
        # If no good scenes found, create generic ones
        if not scenes:
            scenes = [
                f"Opening scene of a story about {topic}",
                f"Main character encountering {topic}",
                f"Climactic moment involving {topic}",
                f"Resolution scene with {topic}",
                f"Ending scene showing the lesson about {topic}"
            ]
        
        return scenes
    
    def _cleanup_previous_files(self):
        """Clean up temporary files from previous generations"""
        if self.temp_files:
            self.audio_gen.cleanup_temp_files(self.temp_files)
            self.image_gen.cleanup_temp_files(self.temp_files)
            self.temp_files = []

def create_interface():
    """Create the Gradio interface"""
    
    app = SmartCulturalStoryteller()
    
    # Define available options
    cultures = ["Indian", "African", "European", "Native American", "Asian", "Middle Eastern", "Latin American"]
    story_types = ["Folk Tale", "Legend", "Myth", "Historical Story", "Moral Story"]
    languages = list(app.audio_gen.get_supported_languages().keys())
    language_names = list(app.audio_gen.get_supported_languages().values())
    art_styles = app.image_gen.get_art_styles()
    
    # Modern CSS with gradient cards and effects
    custom_css = """
    /* Hide Gradio footer */
    .gradio-container .footer {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    .footer {
        display: none !important;
    }
    
    /* Hide "Use via API·Built with Gradio·Settings" */
    div[class*="footer"] {
        display: none !important;
    }
    
    div[class*="Footer"] {
        display: none !important;
    }
    
    /* Modern card styling */
    .modern-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        border-color: rgba(255,255,255,0.3);
    }
    
    /* Enhanced buttons */
    .gr-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .gr-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Input styling */
    .gr-textbox, .gr-dropdown {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .gr-textbox:focus, .gr-dropdown:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        background: rgba(255,255,255,0.15) !important;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }
    
    /* Gallery and audio styling */
    .gr-gallery, .gr-audio {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Beautiful Action Buttons with IDs */
    #audio-btn, #images-btn, #save-btn {
        border-radius: 15px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Audio Button - Pink/Purple */
    #audio-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border-color: rgba(240, 147, 251, 0.3) !important;
    }
    
    #audio-btn:hover {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(240, 147, 251, 0.6) !important;
    }
    
    /* Images Button - Blue */
    #images-btn {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border-color: rgba(79, 172, 254, 0.3) !important;
    }
    
    #images-btn:hover {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(79, 172, 254, 0.6) !important;
    }
    
    /* Save Button - Green */
    #save-btn {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
        color: white !important;
        border-color: rgba(67, 233, 123, 0.3) !important;
    }
    
    #save-btn:hover {
        background: linear-gradient(135deg, #38f9d7 0%, #43e97b 100%) !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(67, 233, 123, 0.6) !important;
    }
    """
    
    with gr.Blocks(
        title="Smart Cultural Storyteller", 
        theme=gr.themes.Default(),
        css=custom_css
    ) as interface:
        
        # Beautiful Enhanced Header
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 3rem; padding: 3rem 2rem; background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%); border-radius: 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.1); border: 2px solid #333; position: relative; overflow: hidden;">
            <!-- Decorative elements -->
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
            <div style="position: absolute; top: 10px; right: 10px; width: 100px; height: 100px; background: linear-gradient(45deg, rgba(118, 75, 162, 0.2), rgba(102, 126, 234, 0.2)); border-radius: 50%; filter: blur(20px);"></div>
            <div style="position: absolute; bottom: 10px; left: 10px; width: 80px; height: 80px; background: linear-gradient(45deg, rgba(79, 172, 254, 0.2), rgba(0, 242, 254, 0.2)); border-radius: 50%; filter: blur(15px);"></div>
            
            <!-- Content -->
            <div style="position: relative; z-index: 2;">
                <h1 style="font-size: 3.5rem; margin: 0; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 0 0 20px rgba(102, 126, 234, 0.3); font-weight: 700; letter-spacing: 2px;">
                    📚 <span style="background: linear-gradient(45deg, #667eea, #764ba2, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Smart Cultural Storyteller</span>
                </h1>
                <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2, #4facfe); margin: 1rem auto; border-radius: 2px; box-shadow: 0 2px 10px rgba(102, 126, 234, 0.5);"></div>
                <p style="font-size: 1.4rem; margin: 1rem 0 0.5rem 0; color: rgba(255,255,255,0.95); font-weight: 500; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">
                    🎭 AI-powered cultural storytelling platform ✨
                </p>
                <p style="font-size: 1.1rem; margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8); font-weight: 400; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5;">
                    Create magical stories with authentic cultural narratives and multiple voice options
                </p>
                
                <!-- Feature badges -->
                <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;">
                    <span style="background: rgba(102, 126, 234, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid rgba(102, 126, 234, 0.3); backdrop-filter: blur(10px);">🤖 AI Stories</span>
                    <span style="background: rgba(240, 147, 251, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid rgba(240, 147, 251, 0.3); backdrop-filter: blur(10px);">🎤 8 Voices</span>
                    <span style="background: rgba(79, 172, 254, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid rgba(79, 172, 254, 0.3); backdrop-filter: blur(10px);">🎨 Visual Art</span>
                    <span style="background: rgba(67, 233, 123, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; border: 1px solid rgba(67, 233, 123, 0.3); backdrop-filter: blur(10px);">🌍 4 Languages</span>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.05); }
        }
        </style>
        """)
        
        with gr.Row(equal_height=True):
            # Left Column - Story Configuration Card
            with gr.Column(scale=1):
                gr.HTML("""
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 2rem; margin-bottom: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                    <div style="text-align: center; margin-bottom: 1.5rem;">
                        <h2 style="color: white; margin: 0; font-size: 1.8rem;">
                            🎯 <span style="background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Story Configuration</span>
                        </h2>
                        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 1rem;">
                            Customize your storytelling experience
                        </p>
                    </div>
                </div>
                """)
                
                culture_dropdown = gr.Dropdown(
                    choices=cultures,
                    value="Indian",
                    label="🌍 Cultural Background",
                    info="Select the cultural context for your story",
                    elem_classes="modern-input"
                )
                
                topic_input = gr.Textbox(
                    label="💡 Story Topic/Theme",
                    placeholder="e.g., The wise elephant, The magical tree, The brave warrior...",
                    info="What should the story be about?",
                    lines=2,
                    elem_classes="modern-input"
                )
                
                story_type_dropdown = gr.Dropdown(
                    choices=story_types,
                    value="Folk Tale",
                    label="📖 Story Type",
                    info="Choose the type of cultural story",
                    elem_classes="modern-input"
                )
                
                with gr.Row():
                    ai_provider_dropdown = gr.Dropdown(
                        choices=[("🌸 Pollinations AI (FREE)", "pollinations"), ("🤖 Auto (Best Available)", "auto"), ("🧠 OpenAI GPT + DALL-E", "openai"), ("🦙 Meta AI + Stable Diffusion", "meta"), ("🎨 Professional Placeholders (Fast)", "placeholder")],
                        value="pollinations",
                        label="🔮 AI Provider",
                        info="Choose AI provider for generation",
                        elem_classes="modern-input"
                    )
                
                # Voice Options Card
                gr.HTML("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);">
                    <h3 style="color: white; margin: 0 0 1rem 0; text-align: center; font-size: 1.3rem;">🎤 Voice & Audio Settings</h3>
                </div>
                """)
                
                with gr.Row():
                    language_dropdown = gr.Dropdown(
                        choices=[("🇺🇸 English", "en"), ("🇮🇳 Hindi", "hi"), ("🇪🇸 Spanish", "es"), ("🇫🇷 French", "fr")],
                        value="en",
                        label="🎵 Audio Language",
                        info="Language for narration",
                        elem_classes="modern-input"
                    )
                    
                    voice_type_dropdown = gr.Dropdown(
                        choices=[
                            ("🎵 Default Voice", "default"),
                            ("🇺🇸 American Male", "us_male"), 
                            ("🇺🇸 American Female", "us_female"),
                            ("🇬� BriStish Male", "uk_male"),
                            ("🇬🇧 British Female", "uk_female"),
                            ("🇦🇺 Australian Voice", "au_voice"),
                            ("🇨🇦 Canadian Voice", "ca_voice"),
                            ("🇮🇳 Indian English", "in_voice")
                        ],
                        value="default",
                        label="� Voice tType",
                        info="Choose voice accent/style",
                        elem_classes="modern-input"
                    )
                
                with gr.Row():
                    voice_speed_dropdown = gr.Dropdown(
                        choices=[("🎵 Normal Speed", "normal"), ("🐌 Slow Speed", "slow"), ("⚡ Fast Speed", "fast")],
                        value="normal",
                        label="⚡ Voice Speed",
                        info="Choose narration speed",
                        elem_classes="modern-input"
                    )
                
                with gr.Row():
                    art_style_dropdown = gr.Dropdown(
                        choices=art_styles,
                        value="digital art",
                        label="🎨 Art Style",
                        info="Visual style for images",
                        elem_classes="modern-input"
                    )
                
                # Generation Options Card
                gr.HTML("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);">
                    <h3 style="color: white; margin: 0 0 1rem 0; text-align: center; font-size: 1.3rem;">⚙️ Generation Options</h3>
                </div>
                """)
                
                with gr.Row():
                    generate_audio_checkbox = gr.Checkbox(
                        value=True,
                        label="🎵 Generate Audio Narration",
                        info="Create voice narration"
                    )
                    
                    generate_images_checkbox = gr.Checkbox(
                        value=True,
                        label="🖼️ Generate Scene Images",
                        info="Create visual scenes"
                    )
                
                generate_btn = gr.Button(
                    "🎭 Generate Magical Story ✨",
                    variant="primary",
                    size="lg",
                    elem_classes="modern-button"
                )
                
                # Story suggestions card
                gr.HTML("""
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.15); border-radius: 15px; padding: 1.5rem; margin-top: 1.5rem;">
                    <h3 style="color: white; margin: 0 0 1rem 0; text-align: center; font-size: 1.2rem;">💡 Story Suggestions</h3>
                </div>
                """)
                
                suggestions_display = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=4,
                    show_label=False,
                    placeholder="Select a culture to see suggestions...",
                    elem_classes="modern-input"
                )
                
                # Update suggestions when culture changes
                def update_suggestions(culture):
                    suggestions = app.get_story_suggestions(culture)
                    return "\n".join(f"✨ {suggestion}" for suggestion in suggestions)
                
                culture_dropdown.change(
                    update_suggestions,
                    inputs=[culture_dropdown],
                    outputs=[suggestions_display]
                )
                
                # Initialize suggestions
                suggestions_display.value = update_suggestions("Indian")
            
            # Right Column - Generated Story Card
            with gr.Column(scale=2):
                gr.HTML("""
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 2rem; margin-bottom: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                    <div style="text-align: center; margin-bottom: 1.5rem;">
                        <h2 style="color: white; margin: 0; font-size: 1.8rem;">
                            📖 <span style="background: linear-gradient(45deg, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Your Generated Story</span>
                        </h2>
                        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 1rem;">
                            Your magical story will appear here with audio and visuals
                        </p>
                    </div>
                </div>
                """)
                
                story_title = gr.Textbox(
                    label="📚 Story Title",
                    interactive=True,
                    lines=1,
                    placeholder="Your story title will appear here...",
                    elem_classes="modern-input"
                )
                
                story_content = gr.Textbox(
                    label="📜 Story Content (Editable)",
                    interactive=True,
                    lines=12,
                    max_lines=20,
                    placeholder="Your magical story will appear here...\n\nClick 'Generate Magical Story' to begin! ✨\n\nAfter generation, you can edit this content directly!",
                    elem_classes="modern-input"
                )
                
                # Action buttons card
                gr.HTML("""
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 8px 25px rgba(67, 233, 123, 0.3);">
                    <h3 style="color: white; margin: 0 0 1rem 0; text-align: center; font-size: 1.3rem;">🔄 Story Actions</h3>
                </div>
                """)
                
                with gr.Row():
                    regenerate_audio_btn = gr.Button(
                        "🎵 Regenerate Audio",
                        variant="secondary",
                        size="sm",
                        elem_id="audio-btn"
                    )
                    
                    regenerate_images_btn = gr.Button(
                        "🎨 Regenerate Images", 
                        variant="secondary",
                        size="sm",
                        elem_id="images-btn"
                    )
                    
                    save_story_btn = gr.Button(
                        "💾 Save Story",
                        variant="secondary", 
                        size="sm",
                        elem_id="save-btn"
                    )
                
                # Media output card
                gr.HTML("""
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.15); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
                    <h3 style="color: white; margin: 0 0 1rem 0; text-align: center; font-size: 1.2rem;">🎵 Audio & Visuals</h3>
                </div>
                """)
                
                with gr.Row():
                    audio_output = gr.Audio(
                        label="🎵 Audio Narration",
                        interactive=False,
                        show_label=True,
                        elem_classes="modern-media"
                    )
                
                image_gallery = gr.Gallery(
                    label="🎨 Story Scene Gallery",
                    show_label=True,
                    elem_id="gallery",
                    columns=2,
                    rows=2,
                    height="400px",
                    object_fit="cover",
                    elem_classes="modern-media"
                )
                
                status_output = gr.Textbox(
                    label="📊 Generation Status",
                    interactive=False,
                    lines=2,
                    placeholder="Ready to generate your story! 🚀",
                    elem_classes="modern-input"
                )
        
        # Connect the generate button
        generate_btn.click(
            app.generate_complete_story,
            inputs=[
                topic_input,
                culture_dropdown,
                story_type_dropdown,
                ai_provider_dropdown,
                language_dropdown,
                art_style_dropdown,
                voice_speed_dropdown,
                voice_type_dropdown,
                generate_audio_checkbox,
                generate_images_checkbox
            ],
            outputs=[
                story_title,
                story_content,
                audio_output,
                image_gallery,
                status_output
            ]
        )
        
        # Connect regenerate audio button
        regenerate_audio_btn.click(
            app.regenerate_audio_from_edited_story,
            inputs=[
                story_content,
                language_dropdown,
                voice_speed_dropdown,
                voice_type_dropdown
            ],
            outputs=[
                audio_output,
                status_output
            ]
        )
        
        # Connect regenerate images button
        regenerate_images_btn.click(
            app.regenerate_images_from_edited_story,
            inputs=[
                story_content,
                culture_dropdown,
                topic_input,
                art_style_dropdown,
                ai_provider_dropdown
            ],
            outputs=[
                image_gallery,
                status_output
            ]
        )
        
        # Connect save story button
        save_story_btn.click(
            app.save_story_to_file,
            inputs=[
                story_title,
                story_content
            ],
            outputs=[
                status_output
            ]
        )
        
        # Modern Footer with Cards and Effects
        gr.HTML("""
        <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; color: white; border: 1px solid #333;">
            <!-- Main Title -->
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: white; margin: 0; font-size: 2rem;">
                    🌟 <span style="background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Smart Cultural Storyteller</span>
                </h2>
                <p style="color: #bdc3c7; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                    Preserving cultural heritage through AI storytelling
                </p>
            </div>
            
            <!-- Feature Cards Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                <!-- AI Generation Card -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; text-align: center; transition: transform 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
                    <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.2rem;">AI Story Generation</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Intelligent cultural storytelling with authentic narratives</p>
                </div>
                
                <!-- Voice Options Card -->
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; text-align: center; transition: transform 0.3s ease; box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎤</div>
                    <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.2rem;">8 Voice Types</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Multiple accents and voice styles for personalized narration</p>
                </div>
                
                <!-- Visual Stories Card -->
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; text-align: center; transition: transform 0.3s ease; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨</div>
                    <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Visual Scenes</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Beautiful artwork and scene generation for immersive storytelling</p>
                </div>
                
                <!-- Multi-language Card -->
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 12px; text-align: center; transition: transform 0.3s ease; box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌍</div>
                    <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.2rem;">Multi-language</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Stories in English, Hindi, Spanish, French with native audio</p>
                </div>
            </div>
            
            <!-- Stats Section -->
            <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; text-align: center;">
                    <div>
                        <div style="font-size: 1.8rem; color: #667eea; font-weight: bold;">7+</div>
                        <div style="color: #bdc3c7; font-size: 0.9rem;">Cultural Backgrounds</div>
                    </div>
                    <div>
                        <div style="font-size: 1.8rem; color: #f093fb; font-weight: bold;">8</div>
                        <div style="color: #bdc3c7; font-size: 0.9rem;">Voice Types</div>
                    </div>
                    <div>
                        <div style="font-size: 1.8rem; color: #4facfe; font-weight: bold;">10+</div>
                        <div style="color: #bdc3c7; font-size: 0.9rem;">Art Styles</div>
                    </div>
                    <div>
                        <div style="font-size: 1.8rem; color: #43e97b; font-weight: bold;">4</div>
                        <div style="color: #bdc3c7; font-size: 0.9rem;">Languages</div>
                    </div>
                </div>
            </div>
            
            <!-- How to Use Section -->
            <div style="background: rgba(255,255,255,0.03); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.08);">
                <h3 style="color: white; text-align: center; margin: 0 0 1rem 0; font-size: 1.3rem;">🚀 How to Use</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="text-align: center; padding: 1rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; color: white; font-weight: bold;">1</div>
                        <div style="color: #e0e0e0; font-size: 0.9rem;">Enter your story topic</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #f093fb, #f5576c); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; color: white; font-weight: bold;">2</div>
                        <div style="color: #e0e0e0; font-size: 0.9rem;">Choose culture & voice</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #4facfe, #00f2fe); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; color: white; font-weight: bold;">3</div>
                        <div style="color: #e0e0e0; font-size: 0.9rem;">Generate magical story</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #43e97b, #38f9d7); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; color: white; font-weight: bold;">4</div>
                        <div style="color: #e0e0e0; font-size: 0.9rem;">Enjoy & customize</div>
                    </div>
                </div>
            </div>
            
            <!-- Bottom Section -->
            <div style="text-align: center; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
                <p style="color: #bdc3c7; margin: 0; font-size: 1rem;">
                    Built with ❤️ for cultural preservation • Powered by AI Technology
                </p>
                <p style="color: #888; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                    © 2026 Smart Cultural Storyteller | Preserving Heritage Through Innovation
                </p>
            </div>
        </div>
        
        <style>
        /* Hover effects for cards */
        div[style*="transition: transform 0.3s ease"]:hover {
            transform: translateY(-5px) scale(1.02);
        }
        </style>
        """)
    
    return interface

def main():
    """Main application entry point"""
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("   Story generation and image creation will use fallback methods.")
        print("   To enable full AI features, set your OpenAI API key in a .env file:")
        print("   OPENAI_API_KEY=your_api_key_here")
        print()
    
    # Create and launch the interface
    interface = create_interface()
    
    print("🚀 Starting Smart Cultural Storyteller...")
    print("📚 Preserving cultural heritage through AI storytelling")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()