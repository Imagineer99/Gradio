import gradio as gr
import os

# Pages
from pages.train import create_train_interface
from pages.chat import create_chat_interface
from pages.export import create_export_interface
from pages.eval import create_evaluate_interface

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
    head= """
    <script>
      let userHasManuallyToggled = false;

      function simulateToggleClick(retryCount = 0) {
          const toggleBtn = document.getElementById('theme-toggle-btn');
          if (toggleBtn) {
              toggleBtn.click();
              console.log('Auto-toggled to dark theme');
              document.body.style.opacity = '1';
          } else if (retryCount < 10) {  // Try up to 10 times
              console.log('Toggle button not found, retrying...', retryCount);
              setTimeout(() => simulateToggleClick(retryCount + 1), 200);  // Retry every 200ms
          } else {
              console.log('Failed to find toggle button, showing content anyway');
              document.body.style.opacity = '1';
          }
      }

      function setInitialTheme() {
          if (!userHasManuallyToggled) {
              const htmlElement = document.documentElement;
              
              // First force light theme`
              htmlElement.classList.remove('dark');
              document.body.classList.remove('dark');
              htmlElement.removeAttribute('data-theme');
              document.body.removeAttribute('data-theme');
              htmlElement.setAttribute('data-theme', 'light');
              document.body.setAttribute('data-theme', 'light');
              
              // Check if system prefers dark
              const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
              console.log('System prefers dark:', prefersDark);
              
              if (prefersDark) {
                  // Wait a bit longer for Gradio to fully initialize
                  setTimeout(() => simulateToggleClick(), 500);
              } else {
                  document.body.style.opacity = '1';
              }
          }
      }

      function setupThemeToggleListener() {
          const toggleBtn = document.getElementById('theme-toggle-btn');
          if (toggleBtn) {
              toggleBtn.addEventListener('click', () => {
                  userHasManuallyToggled = true;
                  console.log('Theme manually toggled');
              });
          }
      }

      function onPageLoad() {
          setInitialTheme();
          setupThemeToggleListener();
          
          let h1 = document.querySelector('h1');
          if (h1 && !h1.hasAttribute('data-js-modified')) {
              h1.style.transition = 'all 0.5s';
              h1.innerHTML += ' (Theme Control Active!)';
              h1.setAttribute('data-js-modified', 'true');
          }
      }

      // Run as early as possible
      setInitialTheme();
      document.addEventListener('DOMContentLoaded', onPageLoad);
      window.addEventListener('load', onPageLoad);

      function applyZoomForSmallScreens() {
        if (window.screen.width < 1920) {
          document.body.style.zoom = "0.75";
        } else {
          document.body.style.zoom = "";
        }
      }

      // Run on load
      applyZoomForSmallScreens();

      // Also run on resize (in case user resizes window or moves to another monitor)
      window.addEventListener('resize', applyZoomForSmallScreens);

      function applyZoomFor1080p() {
        if (window.screen.width === 1920 && window.screen.height === 1080) {
          document.body.style.zoom = "0.75";
        } else {
          document.body.style.zoom = "";
        }
      }
      applyZoomFor1080p();
      window.addEventListener('resize', applyZoomFor1080p);
    </script>
    """
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
            evaluate_components = create_evaluate_interface()

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

    # JavaScript click handler
    theme_toggle.click(
        fn=None,  
        inputs=[],  
        outputs=[], 
        js="() => { \
            const htmlElement = document.documentElement; \
            if (htmlElement.getAttribute('data-theme') === 'dark') { \
                htmlElement.setAttribute('data-theme', 'light'); \
                document.body.setAttribute('data-theme', 'light'); \
            } else { \
                htmlElement.setAttribute('data-theme', 'dark'); \
                document.body.setAttribute('data-theme', 'dark'); \
            } \
        }"
    )

if __name__ == "__main__":
    demo.launch(
        share=True,
        server_port=8000,
        server_name="0.0.0.0",
        favicon_path="assets/favicon-32x32.png",
    )