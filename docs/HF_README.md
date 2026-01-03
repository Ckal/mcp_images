---
title: Mcp Images Server
emoji:  🖼️
colorFrom: gray
colorTo: red
sdk: gradio
sdk_version: 5.34.0
app_file: app.py
pinned: false
tags:
  - images
  - mcp-server
  
---
  

# Image Analysis MCP Server

This Gradio application serves as an MCP (Model Control Protocol) server that provides image analysis tools for LLMs like Claude.

## 🔧 Available Tools

- **analyze_image**: Comprehensive image analysis including dimensions, format, colors, and orientation
- **get_image_orientation**: Determine if an image is portrait, landscape, or square
- **count_colors**: Analyze color information and identify dominant colors
- **extract_text_info**: Basic analysis for potential text content in images

## 🚀 Usage with Claude Desktop

To use this MCP server with Claude Desktop, add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "image-analysis": {
      "url": "https://YOUR_USERNAME-image-analysis-mcp.hf.space/gradio_api/mcp/sse"
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual HuggingFace username.

## 📝 Example Prompts

Once configured, you can ask Claude:

- "Analyze this image for me"
- "What are the dominant colors in this photo?"
- "Is this image portrait or landscape?"
- "Does this image contain text?"

Claude will automatically use these tools to provide detailed image analysis!

## 🔍 How It Works

1. Upload an image to Claude or paste an image
2. Claude automatically converts the image to base64
3. Claude calls the appropriate MCP tool on this server
4. The server processes the image using PIL (Python Imaging Library)
5. Results are returned to Claude and presented to you

## 🛠️ Technical Details

- Built with **Gradio** and **PIL (Pillow)**
- Accepts images in various formats (JPEG, PNG, GIF, etc.)
- Automatically handles base64 image data from MCP clients
- Provides JSON-formatted analysis results
- Includes error handling for invalid inputs

## 📋 Requirements

- `gradio[mcp]>=4.0.0`
- `Pillow>=9.0.0`

## 🔗 Links

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Gradio MCP Guide](https://www.gradio.app/guides/building-an-mcp-server-with-gradio)
- [Claude Desktop](https://claude.ai/desktop)

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
