"""
AI Story Generation Module
Generates cultural and folk stories using Large Language Models
Supports OpenAI GPT and Meta Llama models
"""

import os
import openai
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    def __init__(self):
        """Initialize the story generator with multiple AI providers"""
        # OpenAI setup
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = openai.OpenAI(api_key=api_key)
        else:
            self.openai_client = None
            
        # Meta AI setup (using Hugging Face)
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.meta_model = "meta-llama/Llama-2-7b-chat-hf"
        
        # Track generated stories to avoid repetition
        self.generated_stories = set()
        
        print("🤖 AI Providers initialized:")
        print(f"   OpenAI: {'✅' if self.openai_client else '❌'}")
        print(f"   Meta AI: {'✅' if self.hf_api_key else '❌ (using fallback)'}")
        
    def generate_story(self, topic: str, culture: str, story_type: str = "folk tale", ai_provider: str = "auto", language: str = "en") -> Dict[str, Any]:
        """
        Generate a complete cultural story based on user input
        
        Args:
            topic: The main theme or subject of the story
            culture: The cultural background (e.g., Indian, African, European)
            story_type: Type of story (folk tale, legend, myth, etc.)
            ai_provider: AI provider to use ("openai", "meta", "auto")
            language: Language for story generation ("en", "hi", "es", "fr")
            
        Returns:
            Dictionary containing story title, content, and metadata
        """
        
        # Create a unique identifier for this story request
        story_id = f"{topic.lower().strip()}_{culture.lower()}_{story_type.lower()}_{language}"
        
        # Add timestamp-based uniqueness to avoid exact repetition
        import time
        story_id_with_time = f"{story_id}_{int(time.time() // 300)}"  # 5-minute windows
        
        # Auto-select AI provider
        if ai_provider == "auto":
            if self.openai_client:
                ai_provider = "openai"
            elif self.hf_api_key:
                ai_provider = "meta"
            else:
                return self._generate_fallback_story(topic, culture, story_type, language)
        
        # Try selected provider
        if ai_provider == "openai" and self.openai_client:
            story_data = self._generate_openai_story(topic, culture, story_type, language)
        elif ai_provider == "meta" and self.hf_api_key:
            story_data = self._generate_meta_story(topic, culture, story_type, language)
        else:
            story_data = self._generate_fallback_story(topic, culture, story_type, language)
        
        # Track this story to ensure variety in future generations
        self.generated_stories.add(story_id_with_time)
        
        return story_data
    
    def _generate_openai_story(self, topic: str, culture: str, story_type: str, language: str = "en") -> Dict[str, Any]:
        """Generate story using OpenAI GPT"""
        
        prompt = self._create_story_prompt(topic, culture, story_type, language)
        
        try:
            # Add randomness to temperature and other parameters for variety
            import random
            temperature = random.uniform(0.7, 0.9)  # Vary creativity level
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a master storyteller specializing in {culture} cultural stories. Create engaging, authentic, and completely unique stories that preserve cultural heritage while being accessible to modern audiences. Each story should be original and specifically tailored to the user's topic. Never repeat the same story twice. Write in the requested language."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=temperature,
                presence_penalty=0.6,  # Encourage new content
                frequency_penalty=0.3   # Reduce repetition
            )
            
            story_content = response.choices[0].message.content
            story_data = self._parse_story_response(story_content, topic, culture, story_type)
            story_data["ai_provider"] = "OpenAI GPT"
            story_data["language"] = language
            
            return story_data
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return self._generate_fallback_story(topic, culture, story_type, language)
    
    def _generate_meta_story(self, topic: str, culture: str, story_type: str, language: str = "en") -> Dict[str, Any]:
        """Generate story using Meta Llama"""
        
        prompt = self._create_story_prompt(topic, culture, story_type, language)
        
        try:
            # Hugging Face Inference API
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            
            payload = {
                "inputs": f"<s>[INST] {prompt} [/INST]",
                "parameters": {
                    "max_new_tokens": 1500,
                    "temperature": 0.8,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.meta_model}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                story_content = result[0]["generated_text"]
                
                # Clean up the response
                if "[/INST]" in story_content:
                    story_content = story_content.split("[/INST]")[1].strip()
                
                story_data = self._parse_story_response(story_content, topic, culture, story_type)
                story_data["ai_provider"] = "Meta Llama"
                story_data["language"] = language
                
                return story_data
            else:
                print(f"Meta AI API error: {response.status_code}")
                return self._generate_fallback_story(topic, culture, story_type, language)
                
        except Exception as e:
            print(f"Meta AI error: {str(e)}")
            return self._generate_fallback_story(topic, culture, story_type, language)
    
    def _create_story_prompt(self, topic: str, culture: str, story_type: str, language: str = "en") -> str:
        """Create a detailed prompt for story generation with authentic cultural knowledge"""
        
        # Add randomness and specificity to make each story unique
        import random
        
        # Language-specific instructions
        language_instructions = {
            "en": "Write the story in English.",
            "hi": "कहानी हिंदी में लिखें। Use Devanagari script and Hindi language throughout the story.",
            "es": "Escribe la historia en español.",
            "fr": "Écrivez l'histoire en français."
        }
        
        lang_instruction = language_instructions.get(language, "Write the story in English.")
        
        # ENHANCED: Real cultural knowledge database
        authentic_cultural_elements = {
            "Indian": {
                "real_places": ["Varanasi (oldest living city)", "Rishikesh (yoga capital)", "Mathura (Krishna's birthplace)", 
                              "Haridwar (holy Ganges)", "Ujjain (ancient Kshipra river)", "Pushkar (sacred lake)"],
                "authentic_characters": ["village pandit (learned priest)", "wise grandmother (dadi)", "temple priest", 
                                       "traveling sadhu (holy man)", "village elder", "royal guru"],
                "real_traditions": ["Ganga Aarti ceremony", "Diwali festival of lights", "Holi spring festival", 
                                  "Karva Chauth fasting", "Raksha Bandhan brother-sister bond", "Guru Purnima teacher respect"],
                "cultural_values": ["Dharma (righteous duty)", "Ahimsa (non-violence)", "Seva (selfless service)", 
                                  "Guru-Shishya (teacher-student)", "Atithi Devo Bhava (guest is god)"],
                "real_symbols": ["Om sacred sound", "Lotus purity", "Banyan tree wisdom", "Cow motherhood", "Elephant Ganesha"]
            },
            "African": {
                "real_places": ["Serengeti plains", "Victoria Falls", "Kilimanjaro mountain", "Sahara desert", 
                              "Congo rainforest", "Nile river source"],
                "authentic_characters": ["tribal elder", "griot storyteller", "village chief", "medicine woman", 
                                       "hunter-gatherer", "wise grandmother"],
                "real_traditions": ["Ubuntu philosophy", "Ancestral worship", "Coming of age ceremonies", 
                                  "Harvest festivals", "Rain-making rituals", "Oral storytelling"],
                "cultural_values": ["Ubuntu (I am because we are)", "Respect for elders", "Community unity", 
                                  "Connection to nature", "Ancestral wisdom"],
                "real_symbols": ["Baobab tree of life", "African masks", "Drums communication", "Lion courage", "Eagle vision"]
            },
            "European": {
                "real_places": ["Black Forest Germany", "Scottish Highlands", "Stonehenge England", "Alps mountains", 
                              "Rhine river", "Mediterranean coast"],
                "authentic_characters": ["village blacksmith", "wise hermit", "castle lord", "forest guardian", 
                                       "traveling minstrel", "monastery monk"],
                "real_traditions": ["Harvest festivals", "Midsummer celebrations", "Christmas traditions", 
                                  "Easter customs", "Medieval guilds", "Knightly codes"],
                "cultural_values": ["Chivalry and honor", "Craftsmanship", "Community cooperation", 
                                  "Respect for nature", "Christian virtues"],
                "real_symbols": ["Celtic cross", "Oak tree strength", "Castle protection", "Sword justice", "Crown authority"]
            },
            "Native American": {
                "real_places": ["Grand Canyon", "Yellowstone", "Black Hills", "Colorado River", "Great Plains", "Pacific Northwest"],
                "authentic_characters": ["tribal shaman", "wise elder", "spirit guide", "medicine woman", 
                                       "tribal chief", "young brave"],
                "real_traditions": ["Vision quests", "Sweat lodge ceremonies", "Powwow gatherings", "Smudging rituals", 
                                  "Seasonal celebrations", "Storytelling circles"],
                "cultural_values": ["Harmony with nature", "Seven generations thinking", "Respect for all life", 
                                  "Tribal unity", "Spiritual connection"],
                "real_symbols": ["Eagle sacred messenger", "Dreamcatcher protection", "Medicine wheel", "Four directions", "Sacred fire"]
            }
        }
        
        # Get authentic cultural context
        culture_data = authentic_cultural_elements.get(culture, authentic_cultural_elements["Indian"])
        
        # Select authentic elements
        real_place = random.choice(culture_data["real_places"])
        authentic_character = random.choice(culture_data["authentic_characters"])
        real_tradition = random.choice(culture_data["real_traditions"])
        cultural_value = random.choice(culture_data["cultural_values"])
        real_symbol = random.choice(culture_data["real_symbols"])
        
        # Story tone variations
        tones = ["mystical and wise", "heartwarming and inspiring", "adventurous yet meaningful", "contemplative and deep"]
        tone = random.choice(tones)
        
        # ENHANCED: Topic-specific authentic knowledge
        topic_cultural_context = self._get_authentic_topic_context(topic, culture)
        
        prompt = f"""
        {lang_instruction}
        
        Create a CULTURALLY AUTHENTIC and HISTORICALLY ACCURATE {story_type} from {culture} culture about "{topic}".
        
        MANDATORY AUTHENTIC ELEMENTS:
        1. Setting: {real_place} (use real geographical and cultural details)
        2. Character: {authentic_character} (with authentic cultural role)
        3. Cultural Practice: Include {real_tradition} in the story
        4. Core Value: Story must teach {cultural_value}
        5. Cultural Symbol: Incorporate {real_symbol} meaningfully
        6. Topic Context: {topic_cultural_context}
        
        AUTHENTICITY REQUIREMENTS:
        - Use REAL cultural practices, not generic ones
        - Include authentic {culture} values and beliefs
        - Reference actual geographical locations
        - Incorporate traditional wisdom and teachings
        - Ensure cultural accuracy and respect
        - Make the story educational about {culture} culture
        
        Story Requirements:
        - Length: 800-1200 words
        - Tone: {tone}
        - The story MUST directly relate to "{topic}" throughout
        - Include vivid, culturally accurate descriptions
        - End with a meaningful moral lesson
        - Write in {language_instructions.get(language, "English")}
        
        Structure EXACTLY as:
        TITLE: [Authentic title incorporating "{topic}" and {culture} elements]
        
        STORY:
        [Complete authentic story with real cultural elements, set in {real_place}, featuring {authentic_character}]
        
        SCENES: 
        Scene: [First authentic cultural scene]
        Scene: [Second authentic cultural scene]  
        Scene: [Third authentic cultural scene]
        Scene: [Fourth authentic cultural scene]
        Scene: [Fifth authentic cultural scene]
        
        MORAL: [Authentic {culture} wisdom about "{topic}"]
        
        CULTURAL NOTES: [Brief explanation of the real cultural elements used]
        
        Remember: This must be an AUTHENTIC {culture} story that could actually be told in that culture, not a generic story with {culture} names!
        """
        
        return prompt
    
    def _parse_story_response(self, content: str, topic: str, culture: str, story_type: str) -> Dict[str, Any]:
        """Parse the AI response into structured story data with cultural notes"""
        
        lines = content.strip().split('\n')
        
        story_data = {
            "topic": topic,
            "culture": culture,
            "story_type": story_type,
            "title": "Untitled Story",
            "content": "",
            "scenes": [],
            "moral": "",
            "cultural_notes": ""
        }
        
        current_section = None
        content_lines = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("TITLE:"):
                story_data["title"] = line.replace("TITLE:", "").strip()
            elif line.startswith("STORY:"):
                current_section = "story"
            elif line.startswith("SCENES:"):
                current_section = "scenes"
            elif line.startswith("MORAL:"):
                current_section = "moral"
            elif line.startswith("CULTURAL NOTES:"):
                current_section = "cultural_notes"
            elif line.startswith("Scene:"):
                scene_desc = line.replace("Scene:", "").strip()
                if scene_desc:
                    story_data["scenes"].append(scene_desc)
            elif current_section == "story" and line:
                content_lines.append(line)
            elif current_section == "moral" and line:
                story_data["moral"] = line
            elif current_section == "cultural_notes" and line:
                story_data["cultural_notes"] = line
        
        story_data["content"] = '\n\n'.join(content_lines)
        
        # Add cultural notes to the story content if available
        if story_data["cultural_notes"]:
            story_data["content"] += f"\n\n📚 Cultural Context: {story_data['cultural_notes']}"
        
        return story_data

    def get_story_suggestions(self, culture: str) -> list:
        """Get suggested story topics for a given culture"""
        
        suggestions = {
            "Indian": [
                "The wise elephant and the village",
                "The magical banyan tree",
                "The brave princess and the dragon",
                "The merchant's journey across the mountains",
                "The festival of lights origin story"
            ],
            "African": [
                "Why the lion became king of animals",
                "The clever rabbit and the crocodile",
                "The origin of the baobab tree",
                "The drummer who saved his village",
                "The story of the first rain"
            ],
            "European": [
                "The knight and the enchanted forest",
                "The baker's magical bread",
                "The village that forgot how to laugh",
                "The shepherd's star",
                "The castle in the clouds"
            ],
            "Native American": [
                "How the eagle got its wings",
                "The spirit of the great river",
                "The medicine woman's wisdom",
                "The dancing bear ceremony",
                "The legend of the dreamcatcher"
            ]
        }
        
        return suggestions.get(culture, [
            "The wise elder's teaching",
            "The magical object's journey",
            "The brave hero's quest",
            "The origin of a tradition",
            "The animal's great adventure"
        ])
    
    def _generate_fallback_story(self, topic: str, culture: str, story_type: str, language: str = "en") -> Dict[str, Any]:
        """Generate a dynamic fallback story based on user input when OpenAI API is not available"""
        
        import random
        
        # Create a completely dynamic story based on the topic
        story_data = self._create_dynamic_story(topic, culture, story_type, language)
        
        return {
            "topic": topic,
            "culture": culture,
            "story_type": story_type,
            "language": language,
            "title": story_data["title"],
            "content": story_data["content"],
            "scenes": story_data["scenes"],
            "moral": story_data["moral"],
            "ai_provider": "Dynamic Fallback Generator"
        }
    
    def _create_dynamic_story(self, topic: str, culture: str, story_type: str, language: str = "en") -> Dict[str, Any]:
        """Create a completely dynamic story based on user input"""
        import random
        
        # Language-specific content
        if language == "hi":
            return self._create_hindi_story(topic, culture, story_type)
        elif language == "es":
            return self._create_spanish_story(topic, culture, story_type)
        elif language == "fr":
            return self._create_french_story(topic, culture, story_type)
        else:
            return self._create_english_story(topic, culture, story_type)
    
    def _create_hindi_story(self, topic: str, culture: str, story_type: str) -> Dict[str, Any]:
        """Create a story in Hindi"""
        import random
        
        # Hindi story templates
        hindi_openings = [
            f"बहुत समय पहले, {topic} के बारे में एक अद्भुत कहानी थी।",
            f"एक समय की बात है, जब {topic} का रहस्य सभी को पता नहीं था।",
            f"प्राचीन काल में, {topic} की शक्ति से सभी परिचित थे।"
        ]
        
        hindi_content = f"""{random.choice(hindi_openings)}

एक छोटे से गांव में एक बुद्धिमान व्यक्ति रहता था जो {topic} के बारे में सब कुछ जानता था। गांव के लोग जब भी किसी समस्या में होते, वे उसके पास जाते थे।

एक दिन, गांव में बड़ी समस्या आई। लोग परेशान थे और नहीं जानते थे कि क्या करें। तब बुद्धिमान व्यक्ति ने {topic} की शक्ति का उपयोग करके सभी की मदद की।

उसने सभी को सिखाया कि {topic} केवल एक चीज़ नहीं है, बल्कि यह जीवन का एक महत्वपूर्ण हिस्सा है। जो लोग {topic} को समझते हैं, वे जीवन में सफल होते हैं।

गांव के लोगों ने इस सीख को अपने बच्चों को भी दिया। आज भी वह गांव {topic} की शिक्षा के लिए प्रसिद्ध है।

इस कहानी से हमें पता चलता है कि ज्ञान और समझदारी से हर समस्या का समाधान मिल सकता है।"""
        
        return {
            "title": f"{topic} की अद्भुत कहानी",
            "content": hindi_content,
            "scenes": [
                f"एक बुद्धिमान व्यक्ति {topic} के साथ गांव में",
                f"गांव के लोग समस्या में परेशान",
                f"{topic} की शक्ति का प्रदर्शन",
                f"गांव में खुशी और समृद्धि",
                f"बच्चों को {topic} की शिक्षा"
            ],
            "moral": f"ज्ञान और {topic} की समझ से जीवन में सफलता मिलती है।"
        }
    
    def _create_english_story(self, topic: str, culture: str, story_type: str) -> Dict[str, Any]:
        """Create an authentic English story with real cultural knowledge"""
        import random
        
        # ENHANCED: Real cultural knowledge instead of generic templates
        authentic_cultural_data = {
            "Indian": {
                "real_places": ["ancient Varanasi", "sacred Rishikesh", "holy Haridwar", "mystical Vrindavan", "royal Jaipur"],
                "authentic_characters": ["village pandit", "wise dadi (grandmother)", "traveling sadhu", "temple priest", "learned guru"],
                "real_traditions": ["Ganga Aarti ceremony", "Diwali celebrations", "Guru Purnima", "village panchayat", "sacred thread ceremony"],
                "cultural_values": ["Dharma (righteous duty)", "Ahimsa (non-violence)", "Seva (selfless service)", "Guru-Shishya tradition"],
                "authentic_symbols": ["sacred Om", "lotus flower", "banyan tree", "holy cow", "Ganesha elephant"]
            },
            "African": {
                "real_places": ["Serengeti plains", "Victoria Falls", "Kilimanjaro slopes", "Congo rainforest", "Sahara oasis"],
                "authentic_characters": ["tribal elder", "griot storyteller", "village chief", "medicine woman", "wise grandmother"],
                "real_traditions": ["Ubuntu philosophy", "ancestral ceremonies", "harvest festivals", "coming of age rituals", "oral storytelling"],
                "cultural_values": ["Ubuntu (I am because we are)", "ancestral wisdom", "community unity", "respect for nature"],
                "authentic_symbols": ["baobab tree of life", "African drums", "ancestral masks", "lion courage", "eagle vision"]
            },
            "European": {
                "real_places": ["Black Forest", "Scottish Highlands", "Rhine Valley", "Alpine meadows", "Stonehenge"],
                "authentic_characters": ["village blacksmith", "wise hermit", "castle lord", "forest keeper", "traveling minstrel"],
                "real_traditions": ["harvest festivals", "midsummer celebrations", "guild traditions", "knightly codes", "monastery life"],
                "cultural_values": ["chivalry and honor", "craftsmanship", "community cooperation", "Christian virtues"],
                "authentic_symbols": ["Celtic cross", "oak tree", "medieval castle", "knight's sword", "royal crown"]
            },
            "Native American": {
                "real_places": ["Grand Canyon", "Black Hills", "Yellowstone", "Colorado River", "Great Plains"],
                "authentic_characters": ["tribal shaman", "wise elder", "medicine woman", "spirit guide", "tribal chief"],
                "real_traditions": ["vision quests", "sweat lodge ceremonies", "powwow gatherings", "smudging rituals", "storytelling circles"],
                "cultural_values": ["harmony with nature", "seven generations thinking", "respect for all life", "tribal unity"],
                "authentic_symbols": ["sacred eagle", "dreamcatcher", "medicine wheel", "four directions", "sacred fire"]
            }
        }
        
        # Get authentic cultural context
        culture_data = authentic_cultural_data.get(culture, authentic_cultural_data["Indian"])
        
        # Select authentic elements
        real_place = random.choice(culture_data["real_places"])
        authentic_character = random.choice(culture_data["authentic_characters"])
        real_tradition = random.choice(culture_data["real_traditions"])
        cultural_value = random.choice(culture_data["cultural_values"])
        authentic_symbol = random.choice(culture_data["authentic_symbols"])
        
        # Get topic-specific authentic context
        topic_context = self._get_authentic_topic_context(topic, culture)
        
        # Create authentic title
        title = f"The Sacred {topic.title()} of {real_place.split()[-1]}"
        
        # Generate authentic story content
        content = self._generate_authentic_story_content(topic, culture, real_place, authentic_character, real_tradition, cultural_value, authentic_symbol, topic_context)
        
        # Generate culturally accurate scenes
        scenes = self._generate_authentic_scenes(topic, culture, real_place, authentic_character, authentic_symbol)
        
        # Generate meaningful moral with cultural context
        moral = f"This {culture} story teaches us that {cultural_value} and understanding of '{topic}' brings wisdom and harmony to our lives."
        
        return {
            "title": title,
            "content": content,
            "scenes": scenes,
            "moral": moral,
            "cultural_notes": f"This story incorporates authentic {culture} elements: {real_tradition}, {authentic_symbol}, and the cultural value of {cultural_value}."
        }
    
    def _generate_story_content(self, topic: str, culture: str, place: str, character: str, element: str, value: str) -> str:
        """Generate dynamic story content based on inputs"""
        import random
        
        # Story templates that incorporate the topic dynamically
        story_parts = {
            "opening": [
                f"In the heart of {place}, where legends come alive, there lived a {character} who understood the true meaning of {topic}.",
                f"Long ago in {place}, when the world was young, a {character} discovered the secret of {topic}.",
                f"In the mystical land of {place}, a {character} was known throughout the region for their connection to {topic}."
            ],
            "challenge": [
                f"One day, the people faced a great challenge that could only be solved by understanding {topic}.",
                f"A terrible problem arose that threatened the peace, and only the wisdom of {topic} could help.",
                f"When darkness fell upon the land, the {character} knew that {topic} held the key to salvation."
            ],
            "journey": [
                f"The {character} embarked on a journey to the {element}, seeking the deeper meaning of {topic}.",
                f"Guided by ancient wisdom, the {character} traveled far and wide to learn about {topic}.",
                f"Through trials and tribulations, the {character} discovered that {topic} was more than they had imagined."
            ],
            "resolution": [
                f"In the end, the {character} learned that {topic} represents {value} and shared this wisdom with all.",
                f"The {character} realized that {topic} was the key to bringing {value} to their people.",
                f"Through understanding {topic}, the {character} was able to restore {value} to the land."
            ]
        }
        
        # Build the story
        opening = random.choice(story_parts["opening"])
        challenge = random.choice(story_parts["challenge"])
        journey = random.choice(story_parts["journey"])
        resolution = random.choice(story_parts["resolution"])
        
        # Add specific details based on topic keywords
        topic_details = self._add_topic_specific_details(topic, culture)
        
        story = f"""{opening}

{challenge} The people were worried and didn't know where to turn. They had heard stories about {topic}, but few truly understood its power.

{journey} Along the way, the {character} encountered many who had different ideas about {topic}. {topic_details}

Through patience and wisdom, the {character} learned that {topic} was not just a concept, but a living force that connected all things. The {element} revealed ancient secrets that had been forgotten by many.

{resolution} The people celebrated, and from that day forward, they remembered the lesson of {topic}. Children would gather around the {element} to hear this story, learning that true wisdom comes from understanding and respecting {topic}.

And so the legend of {topic} lived on, passed down through generations, reminding everyone that {value} and wisdom can overcome any challenge."""
        
        return story
    
    def _add_topic_specific_details(self, topic: str, culture: str) -> str:
        """Add specific details based on the topic"""
        topic_lower = topic.lower()
        
        # Topic-specific story elements
        if "elephant" in topic_lower:
            return "Some said elephants were just large animals, but the wise knew they represented memory, wisdom, and gentle strength."
        elif "tree" in topic_lower:
            return "Some saw trees as mere wood, but the enlightened understood they were bridges between earth and sky, givers of life."
        elif "river" in topic_lower:
            return "Some viewed rivers as just water, but the wise knew they carried the stories of the land and the tears of joy."
        elif "mountain" in topic_lower:
            return "Some saw mountains as obstacles, but the wise understood they were teachers of patience and perseverance."
        elif "bird" in topic_lower or "eagle" in topic_lower:
            return "Some saw birds as simple creatures, but the wise knew they carried messages between the earthly and divine realms."
        elif "fire" in topic_lower:
            return "Some feared fire as destruction, but the wise understood it as transformation and the light that guides us home."
        elif "water" in topic_lower:
            return "Some took water for granted, but the wise knew it was the source of all life and the mirror of the soul."
        else:
            return f"Some dismissed {topic} as ordinary, but the wise understood its deeper significance in the web of life."
    
    def _generate_dynamic_scenes(self, topic: str, culture: str, place: str, character: str, element: str) -> List[str]:
        """Generate dynamic visual scenes based on the story elements"""
        
        cultural_visual_elements = {
            "Indian": ["golden sunlight", "colorful saris", "temple bells", "lotus flowers", "sacred fire"],
            "African": ["sunset colors", "tribal patterns", "acacia trees", "animal silhouettes", "starry skies"],
            "European": ["misty mornings", "stone architecture", "forest paths", "candlelight", "mountain views"],
            "Native American": ["eagle feathers", "sacred symbols", "natural landscapes", "ceremonial fires", "spirit animals"]
        }
        
        visual_elements = cultural_visual_elements.get(culture, cultural_visual_elements["Indian"])
        
        scenes = [
            f"A {character} in {place} contemplating {topic} with {visual_elements[0]} in the background",
            f"The people gathering around the {element} seeking wisdom about {topic} with {visual_elements[1]} decorating the scene",
            f"A journey scene showing the {character} traveling through {place} in search of {topic} with {visual_elements[2]} along the path",
            f"The moment of discovery when the {character} understands the true meaning of {topic} with {visual_elements[3]} illuminating the scene",
            f"A celebration scene where the community learns about {topic} with {visual_elements[4]} creating a festive atmosphere"
        ]
        
        return scenes
    
    def _create_spanish_story(self, topic: str, culture: str, story_type: str) -> Dict[str, Any]:
        """Create a story in Spanish"""
        import random
        
        # Spanish story templates
        spanish_openings = [
            f"Hace mucho tiempo, había una historia maravillosa sobre {topic}.",
            f"Érase una vez, cuando el misterio de {topic} no era conocido por todos.",
            f"En tiempos antiguos, todos conocían el poder de {topic}."
        ]
        
        spanish_content = f"""{random.choice(spanish_openings)}

En un pequeño pueblo vivía una persona sabia que sabía todo sobre {topic}. Cuando la gente del pueblo tenía problemas, siempre acudían a esta persona.

Un día, llegó un gran problema al pueblo. La gente estaba preocupada y no sabía qué hacer. Entonces, la persona sabia usó el poder de {topic} para ayudar a todos.

Enseñó a todos que {topic} no es solo una cosa, sino una parte importante de la vida. Las personas que entienden {topic} tienen éxito en la vida.

La gente del pueblo también enseñó esta lección a sus hijos. Hoy en día, ese pueblo sigue siendo famoso por la enseñanza de {topic}.

Esta historia nos muestra que con conocimiento y sabiduría, se puede encontrar una solución a cualquier problema."""
        
        return {
            "title": f"La Historia Maravillosa de {topic}",
            "content": spanish_content,
            "scenes": [
                f"Una persona sabia con {topic} en el pueblo",
                f"La gente del pueblo preocupada por el problema",
                f"La demostración del poder de {topic}",
                f"Felicidad y prosperidad en el pueblo",
                f"Enseñando a los niños sobre {topic}"
            ],
            "moral": f"El conocimiento y la comprensión de {topic} traen éxito en la vida."
        }
    
    def _create_french_story(self, topic: str, culture: str, story_type: str) -> Dict[str, Any]:
        """Create a story in French"""
        import random
        
        # French story templates
        french_openings = [
            f"Il y a longtemps, il y avait une histoire merveilleuse sur {topic}.",
            f"Il était une fois, quand le mystère de {topic} n'était pas connu de tous.",
            f"Dans les temps anciens, tout le monde connaissait le pouvoir de {topic}."
        ]
        
        french_content = f"""{random.choice(french_openings)}

Dans un petit village vivait une personne sage qui savait tout sur {topic}. Quand les gens du village avaient des problèmes, ils venaient toujours voir cette personne.

Un jour, un grand problème arriva au village. Les gens étaient inquiets et ne savaient pas quoi faire. Alors, la personne sage utilisa le pouvoir de {topic} pour aider tout le monde.

Elle enseigna à tous que {topic} n'est pas seulement une chose, mais une partie importante de la vie. Les personnes qui comprennent {topic} réussissent dans la vie.

Les gens du village enseignèrent aussi cette leçon à leurs enfants. Aujourd'hui encore, ce village est célèbre pour l'enseignement de {topic}.

Cette histoire nous montre qu'avec la connaissance et la sagesse, on peut trouver une solution à n'importe quel problème."""
        
        return {
            "title": f"L'Histoire Merveilleuse de {topic}",
            "content": french_content,
            "scenes": [
                f"Une personne sage avec {topic} dans le village",
                f"Les gens du village inquiets du problème",
                f"La démonstration du pouvoir de {topic}",
                f"Bonheur et prospérité dans le village",
                f"Enseigner aux enfants sur {topic}"
            ],
            "moral": f"La connaissance et la compréhension de {topic} apportent le succès dans la vie."
        }
    
    def _get_authentic_topic_context(self, topic: str, culture: str) -> str:
        """Get authentic cultural context for specific topics"""
        
        topic_lower = topic.lower()
        
        # Authentic cultural knowledge for specific topics
        authentic_contexts = {
            "Indian": {
                "elephant": "In Indian culture, elephants represent Ganesha (remover of obstacles), are symbols of wisdom and memory, and are considered sacred. Real context: Elephants in Indian temples, Airavata (Indra's elephant), elephant festivals in Kerala.",
                "tree": "Sacred trees in Indian culture include Banyan (Brahma), Peepal (Buddha's enlightenment), Neem (healing), and Tulsi (Vishnu's consort). Real context: Village panchayats under banyan trees, tree worship traditions.",
                "river": "Sacred rivers: Ganga (purification), Yamuna (Krishna), Saraswati (knowledge), Narmada (Shiva). Real context: Ganga Aarti ceremonies, river pilgrimages, spiritual bathing.",
                "fire": "Sacred fire (Agni) is messenger to gods, used in yajnas (fire sacrifices), wedding ceremonies (saat phere), and Diwali lamps. Real context: Vedic fire rituals, eternal flames in temples.",
                "mountain": "Sacred mountains: Kailash (Shiva's abode), Govardhan (Krishna lifted), Arunachala (Shiva as fire). Real context: Mountain pilgrimages, cave meditation traditions."
            },
            "African": {
                "elephant": "In African cultures, elephants symbolize wisdom, memory, and family bonds. Real context: Elephant matriarchs leading herds, ancestral spirits, ivory as sacred material in ceremonies.",
                "tree": "Baobab trees are 'Tree of Life', meeting places, and ancestral spirits' homes. Real context: Community gatherings under baobabs, traditional medicine from bark.",
                "river": "Rivers like Nile, Congo, Zambezi are life sources and spiritual pathways. Real context: River ceremonies, crocodile totems, fishing traditions.",
                "lion": "Lions represent courage, leadership, and royal power in many African cultures. Real context: Lion clans, coming-of-age ceremonies, traditional hunting stories.",
                "drum": "Drums are communication tools, spiritual connectors, and community heartbeat. Real context: Talking drums, ceremonial rhythms, ancestral calling."
            },
            "European": {
                "tree": "Sacred trees: Oak (strength, druids), Ash (Yggdrasil world tree), Hawthorn (fairy trees). Real context: Celtic tree worship, Christmas trees, May Day celebrations.",
                "castle": "Medieval castles represent protection, feudal system, and noble heritage. Real context: Castle life, knightly codes, siege warfare, royal courts.",
                "forest": "Enchanted forests in European folklore: Black Forest, Sherwood, Broceliande. Real context: Forest laws, hermit traditions, fairy tale origins.",
                "knight": "Knights embody chivalry, honor, and Christian virtues. Real context: Crusades, Round Table legends, courtly love, knightly orders.",
                "dragon": "Dragons in European lore represent chaos, treasure guardians, or wisdom. Real context: Saint George legend, Norse dragons, Welsh red dragon."
            },
            "Native American": {
                "eagle": "Eagles are sacred messengers between earth and sky, symbols of courage and vision. Real context: Eagle feathers in ceremonies, vision quests, tribal totems.",
                "mountain": "Sacred mountains are prayer places and vision quest sites. Real context: Black Hills (Lakota), Mount Shasta (various tribes), ceremonial climbing.",
                "river": "Rivers are life givers and spiritual pathways. Real context: Salmon runs, water ceremonies, river as grandmother spirit.",
                "buffalo": "Buffalo provided everything: food, shelter, tools, and spiritual connection. Real context: Buffalo hunts, sacred white buffalo, Plains Indian culture.",
                "fire": "Sacred fire connects to Great Spirit and ancestors. Real context: Sweat lodge fires, ceremonial pipes, eternal flames, fire keepers."
            }
        }
        
        # Get culture-specific contexts
        culture_contexts = authentic_contexts.get(culture, authentic_contexts["Indian"])
        
        # Find matching topic context
        for key, context in culture_contexts.items():
            if key in topic_lower:
                return context
        
        # Default authentic context for the culture
        default_contexts = {
            "Indian": "This topic should be understood through the lens of Dharma (righteous duty), Karma (action and consequence), and the interconnectedness of all life as taught in Indian philosophy.",
            "African": "This topic should reflect Ubuntu philosophy (I am because we are), ancestral wisdom, and the deep connection between community and nature in African traditions.",
            "European": "This topic should embody European values of honor, craftsmanship, community cooperation, and the balance between civilization and nature.",
            "Native American": "This topic should honor the Seven Generations principle, respect for all living beings, and the sacred relationship between humans and Mother Earth."
        }
        
        return default_contexts.get(culture, default_contexts["Indian"])
    
    def _generate_authentic_story_content(self, topic: str, culture: str, place: str, character: str, tradition: str, value: str, symbol: str, context: str) -> str:
        """Generate authentic story content with real cultural knowledge"""
        import random
        
        # Authentic story openings based on real cultural storytelling patterns
        cultural_openings = {
            "Indian": [
                f"In the sacred city of {place}, where the ancient wisdom flows like the holy Ganga, there lived a {character} who understood the true essence of {topic}.",
                f"Long ago, when {place} was blessed by the gods themselves, a {character} discovered the divine secret of {topic}.",
                f"In the time of our ancestors, in the blessed land of {place}, a {character} was renowned for their deep connection to {topic}."
            ],
            "African": [
                f"In the heart of {place}, where the ancestors' spirits dance with the wind, there lived a {character} who held the ancient wisdom of {topic}.",
                f"When the great baobab trees were young and {place} echoed with the drums of creation, a {character} learned the sacred truth of {topic}.",
                f"In the time when {place} was one with the rhythm of Mother Earth, a {character} became the keeper of {topic}'s wisdom."
            ],
            "European": [
                f"In the ancient realm of {place}, where stone circles hold the memories of old, there dwelt a {character} who mastered the art of {topic}.",
                f"When the mists of time covered {place} and legends walked among mortals, a {character} discovered the noble truth of {topic}.",
                f"In the days of honor and chivalry, in the storied land of {place}, a {character} became guardian of {topic}'s sacred knowledge."
            ],
            "Native American": [
                f"In the sacred lands of {place}, where the Great Spirit speaks through every stone and stream, there lived a {character} who walked in harmony with {topic}.",
                f"When {place} was young and the four winds carried the prayers of the people, a {character} received the sacred gift of understanding {topic}.",
                f"In the time of the great vision, in the blessed territory of {place}, a {character} became one with the spirit of {topic}."
            ]
        }
        
        # Get culture-specific opening
        openings = cultural_openings.get(culture, cultural_openings["Indian"])
        opening = random.choice(openings)
        
        # Build authentic story with real cultural elements
        story = f"""{opening}

The people of the community had always honored the tradition of {tradition}, but few truly understood how it connected to the deeper meaning of {topic}. {context}

One day, a great challenge arose that tested the very foundation of their beliefs. The community was troubled, for they had forgotten the ancient ways that their ancestors had taught them about {topic}. The {symbol} that had always guided them seemed to have lost its power.

The {character} knew that this was a time for great wisdom. Drawing upon the sacred tradition of {tradition}, they began to teach the people the true meaning of {topic}. Through patience, ceremony, and the guidance of ancestral wisdom, the community began to understand.

The {symbol} once again shone with its ancient power, for the people had rediscovered the sacred connection between {topic} and the cultural value of {value}. The tradition of {tradition} was renewed with deeper understanding.

From that day forward, the story of {topic} was passed down through generations, always connected to the sacred tradition of {tradition} and the guiding symbol of {symbol}. The people learned that {value} and the wisdom of {topic} are inseparable, like the earth and sky.

And so the ancient wisdom lives on, teaching us that {topic} is not merely a concept, but a living truth that connects us to our ancestors, our community, and the sacred world around us."""
        
        return story
    
    def _generate_authentic_scenes(self, topic: str, culture: str, place: str, character: str, symbol: str) -> List[str]:
        """Generate culturally authentic visual scenes"""
        
        # Authentic cultural visual elements
        cultural_visuals = {
            "Indian": {
                "settings": ["temple courtyard with oil lamps", "Ganga riverbank at sunrise", "village under banyan tree", "palace garden with lotus pond", "mountain ashram with prayer flags"],
                "elements": ["saffron robes", "temple bells", "incense smoke", "marigold garlands", "sacred fire"]
            },
            "African": {
                "settings": ["village circle under baobab tree", "savanna at golden sunset", "river crossing with wildlife", "mountain cave with ancestral paintings", "desert oasis with palm trees"],
                "elements": ["colorful tribal cloth", "wooden masks", "drum rhythms", "animal totems", "starlit sky"]
            },
            "European": {
                "settings": ["castle great hall with tapestries", "forest clearing with stone circle", "monastery garden with herbs", "village square with market", "mountain peak with ancient ruins"],
                "elements": ["medieval banners", "stained glass light", "oak tree shadows", "stone architecture", "candlelit chambers"]
            },
            "Native American": {
                "settings": ["sacred mountain at dawn", "river valley with eagles", "forest clearing with medicine wheel", "canyon with ancient petroglyphs", "plains with buffalo herds"],
                "elements": ["eagle feathers", "sacred smoke", "traditional patterns", "natural landscapes", "ceremonial fire"]
            }
        }
        
        # Get culture-specific visuals
        visuals = cultural_visuals.get(culture, cultural_visuals["Indian"])
        
        scenes = [
            f"The {character} in {place} contemplating {topic} with {visuals['elements'][0]} and {visuals['settings'][0]}",
            f"Community gathering around {symbol} seeking wisdom about {topic} in {visuals['settings'][1]} with {visuals['elements'][1]}",
            f"The moment of teaching when {character} reveals the truth of {topic} in {visuals['settings'][2]} illuminated by {visuals['elements'][2]}",
            f"The transformation scene where the community understands {topic} in {visuals['settings'][3]} decorated with {visuals['elements'][3]}",
            f"The celebration of renewed wisdom about {topic} in {visuals['settings'][4]} under {visuals['elements'][4]}"
        ]
        
        return scenes