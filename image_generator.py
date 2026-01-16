"""
Image Generation Module
Generates visual content for story scenes using AI models
Supports OpenAI DALL-E and Meta Imagine
"""

import os
import requests
import tempfile
from PIL import Image
from typing import Optional, List
import base64
import io
import urllib.parse

class ImageGenerator:
    def __init__(self):
        """Initialize the image generator with multiple AI providers"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        print("🎨 Image AI Providers initialized:")
        print(f"   🌸 Pollinations AI: ✅ (FREE)")
        print(f"   OpenAI DALL-E: {'✅' if self.openai_api_key else '❌'}")
        print(f"   Meta Imagine: {'✅' if self.hf_api_key else '❌ (using placeholders)'}")
        
    def generate_story_image(self, scene_description: str, style: str = "digital art", ai_provider: str = "auto") -> Optional[str]:
        """
        Generate an image for a story scene using AI models
        
        Args:
            scene_description: Description of the scene to visualize
            style: Art style for the image
            ai_provider: AI provider to use ("pollinations", "openai", "meta", "placeholder", "auto")
            
        Returns:
            Path to the generated image file or None if failed
        """
        
        # Auto-select AI provider - prioritize Pollinations AI (FREE)
        if ai_provider == "auto":
            ai_provider = "pollinations"  # Default to free Pollinations AI
        
        # Try selected provider
        if ai_provider == "pollinations":
            return self._generate_pollinations_image(scene_description, style)
        elif ai_provider == "openai" and self.openai_api_key:
            return self._generate_openai_image(scene_description, style)
        elif ai_provider == "meta":
            return self._generate_meta_image(scene_description, style)
        else:
            # Generate high-quality professional placeholder
            print(f"🎨 Creating professional placeholder image...")
            return self._generate_professional_placeholder(scene_description, style)
    
    def _generate_professional_placeholder(self, scene_description: str, style: str) -> str:
        """Generate professional-looking placeholder image (FAST & HIGH QUALITY)"""
        
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageFilter
            import random
            import math
            
            # Get topic-specific colors and elements
            topic_info = self._get_enhanced_topic_info(scene_description, style)
            
            # Create high-resolution image
            img = Image.new('RGB', (512, 512), color=topic_info["bg_color"])
            draw = ImageDraw.Draw(img)
            
            # Create beautiful gradient background
            self._create_gradient_background(draw, topic_info)
            
            # Add artistic elements based on topic
            self._add_artistic_elements(draw, scene_description, topic_info)
            
            # Add professional text overlay
            self._add_professional_text(draw, scene_description, topic_info)
            
            # Add decorative border
            self._add_decorative_border(draw, topic_info)
            
            # Save high-quality image
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            img.save(temp_file.name, 'PNG', quality=95, optimize=True)
            temp_file.close()
            
            print(f"✅ Professional placeholder created instantly!")
            return temp_file.name
            
        except Exception as e:
            print(f"Error creating professional placeholder: {str(e)}")
            return self._generate_simple_fallback()
    
    def _get_enhanced_topic_info(self, scene_description: str, style: str) -> dict:
        """Get enhanced styling info for professional placeholders"""
        
        scene_lower = scene_description.lower()
        
        # Enhanced topic-based themes
        if any(word in scene_lower for word in ["elephant", "temple", "indian", "hindu"]):
            return {
                "bg_color": (255, 248, 220),  # Cornsilk
                "accent_color": (184, 134, 11),  # Dark golden
                "secondary_color": (220, 20, 60),  # Crimson
                "theme": "indian",
                "patterns": ["lotus", "mandala", "temple"]
            }
        elif any(word in scene_lower for word in ["tree", "forest", "nature", "green"]):
            return {
                "bg_color": (240, 255, 240),  # Honeydew
                "accent_color": (34, 139, 34),  # Forest green
                "secondary_color": (107, 142, 35),  # Olive drab
                "theme": "nature",
                "patterns": ["leaves", "branches", "flowers"]
            }
        elif any(word in scene_lower for word in ["ocean", "river", "water", "blue"]):
            return {
                "bg_color": (240, 248, 255),  # Alice blue
                "accent_color": (30, 144, 255),  # Dodger blue
                "secondary_color": (70, 130, 180),  # Steel blue
                "theme": "water",
                "patterns": ["waves", "drops", "ripples"]
            }
        elif any(word in scene_lower for word in ["fire", "sun", "flame", "red"]):
            return {
                "bg_color": (255, 250, 240),  # Floral white
                "accent_color": (255, 69, 0),  # Red orange
                "secondary_color": (255, 140, 0),  # Dark orange
                "theme": "fire",
                "patterns": ["flames", "rays", "sparkles"]
            }
        else:
            # Default elegant theme
            return {
                "bg_color": (248, 248, 255),  # Ghost white
                "accent_color": (123, 104, 238),  # Medium slate blue
                "secondary_color": (147, 112, 219),  # Medium purple
                "theme": "elegant",
                "patterns": ["geometric", "abstract", "artistic"]
            }
    
    def _create_gradient_background(self, draw, topic_info):
        """Create beautiful gradient background"""
        
        bg_color = topic_info["bg_color"]
        accent_color = topic_info["accent_color"]
        
        # Radial gradient from center
        center_x, center_y = 256, 256
        max_radius = 362  # sqrt(256^2 + 256^2)
        
        for radius in range(0, max_radius, 5):
            alpha = radius / max_radius
            # Blend colors
            blended_color = tuple(
                int(bg_color[i] * (1 - alpha * 0.3) + accent_color[i] * alpha * 0.1)
                for i in range(3)
            )
            draw.ellipse([
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius
            ], outline=blended_color)
    
    def _add_artistic_elements(self, draw, scene_description, topic_info):
        """Add artistic elements based on topic"""
        
        import random
        import math
        
        theme = topic_info["theme"]
        accent_color = topic_info["accent_color"]
        secondary_color = topic_info["secondary_color"]
        
        if theme == "indian":
            # Add lotus-like patterns
            for i in range(8):
                angle = i * 45
                x = 256 + 80 * math.cos(math.radians(angle))
                y = 256 + 80 * math.sin(math.radians(angle))
                draw.ellipse([x-15, y-15, x+15, y+15], fill=accent_color)
                
        elif theme == "nature":
            # Add leaf-like shapes
            for i in range(12):
                x = random.randint(50, 462)
                y = random.randint(50, 462)
                # Draw leaf shape
                draw.ellipse([x-10, y-20, x+10, y+20], fill=accent_color)
                draw.ellipse([x-20, y-10, x+20, y+10], fill=secondary_color)
                
        elif theme == "water":
            # Add wave patterns
            for y in range(100, 400, 40):
                for x in range(0, 512, 20):
                    wave_y = y + 10 * math.sin(x * 0.1)
                    draw.ellipse([x-3, wave_y-3, x+3, wave_y+3], fill=accent_color)
                    
        elif theme == "fire":
            # Add flame-like shapes
            center_x, center_y = 256, 256
            for i in range(6):
                angle = i * 60
                x = center_x + 60 * math.cos(math.radians(angle))
                y = center_y + 60 * math.sin(math.radians(angle))
                # Flame shape
                points = [
                    (x, y-20), (x-10, y+10), (x+10, y+10)
                ]
                draw.polygon(points, fill=accent_color)
                
        else:
            # Default geometric patterns
            for i in range(16):
                x = random.randint(100, 412)
                y = random.randint(100, 412)
                size = random.randint(5, 15)
                draw.rectangle([x-size, y-size, x+size, y+size], fill=accent_color)
    
    def _add_professional_text(self, draw, scene_description, topic_info):
        """Add professional text overlay"""
        
        try:
            from PIL import ImageFont
            font = ImageFont.load_default()
            
            # Main title
            title = "Story Scene"
            bbox = draw.textbbox((0, 0), title, font=font)
            title_width = bbox[2] - bbox[0]
            x_offset = (512 - title_width) // 2
            
            # Add background for title
            draw.rectangle([x_offset-10, 30, x_offset+title_width+10, 55], 
                          fill=(*topic_info["accent_color"], 200))
            draw.text((x_offset, 35), title, fill=(255, 255, 255), font=font)
            
            # Scene description (wrapped)
            import textwrap
            desc_text = scene_description[:80] + "..." if len(scene_description) > 80 else scene_description
            wrapped_lines = textwrap.wrap(desc_text, width=35)
            
            y_offset = 220
            for line in wrapped_lines[:3]:  # Max 3 lines
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_offset = (512 - text_width) // 2
                
                # Semi-transparent background
                draw.rectangle([x_offset-8, y_offset-2, x_offset+text_width+8, y_offset+18], 
                              fill=(*topic_info["bg_color"], 220))
                draw.text((x_offset, y_offset), line, fill=(60, 60, 60), font=font)
                y_offset += 22
                
        except Exception as e:
            print(f"Error adding text: {str(e)}")
            # Add simple text without font
            try:
                draw.text((200, 250), "Story Scene", fill=(100, 100, 100))
                draw.text((150, 280), scene_description[:30], fill=(80, 80, 80))
            except:
                pass
    
    def _add_decorative_border(self, draw, topic_info):
        """Add decorative border"""
        
        accent_color = topic_info["accent_color"]
        secondary_color = topic_info["secondary_color"]
        
        # Outer border
        draw.rectangle([5, 5, 507, 507], outline=accent_color, width=3)
        # Inner border
        draw.rectangle([15, 15, 497, 497], outline=secondary_color, width=1)
        
        # Corner decorations
        corner_size = 20
        corners = [(15, 15), (497-corner_size, 15), (15, 497-corner_size), (497-corner_size, 497-corner_size)]
        
        for x, y in corners:
            draw.rectangle([x, y, x+corner_size, y+corner_size], fill=accent_color)
    
    def _generate_simple_fallback(self) -> str:
        """Ultimate simple fallback"""
        try:
            img = Image.new('RGB', (512, 512), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Simple centered text
            draw.text((200, 250), "Story Image", fill=(100, 100, 100))
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            img.save(temp_file.name, 'PNG')
            temp_file.close()
            return temp_file.name
        except:
            return None
        """
        Generate an image directly from user topic input
        
        Args:
            topic: User's story topic
            culture: Cultural context
            style: Art style preference
            
        Returns:
            Path to generated image
        """
        
        # Create topic-specific prompt
        cultural_context = {
            "Indian": "in traditional Indian setting with temples, saris, and warm golden colors",
            "African": "in African savanna with tribal patterns and earth tones", 
            "European": "in medieval European setting with castles and forests",
            "Native American": "in natural American landscape with sacred symbols"
        }
        
        context = cultural_context.get(culture, "in beautiful cultural setting")
        
        # Build comprehensive prompt
        topic_prompt = f"{style} illustration of {topic} {context}, highly detailed, beautiful composition, cultural authenticity"
        
        print(f"🎯 Generating topic-specific image for: {topic}")
        
        # Generate using free API
        return self._generate_pollinations_image(topic_prompt, style)
    
    def _generate_meta_image(self, scene_description: str, style: str) -> Optional[str]:
        """Generate image using Meta AI models via Hugging Face (fallback to professional placeholder)"""
        
        try:
            print("🎨 Meta AI models currently unavailable, using professional placeholder...")
            return self._generate_professional_placeholder(scene_description, style)
                
        except Exception as e:
            print(f"Error generating AI image: {str(e)}")
            return self._generate_professional_placeholder(scene_description, style)
    
    def _generate_pollinations_image(self, scene_description: str, style: str) -> Optional[str]:
        """Generate image using Pollinations.ai (FREE & FAST)"""
        
        try:
            # Create optimized prompt for Pollinations AI
            clean_prompt = self._create_pollinations_prompt(scene_description, style)
            
            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(clean_prompt)
            
            # Use Pollinations AI with optimized parameters
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true&enhance=true"
            
            print(f"🌸 Generating Pollinations AI image: {clean_prompt[:60]}...")
            
            # Make request with reasonable timeout
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
                # Save image
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                temp_file.write(response.content)
                temp_file.close()
                
                file_size = len(response.content)
                print(f"✅ Pollinations AI image generated! Size: {file_size} bytes")
                
                return temp_file.name
            else:
                print(f"❌ Pollinations AI failed (status: {response.status_code}), using placeholder...")
                return self._generate_professional_placeholder(scene_description, style)
                
        except Exception as e:
            print(f"❌ Pollinations AI error: {str(e)}, using placeholder...")
            return self._generate_professional_placeholder(scene_description, style)
    
    def _create_pollinations_prompt(self, scene_description: str, style: str) -> str:
        """Create optimized prompt for Pollinations AI"""
        
        # Clean and optimize the scene description
        clean_scene = scene_description.strip()
        
        # Remove excessive details that might confuse the AI
        if len(clean_scene) > 150:
            clean_scene = clean_scene[:150] + "..."
        
        # Create focused prompt
        prompt = f"{style} illustration of {clean_scene}, high quality, detailed, beautiful colors, family-friendly"
        
        # Ensure prompt is not too long (Pollinations works better with shorter prompts)
        if len(prompt) > 200:
            prompt = prompt[:200]
        
        return prompt
    def _generate_openai_image(self, scene_description: str, style: str) -> Optional[str]:
        """Generate image using OpenAI DALL-E (fallback to professional placeholder if billing issues)"""
        
        try:
            # Create a simpler, cleaner prompt for DALL-E
            simple_prompt = f"{style} illustration of {scene_description}"
            
            # Ensure prompt is not too long (DALL-E has limits)
            if len(simple_prompt) > 1000:
                simple_prompt = simple_prompt[:1000]
            
            print(f"🎨 Trying DALL-E: {simple_prompt[:100]}...")
            
            # Make API request to DALL-E
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "dall-e-2",  # Use DALL-E 2 instead of 3 (more reliable)
                    "prompt": simple_prompt,
                    "size": "512x512",    # Smaller size for faster generation
                    "n": 1
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result["data"][0]["url"]
                
                # Download and save the image
                downloaded_path = self._download_image(image_url)
                if downloaded_path:
                    print(f"✅ OpenAI DALL-E image generated successfully!")
                return downloaded_path
            else:
                print(f"❌ DALL-E failed ({response.status_code}), using professional placeholder...")
                # If DALL-E fails, use professional placeholder
                return self._generate_professional_placeholder(scene_description, style)
                
        except Exception as e:
            print(f"❌ DALL-E error, using professional placeholder: {str(e)}")
            return self._generate_professional_placeholder(scene_description, style)
    
    def generate_scene_images(self, scenes: List[str], culture: str, topic: str = "", style: str = "digital art", ai_provider: str = "auto") -> List[Optional[str]]:
        """
        Generate images for multiple story scenes with topic-specific enhancement
        
        Args:
            scenes: List of scene descriptions
            culture: Cultural context for styling
            topic: Original user topic to ensure relevance
            style: Art style preference
            ai_provider: AI provider to use
            
        Returns:
            List of image file paths
        """
        
        image_paths = []
        
        for i, scene in enumerate(scenes):
            print(f"Generating image for scene {i+1}/{len(scenes)}...")
            
            # Enhance scene with topic and cultural context
            enhanced_scene = self._create_topic_relevant_scene(scene, culture, topic, style)
            image_path = self.generate_story_image(enhanced_scene, style, ai_provider)
            image_paths.append(image_path)
        
        return image_paths
    
    def _create_topic_relevant_scene(self, scene: str, culture: str, topic: str, style: str) -> str:
        """Create a topic-relevant scene description for image generation"""
        
        # Extract key elements from the topic
        topic_keywords = self._extract_topic_keywords(topic)
        
        # Cultural visual elements
        cultural_elements = {
            "Indian": {
                "colors": "warm golden, saffron, deep red, emerald green",
                "architecture": "ancient temples, carved pillars, ornate domes",
                "clothing": "colorful saris, traditional dhoti, royal attire",
                "nature": "lotus flowers, banyan trees, sacred rivers",
                "decorative": "intricate patterns, rangoli designs, diyas"
            },
            "African": {
                "colors": "earth tones, sunset orange, deep brown, vibrant red",
                "architecture": "mud huts, tribal structures, baobab trees",
                "clothing": "colorful tribal patterns, traditional robes, beadwork",
                "nature": "savanna landscape, acacia trees, wildlife",
                "decorative": "tribal masks, geometric patterns, ceremonial items"
            },
            "European": {
                "colors": "medieval blues, forest green, stone gray, royal purple",
                "architecture": "stone castles, wooden cottages, church spires",
                "clothing": "medieval robes, peasant clothing, royal garments",
                "nature": "enchanted forests, mountain landscapes, flowing rivers",
                "decorative": "heraldic symbols, Celtic patterns, stained glass"
            },
            "Native American": {
                "colors": "earth tones, turquoise, sunset red, natural brown",
                "architecture": "tepees, pueblo buildings, natural rock formations",
                "clothing": "feathered headdresses, leather garments, beadwork",
                "nature": "vast plains, sacred mountains, flowing rivers",
                "decorative": "dreamcatchers, totem poles, sacred symbols"
            }
        }
        
        # Get cultural context
        culture_data = cultural_elements.get(culture, cultural_elements["Indian"])
        
        # Build enhanced scene description
        enhanced_scene = f"""
        {culture} cultural {style} illustration: {scene}
        
        Key elements to include: {topic_keywords}
        Visual style: {culture_data['colors']} color palette
        Cultural details: {culture_data['architecture']}, {culture_data['clothing']}
        Natural elements: {culture_data['nature']}
        Decorative elements: {culture_data['decorative']}
        
        Make sure the image clearly shows elements related to "{topic}" in {culture} cultural context.
        Beautiful, detailed, family-friendly artwork suitable for storytelling.
        """
        
        return enhanced_scene.strip()
    
    def _extract_topic_keywords(self, topic: str) -> str:
        """Extract and enhance keywords from the user topic"""
        
        topic_lower = topic.lower()
        
        # Topic-specific visual enhancements
        keyword_mappings = {
            "elephant": "majestic elephant, large tusks, wise eyes, gentle giant",
            "tree": "ancient tree, spreading branches, lush foliage, sacred presence",
            "river": "flowing water, riverbank, reflection, life-giving stream",
            "mountain": "towering peak, rocky slopes, misty summit, natural majesty",
            "bird": "graceful bird, spread wings, colorful feathers, soaring flight",
            "eagle": "powerful eagle, sharp talons, keen eyes, mountain perch",
            "lion": "mighty lion, golden mane, regal presence, king of animals",
            "tiger": "striped tiger, powerful build, jungle setting, fierce beauty",
            "peacock": "colorful peacock, fanned tail, iridescent feathers, dancing display",
            "lotus": "blooming lotus, pink petals, sacred flower, water lily",
            "fire": "sacred fire, dancing flames, warm glow, ceremonial light",
            "water": "clear water, rippling surface, life essence, purifying element",
            "sun": "golden sun, bright rays, warm light, celestial body",
            "moon": "silver moon, gentle glow, night sky, celestial beauty",
            "star": "twinkling stars, night sky, celestial light, cosmic wonder",
            "flower": "beautiful flowers, colorful petals, natural beauty, blooming garden",
            "forest": "dense forest, tall trees, dappled sunlight, woodland scene",
            "ocean": "vast ocean, rolling waves, blue waters, endless horizon",
            "butterfly": "colorful butterfly, delicate wings, graceful flight, transformation",
            "snake": "serpentine form, scaled skin, coiled body, mystical presence",
            "horse": "noble horse, flowing mane, powerful stride, graceful movement",
            "cow": "gentle cow, sacred animal, peaceful presence, nurturing spirit",
            "monkey": "playful monkey, agile movement, expressive face, tree dwelling",
            "fish": "swimming fish, scaled body, underwater scene, aquatic life",
            "turtle": "wise turtle, protective shell, slow movement, ancient wisdom",
            "rabbit": "cute rabbit, long ears, fluffy tail, quick movement",
            "deer": "graceful deer, gentle eyes, forest dwelling, elegant form",
            "bear": "strong bear, thick fur, powerful presence, forest guardian",
            "wolf": "wild wolf, pack animal, howling moon, forest predator",
            "fox": "clever fox, red fur, bushy tail, cunning expression"
        }
        
        # Find matching keywords
        enhanced_keywords = []
        for keyword, description in keyword_mappings.items():
            if keyword in topic_lower:
                enhanced_keywords.append(description)
        
        # If no specific matches, use the topic as is with general enhancement
        if not enhanced_keywords:
            enhanced_keywords.append(f"{topic}, detailed representation, culturally authentic")
        
    def _enhance_prompt(self, scene_description: str, style: str) -> str:
        """Enhance the prompt for better AI image generation"""
        
        enhanced_prompt = f"""
        {style} illustration: {scene_description}
        
        High quality, detailed, culturally authentic artwork.
        Beautiful composition, warm lighting, family-friendly.
        Professional digital art suitable for children's book illustration.
        Clear focus on main subject, vibrant but harmonious colors.
        """
        
        return enhanced_prompt.strip()
    
    def _download_image(self, image_url: str) -> Optional[str]:
        """Download image from URL and save to temporary file"""
        
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                temp_file.write(response.content)
                temp_file.close()
                
                return temp_file.name
            else:
                return None
                
        except Exception as e:
            print(f"Error downloading image: {str(e)}")
            return None
    
    def _generate_placeholder_image(self, scene_description: str) -> str:
        """Generate a topic-relevant placeholder image when AI generation fails"""
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            import textwrap
            
            # Extract topic from scene description for better placeholder
            topic_colors = self._get_topic_colors(scene_description)
            
            # Create a colorful placeholder image based on topic
            bg_color = topic_colors["background"]
            accent_color = topic_colors["accent"]
            
            img = Image.new('RGB', (512, 512), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Add gradient effect
            for i in range(512):
                alpha = i / 512.0
                gradient_color = tuple(int(bg_color[j] * (1 - alpha * 0.2)) for j in range(3))
                draw.line([(0, i), (512, i)], fill=gradient_color)
            
            # Add topic-relevant decorative elements
            self._add_topic_decorations(draw, scene_description, accent_color)
            
            # Add text with better formatting
            try:
                # Try to use a default font
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            except:
                font_large = None
                font_small = None
            
            # Add "Story Scene" label at top
            label = "Story Scene"
            if font_large:
                bbox = draw.textbbox((0, 0), label, font=font_large)
                text_width = bbox[2] - bbox[0]
                x_offset = (512 - text_width) // 2
                # Add background for text
                draw.rectangle([x_offset-10, 40, x_offset+text_width+10, 70], fill=(255, 255, 255, 200))
                draw.text((x_offset, 45), label, fill=(50, 50, 50), font=font_large)
            
            # Add scene description text (wrapped)
            if len(scene_description) > 60:
                text = scene_description[:60] + "..."
            else:
                text = scene_description
                
            # Wrap text to multiple lines
            wrapped_lines = textwrap.wrap(text, width=30)
            
            y_offset = 200
            for line in wrapped_lines[:4]:  # Max 4 lines
                if font_small:
                    bbox = draw.textbbox((0, 0), line, font=font_small)
                    text_width = bbox[2] - bbox[0]
                    x_offset = (512 - text_width) // 2
                    # Add semi-transparent background
                    draw.rectangle([x_offset-5, y_offset-2, x_offset+text_width+5, y_offset+18], fill=(255, 255, 255, 180))
                    draw.text((x_offset, y_offset), line, fill=(30, 30, 30), font=font_small)
                y_offset += 25
            
            # Add decorative border
            border_color = accent_color
            draw.rectangle([5, 5, 507, 507], outline=border_color, width=3)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            img.save(temp_file.name, 'PNG')
            temp_file.close()
            
            print(f"✅ Topic-relevant placeholder created: {scene_description[:30]}...")
            return temp_file.name
            
        except Exception as e:
            print(f"Error creating placeholder image: {str(e)}")
            # Fallback to simple colored image
            try:
                img = Image.new('RGB', (512, 512), color=(135, 206, 235))  # Light blue
                
                # Add simple text
                draw = ImageDraw.Draw(img)
                text = "Story Scene"
                bbox = draw.textbbox((0, 0), text)
                text_width = bbox[2] - bbox[0]
                x_offset = (512 - text_width) // 2
                draw.text((x_offset, 250), text, fill=(50, 50, 50))
                
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                img.save(temp_file.name, 'PNG')
                temp_file.close()
                return temp_file.name
            except:
                return None
    
    def _get_topic_colors(self, scene_description: str) -> dict:
        """Get appropriate colors based on the topic/scene"""
        
        scene_lower = scene_description.lower()
        
        # Topic-based color schemes
        if any(word in scene_lower for word in ["elephant", "temple", "golden", "indian"]):
            return {
                "background": (255, 218, 185),  # Peach/golden
                "accent": (184, 134, 11)        # Dark golden
            }
        elif any(word in scene_lower for word in ["tree", "forest", "green", "nature"]):
            return {
                "background": (144, 238, 144),  # Light green
                "accent": (34, 139, 34)         # Forest green
            }
        elif any(word in scene_lower for word in ["river", "water", "blue", "ocean"]):
            return {
                "background": (173, 216, 230),  # Light blue
                "accent": (30, 144, 255)        # Dodger blue
            }
        elif any(word in scene_lower for word in ["fire", "sun", "red", "flame"]):
            return {
                "background": (255, 160, 122),  # Light salmon
                "accent": (220, 20, 60)         # Crimson
            }
        elif any(word in scene_lower for word in ["mountain", "stone", "gray", "rock"]):
            return {
                "background": (211, 211, 211),  # Light gray
                "accent": (105, 105, 105)       # Dim gray
            }
        elif any(word in scene_lower for word in ["flower", "pink", "lotus", "bloom"]):
            return {
                "background": (255, 182, 193),  # Light pink
                "accent": (219, 112, 147)       # Pale violet red
            }
        elif any(word in scene_lower for word in ["african", "savanna", "tribal", "earth"]):
            return {
                "background": (222, 184, 135),  # Burlywood
                "accent": (160, 82, 45)         # Saddle brown
            }
        else:
            # Default pleasant colors
            return {
                "background": (255, 228, 181),  # Moccasin
                "accent": (205, 133, 63)        # Peru
            }
    
    def _add_topic_decorations(self, draw, scene_description: str, accent_color: tuple):
        """Add topic-relevant decorative elements to placeholder"""
        
        import random
        scene_lower = scene_description.lower()
        
        try:
            if any(word in scene_lower for word in ["elephant", "indian", "temple"]):
                # Add elephant-like shapes and Indian patterns
                for i in range(6):
                    x = random.randint(50, 450)
                    y = random.randint(50, 450)
                    # Draw oval shapes for elephant-like forms
                    draw.ellipse([x-20, y-15, x+20, y+15], fill=accent_color)
                    
            elif any(word in scene_lower for word in ["tree", "forest", "branch"]):
                # Add tree-like shapes
                for i in range(4):
                    x = random.randint(100, 400)
                    y = random.randint(100, 400)
                    # Draw tree trunk
                    draw.rectangle([x-5, y, x+5, y+60], fill=accent_color)
                    # Draw tree crown
                    draw.ellipse([x-25, y-20, x+25, y+20], fill=accent_color)
                    
            elif any(word in scene_lower for word in ["river", "water", "wave"]):
                # Add wave-like patterns
                for i in range(8):
                    y = 100 + i * 40
                    for x in range(0, 512, 40):
                        draw.arc([x, y-10, x+40, y+10], 0, 180, fill=accent_color, width=3)
                        
            elif any(word in scene_lower for word in ["bird", "eagle", "fly"]):
                # Add bird-like shapes
                for i in range(5):
                    x = random.randint(100, 400)
                    y = random.randint(100, 400)
                    # Simple bird shape
                    draw.arc([x-15, y-5, x+15, y+5], 0, 180, fill=accent_color, width=2)
                    draw.arc([x-15, y-5, x+15, y+5], 180, 360, fill=accent_color, width=2)
                    
            else:
                # Default decorative circles and shapes
                for i in range(8):
                    x = random.randint(50, 450)
                    y = random.randint(50, 450)
                    radius = random.randint(10, 30)
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=accent_color)
                    
        except Exception as e:
            # If decoration fails, just add simple circles
            for i in range(6):
                x = random.randint(50, 450)
                y = random.randint(50, 450)
                radius = random.randint(15, 25)
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=accent_color)
    
    def create_story_collage(self, image_paths: List[str], title: str) -> Optional[str]:
        """
        Create a collage of story scene images
        
        Args:
            image_paths: List of paths to scene images
            title: Story title for the collage
            
        Returns:
            Path to the collage image
        """
        
        try:
            valid_images = [path for path in image_paths if path and os.path.exists(path)]
            
            if not valid_images:
                return None
            
            # Load images
            images = []
            for path in valid_images[:4]:  # Limit to 4 images
                try:
                    img = Image.open(path)
                    img = img.resize((256, 256))  # Standardize size
                    images.append(img)
                except Exception as e:
                    print(f"Error loading image {path}: {str(e)}")
            
            if not images:
                return None
            
            # Create collage layout
            if len(images) == 1:
                collage = images[0].resize((512, 512))
            elif len(images) == 2:
                collage = Image.new('RGB', (512, 256))
                collage.paste(images[0], (0, 0))
                collage.paste(images[1], (256, 0))
            elif len(images) == 3:
                collage = Image.new('RGB', (512, 512))
                collage.paste(images[0], (0, 0))
                collage.paste(images[1], (256, 0))
                collage.paste(images[2], (128, 256))
            else:  # 4 images
                collage = Image.new('RGB', (512, 512))
                collage.paste(images[0], (0, 0))
                collage.paste(images[1], (256, 0))
                collage.paste(images[2], (0, 256))
                collage.paste(images[3], (256, 256))
            
            # Save collage
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='_collage.png')
            collage.save(temp_file.name, 'PNG')
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error creating collage: {str(e)}")
            return None
    
    def get_art_styles(self) -> List[str]:
        """Get available art styles for image generation"""
        
        return [
            "digital art",
            "watercolor painting",
            "oil painting",
            "cartoon illustration",
            "traditional folk art",
            "children's book illustration",
            "realistic photography",
            "fantasy art",
            "vintage poster style",
            "minimalist design"
        ]
    
    def cleanup_temp_files(self, file_paths: List[str]):
        """Clean up temporary image files"""
        
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f"Error cleaning up file {file_path}: {str(e)}")
    def generate_topic_image(self, topic: str, culture: str, style: str = "digital art") -> Optional[str]:
        """
        Generate an image directly from user topic input using Pollinations AI
        
        Args:
            topic: User's story topic
            culture: Cultural context
            style: Art style preference
            
        Returns:
            Path to generated image
        """
        
        # Create topic-specific prompt for Pollinations AI
        cultural_context = {
            "Indian": "in traditional Indian setting with temples, saris, and warm golden colors",
            "African": "in African savanna with tribal patterns and earth tones", 
            "European": "in medieval European setting with castles and forests",
            "Native American": "in natural American landscape with sacred symbols",
            "Asian": "in traditional Asian setting with pagodas and cherry blossoms",
            "Middle Eastern": "in Middle Eastern setting with deserts and ancient architecture",
            "Latin American": "in Latin American setting with vibrant colors and cultural elements"
        }
        
        context = cultural_context.get(culture, "in beautiful cultural setting")
        
        # Build comprehensive prompt for Pollinations AI
        topic_prompt = f"{style} illustration of {topic} {context}, highly detailed, beautiful composition, cultural authenticity, family-friendly"
        
        print(f"🎯 Generating Pollinations AI image for topic: {topic}")
        
        # Generate using Pollinations AI
        return self._generate_pollinations_image(topic_prompt, style)