# Smart Cultural Storyteller 📚

An AI-powered storytelling platform that automatically generates complete cultural and folk stories using Artificial Intelligence.

## 🎯 Overview

Smart Cultural Storyteller preserves cultural heritage and makes cultural education engaging for younger, digitally native generations by:

- 🤖 **AI Story Generation**: Automatically generates unique cultural and folk stories
- 🎵 **Audio Narration**: Converts stories into natural voice narration with multi-language support
- 🎨 **Visual Storytelling**: Creates beautiful scene images and artwork
- 📝 **Interactive Editing**: Edit stories and regenerate audio/images in real-time
- 💾 **Save & Export**: Save your stories to files for later use
- 🌍 **Cultural Authenticity**: Supports 7+ cultural backgrounds with authentic storytelling

## 🛠️ Technology Stack

- **Programming Language**: Python 3.11+
- **AI & ML**: OpenAI GPT-3.5/4 for story generation, DALL-E for images
- **Audio Generation**: Google Text-to-Speech (gTTS) with pygame playback
- **Visual Generation**: Professional placeholder system + AI image generation
- **Frontend**: Gradio with clean, simple interface
- **Image Processing**: PIL/Pillow for advanced image manipulation

## 🚀 Quick Start

### Windows Users (Easiest Way):
1. **Double-click** `START.bat` - This will automatically:
   - ✅ Check Python installation
   - 📦 Install all dependencies
   - 🔧 Create environment configuration
   - 🚀 Start the application on port 7860
   - 🌐 Open browser automatically to http://localhost:7860

### Manual Installation:
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python app.py
```

4. Open http://localhost:7860 in your browser

## 🎭 Features

### Story Generation
- **Multiple Cultures**: Indian, African, European, Native American, Asian, Middle Eastern, Latin American
- **Story Types**: Folk Tales, Legends, Myths, Historical Stories, Moral Stories
- **Languages**: English, Hindi, Spanish, French with native audio support
- **AI Providers**: Pollinations AI (FREE), OpenAI GPT, Meta AI, and intelligent fallback systems

### Visual & Audio
- **Professional Images**: Instant high-quality placeholder generation
- **Scene Gallery**: Multiple images per story with cultural themes
- **Audio Narration**: Natural voice synthesis in multiple languages
- **Art Styles**: 10+ different visual styles from digital art to watercolor

### Interactive Features
- **Live Editing**: Edit story content and regenerate audio/images
- **Save Stories**: Export stories to text files with timestamps
- **Suggestions**: Cultural story topic suggestions for each background
- **Real-time Status**: Live generation progress and status updates

## 📂 Project Structure

```
smart-cultural-storyteller/
│
├── app.py                 # Main application with simple UI
├── story_generator.py     # Multi-language AI story generation
├── audio_generator.py     # Advanced text-to-speech module
├── image_generator.py     # Professional image generation system
├── requirements.txt       # Project dependencies
├── START.bat             # One-click Windows launcher
├── .env                  # Environment configuration
└── README.md             # Project documentation
```

## 🎯 Target Audience

- 👨‍🏫 **Educators & Teachers**: Cultural education and storytelling
- 👨‍👩‍👧‍👦 **Parents & Children**: Family storytelling and learning
- 🏛️ **Cultural Organizations**: Heritage preservation and outreach
- 📚 **Students & Researchers**: Cultural studies and documentation
- 🎪 **Storytelling Enthusiasts**: Creative content generation
- 🌐 **Content Creators**: Educational and entertainment content

## 🌟 Key Features

### Simple & Clean Interface
- ✨ Clean, intuitive design focused on functionality
- 🎯 Easy-to-use controls and clear navigation
- 📱 Responsive design that works on all devices
- 🚀 Fast loading and smooth performance

### Technical Improvements
- 🚀 Faster image generation with professional placeholders
- 🔧 Fixed text encoding issues in image generation
- 🎵 Enhanced audio generation with better language support
- 💾 Improved file management and cleanup
- 🛡️ Better error handling and fallback systems

## 🌱 Future Enhancements

- 🎬 **Animated Stories**: AI-generated video storytelling
- 🗣️ **Voice Cloning**: Custom narrator voices
- 🎮 **Interactive Stories**: Choose-your-own-adventure format
- 📱 **Mobile App**: Native iOS and Android applications
- 🌐 **Web Platform**: Cloud-based storytelling platform
- 🤝 **Community Features**: Story sharing and collaboration

## 📜 License

This project is developed for educational and research purposes. Built with ❤️ for preserving cultural heritage through AI technology.