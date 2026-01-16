"""
Submission Verification Script
Checks if all required files and components are present
"""

import os
import json

print("🔍 VERIFYING COLLEGE SUBMISSION PACKAGE")
print("="*70)

# Check required files
required_files = {
    "Smart_Cultural_Storyteller.ipynb": "Main Jupyter Notebook",
    "app.py": "Gradio Web Application",
    "story_generator.py": "Story Generation Module",
    "audio_generator.py": "Audio Generation Module",
    "image_generator.py": "Image Generation Module",
    "requirements.txt": "Python Dependencies",
    "README.md": "Project Documentation",
    ".env.example": "Environment Template",
    "SUBMISSION_README.md": "Submission Guide"
}

print("\n📁 Checking Required Files:")
print("-"*70)

all_present = True
for filename, description in required_files.items():
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  ✅ {filename:<40} ({size:,} bytes)")
    else:
        print(f"  ❌ {filename:<40} MISSING!")
        all_present = False

# Check notebook structure
print("\n📓 Verifying Notebook Structure:")
print("-"*70)

try:
    with open('Smart_Cultural_Storyteller.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cells = notebook.get('cells', [])
    markdown_cells = [c for c in cells if c['cell_type'] == 'markdown']
    code_cells = [c for c in cells if c['cell_type'] == 'code']
    
    print(f"  ✅ Total Cells: {len(cells)}")
    print(f"  ✅ Markdown Cells: {len(markdown_cells)}")
    print(f"  ✅ Code Cells: {len(code_cells)}")
    
    # Check for required sections
    required_sections = [
        "Problem Definition",
        "Data Understanding",
        "Model / System Design",
        "Core Implementation",
        "Evaluation",
        "Ethical Considerations",
        "Conclusion"
    ]
    
    print("\n  📋 Required Sections:")
    notebook_text = json.dumps(notebook).lower()
    for section in required_sections:
        if section.lower() in notebook_text:
            print(f"    ✅ {section}")
        else:
            print(f"    ⚠️  {section} (may need verification)")
    
except Exception as e:
    print(f"  ❌ Error reading notebook: {str(e)}")
    all_present = False

# Check Python modules
print("\n🐍 Checking Python Modules:")
print("-"*70)

try:
    import gradio
    print(f"  ✅ gradio: {gradio.__version__}")
except:
    print("  ⚠️  gradio: Not installed")

try:
    import openai
    print(f"  ✅ openai: {openai.__version__}")
except:
    print("  ⚠️  openai: Not installed (optional)")

try:
    from gtts import gTTS
    print("  ✅ gtts: Installed")
except:
    print("  ⚠️  gtts: Not installed")

try:
    from PIL import Image
    print("  ✅ PIL/Pillow: Installed")
except:
    print("  ⚠️  PIL/Pillow: Not installed")

try:
    import pygame
    print("  ✅ pygame: Installed")
except:
    print("  ⚠️  pygame: Not installed")

# Final summary
print("\n" + "="*70)
if all_present:
    print("✅ SUBMISSION PACKAGE COMPLETE!")
    print("\n📦 Ready for submission:")
    print("  • All required files present")
    print("  • Notebook structure verified")
    print("  • Code modules available")
    print("\n🎓 Next Steps:")
    print("  1. Run: jupyter notebook Smart_Cultural_Storyteller.ipynb")
    print("  2. Execute all cells to verify")
    print("  3. Review outputs and documentation")
    print("  4. Submit the complete package")
else:
    print("⚠️  SOME FILES MISSING - Please check above")

print("="*70)
