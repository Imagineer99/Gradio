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
                scale=3,
            )
            with gr.Column(elem_classes=["model-selection-card"]):
                model_search = gr.Textbox(
                    placeholder="Search for a model",
                    label="Search",
                    interactive=True,
                    scale=1,    
                    elem_classes="search-input-with-icon",
            )
            hf_token = gr.Textbox(
                placeholder="Enter your token",
                label="Hugging Face",
                interactive=True,
                scale=1,
                elem_classes="token-input",
            )
            load_4bit = gr.Checkbox(
                value=True,
                label="Load in 4-bit",
                info="Reduce VRAM use",
                interactive=True,
                scale=1,
                elem_classes="load-4bit-checkbox",
            )

    # Main Layout with Three Columns for Dataset, Parameters, and Progress
    with gr.Row():
        # Left Column - Dataset
        with gr.Column(scale=1):
            with gr.Column(elem_classes=["card", "training-dataset-card"]):
                gr.Markdown("## Training Dataset")
                with gr.Column():
                    with gr.Row():  
                        input_text = gr.Textbox(
                            placeholder="Type dataset from 🤗",
                            label="Hugging Face Dataset",
                            interactive=True,
                            scale=1,
                        )
                        data_template = gr.Dropdown(
                            choices=[
                                "Alpaca",
                                "Auto-Select",
                                "ShareGPT",
                                "OpenAssistant",
                                "Anthropic Claude",
                                "GPTeacher",
                                "CodeAlpaca",
                                "Dolly",
                                "Baize",
                                "OpenOrca",
                                "WizardLM",
                                "Platypus",
                                "Vicuna",
                                "LIMA",
                                "Custom"
                            ],
                            value="Auto-Select",
                            label="Dataset Template",
                            interactive=True,
                            scale=1,
                        )

                    # Scan for local JSON datasets
                    def get_json_datasets():
                        import glob
                        import os
                        json_files = glob.glob("datasets/*.json")  # Adjust path as needed
                        return [os.path.basename(f) for f in json_files]

                    with gr.Column():
                        local_datasets = gr.Dropdown(
                            choices=get_json_datasets(),
                            label="Local Datasets",
                            #info="Select one or more JSON datasets to combine",
                            multiselect=True,
                            interactive=True,
                            elem_classes="local-datasets-dropdown",
                            value=get_json_datasets()[0] if get_json_datasets() else None
                        )
                        # Nested row for buttons
                        with gr.Row():
                            upload_btn = gr.UploadButton(
                                "Upload Files",
                                file_types=[".json", ".csv", ".xlsx", ".xls"],
                                elem_classes=["upload-button"],
                                scale=2,
                            )            
                            combine_btn = gr.Button(
                                "Combine",
                                elem_classes=["combine-datasets-btn"],
                                scale=1,
                            )

        # Middle Column - Basic Parameters
        with gr.Column(scale=1):
            with gr.Column(elem_classes=["card", "basic-params-card", "Configure-Parameters-Card"]) as basic_params:
                gr.Markdown("## Configure Parameters")
                with gr.Column():
                    num_epochs = gr.Slider(
                        minimum=1, maximum=20,
                        value=4,
                        label="Number of epochs",
                        info="Times the model will see the entire dataset",
                        step=1,
                        interactive=True
                    )                                       
                    max_sequence_length = gr.Textbox(
                        value="2048",
                        label="Max Context Length",
                        info="Maximum sequence length for the model",
                        interactive=True
                    )

        # Right Column - Training Progress
        with gr.Column(scale=1):
            with gr.Column(elem_classes=["card", "training-progress-card"]):
                gr.Markdown("## Training Progress")
                loss_plot = gr.Plot(
                    label="Training Loss",
                    show_label=True,
                    elem_classes=["plot-container"],
                    container=False
                )
                with gr.Row():
                    start_btn = gr.Button(  
                        "Start finetuning",
                        variant="primary", 
                        elem_classes=["gr-button", "start-finetune-btn"],
                        interactive=True,
                    )                    
                    stop_btn = gr.Button(
                        "Stop",
                        variant="stop",
                        elem_classes=["gr-button", "stop-finetune-btn"],
                        interactive=False,
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
    with gr.Column(visible=False) as advanced_params:
        with gr.Column(elem_classes=["advanced-params"]):
            # First Row - LoRA Adapter Settings
            with gr.Row():
                with gr.Column(elem_classes=["card", "compact-card"]):
                    gr.Markdown("## LoRA Adapter Settings")
                    
                    # Group 1: Core LoRA Parameters
                    with gr.Row():
                        with gr.Column(scale=1):
                            lora_r = gr.Slider(
                                minimum=1, maximum=128, value=16,
                                label="LoRA rank (r)",
                                info="Controls adapter capacity",
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            lora_alpha = gr.Slider(
                                minimum=1, maximum=128, value=16,
                                label="LoRA alpha",
                                info="Scaling factor",
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            lora_dropout = gr.Slider(
                                minimum=0, maximum=1, value=0,
                                label="LoRA dropout",
                                info="Regularization",
                                interactive=True
                            )

                    # Group 2: Target Modules and Gradient Checkpointing side by side
                    with gr.Row():
                        with gr.Column(scale=2):
                            target_modules = gr.Dropdown(
                                choices=[
                                    "q_proj", "k_proj", "v_proj", "o_proj",
                                    "gate_proj", "up_proj", "down_proj"
                                ],
                                value=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                                label="Target Modules",
                                info="Model layers for LoRA fine-tuning",
                                multiselect=True,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            gradient_checkpointing = gr.Dropdown(
                                choices=["none", "true", "unsloth"],
                                value="unsloth",
                                label="Gradient Checkpointing",
                                info="Memory optimization",
                                interactive=True
                            )

                    # Group 3: Advanced Options - More compact checkbox layout
                    with gr.Row():
                        with gr.Column(elem_classes=["checkbox-group"]):
                            with gr.Row():
                                with gr.Column(scale=1, min_width=100):
                                    use_rslora = gr.Checkbox(
                                        value=False,
                                        label="RS-LoRA",
                                        info="Stable rank training",
                                        interactive=True,
                                        elem_classes=["checkbox"]
                                    )
                                with gr.Column(scale=1, min_width=100):
                                    use_loftq = gr.Checkbox(
                                        value=False,
                                        label="LoftQ",
                                        info="Memory efficient",
                                        interactive=True,
                                        elem_classes=["checkbox"]
                                    )
                                with gr.Column(scale=1, min_width=100):
                                    train_on_completions = gr.Checkbox(
                                        value=False,
                                        label="Outputs only",
                                        info="Assistant outputs only",
                                        interactive=True,
                                        elem_classes=["checkbox"]
                                    )

            # Second Row - Training Optimization
            with gr.Row():
                with gr.Column(elem_classes=["card", "compact-card", "training-optimization-card"]):
                    gr.Markdown("## Training Optimization")
                    
                    # Group 1: Learning Rate and GPU Settings
                    with gr.Row():
                        with gr.Column(scale=2):
                            learning_rate = gr.Dropdown(
                                choices=["1e-5", "2e-5", "5e-5", "1e-4", "2e-4", "5e-4", "1e-3"],
                                value="5e-5",
                                label="LR",
                                info="Weight updates",
                                allow_custom_value=True,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            gpu_count = gr.Dropdown(
                                choices=["auto", "1", "2", "4", "8"],
                                value="auto",
                                label="Number of GPUs",
                                info="Select GPUs or 'auto'",
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            random_seed = gr.Number(
                                value=3407,
                                label="Random Seed",
                                info="For reproducibility",
                                precision=0,
                                interactive=True
                            )
                    # Group 2: Batch Processing Settings
                    with gr.Row():
                        with gr.Column(scale=1):
                            batch_size = gr.Slider(
                                minimum=1, maximum=32,
                                value=2,
                                label="Batch size",
                                info="Examples per pass",
                                step=1,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            grad_accumulation = gr.Slider(
                                minimum=1, maximum=16,
                                value=4,
                                label="Gradient accumulation",
                                info="Steps before update",
                                step=1,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            weight_decay = gr.Slider(
                                minimum=0, maximum=0.1, value=0.01, 
                                label="Weight Decay",
                                info="Regularization strength",
                                interactive=True
                            )

                    # Group 3: Training Steps and Sequence Settings
                    with gr.Row():
                        with gr.Column(scale=1):
                            warmup_steps = gr.Slider(
                                minimum=0, maximum=100, value=5,
                                label="Warmup Steps",
                                info="LR warmup period",
                                step=1,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            max_steps = gr.Slider(
                                minimum=0, maximum=1000, value=0,
                                label="Max Steps",
                                info="0 uses epochs instead",
                                step=1,
                                interactive=True
                            )
                        with gr.Column(scale=1):
                            save_steps = gr.Slider(
                                minimum=0, maximum=1000, value=0,
                                label="Save Steps",
                                info="Steps between saving model",
                                step=1,
                                interactive=True
                            )
                                
                    # Group 5: Sequence Packing Option
                    with gr.Row():
                        packing = gr.Checkbox(
                            value=False,
                            label="Enable Sequence Packing",
                            info="Optimize memory by combining sequences",
                            interactive=True
                        )

            # Third Row - Logging & Monitoring
            with gr.Row():
                with gr.Column(elem_classes=["card", "logging-monitoring-card"]):
                    gr.Markdown("## Logging & Monitoring")
                    
                    with gr.Row():
                        # Weights & Biases Section
                        with gr.Column(scale=1):
                            gr.Markdown("#### Weights & Biases")
                            enable_wandb = gr.Checkbox(
                                value=False,
                                label="Enable W&B Logging",
                                info="Enable logging to Weights & Biases platform",
                                interactive=True
                            )
                            with gr.Column():
                                wandb_token = gr.Textbox(
                                    placeholder="Enter your W&B API token",
                                    label="W&B API Token",
                                    info="Enter your W&B API token",
                                    type="password",
                                    interactive=True,
                                    visible=False
                                )
                                wandb_project = gr.Textbox(
                                    value="llm-finetuning",
                                    label="W&B Project Name",
                                    info="Name of the project in W&B",
                                    interactive=True,
                                    visible=False
                                )

                        # TensorBoard Section
                        with gr.Column(scale=1):
                            gr.Markdown("#### TensorBoard")
                            enable_tensorboard = gr.Checkbox(
                                value=False,
                                label="Enable TensorBoard",
                                info="Enable logging to TensorBoard",
                                interactive=True
                            )
                            with gr.Column(visible=False) as tensorboard_settings:
                                tensorboard_dir = gr.Textbox(
                                    value="runs",
                                    label="TensorBoard Log Directory",
                                    info="Directory where TensorBoard logs will be saved",
                                    interactive=True
                                )
                                log_frequency = gr.Number(
                                    value=10,
                                    label="Logging Frequency",
                                    info="Log metrics every N steps",
                                    precision=0,
                                    interactive=True
                                )

                    # Update visibility toggles for both logging systems
                    def toggle_wandb_fields(enable):
                        return {
                            wandb_token: gr.update(visible=enable),
                            wandb_project: gr.update(visible=enable)
                        }

                    def toggle_tensorboard_fields(enable):
                        return {
                            tensorboard_settings: gr.update(visible=enable)
                        }

                    enable_wandb.change(
                        fn=toggle_wandb_fields,
                        inputs=[enable_wandb],
                        outputs=[wandb_token, wandb_project]
                    )

                    enable_tensorboard.change(
                        fn=toggle_tensorboard_fields,
                        inputs=[enable_tensorboard],
                        outputs=[tensorboard_settings]
                    )

    # Event Handlers
    # Define paste_token function first
    # def paste_token():
    #     import pyperclip
    #     return pyperclip.paste()

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

    # Add paste handler for W&B token
    # wandb_paste_btn.click(
    #     fn=paste_token,
    #     outputs=wandb_token,
    # )

    # Handle file upload
    def handle_file_upload(file, current_selection):
        import os
        import json
        import pandas as pd
        
        # Create datasets directory if it doesn't exist
        os.makedirs('datasets', exist_ok=True)
        
        save_path = os.path.join('datasets', os.path.basename(file.name))
        
        try:
            file_ext = file.name.lower().split('.')[-1]
            if file_ext == 'json':
                # Read the file line by line to handle JSONL format
                with open(file.name, 'r', encoding='utf-8') as f:
                    content = f.read()
                    try:
                        # Try parsing as single JSON object
                        data = json.loads(content)
                    except json.JSONDecodeError:
                        # If that fails, parsing as JSONL
                        try:
                            data = [json.loads(line) for line in content.splitlines() if line.strip()]
                        except json.JSONDecodeError as e:
                            return gr.Warning(f"Invalid JSON format. Please ensure your file is valid JSON or JSONL. Error: {str(e)}")
                
                # Save the processed data
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
            elif file_ext in ['csv', 'xlsx', 'xls']:
                if file_ext in ['xlsx', 'xls']:
                    df = pd.read_excel(file.name)
                    df.to_excel(save_path, index=False)
                else:
                    df = pd.read_csv(file.name)
                    df.to_csv(save_path, index=False)
            
            # Get new filename and all dataset choices
            new_filename = os.path.basename(save_path)
            choices = get_json_datasets()
            
            # Handle current selection
            if current_selection is None:
                current_selection = []
            elif isinstance(current_selection, str):
                current_selection = [current_selection]
            
            # Add new file to selection if not already present
            if new_filename not in current_selection:
                updated_selection = current_selection + [new_filename]
            else:
                updated_selection = current_selection
            
            # Return updated choices and combined selection
            return gr.update(choices=choices, value=updated_selection)
            
        except Exception as e:
            return gr.Warning(f"Error uploading file: {str(e)}")

    # Update the upload event handler to include current selection
    upload_btn.upload(
        fn=handle_file_upload,
        inputs=[upload_btn, local_datasets],
        outputs=local_datasets
    )

    # Update the toggle function
    def toggle_training_buttons(is_training):
        return {
            start_btn: gr.update(interactive=not is_training),
            stop_btn: gr.update(interactive=is_training)
        }

    start_btn.click(
        fn=lambda: toggle_training_buttons(True),
        outputs=[start_btn, stop_btn]
    )

    stop_btn.click(
        fn=lambda: toggle_training_buttons(False),
        outputs=[start_btn, stop_btn]
    )

    # Components dictionary
    return {
        'model_dropdown': model_dropdown,
        'model_search': model_search,
        'load_4bit': load_4bit,
        'hf_token' : hf_token,
        'local_datasets' : local_datasets,
        'learning_rate': learning_rate,
        'num_epochs': num_epochs,
        'loss_plot': loss_plot,
        'start_btn': start_btn,
        'warmup_steps': warmup_steps,
        'max_steps': max_steps,
        'max_seq_length': max_sequence_length,
        'input_text': input_text,
        'upload_btn': upload_btn,
        'random_seed': random_seed,
        'weight_decay': weight_decay,
        'batch_size': batch_size,
        'grad_accumulation': grad_accumulation,
        'data_template': data_template, 
        'packing': packing,
        'target_modules': target_modules,
        'lora_r': lora_r,
        'lora_alpha': lora_alpha,
        'lora_dropout': lora_dropout,
        'gradient_checkpointing': gradient_checkpointing,
        'use_rslora': use_rslora,
        'use_loftq': use_loftq,
        'train_on_completions': train_on_completions, 
        'enable_wandb': enable_wandb,
        'wandb_token': wandb_token,
        'wandb_project': wandb_project,
        'enable_tensorboard': enable_tensorboard,
        'tensorboard_dir': tensorboard_dir,
        'log_frequency': log_frequency,
        'gpu_count': gpu_count,
        'combine_btn': combine_btn,
        'stop_btn': stop_btn,
        'save_steps': save_steps,
    } 