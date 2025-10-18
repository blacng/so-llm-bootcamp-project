# LangGraph Presentations & Visualizations

This directory contains multiple formats for presenting and understanding the LangGraph agent architectures.

## 📁 Available Formats

### 1. **Markdown Slides** (Recommended for editing)
- **File**: `langgraph_presentation.md`
- **Slides**: 25 comprehensive slides
- **Format**: Marp-compatible Markdown
- **Best for**: Version control, easy editing, multi-format export

### 2. **PowerPoint** (Recommended for meetings)
- **File**: `langgraph_agents_presentation.pptx`
- **Slides**: 14 professionally formatted slides
- **Format**: Microsoft PowerPoint (.pptx)
- **Best for**: Corporate meetings, traditional presentations

### 3. **Jupyter Notebook** (Recommended for learning)
- **File**: `langgraph_visualization.ipynb`
- **Format**: Interactive Python notebook
- **Best for**: Learning, code experimentation, graph visualization

### 4. **Generator Script**
- **File**: `generate_langgraph_presentation.py`
- **Purpose**: Regenerate PowerPoint from scratch
- **Usage**: `python generate_langgraph_presentation.py`

---

## 🚀 Quick Start

### View Markdown Slides (Easiest)

**Option A: VS Code with Marp Extension**
1. Install "Marp for VS Code" extension
2. Open `langgraph_presentation.md`
3. Click "Preview" button (top-right)
4. Export to PPTX, PDF, or HTML as needed

**Option B: Command Line**
```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Export to PowerPoint
marp langgraph_presentation.md --pptx -o output.pptx

# Export to PDF
marp langgraph_presentation.md --pdf -o output.pdf
```

### Open PowerPoint (Instant)
```bash
# macOS
open langgraph_agents_presentation.pptx

# Windows
start langgraph_agents_presentation.pptx

# Linux
xdg-open langgraph_agents_presentation.pptx
```

### Run Jupyter Notebook (Interactive)
```bash
# Start Jupyter
jupyter notebook langgraph_visualization.ipynb

# Or use VS Code Jupyter extension
code langgraph_visualization.ipynb
```

---

## 📊 Content Overview

All presentations cover:

### 🔷 Agentic RAG Workflow
- **Architecture**: START → classify_mode → retrieve → generate → END
- **Node Details**: Classification, retrieval, generation logic
- **State Management**: TypedDict-based state flow
- **Features**: Mode-adaptive retrieval, PII anonymization, caching

### 🔶 ReAct Agent
- **Architecture**: Cyclic agent-tool loop with conditional edges
- **Tool Integration**: Tavily web search with 5 results
- **Features**: Streaming, multi-step reasoning, timeout protection

### 📈 Comparisons
- Side-by-side feature comparison
- Use case recommendations
- Performance characteristics

### 💻 Implementation
- Code examples from the codebase
- File references with line numbers
- Integration with Streamlit

---

## 🎯 Which Format Should I Use?

### For Corporate Presentations
→ Use `langgraph_agents_presentation.pptx`
- Professional styling
- Works everywhere
- No setup required

### For Technical Documentation
→ Use `langgraph_presentation.md`
- Version controllable
- Easy to update
- Can be viewed on GitHub

### For Learning/Teaching
→ Use `langgraph_visualization.ipynb`
- Interactive code
- Live graph visualization
- Executable examples

### For Custom Exports
→ Use `langgraph_presentation.md` with Marp
- Export to any format
- Customize themes
- Automated CI/CD

---

## 🎨 Customization

### Modify Markdown Slides
Edit `langgraph_presentation.md`:
```markdown
---

# Your New Slide Title

Content here...

---
```

### Regenerate PowerPoint
Edit and run the generator:
```bash
python generate_langgraph_presentation.py
```

### Update Notebook
Open `langgraph_visualization.ipynb` in Jupyter and edit cells.

---

## 📚 Detailed Guide

See `PRESENTATION_GUIDE.md` for:
- Complete usage instructions for all tools
- Troubleshooting tips
- Theme customization
- Export options
- Keyboard shortcuts

---

## 🔧 Dependencies

### For Markdown Slides (Marp)
```bash
# VS Code Extension (recommended)
# Search "Marp for VS Code" in VS Code extensions

# OR CLI
npm install -g @marp-team/marp-cli
```

### For PowerPoint Generation
```bash
pip install python-pptx
```

### For Jupyter Notebook
```bash
# Already installed with project dependencies
pip install jupyter ipykernel
```

---

## 📝 File Structure

```
.
├── langgraph_presentation.md              # Markdown slides (25 slides)
├── langgraph_agents_presentation.pptx     # PowerPoint (14 slides)
├── langgraph_visualization.ipynb          # Jupyter notebook
├── generate_langgraph_presentation.py     # PowerPoint generator
├── PRESENTATION_GUIDE.md                  # Detailed usage guide
└── PRESENTATIONS_README.md                # This file
```

---

## 🎓 Presentation Content

### Slide Topics

1. **Introduction** (Slides 1-2)
   - Title and overview

2. **RAG Architecture** (Slides 3-6)
   - Flow diagram
   - Node explanations
   - State management
   - Key features

3. **ReAct Architecture** (Slides 7-8)
   - Cyclic flow diagram
   - Features and capabilities

4. **Comparison** (Slides 9-10)
   - Feature comparison table
   - Use case recommendations

5. **Implementation** (Slides 11-12)
   - Code examples
   - Graph construction

6. **Advanced Topics** (Slides 13-16)
   - File references
   - Node functions
   - Caching system
   - PII anonymization

7. **Visualization** (Slide 17)
   - Graph visualization techniques

8. **Performance** (Slide 18)
   - Optimization strategies

9. **Integration** (Slide 19)
   - Streamlit integration example

10. **Conclusion** (Slides 20-22)
    - Key takeaways
    - Next steps
    - Resources

11. **Appendix** (Slides 23-25)
    - State types
    - Error handling

---

## 🌟 Highlights

### Markdown Presentation
- ✅ 608 lines of content
- ✅ ASCII art diagrams
- ✅ Syntax-highlighted code blocks
- ✅ Two-column layouts
- ✅ Custom CSS styling
- ✅ Marp frontmatter configuration

### PowerPoint Presentation
- ✅ 14 professionally designed slides
- ✅ Visual flow diagrams with shapes
- ✅ Color-coded nodes
- ✅ Comparison tables
- ✅ Code examples with monospace fonts
- ✅ Consistent branding

### Jupyter Notebook
- ✅ Executable Python code
- ✅ Live graph compilation
- ✅ Visual diagram generation
- ✅ Detailed markdown explanations
- ✅ State management examples

---

## 💡 Tips

1. **For Version Control**: Keep Markdown as source of truth
2. **For Meetings**: Use PowerPoint for compatibility
3. **For Learning**: Start with Jupyter notebook
4. **For Documentation**: Markdown renders on GitHub
5. **For Web Sharing**: Export Markdown to HTML

---

## 🔗 Related Files

- `CLAUDE.md` - Full project architecture documentation
- `README.md` - Project setup and installation
- `langchain_helpers.py` - Source code for agents
- `pages/` - Streamlit pages using the agents

---

## 📞 Support

For detailed instructions, see:
- `PRESENTATION_GUIDE.md` - Complete usage guide
- `CLAUDE.md` - Project architecture
- Marp documentation: https://marp.app/

---

## ✅ Summary

You have **three presentation formats** ready to use:

| Format | File | Slides | Best For |
|--------|------|--------|----------|
| Markdown | `langgraph_presentation.md` | 25 | Editing, version control |
| PowerPoint | `langgraph_agents_presentation.pptx` | 14 | Meetings, sharing |
| Notebook | `langgraph_visualization.ipynb` | Interactive | Learning, coding |

**Recommendation**:
- Start with the **PowerPoint** for immediate use
- Use **Markdown** for long-term maintenance
- Explore the **Notebook** to understand the code

Enjoy your presentations! 🎉
