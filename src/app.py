import gradio as gr
import PIL.Image as Image
import io
import base64
import json
from typing import Union

def analyze_image(image: Image.Image) -> str:
    """
    Analyze an image and return detailed information about it.
    
    Args:
        image: The image to analyze (can be base64 string or file upload)
    
    Returns:
        str: JSON string with image analysis including dimensions, format, mode, and orientation
    """
    if image is None:
        return json.dumps({"error": "No image provided"})
    
    try:
        # Get image properties
        width, height = image.size
        format_type = image.format or "Unknown"
        mode = image.mode
        orientation = "Portrait" if height > width else "Landscape" if width > height else "Square"
        
        # Calculate aspect ratio
        aspect_ratio = round(width / height, 2) if height > 0 else 0
        
        # Get color information
        colors = image.getcolors(maxcolors=256*256*256)
        dominant_colors = len(colors) if colors else "Many"
        
        analysis = {
            "dimensions": {"width": width, "height": height},
            "format": format_type,
            "mode": mode,
            "orientation": orientation,
            "aspect_ratio": aspect_ratio,
            "approximate_colors": dominant_colors,
            "file_info": f"{width}x{height} {format_type} image in {mode} mode"
        }
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error analyzing image: {str(e)}"})

def get_image_orientation(image: Image.Image) -> str:
    """
    Determine if an image is portrait, landscape, or square.
    
    Args:
        image: The image to check orientation
    
    Returns:
        str: "Portrait", "Landscape", or "Square"
    """
    if image is None:
        return "No image provided"
    
    try:
        width, height = image.size
        if height > width:
            return "Portrait"
        elif width > height:
            return "Landscape"
        else:
            return "Square"
    except Exception as e:
        return f"Error: {str(e)}"

def count_colors(image: Image.Image) -> str:
    """
    Count the approximate number of unique colors in an image.
    
    Args:
        image: The image to analyze for color count
    
    Returns:
        str: Description of color count and dominant color information
    """
    if image is None:
        return "No image provided"
    
    try:
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get colors (limit to prevent memory issues)
        colors = image.getcolors(maxcolors=256*256*256)
        
        if colors is None:
            return "Image has more than 16.7 million unique colors"
        
        # Sort by frequency
        colors.sort(key=lambda x: x[0], reverse=True)
        
        # Get top 3 colors
        top_colors = colors[:3]
        color_info = []
        
        for count, color in top_colors:
            if isinstance(color, tuple) and len(color) >= 3:
                r, g, b = color[:3]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                percentage = round((count / sum(c[0] for c in colors)) * 100, 1)
                color_info.append(f"RGB{color} ({hex_color}) - {percentage}%")
        
        result = f"Total unique colors: {len(colors)}\n"
        result += "Top colors by frequency:\n" + "\n".join(color_info)
        
        return result
        
    except Exception as e:
        return f"Error analyzing colors: {str(e)}"

def extract_text_info(image: Image.Image) -> str:
    """
    Extract basic information about text-like content in an image.
    
    Args:
        image: The image to analyze for text content
    
    Returns:
        str: Basic information about potential text content
    """
    if image is None:
        return "No image provided"
    
    try:
        # Convert to grayscale for analysis
        gray = image.convert('L')
        
        # Get image statistics
        extrema = gray.getextrema()
        
        # Simple heuristics for text detection
        contrast = extrema[1] - extrema[0]
        
        analysis = {
            "image_mode": image.mode,
            "grayscale_range": f"{extrema[0]} to {extrema[1]}",
            "contrast_level": "High" if contrast > 200 else "Medium" if contrast > 100 else "Low",
            "potential_text": "Likely contains text" if contrast > 150 else "May contain text" if contrast > 100 else "Unlikely to contain text",
            "note": "This is a basic analysis. For proper OCR, use specialized text extraction tools."
        }
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return f"Error analyzing for text: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Image Analysis MCP Server") as demo:
    gr.Markdown("""
    # Image Analysis MCP Server
    
    This Gradio app serves as an MCP server that can analyze images sent from Claude or other MCP clients.
    
    **Available Tools:**
    - `analyze_image`: Get comprehensive image analysis (dimensions, format, colors, etc.)
    - `get_image_orientation`: Check if image is portrait, landscape, or square
    - `count_colors`: Analyze color information and dominant colors
    - `extract_text_info`: Basic analysis for potential text content
    
    **Usage with Claude Desktop:**
    1. Deploy this to HuggingFace Spaces
    2. Add the MCP configuration to Claude Desktop
    3. Send images to Claude and ask it to analyze them using these tools
    """)
    
    # Create interface for each function (these will be exposed as MCP tools)
    with gr.Tab("Image Analysis"):
        with gr.Row():
            img_input1 = gr.Image(type="pil", label="Upload Image")
            analysis_output = gr.JSON(label="Analysis Result")
        analyze_btn = gr.Button("Analyze Image")
        analyze_btn.click(analyze_image, inputs=[img_input1], outputs=[analysis_output])
    
    with gr.Tab("Orientation Check"):
        with gr.Row():
            img_input2 = gr.Image(type="pil", label="Upload Image")
            orientation_output = gr.Textbox(label="Orientation")
        orientation_btn = gr.Button("Check Orientation")
        orientation_btn.click(get_image_orientation, inputs=[img_input2], outputs=[orientation_output])
    
    with gr.Tab("Color Analysis"):
        with gr.Row():
            img_input3 = gr.Image(type="pil", label="Upload Image")
            color_output = gr.Textbox(label="Color Analysis", lines=10)
        color_btn = gr.Button("Analyze Colors")
        color_btn.click(count_colors, inputs=[img_input3], outputs=[color_output])
    
    with gr.Tab("Text Detection"):
        with gr.Row():
            img_input4 = gr.Image(type="pil", label="Upload Image")
            text_output = gr.JSON(label="Text Analysis")
        text_btn = gr.Button("Analyze for Text")
        text_btn.click(extract_text_info, inputs=[img_input4], outputs=[text_output])

if __name__ == "__main__":
    # Launch with MCP server enabled
    demo.launch(mcp_server=True, share=True)