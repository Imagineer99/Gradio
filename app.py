import gradio as gr
import time

def process_data(text: str) -> str:
    """Basic text processing function"""
    time.sleep(0.5)
    return text.upper()

def load_css():
    try:
        # Use relative path which works in both environments
        css_path = "static/style.css"
        
        with open(css_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load CSS file: {e}")
        return ""  # Return empty string if file can't be loaded

css_content = load_css()

with gr.Blocks(
    css=css_content,
    title="unsloth - Fast and Easy LLM Finetuning",
    analytics_enabled=False,
) as interface:
    gr.HTML("""
        <head>
            <meta property="og:title" content="unsloth - Fast and Easy LLM Finetuning">
            <meta property="og:description" content="Finetune your LLMs faster with unsloth - an easy-to-use interface for model training and optimization.">
            <meta property="og:image" content="https://raw.githubusercontent.com/unslothai/unsloth/main/images/unsloth.png">
            <meta name="twitter:card" content="summary_large_image">
            <meta name="twitter:title" content="unsloth - Fast and Easy LLM Finetuning">
            <meta name="twitter:description" content="Finetune your LLMs faster with unsloth - an easy-to-use interface for model training and optimization.">
            <meta name="twitter:image" content="https://raw.githubusercontent.com/unslothai/unsloth/main/images/unsloth.png">
        </head>
    """)
    
    # Top navigation bar
    with gr.Row():
        with gr.Column(scale=1):
            # Modified logo implementation
            with gr.Row(elem_classes=["logo-container"]):
                try:
                    gr.Image("logo.png", label=None, show_label=False, container=False)
                    gr.Markdown("# unsloth")
                except:
                    gr.Markdown("# unsloth")
        
        # Main navigation buttons
        with gr.Column(scale=3):
            with gr.Row(elem_classes=["navigation-buttons"]):
                nav_train = gr.Button("Train", elem_classes=["lg", "primary", "nav-train-btn"])
                nav_evaluate = gr.Button("Evaluate", elem_classes=["lg", "secondary", "nav-evaluate-btn"])
                nav_chat = gr.Button("Chat", elem_classes=["lg", "secondary", "nav-chat-btn"])
                nav_export = gr.Button("Export", elem_classes=["lg", "secondary", "nav-export-btn"])
        
        # Mode toggle buttons
        with gr.Column(scale=2):
            with gr.Row(elem_classes=["mode-toggle-buttons"]):
                mode_basic = gr.Button("Basic", variant="primary", elem_classes=["mode-basic-btn"])
                mode_advanced = gr.Button("Advanced", elem_classes=["mode-advanced-btn"])
    
    with gr.Column(elem_classes=["container"]):
        # Model selection section
        gr.Markdown("# Select a model:")
        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=[
                    "Llama-3.1-8B-Instruct",
                    "Mistral-7B-Instruct",
                    "Phi-2",
                    "Gemma-7B"
                ],  # Added more model options
                value="Llama-3.1-8B-Instruct",
                label="",
                interactive=True
            )
            model_search = gr.Textbox(
                placeholder="Search for a model",
                label="",
                interactive=True
            )
        
        with gr.Row():
            with gr.Column(elem_classes=["card"], scale=1):
                gr.Markdown("### Training Dataset:")
                upload_btn = gr.UploadButton(
                    "Upload JSON, CSV or Excel",
                    variant="secondary",
                )
                input_text = gr.Textbox(
                    placeholder="Type dataset from 🤗HF",
                    label="",
                    interactive=True
                )
            
            with gr.Column(elem_classes=["card"], scale=1):
                gr.Markdown("### Configure Parameters")
                with gr.Row():
                    learning_rate = gr.Slider(
                        minimum=0, maximum=100,
                        value=31,
                        label="Learning rate",
                        interactive=True,
                        step=1
                    )
                    lora_rank = gr.Slider(
                        minimum=0, maximum=100,
                        value=31,
                        label="LoRA rank",
                        interactive=True,
                        step=1
                    )
                with gr.Row():
                    context_length = gr.Slider(
                        minimum=0, maximum=100,
                        value=31,
                        label="Context length",
                        interactive=True,
                        step=1
                    )
                    batch_size = gr.Slider(
                        minimum=0, maximum=100,
                        value=31,
                        label="Batch size",
                        interactive=True,
                        step=1
                    )
        
        with gr.Row():
            start_btn = gr.Button(
                "♡ Start finetuning",
                variant="primary",
                elem_classes=["gr-button", "start-finetune-btn"]
            )
            

if __name__ == "__main__":
    interface.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="favicon-32x32.png"
    )
