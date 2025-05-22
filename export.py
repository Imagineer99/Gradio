import gradio as gr


def create_export_interface():
    with gr.Column(elem_classes=["export-container"]) as export_interface:
        
        # Export Type & Format Card
        with gr.Column(elem_classes=["card", "export-type-card"]):
            gr.Markdown("## Type & Format")
            with gr.Row():
                # Export Type (left)
                with gr.Column():
                    export_type = gr.Radio(
                        choices=[
                            "Merged Model",
                            "LoRA Adapter",
                        ],
                        value="Merged Model",
                        label="Export Type",
                        info="Choose how to export your model",
                        interactive=True,
                    )
                # Model Format (right, only for Merged Model)
                with gr.Column(elem_classes=["model-format"]) as merge_format_group:
                    with gr.Row():
                        merge_format = gr.Radio(
                            choices=[
                                "4-bit (FP4)",
                                "16-bit (FP16)",
                                "GGUF",
                            ],
                            value="16-bit (FP16)",
                            label="Model Format",
                            info="Choose precision for the merged model",
                            interactive=True,
                        )
                        with gr.Column(visible=True, elem_classes=["gguf-group"]) as gguf_group:
                            with gr.Row():
                                gguf_quant = gr.Radio(
                                    choices=[
                                        "Q4_K_M",
                                        "Q4_0",
                                        "Q5_K_M",
                                        "Q5_0",
                                        "Q8_0",
                                    ],
                                    value="Q4_K_M",
                                    label="GGUF Quantization",
                                    info="Choose GGUF quantization method",
                                    interactive=True,
                                )
         

        # Three Export Destination Cards Side by Side
        with gr.Row():
            # Local Save Card
            with gr.Column(elem_classes=["card", "local-save-card"]):
                gr.Markdown("## .")
                local_save = gr.Checkbox(
                    label="💾 Save Locally",
                    value=True,
                    interactive=True,
                )
                # Always visible
                with gr.Column() as local_group:
                    output_dir = gr.Textbox(
                        label="Output Directory",
                        placeholder="Path to save the model",
                        value="models/export",
                        elem_classes=["export-input"],
                        interactive=True,
                    )
                    file_name = gr.Textbox(
                        label="Filename",
                        placeholder="Name of the model",
                        elem_classes=["export-input"],
                    )

            # Hugging Face Card
            with gr.Column(elem_classes=["card", "hf-card"]):
                gr.Markdown("## .")
                push_to_hub = gr.Checkbox(
                    label="🤗 Push to Hugging Face",
                    value=False,
                    interactive=True,
                )
                # Always visible
                with gr.Column() as hub_group:
                    hub_model_id = gr.Textbox(
                        label="Hub Model ID",
                        placeholder="username/model-name",
                        elem_classes=["export-input"],
                    )
                    hub_token = gr.Textbox(
                        label="Hub Token",
                        placeholder="Enter your Hugging Face token",
                        type="password",
                        scale=3,
                        elem_classes=["export-input"],
                    )

            # Ollama Card
            with gr.Column(elem_classes=["card", "ollama-card"]):
                gr.Markdown("## .")
                push_to_ollama = gr.Checkbox(
                    label="🦙 Push to Ollama",
                    value=False,
                    interactive=True,
                )
                # Always visible
                with gr.Column() as ollama_group:
                    ollama_model_name = gr.Textbox(
                        label="Ollama Model Name",
                        placeholder="username/model-name",
                        elem_classes=["export-input"]
                    )
                    ollama_key = gr.Textbox(
                        label="Ollama Public Key",
                        placeholder="Your ollama.com public key",
                        type="password",
                        scale=3,
                        interactive=True,
                    )

        gr.Button("Export Model", variant="primary", elem_classes=["export-btn"])

    # GGUF visibility toggle
    export_type.change(
        fn=lambda x: gr.update(visible=(x == "Merged Model")),
        inputs=[export_type],
        outputs=[merge_format_group]
    )

    # Components dictionary
    return {
        'export_interface': export_interface,
        'export_type': export_type,
        'merge_format': merge_format,
        'gguf_quant': gguf_quant,
        'local_save': local_save,
        'push_to_hub': push_to_hub,
        'push_to_ollama': push_to_ollama,
        'hub_token': hub_token,
        'hub_model_id': hub_model_id,
        'ollama_model_name': ollama_model_name,
        'ollama_key': ollama_key,
        'output_dir': output_dir,
        'file_name': file_name,
    } 