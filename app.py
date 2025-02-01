import gradio as gr
import time

def process_data(text: str) -> str:
    """Basic text processing function"""
    time.sleep(0.5)
    return text.upper()

# Update the custom CSS to handle missing fonts
custom_css = """
/* Base styles */
:root {
    --primary-500: #55b685;
}

body {
    background-color: #f9fafb;
    font-family: 'Inter', sans-serif;
}

/* Container styling */
.gradio-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem !important;
}

/* Header */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
}

/* Navigation buttons */
.lg.primary, .lg.secondary {
    padding: 6px 16px !important;
    border-radius: 20px !important;
    border: none !important;
    background: transparent !important;
    cursor: pointer !important;
    color: #111827 !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.lg.secondary:hover {
    background: rgba(0, 0, 0, 0.05) !important;
}

.lg.primary {
    background: white !important;
}

/* Cards */
.card {
    background: white !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
}

/* Model selector */
.gr-dropdown {
    background: #111827 !important;
    color: white !important;
    padding: 0.75rem 1rem !important;
    border-radius: 0.5rem !important;
    border: none !important;
    width: 100% !important;
}

/* Search input */
.gr-textbox {
    width: 100% !important;
    padding: 0.75rem 1rem 0.75rem 2.5rem !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 0.5rem !important;
    background: white !important;
}

/* Parameter sliders */
.gr-slider {
    width: 100% !important;
    height: 0.5rem !important;
    background: #e5e7eb !important;
    border-radius: 9999px !important;
    --slider-color: #10b981 !important;
}

.gr-slider-handle {
    background: #10b981 !important;
    border-radius: 50% !important;
    height: 1rem !important;
    width: 1rem !important;
}

/* Start button - keeping neuromorphic style */
.start-button {
    width: 100% !important;
    padding: 0.75rem !important;
    background: #f8faf9 !important;
    color: #111827 !important;
    border-radius: 20px !important;
    border: 1px solid #e5e7eb !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.start-button:hover {
    background: white !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
}

/* Theme toggle - neuromorphic style */
.theme-toggle {
    padding: 8px !important;
    border-radius: 50% !important;
    background: #f8faf9 !important;
    border: 1px solid #e5e7eb !important;
    color: #6b7280 !important;
    transition: all 0.2s ease !important;
}

.theme-toggle:hover {
    background: white !important;
    transform: translateY(-1px) !important;
}

/* Headers */
.gr-markdown h1 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
    margin-bottom: 1rem !important;
    margin-top: 0.5rem !important;
}

.gr-markdown h3 {
    font-size: 1.125rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
    margin-bottom: 1rem !important;
}

/* Labels */
.gr-label {
    font-size: 0.875rem !important;
    color: #6b7280 !important;
    margin-bottom: 0.5rem !important;
}

/* Upload button */
.upload-button {
    width: 100% !important;
    padding: 0.75rem !important;
    border: 1px dashed #e5e7eb !important;
    border-radius: 0.5rem !important;
    background: white !important;
    color: #6b7280 !important;
}

.primary.svelte-5st68j {
    background: #f8faf9 !important;
    border: 1px solid #e5e7eb !important;

    transition: all 0.2s ease !important;
}

.primary.svelte-5st68j:hover {
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1), 
                -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
    transform: translateY(1px) !important;
}

.primary.svelte-5st68j:active {
    box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.1), 
                inset -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
    transform: translateY(2px) !important;
}

/* Logo styling */
.logo-container {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    height: 40px !important;
    gap: 10px !important;
    margin: 0 !important;
}

.logo-container img {
    height: 100% !important;
    width: auto !important;
    object-fit: contain !important;
}

.logo-container h1 {
    margin: 0 !important;
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
    font-family: Hellix, sans-serif !important;
}

/* Hide icon buttons for logo */
.logo-container .icon-button-wrapper {
    display: none !important;
}

.image-container.svelte-dpdy90.svelte-dpdy90 {
    height: 100%;
    position: relative;
    min-width: var(--size-20);
    margin-top: 10px !important;
    margin-left: 60px !important;
}

.image-frame.svelte-dpdy90.svelte-dpdy90 {
    width: 75%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.gradio-container-5-14-0 .prose :last-child {
    margin-bottom: 0 !important;
    margin-top: 50px;
}

.gradio-container.gradio-container-5-14-0 .contain .logo-container h1 {
    margin: 0px !important;
    font-size: 1.95rem !important;
    font-weight: 600 !important;
    color: rgb(17, 24, 39) !important;
    font-family: Hellix, sans-serif !important;
    margin-top: 25px !important;
}

.gradio-container.gradio-container-5-14-0 .contain .gr-button-row {
    background: rgb(248, 250, 249) !important;
    border-radius: 24px !important;
    padding: 4px !important;
    display: inline-flex !important;
    border: 1px solid rgb(229, 231, 235) !important;
    gap: 4px !important;
    margin-top: 0 !important;
}

.gr-button-row {
    background: transparent !important;
    border: none !important;
}

.gr-button-row button {
    background: transparent !important;
    border: none !important;
}

.gradio-container.gradio-container-5-14-0 .contain .image-container.svelte-dpdy90.svelte-dpdy90 {
    height: 100%;
    position: relative;
    min-width: var(--size-20);
    margin-top: 25px !important;
    margin-left: 60px !important;
}

.gradio-container.gradio-container-5-14-0 .contain .gr-button-row {
    background: rgb(248, 250, 249) !important;
    border-radius: 24px !important;
    padding: 4px !important;
    display: inline-flex !important;
    border: 1px solid rgb(229, 231, 235) !important;
    gap: 4px !important;
    margin-top: 0 !important;
}

/* Navigation buttons */
.navigation-buttons {
    background: transparent !important;
    border: none !important;
    display: inline-flex !important;
    gap: 4px !important;
    justify-content: flex-start !important;
    width: auto !important;
    padding: 4px !important;
}

/* Base style for all navigation buttons */
.navigation-buttons .lg.primary.svelte-5st68j,
.navigation-buttons .lg.secondary.svelte-5st68j {
    background: transparent !important;
    border: none !important;
    padding: 6px 16px !important;
    margin-top: 37px !important;
    transition: 0.2s !important;
}

/* Style for the active/selected button (Train by default) */
.navigation-buttons .lg.primary.svelte-5st68j {
    background: rgb(255 255 255) !important;
    border: 1px solid rgb(0 0 0 / 52%) !important;
}

/* Hover effect for non-selected buttons */
.navigation-buttons .lg.secondary.svelte-5st68j:hover {
    background: rgba(0, 0, 0, 0.05) !important;
}

/* Mode toggle buttons container */
.mode-toggle-buttons {
    background: #f8faf9 !important;
    border-radius: 24px !important;
    padding: 4px !important;
    display: inline-flex !important;
    border: 1px solid #e5e7eb !important;
    gap: 4px !important;
    margin-top: 37px !important;

}

/* Individual toggle buttons */
.mode-toggle-buttons .primary,
.mode-toggle-buttons .secondary {
    padding: 6px 16px !important;
    border-radius: 20px !important;
    border: none !important;
    background: transparent !important;
    cursor: pointer !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

/* Hover state for non-active buttons */
.mode-toggle-buttons .secondary:hover {
    background: rgba(0, 0, 0, 0.05) !important;
}

/* Active/selected button state */
.mode-toggle-buttons .primary {
    background: white !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}
div.svelte-1xp0cw7>*, div.svelte-1xp0cw7>.form>* {
    flex: 1 1 0%;
    flex-wrap: nowrap !important;
    min-width: min(160px, 100%);
}

.start-finetune-btn.svelte-5st68j {
    max-width: 25px;
    padding: 5px !important;
        margin-top: 5px;
    background-color: rgb(20, 189, 141) !important;
    color: white !important;
    box-shadow: none !important;
}

/* Add hover state for better interactivity */
.start-finetune-btn.svelte-5st68j:hover {
    background-color: #12a67b !important;
    box-shadow: none !important;
}

/* Target the Training Dataset header specifically */
.block.svelte-11xb1hd .prose h3 {
    margin-top: -20px !important;
}
.card {
    background: white !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    min-height: 300px !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Card headers/titles */
.card .prose h3 {
    font-size: 1.125rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
    margin-bottom: 1rem !important;
    margin-top: 0 !important;
    display: block !important;  /* Ensure visibility */
}

/* Ensure the content inside cards fills the space properly */
.card .prose {
    margin-bottom: 1rem !important;
    display: block !important;  /* Ensure visibility */
}
.gradio-container.gradio-container-5-14-0 .contain .card {
    background: white !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    min-height: 300px !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 320px !important;
}
/* Target only the Upload JSON/CSV/Excel button */
#component-25.lg.secondary.svelte-5st68j {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    transition: all 0.2s ease !important;
    background: #f5f5f5 !important;
}

#component-25.lg.secondary.svelte-5st68j:hover {
    box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1),
                -3px -3px 6px rgba(255, 255, 255, 0.8) !important;
}

#component-25.lg.secondary.svelte-5st68j:active {
    box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.1),
                inset -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
    transform: translateY(1px) !important;
}
.gradio-container.gradio-container-5-14-0 .contain .card {
    background: white !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 320px !important;
    padding: 10px !important;
    padding-left: 30px !important;
    padding-right: 30px !important;
}

/* Neuromorphic input styles */
.container.svelte-1hfxrpf .wrap.svelte-1hfxrpf {
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;

    transition: all 0.2s ease !important;
    margin-bottom: 16px !important;
}

.container.svelte-1hfxrpf .wrap.svelte-1hfxrpf:hover,
.container.svelte-1hfxrpf .wrap.svelte-1hfxrpf:focus-within {
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1),
                -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
}

.container.svelte-1hfxrpf .wrap.svelte-1hfxrpf:active {
    box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.1),
                inset -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
}

/* Style for the textbox */
label.container.show_textbox_border.svelte-173056l input.svelte-173056l,
label.container.show_textbox_border.svelte-173056l textarea.svelte-173056l {
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    margin-bottom: 17px !important;
}

label.container.show_textbox_border.svelte-173056l input.svelte-173056l:hover,
label.container.show_textbox_border.svelte-173056l textarea.svelte-173056l:hover,
label.container.show_textbox_border.svelte-173056l input.svelte-173056l:focus,
label.container.show_textbox_border.svelte-173056l textarea.svelte-173056l:focus {

}

.gradio-container-5-14-0, .gradio-container-5-14-0 *, .gradio-container-5-14-0 :before, .gradio-container-5-14-0 :after {
    box-sizing: border-box;
    border-width: 0;
    border-style: hidden !important;
}

/* Target only the Upload JSON/CSV/Excel button */
#component-26.lg.secondary.svelte-5st68j {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    transition: all 0.2s ease !important;
    background: #f5f5f5 !important;
}

#component-26.lg.secondary.svelte-5st68j:hover {
    box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1),
                -3px -3px 6px rgba(255, 255, 255, 0.8) !important;
}

#component-26.lg.secondary.svelte-5st68j:active {
    box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.1),
                inset -2px -2px 4px rgba(255, 255, 255, 0.8) !important;
    transform: translateY(1px) !important;
}

/* Style for dataset input textbox */
textarea[placeholder="Type dataset from 🤗HF"].svelte-173056l {
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 8px 12px !important;
    width: 100% !important;
    background: white !important;
    margin: -10px !important;
    transition: all 0.2s ease !important;
    margin-bottom: 17px !important;
    resize: none !important;
    height: 40px !important;
}

textarea[placeholder="Type dataset from 🤗HF"].svelte-173056l:hover,
textarea[placeholder="Type dataset from 🤗HF"].svelte-173056l:focus {
    border-color: #d1d5db !important;
    margin: -10px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    outline: none !important;
}


/* Target the specific training dataset card */
#component-24.column.card {
 max-width: 320px !important;
}

/* Style for the model selection container */
#component-19.row.svelte-1xp0cw7 {
    max-width: 655px !important;
    margin-left: -15px;
}

/* Style for the search textbox container */
#component-21.block.svelte-11xb1hd {
    margin-left: -12px !important;
}

/* Style for the main content container */
#component-17.column.container.svelte-vt1mxs {
    margin-left: 75px !important;
}

#component-24 {
    box-shadow: rgb(0 0 0 / 12%) 0px 1px 3px !important;
    max-width: 900px !important;
}

#component-29 {
    box-shadow: rgb(0 0 0 / 12%) 0px 1px 3px !important;
    max-width: 967px !important;
}

#component-19.row.svelte-1xp0cw7 {
    max-width: 680px !important;
    min-width: 686px !important;
    margin-bottom: -15px !important;
    margin-bottom: -21px !important;
}

#component-14.row.mode-toggle-buttons {
    max-width: 335px !important;
}

#component-16.lg.secondary.mode-advanced-btn {
    padding-left: 0px !important;
    padding-right: 0px !important;
}

"""


with gr.Blocks(
    css=custom_css,
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
