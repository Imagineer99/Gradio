import gradio as gr

def create_train_interface():
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

    # Main Layout
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
                    info="Controls how much the model adjusts its weights during training.",
                    allow_custom_value=True,
                    interactive=True
                )
                num_epochs = gr.Slider(
                    minimum=1, maximum=20,
                    value=4,
                    label="Number of epochs",
                    info="Number of times the model will see the entire dataset",
                    step=1,
                    interactive=True
                )
                max_sequence_length = gr.Textbox(
                    value="2048",
                    label="Max Sequence Length",
                    info="Maximum sequence length for the model. Choose any!",
                    interactive=True
                )

        # Progress Card
        with gr.Column(elem_classes=["card"], scale=1):
            gr.Markdown("## Training Progress")
            loss_plot = gr.Plot(
                label="Training Loss",
                show_label=True,
            )

    # Advanced Mode Toggle
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
            # LoRA Adapter Settings
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
                    info="Specifies which model layers to apply LoRA fine-tuning to",
                    multiselect=True,
                    interactive=True
                )
                lora_r = gr.Slider(
                    minimum=1, maximum=128, value=16,
                    label="LoRA rank (r)",
                    info="Controls the capacity and compression ratio of LoRA adapters",
                    interactive=True
                )
                lora_alpha = gr.Slider(
                    minimum=1, maximum=128, value=16,
                    label="LoRA alpha",
                    info="Scaling factor for LoRA updates during training",
                    interactive=True
                )
                lora_dropout = gr.Slider(
                    minimum=0, maximum=1, value=0,
                    label="LoRA dropout",
                    info="Adds regularization to prevent overfitting during training",
                    interactive=True
                )
                gradient_checkpointing = gr.Dropdown(
                    choices=["none", "true", "unsloth"],
                    value="unsloth",
                    label="Gradient Checkpointing",
                    info="Memory optimization technique that trades computation for memory",
                    interactive=True
                )
                use_rslora = gr.Checkbox(
                    value=False,
                    label="Use RS-LoRA",
                    info="Stabilizes training by maintaining consistent rank throughout layers",
                    interactive=True
                )
                use_loftq = gr.Checkbox(
                    value=False,
                    label="Use LoftQ",
                    info="Quantization method that improves memory efficiency of LoRA",
                    interactive=True
                )

         # Training Optimization       
            with gr.Column(scale=1):
                gr.Markdown("### Training Optimization")
                weight_decay = gr.Slider(
                    minimum=0, maximum=0.1, value=0.01, 
                    label="Weight Decay",
                    info="Regularization technique that reduces model complexity by penalizing large weights",
                    interactive=True
                )
                random_seed = gr.Number(
                    value=3407,
                    label="Random Seed",
                    info="Controls randomness in training for reproducible results",
                    precision=0,
                    interactive=True
                )
                batch_size = gr.Slider(
                    minimum=1, maximum=32,
                    value=2,
                    label="Batch size",
                    info="Number of training examples processed together in one forward/backward pass",
                    step=1,
                    interactive=True
                )
                grad_accumulation = gr.Slider(
                    minimum=1, maximum=16,
                    value=4,
                    label="Gradient accumulation steps",
                    info="Simulates larger batch sizes by accumulating gradients over multiple forward passes",
                    step=1,
                    interactive=True
                )
                warmup_steps = gr.Slider(
                    minimum=0, maximum=100, value=5,
                    label="Warmup Steps",
                    info="Number of steps for learning rate warmup",
                    step=1,
                    interactive=True
                )
                max_steps = gr.Slider(
                    minimum=0, maximum=1000, value=0,
                    label="Max Steps",
                    info="Maximum number of training steps. When 0, uses number of epochs instead",
                    step=1,
                    interactive=True
                )
                max_seq_length = gr.Slider(
                    minimum=32, maximum=4096, value=512,
                    label="Max Sequence Length",
                    info="Maximum length of input sequences. Longer sequences will be truncated",
                    step=32,
                    interactive=True
                )
                dataset_text_field = gr.Textbox(
                    value="text",
                    label="Dataset Text Field",
                    info="Name of the column in your dataset that contains the text to train on",
                    interactive=True
                )
                packing = gr.Checkbox(
                    value=False,
                    label="Enable Sequence Packing",
                    info="Optimizes memory usage by combining multiple sequences into single training examples",
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
    # Toggle basic mode
    mode_basic.click(
        toggle_advanced_mode,
        inputs=[gr.State(False)],
        outputs=[advanced_params, mode_advanced, mode_basic, basic_params]
    )
    # Toggle advanced mode
    mode_advanced.click(
        toggle_advanced_mode,
        inputs=[gr.State(True)],
        outputs=[advanced_params, mode_advanced, mode_basic, basic_params]
    )

    # Components dictionary
    return {
        'model_dropdown': model_dropdown,
        'model_search': model_search,
        'load_4bit': load_4bit,
        'learning_rate': learning_rate,
        'num_epochs': num_epochs,
        'loss_plot': loss_plot,
        'start_btn': start_btn,
        'warmup_steps': warmup_steps,
        'max_steps': max_steps,
        'max_seq_length': max_seq_length,
        'dataset_text_field': dataset_text_field,
        'packing': packing,
        'target_modules': target_modules,
        'lora_r': lora_r,
        'lora_alpha': lora_alpha,
        'lora_dropout': lora_dropout,
        'gradient_checkpointing': gradient_checkpointing,
        'use_rslora': use_rslora,
        'use_loftq': use_loftq,
        'max_sequence_length': max_sequence_length,
        'input_text': input_text,
        'upload_btn': upload_btn,
        'random_seed': random_seed,
        'weight_decay': weight_decay,
        'batch_size': batch_size,
        'grad_accumulation': grad_accumulation
    } 