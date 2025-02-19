import gradio as gr
import time
import os

def process_data(text: str) -> str:
    """Basic text processing function"""
    time.sleep(0.5)
    return text.upper()

def load_css():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, "static", "styles.css")
        print(f"Looking for CSS at: {css_path}")
        
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to load CSS: {e}")
        return ""

css_content = load_css()
with gr.Blocks(
    css=css_content,
    title="unsloth - Fast and Easy LLM Finetuning",
    analytics_enabled=False,
) as demo:
    # Meta tags for social media
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
    
    # Header Section
    with gr.Row(elem_classes=["header"]):
        with gr.Column(scale=1):
            with gr.Row(elem_classes=["logo-container"]):
                try:
                    gr.Image("logo.png", label=None, show_label=False, container=False)
                    gr.Markdown("# unsloth")
                except:
                    gr.Markdown("# unsloth")
        
        with gr.Column(scale=3):
            with gr.Row(elem_classes=["navigation-buttons"]):
                nav_train = gr.Button("Train", elem_classes=["lg", "primary", "nav-train-btn", "nav-button"])
                nav_evaluate = gr.Button("Evaluate", elem_classes=["lg", "secondary", "nav-evaluate-btn", "nav-button"])
                nav_chat = gr.Button("Chat", elem_classes=["lg", "secondary", "nav-chat-btn", "nav-button"])
                nav_export = gr.Button("Export", elem_classes=["lg", "secondary", "nav-export-btn", "nav-button"])
        
        with gr.Column(scale=2):
            gr.Row()  # Spacer for layout balance

    # Main Content
    with gr.Column(elem_classes=["main-container"]):
        # Model Selection Card
        with gr.Column(elem_classes=["card", "model-selection-card"]):
            gr.Markdown("## Model Selection")
            with gr.Row():
                model_dropdown = gr.Dropdown(
                    choices=[
                        "unsloth/Meta-Llama-3.1-8B-bnb-4bit",
                        "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
                        "unsloth/Meta-Llama-3.1-70B-bnb-4bit",
                        "unsloth/Meta-Llama-3.1-405B-bnb-4bit",
                        "unsloth/Mistral-Nemo-Base-2407-bnb-4bit",
                        "unsloth/Mistral-Nemo-Instruct-2407-bnb-4bit",
                        "unsloth/mistral-7b-v0.3-bnb-4bit",
                        "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
                        "unsloth/Phi-3.5-mini-instruct",
                        "unsloth/Phi-3-medium-4k-instruct",
                        "unsloth/gemma-2-9b-bnb-4bit",
                        "unsloth/gemma-2-27b-bnb-4bit"
                    ],
                    value="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
                    label="Select Model",
                    interactive=True,
                    scale=3
                )
                model_search = gr.Textbox(
                    placeholder="Search for a model",
                    label="Search",
                    interactive=True,
                    scale=1
                )
                load_4bit = gr.Checkbox(
                    value=True,
                    label="Load in 4-bit",
                    info="Enable 4-bit quantization to reduce memory usage. Recommended for most cases.",
                    interactive=True,
                    scale=1
                )

        # Main Three-Column Layout
        with gr.Row(elem_classes=["content-cards"]):
            # Dataset Card
            with gr.Column(elem_classes=["card"], scale=1):
                gr.Markdown("## Training Dataset")
                upload_btn = gr.UploadButton(
                    "Upload JSON, CSV or Excel",
                    variant="secondary",
                    elem_classes=["upload-button"],
                )
                input_text = gr.Textbox(
                    placeholder="Type dataset from 🤗",
                    label="HuggingFace Dataset",
                    interactive=True,
                )
            
            # Parameters Card
            with gr.Column(elem_classes=["card"], scale=1) as basic_params:
                gr.Markdown("## Training Parameters")
                with gr.Column():
                    learning_rate = gr.Dropdown(
                        choices=["1e-5", "2e-5", "5e-5", "1e-4", "2e-4", "5e-4", "1e-3"],
                        value="5e-5",
                        label="Learning rate",
                        info="Typically between 1e-5 to 1e-3",
                        allow_custom_value=True,
                        interactive=True
                    )
                    num_epochs = gr.Slider(
                        minimum=1, maximum=20,
                        value=4,
                        label="Number of epochs",
                        step=1,
                        interactive=True
                    )

            # Progress Card
            with gr.Column(elem_classes=["card"], scale=1):
                gr.Markdown("## Training Progress")
                loss_plot = gr.Plot(
                    label="Training Loss",
                    show_label=True,
                )

        # Mode Toggle
        with gr.Row(elem_classes=["mode-toggle-container"]):
            with gr.Column(scale=3):
                gr.Row()  # Left spacer
            with gr.Column(scale=2):
                with gr.Row(elem_classes=["mode-toggle-buttons"]):
                    mode_basic = gr.Button("Basic", variant="primary", elem_classes=["mode-basic-btn"])
                    mode_advanced = gr.Button("Advanced", elem_classes=["mode-advanced-btn"])
            with gr.Column(scale=3):

                gr.Row()  # Right spacer
        # Advanced Parameters Section (Initially Hidden)
        with gr.Column(elem_classes=["card", "advanced-params"], visible=False) as advanced_params:
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### LoRA Adapter Settings")
                    target_modules = gr.Dropdown(
                        choices=[
                            "q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"
                        ],
                        value=["q_proj", "k_proj", "v_proj", "o_proj",
                              "gate_proj", "up_proj", "down_proj"],
                        label="Target Modules",
                        multiselect=True,
                        interactive=True
                    )
                    lora_r = gr.Slider(
                        minimum=1, maximum=128, value=16,
                        label="LoRA rank (r)",
                        info="Suggested values: 8, 16, 32, 64, 128",
                        interactive=True
                    )
                    lora_alpha = gr.Slider(
                        minimum=1, maximum=128, value=16,
                        label="LoRA alpha",
                        interactive=True
                    )
                    lora_dropout = gr.Slider(
                        minimum=0, maximum=1, value=0,
                        label="LoRA dropout",
                        info="0 is optimized for best performance",
                        interactive=True
                    )
                    use_rslora = gr.Checkbox(
                        value=True, 
                        label="Use RS-LoRA",
                        interactive=True
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### Training Optimization")
                    weight_decay = gr.Slider(
                        minimum=0, maximum=0.1, value=0.01, 
                        label="Weight Decay",
                        interactive=True
                    )
                    gradient_checkpointing = gr.Dropdown(
                        choices=["none", "true", "unsloth"],
                        value="unsloth",
                        label="Gradient Checkpointing",
                        info="'unsloth' uses 30% less VRAM",
                        interactive=True
                    )
                    use_rslora = gr.Checkbox(
                        value=False,
                        label="Use RS-LoRA",
                        info="Rank stabilized LoRA for better training stability",
                        interactive=True
                    )
                    random_seed = gr.Number(
                        value=3407,
                        label="Random Seed",
                        precision=0,
                        interactive=True
                    )
                    use_loftq = gr.Checkbox(
                        value=False,
                        label="Use LoftQ",
                        info="Low-rank factorization with quantization",
                        interactive=True
                    )
                    batch_size = gr.Slider(
                        minimum=1, maximum=32,
                        value=2,
                        label="Batch size",
                        step=1,
                        interactive=True
                    )
                    grad_accumulation = gr.Slider(
                        minimum=1, maximum=16,
                        value=4,
                        label="Gradient accumulation steps",
                        step=1,
                        interactive=True
                    )
        # Start Training Button
        with gr.Row(elem_classes=["footer"]):
            start_btn = gr.Button(
                "♡ Start finetuning",
                variant="primary",
                elem_classes=["gr-button", "start-finetune-btn"],
            )

        # Event Handlers
        def toggle_advanced_mode(advanced: bool):
            return [
                gr.update(visible=advanced),
                gr.update(variant="primary" if advanced else "secondary"),
                gr.update(variant="secondary" if advanced else "primary"),
                gr.update(visible=True)
            ]

        mode_basic.click(
            toggle_advanced_mode,
            inputs=[gr.State(False)],
            outputs=[advanced_params, mode_advanced, mode_basic, basic_params]
        )
        
        mode_advanced.click(
            toggle_advanced_mode,
            inputs=[gr.State(True)],
            outputs=[advanced_params, mode_advanced, mode_basic, basic_params]
        )

if __name__ == "__main__":
    demo.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="favicon-32x32.png",
    )
    
