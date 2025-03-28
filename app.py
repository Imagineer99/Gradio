import gradio as gr
import os

# Pages
from train import create_train_interface
from chat import create_chat_interface
from export import create_export_interface

# CSS 
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
    theme="system"
) as demo: 
    # Meta tags 
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
                nav_train = gr.Button("Train", elem_classes=["nav-button", "primary"])
                nav_evaluate = gr.Button("Evaluate", elem_classes=["nav-button", "secondary"])
                nav_chat = gr.Button("Chat", elem_classes=["nav-button", "secondary"])
                nav_export = gr.Button("Export", elem_classes=["nav-button", "secondary"])
        # Light/dark theme toggle
        with gr.Column(scale=2):
            gr.Row(elem_classes=["theme-toggle-spacer"])
            with gr.Row(elem_classes=["theme-toggle-container"]):
                theme_toggle = gr.Button("", elem_id="theme-toggle-btn", elem_classes=["theme-toggle-btn"])

    # Main Content
    with gr.Column(elem_classes=["main-container"]):
        with gr.Column(visible=True) as train_tab:
            train_components = create_train_interface()
        
        with gr.Column(visible=False) as chat_tab:
            chat_components = create_chat_interface()
        
        with gr.Column(visible=False) as export_tab:
            export_components = create_export_interface()
            
        with gr.Column(visible=False) as evaluate_tab:
            export_components = create_export_interface()

    # Tab switching
    def switch_to_chat():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "primary"]), \
               gr.update(elem_classes=["nav-button", "secondary"])

    def switch_to_train():
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
               gr.update(elem_classes=["nav-button", "primary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"])
    
    def switch_to_export():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "primary"])
               
    def switch_to_evaluate():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "primary"]), \
               gr.update(elem_classes=["nav-button", "secondary"]), \
               gr.update(elem_classes=["nav-button", "secondary"])

    # Click handlers
    nav_chat.click(
        switch_to_chat,
        outputs=[train_tab, chat_tab, export_tab, evaluate_tab, nav_train, nav_evaluate, nav_chat, nav_export]
    )

    nav_train.click(
        switch_to_train,
        outputs=[train_tab, chat_tab, export_tab, evaluate_tab, nav_train, nav_evaluate, nav_chat, nav_export]
    )

    nav_export.click(
        switch_to_export,
        outputs=[train_tab, chat_tab, export_tab, evaluate_tab, nav_train, nav_evaluate, nav_chat, nav_export]
    )
    
    nav_evaluate.click(
        switch_to_evaluate,
        outputs=[train_tab, chat_tab, export_tab, evaluate_tab, nav_train, nav_evaluate, nav_chat, nav_export]
    )

    # Simplify the JavaScript click handler
    theme_toggle.click(
        fn=None,  
        inputs=[],  
        outputs=[], 
        js="() => { \
            const currentTheme = document.documentElement.getAttribute('data-theme'); \
            const newTheme = currentTheme === 'light' ? 'dark' : 'light'; \
            document.documentElement.setAttribute('data-theme', newTheme); \
            document.body.setAttribute('data-theme', newTheme); \
            console.log('Theme set to:', newTheme); \
        }"
    )

    # Launch the interface
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="favicon-32x32.png",
    )