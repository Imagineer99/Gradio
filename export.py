import gradio as gr
import pyperclip

def get_clipboard_content():
    try:
        return pyperclip.paste()
    except:
        return "Please install pyperclip: pip install pyperclip"

def create_export_interface():
    with gr.Column(elem_classes=["export-container"]) as export_interface:
        gr.Markdown("## Export Your Model", elem_classes=["export-title"])
        
        with gr.Group(elem_classes=["export-form"]):
            # Model Type Selection
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
            
            # Model Format (for Merged Model)
            merge_format = gr.Radio(
                choices=[
                    "16-bit (FP16)",
                    "4-bit (INT4)",
                    "GGUF",
                ],
                value="16-bit (FP16)",
                label="Model Format",
                info="Choose precision for the merged model",
                interactive=True,
            )
            
            # GGUF Options (initially hidden)
            with gr.Group(visible=False) as gguf_group:
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
                context_length = gr.Slider(
                    minimum=512,
                    maximum=32768,
                    value=4096,
                    step=512,
                    label="Context Length",
                    info="Maximum sequence length for GGUF model",
                    interactive=True,
                )            
            # Export Destinations
            gr.Markdown("### Export Destinations")
            with gr.Row():
                local_save = gr.Checkbox(
                    label="💾 Save Locally",
                    value=True,
                    info="Save model to local storage",
                    interactive=True,
                )
                push_to_hub = gr.Checkbox(
                    label="🤗 Push to Hugging Face",
                    value=False,
                    info="Upload to Hugging Face Hub",
                    interactive=True,
                )
                push_to_ollama = gr.Checkbox(
                    label="🦙 Push to Ollama",
                    value=False,
                    info="Export to Ollama",
                    interactive=True,
                )
            
            # Local Save Options
            with gr.Group(visible=True) as local_group:
                output_dir = gr.Textbox(
                    label="Output Directory",
                    placeholder="Path to save the model",
                    value="models/export",
                    elem_classes=["export-input"],
                    interactive=True,
                )
            
            # Hugging Face Options
            with gr.Group(visible=False) as hub_group:
                hub_model_id = gr.Textbox(
                    label="Hub Model ID",
                    placeholder="username/model-name",
                    elem_classes=["export-input"],
                )
                with gr.Row():
                    hub_token = gr.Textbox(
                        label="Hub Token",
                        placeholder="Enter your Hugging Face token",
                        type="password",
                        elem_classes=["export-input"],
                        scale=3
                    )
                    paste_btn = gr.Button(
                        "📋 Paste",
                        scale=1,
                        variant="primary",
                        size="sm",
                        interactive=True,
                    )
            
            # Ollama Options
            with gr.Group(visible=False) as ollama_group:
                ollama_model_name = gr.Textbox(
                    label="Ollama Model Name",
                    placeholder="username/model-name",
                    info="Name for your Ollama model",
                    elem_classes=["export-input"]
                )
                ollama_username = gr.Textbox(
                    label="Ollama Username",
                    placeholder="Your ollama.com username",
                    info="Required for publishing to ollama.com"
                )
                with gr.Row():
                    ollama_key = gr.Textbox(
                        label="Ollama Public Key",
                        placeholder="Your ollama.com public key",
                        type="password",
                        info="Find this in ollama.com/settings/keys",
                        scale=3,
                        interactive=True,
                    )
                    ollama_paste_btn = gr.Button(
                        "📋 Paste",
                        scale=1,
                        variant="primary",
                        size="sm"
                    )
            
            gr.Button("Export Model", variant="primary", elem_classes=["export-button"])

        # Recent Exports Section
        with gr.Group(elem_classes=["export-status-group"]):
            gr.Markdown("### Recent Exports", elem_classes=["recent-exports-title"])
            gr.Markdown("""
                - ✅ mistral-7b-finetuned → Local Storage (2 minutes ago)
                - ✅ customer-support-bot → Hugging Face Hub (1 hour ago)
            """)

    # Visibility toggles
    push_to_hub.change(
        fn=lambda x: gr.update(visible=x),
        inputs=[push_to_hub],
        outputs=[hub_group]
    )
    
    push_to_ollama.change(
        fn=lambda x: gr.update(visible=x),
        inputs=[push_to_ollama],
        outputs=[ollama_group]
    )
    
    # Paste button handler
    paste_btn.click(
        fn=lambda: gr.update(value=get_clipboard_content()),
        outputs=[hub_token]
    )
    
    # Ollama paste button handler
    ollama_paste_btn.click(
        fn=lambda: gr.update(value=get_clipboard_content()),
        outputs=[ollama_key]
    )

    # GGUF visibility toggle
    merge_format.change(
        fn=lambda x: gr.update(visible=(x == "GGUF")),
        inputs=[merge_format],
        outputs=[gguf_group]
    )

    # Components dictionary
    return {
        'export_interface': export_interface,
        'export_type': export_type,
        'merge_format': merge_format,
        'gguf_quant': gguf_quant,
        'context_length': context_length,
        'local_save': local_save,
        'push_to_hub': push_to_hub,
        'push_to_ollama': push_to_ollama,
        'hub_token': hub_token,
        'hub_model_id': hub_model_id,
        'ollama_model_name': ollama_model_name,
        'ollama_username': ollama_username,
        'ollama_key': ollama_key,
    } 