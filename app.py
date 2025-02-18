import gradio as gr
import time

def process_data(text: str) -> str:
    """Basic text processing function"""
    time.sleep(0.5)
    return text.upper()

def load_css():
    try:
        # Use relative path which works in both environments
        css_path = "static/style.css" # <-- change to style.css 
        
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
    
    # Top nav bar
    with gr.Row():
        with gr.Column(scale=1):
            # Logo implementation
            with gr.Row(elem_classes=["logo-container"]):
                try:
                    gr.Image("logo.png", label=None, show_label=False, container=False)
                    gr.Markdown("# unsloth")
                except:
                    gr.Markdown("# unsloth")
        
        # Main nav buttons
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
        gr.Markdown("## Model Selection", elem_classes=["section-header"])
        with gr.Row(elem_classes=["model-selection-container"]):
            with gr.Column(scale=2):
                model_dropdown = gr.Dropdown(
                    choices=[
                        "Llama-3.1-8B-Instruct",
                        "Mistral-7B-Instruct",
                        "Phi-2",
                        "Gemma-7B"
                    ],
                    value="Llama-3.1-8B-Instruct",
                    label="Select Model",
                    interactive=True,
                )
            with gr.Column(scale=1):
                model_search = gr.Textbox(
                    placeholder="Search for a model",
                    label="Search",
                    interactive=True,
                )

        with gr.Row(elem_classes=["main-content"]):
            # Left column: Dataset
            with gr.Column(elem_classes=["card"], scale=1):
                gr.Markdown("## Training Dataset", elem_classes=["section-header"])
                upload_btn = gr.UploadButton(
                    "Upload JSON, CSV or Excel",
                    variant="secondary",
                )
                input_text = gr.Textbox(
                    placeholder="Type dataset from 🤗HF",
                    label="HuggingFace Dataset",
                    interactive=True,
                )
            
            # Middle column: Basic Parameters
            with gr.Column(elem_classes=["card"], scale=1) as basic_params:
                gr.Markdown("## Training Parameters", elem_classes=["section-header"])
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
                        interactive=True,
                        step=1
                    )
                    batch_size = gr.Slider(
                        minimum=1, maximum=32,
                        value=2,
                        label="Batch size",
                        interactive=True,
                        step=1
                    )
                    grad_accumulation = gr.Slider(
                        minimum=1, maximum=16,
                        value=4,
                        label="Gradient accumulation steps",
                        interactive=True,
                        step=1
                    )

            # Right column: Training Progress
            with gr.Column(elem_classes=["card"], scale=1) as training_progress:
                gr.Markdown("## Training Progress", elem_classes=["section-header"])
                loss_plot = gr.Plot(
                    label="Training Loss",
                    show_label=True,
                )

        # Advanced parameters section (initially hidden)
        with gr.Column(elem_classes=["card"], scale=1, visible=False) as advanced_params:
            gr.Markdown("### LoRA Adapter Settings")
            with gr.Row():
                lora_r = gr.Slider(
                    minimum=1, maximum=128,
                    value=16,
                    label="LoRA rank (r)",
                    info="Suggested: 8, 16, 32, 64, 128",
                    interactive=True,
                    step=1
                )
                lora_alpha = gr.Slider(
                    minimum=1, maximum=128,
                    value=16,
                    label="LoRA alpha",
                    interactive=True,
                    step=1
                )
            with gr.Row():
                lora_dropout = gr.Slider(
                    minimum=0, maximum=1,
                    value=0,
                    label="LoRA dropout",
                    info="0 is optimized",
                    interactive=True,
                    step=0.1
                )
                use_rslora = gr.Checkbox(
                    value=True,
                    label="Use RS-LoRA",
                    info="Rank stabilized LoRA"
                )

            gr.Markdown("### Training Optimization")
            with gr.Row():
                weight_decay = gr.Slider(
                    minimum=0, maximum=0.1,
                    value=0.01,
                    label="Weight Decay",
                    interactive=True,
                    step=0.001
                )
                warmup_ratio = gr.Slider(
                    minimum=0, maximum=0.5,
                    value=0.1,
                    label="Warmup Ratio",
                    interactive=True,
                    step=0.01
                )
            with gr.Row():
                lr_scheduler = gr.Dropdown(
                    choices=["cosine", "linear", "constant", "constant_with_warmup"],
                    value="cosine",
                    label="LR Scheduler",
                    info="Cosine is recommended",
                    interactive=True
                )
                gradient_checkpointing = gr.Dropdown(
                    choices=["none", "true", "unsloth"],
                    value="unsloth",
                    label="Gradient Checkpointing",
                    info="'unsloth' uses 30% less VRAM",
                    interactive=True
                )

            gr.Markdown("### Experiment Tracking")
            with gr.Row():
                use_wandb = gr.Checkbox(
                    value=False,
                    label="Enable WandB logging",
                    info="Track your training metrics with Weights & Biases"
                )
                wandb_project = gr.Textbox(
                    value="unsloth-finetune",
                    label="WandB Project Name",
                    interactive=True,
                    visible=False  # Initially hidden until WandB is enabled
                )
            with gr.Row(visible=False) as wandb_options:
                wandb_name = gr.Textbox(
                    value="",
                    placeholder="my-experiment-name",
                    label="Experiment Name",
                    interactive=True
                )
                wandb_tags = gr.Textbox(
                    value="",
                    placeholder="tag1,tag2,tag3",
                    label="Tags (comma-separated)",
                    interactive=True
                )

        # Add click handlers for mode toggle
        def toggle_advanced_mode(advanced: bool):
            # Only update visibility and button styles, not the parameter values
            return {
                advanced_params: gr.update(visible=advanced),
                mode_advanced: gr.update(variant="primary" if advanced else "secondary"),
                mode_basic: gr.update(variant="secondary" if advanced else "primary"),
                # Keep the basic params section always visible
                basic_params: gr.update(visible=True)
            }

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

        # Add visibility toggle for WandB options
        def toggle_wandb_options(enabled):
            return {
                wandb_project: gr.update(visible=enabled),
                wandb_options: gr.update(visible=enabled)
            }

        use_wandb.change(
            fn=toggle_wandb_options,
            inputs=[use_wandb],
            outputs=[wandb_project, wandb_options]
        )

        with gr.Row():
            start_btn = gr.Button(
                "♡ Start finetuning",
                variant="primary",
                elem_classes=["gr-button", "start-finetune-btn"],
            )
        

if __name__ == "__main__":
    demo.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="favicon-32x32.png",
    )
