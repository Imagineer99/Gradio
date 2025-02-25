import gradio as gr
import os

# Pages
from train import create_train_interface
from chat import create_chat_interface
from export import create_export_interface

# CSS loading
def load_css():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, "static", "style.css")
        print(f"Looking for CSS at: {css_path}")
        
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to load CSS: {e}")
        return ""
css_content = load_css()

# Create interface 
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
    
    # Header Section (logo, navigation buttons, spacer)
    with gr.Row(elem_classes=["header"]):
        with gr.Column(scale=1):
            with gr.Row(elem_classes=["logo-container"]):
                try:
                    gr.Image("assets/logo.png", label=None, show_label=False, container=False)
                    gr.Markdown("# unsloth")
                except:
                    gr.Markdown("# unsloth")
        # Navbar
        with gr.Column(scale=3):
            with gr.Row(elem_classes=["navigation-buttons"]):
                nav_train = gr.Button("Train", elem_classes=["lg", "primary", "nav-train-btn", "nav-button"])
                nav_evaluate = gr.Button("Evaluate", elem_classes=["lg", "secondary", "nav-evaluate-btn", "nav-button"])
                nav_chat = gr.Button("Chat", elem_classes=["lg", "secondary", "nav-chat-btn", "nav-button"])
                nav_export = gr.Button("Export", elem_classes=["lg", "secondary", "nav-export-btn", "nav-button"])
        # Light/dark theme toggle
        with gr.Column(scale=2):
            gr.Row(elem_classes=["theme-toggle-spacer"])
            with gr.Row(elem_classes=["theme-toggle-container"]):
                theme_toggle = gr.Button("☀️ Light", elem_id="theme-toggle-btn", elem_classes=["theme-toggle-btn"])

    # Main Content
    with gr.Column(elem_classes=["main-container"]):
        with gr.Column(visible=True) as train_tab:
            train_components = create_train_interface()
        
        with gr.Column(visible=False) as chat_tab:
            chat_components = create_chat_interface()
        
        with gr.Column(visible=False) as export_tab:
            export_components = create_export_interface()

    # Tab switching
    def switch_to_chat():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

    def switch_to_train():
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    
    def switch_to_export():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

    # Click handlers
    nav_chat.click(
        switch_to_chat,
        outputs=[train_tab, chat_tab, export_tab]
    )

    nav_train.click(
        switch_to_train,
        outputs=[train_tab, chat_tab, export_tab]
    )

    nav_export.click(
        switch_to_export,
        outputs=[train_tab, chat_tab, export_tab]
    )

    # Modify the toggle_theme function
    def toggle_theme(btn_text):
        is_dark = "🌙 Dark" in btn_text
        new_text = "☀️ Light" if is_dark else "🌙 Dark"
        debug_msg = f"Button clicked! Changed from '{btn_text}' to '{new_text}'"
        print(debug_msg)
        return new_text, debug_msg

    # Click handler - JavaScript
    theme_toggle.click(
        fn=None,  # No Python function
        inputs=[theme_toggle],
        outputs=[theme_toggle],
        js="(btn_text) => { \
            const isLight = btn_text.includes('☀️ Light'); \
            const newTheme = isLight ? 'dark' : 'light'; \
            const newText = isLight ? '🌙 Dark' : '☀️ Light'; \
            document.documentElement.setAttribute('data-theme', newTheme); \
            document.body.setAttribute('data-theme', newTheme); \
            console.log('Theme set to:', newTheme); \
            return [newText, 'Theme changed to: ' + newTheme]; \
        }"
    )

    # Launch the interface
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="assets/favicon-32x32.png",
        pwa=True,
    )