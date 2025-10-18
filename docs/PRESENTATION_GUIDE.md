# LangGraph Presentation Guide

This guide explains how to view and convert the `langgraph_presentation.md` Markdown presentation file.

## 📁 Files

- `langgraph_presentation.md` - Markdown slides (25 slides)
- `langgraph_agents_presentation.pptx` - PowerPoint version (14 slides)
- `langgraph_visualization.ipynb` - Interactive Jupyter notebook

## 🎯 Option 1: Marp (Recommended)

**Marp** is the easiest way to view and export Markdown slides.

### Using VS Code (Best Experience)

1. **Install Marp Extension**:
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X)
   - Search for "Marp for VS Code"
   - Install the extension by Marp Team

2. **View Presentation**:
   - Open `langgraph_presentation.md` in VS Code
   - Click the "Open Preview" button in the top-right corner
   - Or use: Cmd+K V (Mac) / Ctrl+K V (Windows)

3. **Export to PowerPoint/PDF**:
   - Open preview
   - Click the "Export Slide Deck" button
   - Choose format: PDF, PowerPoint (PPTX), HTML
   - Save your file

### Using Marp CLI

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Export to PowerPoint
marp langgraph_presentation.md --pptx -o output.pptx

# Export to PDF
marp langgraph_presentation.md --pdf -o output.pdf

# Export to HTML
marp langgraph_presentation.md --html -o output.html

# Start presentation server
marp langgraph_presentation.md --server
```

---

## 🎯 Option 2: Reveal.js

Convert to an interactive web presentation.

### Using Pandoc

```bash
# Install pandoc (if not already installed)
brew install pandoc  # macOS
# or
sudo apt-get install pandoc  # Linux

# Convert to Reveal.js HTML
pandoc langgraph_presentation.md \
  -t revealjs \
  -s \
  -o presentation.html \
  --slide-level=2

# Open in browser
open presentation.html
```

### Presentation Controls (Reveal.js):
- **Arrow keys**: Navigate slides
- **Space**: Next slide
- **Esc**: Overview mode
- **S**: Speaker notes
- **F**: Fullscreen

---

## 🎯 Option 3: Slidev

Modern developer-focused presentation tool.

```bash
# Install Slidev
npm install -g @slidev/cli

# Note: Slidev uses a different format, but you can adapt the content
# Create a new Slidev project
npx slidev init my-presentation

# Copy content from langgraph_presentation.md and adapt format
# Then run:
slidev
```

---

## 🎯 Option 4: GitHub/GitLab

View directly in repository.

- Push `langgraph_presentation.md` to GitHub/GitLab
- The Mermaid diagrams will render automatically
- Use the "Raw" view for reading
- Not ideal for presentation mode, but good for documentation

---

## 🎯 Option 5: Python Script (Already Done)

Use the pre-generated PowerPoint file.

```bash
# Already generated for you:
open langgraph_agents_presentation.pptx
```

---

## 📊 Comparison of Options

| Tool | Pros | Cons | Best For |
|------|------|------|----------|
| **Marp (VS Code)** | Easy, no install, exports PPTX/PDF | Basic styling | Quick presentations |
| **Marp CLI** | Automated, CI/CD friendly | Requires Node.js | Batch conversion |
| **Reveal.js** | Interactive, web-based | Setup complexity | Web presentations |
| **Slidev** | Modern, developer-focused | Different syntax | Developer talks |
| **PowerPoint** | Universal compatibility | Not version-controlled | Traditional meetings |

---

## 🎨 Customizing the Presentation

### Changing the Theme (Marp)

Edit the YAML frontmatter in `langgraph_presentation.md`:

```yaml
---
marp: true
theme: default  # Options: default, gaia, uncover
paginate: true
backgroundColor: #fff
# Add custom CSS in the style section
---
```

### Custom Themes

Create a custom theme file (e.g., `custom-theme.css`):

```css
/* custom-theme.css */
section {
  background-color: #1a1a1a;
  color: #ffffff;
}

h1 {
  color: #00ccff;
}
```

Then reference it:

```yaml
---
marp: true
theme: custom-theme
---
```

---

## 🔧 Troubleshooting

### Marp Extension Not Working
- Restart VS Code
- Check that the file has `.md` extension
- Verify Marp frontmatter is present at the top

### Code Blocks Not Rendering
- Ensure proper markdown syntax with triple backticks
- Specify language for syntax highlighting: ```python

### Diagrams Not Showing
- ASCII art diagrams should display in all viewers
- Mermaid diagrams require Marp or GitHub
- Use PowerPoint version for guaranteed compatibility

### Export Fails
- Check file permissions
- Ensure output directory exists
- Try exporting to a different format

---

## 📝 Editing the Slides

### Adding a New Slide

```markdown
---

# Your New Slide Title

Content goes here...

- Bullet point 1
- Bullet point 2

```

### Two-Column Layout

```markdown
<div class="columns">
<div>

## Left Column

Content here

</div>
<div>

## Right Column

Content here

</div>
</div>
```

### Code Highlighting

```markdown
​```python
# Python code with syntax highlighting
def example():
    return "Hello"
​```
```

### Speaker Notes (Reveal.js)

```markdown
Note: These are speaker notes that only appear in presenter mode
```

---

## 🚀 Quick Start Commands

```bash
# View in VS Code (with Marp extension)
code langgraph_presentation.md

# Export to PowerPoint via CLI
marp langgraph_presentation.md --pptx

# Export to PDF via CLI
marp langgraph_presentation.md --pdf

# Open existing PowerPoint
open langgraph_agents_presentation.pptx

# View Jupyter notebook
jupyter notebook langgraph_visualization.ipynb
```

---

## 📚 Additional Resources

### Marp
- Documentation: https://marp.app/
- VS Code Extension: https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode
- GitHub: https://github.com/marp-team/marp

### Reveal.js
- Documentation: https://revealjs.com/
- GitHub: https://github.com/hakimel/reveal.js

### Slidev
- Documentation: https://sli.dev/
- GitHub: https://github.com/slidevjs/slidev

### Pandoc
- Documentation: https://pandoc.org/
- User Guide: https://pandoc.org/MANUAL.html

---

## 💡 Tips

1. **For Meetings**: Use PowerPoint (`langgraph_agents_presentation.pptx`)
2. **For Documentation**: Use Markdown in GitHub/GitLab
3. **For Web Sharing**: Export to HTML with Marp or Reveal.js
4. **For Printing**: Export to PDF via Marp
5. **For Version Control**: Keep Markdown as source of truth

---

## ✅ Recommendation

**For most users**: Install the **Marp VS Code extension** and open `langgraph_presentation.md`. It provides:
- ✅ Live preview
- ✅ Export to PPTX, PDF, HTML
- ✅ No command-line needed
- ✅ Easy editing with instant preview

**For quick use**: Open `langgraph_agents_presentation.pptx` in PowerPoint.

---

## 🎯 Summary

You now have **three presentation formats**:

1. **Markdown** (`langgraph_presentation.md`) - 25 detailed slides
   - Text-based, version-controllable
   - View with Marp, export to any format

2. **PowerPoint** (`langgraph_agents_presentation.pptx`) - 14 slides
   - Ready to use in meetings
   - Visual diagrams and tables

3. **Jupyter Notebook** (`langgraph_visualization.ipynb`) - Interactive
   - Executable code examples
   - Graph visualizations

Choose the format that works best for your needs!
