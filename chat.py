import gradio as gr
from PIL import Image
import time
import uuid
from datetime import datetime

# Image processing
import base64
from io import BytesIO

# Mock response to test the chat interface
def mock_chat_response(message, temperature, top_p, max_length, image=None):
    """Mock response function that returns hardcoded responses"""
    responses = [
        "That's an interesting point!",
        "I understand what you're asking.",
        "Based on my knowledge, I would say...",
        "That's a great question!",
    ]
    import random
    response = random.choice(responses)
    
    if image is not None:
        response = "I see you've shared an image!"
    
    # Stream the response character by character !placeholder for demo purposes!
    for i in range(len(response)):
        yield response[:i+1]
        time.sleep(0.05)  # Small delay between characters !placeholder for demo purposes!

def create_chat_interface():
    examples = [
        "hello world",
        "what's up?", 
        "this is GradioChat"
    ]

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald")) as chat_interface:
        
        # Main Chat Area
        with gr.Column(scale=10): # Make this column take most space
            # Header row - removed settings button
            with gr.Row(elem_classes=["chat-header"], equal_height=True):
                 gr.Markdown("## Welcome to Unsloth Chat")

            # Initial popup/example section inside chat container
            #with gr.Column(elem_id="chat-examples", visible=True) as example_block:
            #    with gr.Row():
            #        with gr.Column(scale=2):
            #            gr.Markdown("## Welcome to Unsloth Chat", elem_id="welcome-title")
            #            gr.Markdown("Making the community's best AI chat models available to everyone.")
            #        with gr.Column(scale=1):
            #            gr.Markdown("Chat UI is now open sourced on Hugging Face Hub")
            #            gr.Markdown("check out the [↗ repository](https://huggingface.co/spaces/unsloth/chat)")
            #    
            #    gr.Markdown("### Try these examples:")
            #    with gr.Row():
            #        example_buttons = [gr.Button(example, elem_classes=["example-btn"]) for example in examples]

            # Chat History
            chatbot = gr.Chatbot(
                height=600,
                show_label=False,
                elem_classes=["chat-history", "modern-chat"],
                container=True,
                type="messages",
                avatar_images=["user.png", "assistant.png"],
                layout="bubble",
                visible=False
            )

            # Input Area
            with gr.Row(elem_classes=["chat-input-row"]):
                with gr.Column(scale=8):
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        container=False,
                        elem_classes=["chat-input", "modern-input", "chat-input-initial"]  # Start with initial state
                    )
                with gr.Column(scale=1, elem_classes=["chat-controls-container"]):
                    with gr.Row(elem_classes=["chat-controls"]):
                        image_input = gr.Image(
                            label="", type="pil", elem_classes=["chat-image-input"],
                            show_label=False, container=False, visible=False
                        )
                        upload_html = f"""
                        <div class="upload-svg-wrapper initial-state" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                            <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        """
                        send_html = f"""
                        <div class="send-svg-wrapper initial-state" title="Send Message">
                            <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        """
                        upload_icon = gr.HTML(upload_html, elem_classes=["custom-upload"])
                        send_button = gr.HTML(send_html, elem_classes=["custom-send"])

        # Chat History Sidebar
        with gr.Column(scale=2, elem_classes=["chat-history-sidebar"]):
            gr.Markdown("## Chat History")
            
            # Container for saved chats
            saved_chats = gr.HTML(elem_id="saved-chats-container")
            
            # New Chat Button
            new_chat_btn = gr.Button("New Chat", elem_classes=["new-chat-btn"])


        # Settings panel
        with gr.Column(visible=True, elem_id="settings-panel-column") as settings_panel:
            gr.Markdown("## Settings")
            # Model Selection
            with gr.Accordion("Model Selection", open=False):
                 with gr.Row(elem_classes=["model-selection-controls"]):
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
                        elem_classes=["model-search"],
                        scale=1
                    )

            # Sampling Parameters
            with gr.Accordion("Sampling Parameters", open=False):
                with gr.Row():
                    with gr.Column():
                        temperature = gr.Slider(
                            minimum=0.1, maximum=2.0, value=0.7, step=0.1,
                            label="Temperature", info="Controls randomness (higher = more random)"
                        )
                        top_p = gr.Slider(
                            minimum=0.1, maximum=1.0, value=0.9, step=0.1,
                            label="Top P", info="Limits token selection probability P"
                        )
                        min_p = gr.Slider(
                            minimum=0.0, maximum=1.0, value=0.1, step=0.05,
                            label="Min P", info="Filters tokens below probability P"
                        )
                    with gr.Column():
                        top_k = gr.Slider(
                            minimum=1, maximum=100, value=40, step=1,
                            label="Top K", info="Limits token selection to K value"
                        )
                        max_length = gr.Slider(
                            minimum=50, maximum=2000, value=512, step=50,
                            label="Max New Tokens", info="Maximum response length"
                        )
                        repetition_penalty = gr.Slider(
                            minimum=1.0, maximum=2.0, value=1.1, step=0.1,
                            label="Repetition Penalty", info="Penalizes repeated tokens"
                        )

            # Prompting
            with gr.Accordion("Prompting", open=False):
                 with gr.Row():
                    with gr.Column(scale=2):
                        system_prompt = gr.Textbox(
                            value="You are a helpful AI assistant.",
                            info="Defines the LLM's style of response",
                            label="System Prompt", lines=3,
                            placeholder="Define the LLM's behavior and role..."
                        )
                    with gr.Column(scale=1):
                        chat_template = gr.Dropdown(
                            choices=["Auto-Select", "Alpaca", "ShareGPT", "OpenAssistant", "Anthropic Claude", "GPTeacher", "CodeAlpaca", "Dolly", "Baize", "OpenOrca", "WizardLM", "Platypus", "Vicuna", "LIMA", "Custom"],
                            value="Auto-Select", label="Chat Template",
                            info="Format of the conversation", interactive=True
                        )

            # Clear Chat Button (moved inside settings)
            #clear = gr.Button("Clear Chat")

        # --- Image Upload Icon Change Logic ---
        def on_image_upload(image, msg, chatbot):
            
            # Explicit state check - we're in initial state if:
            # 1. Either chatbot is None or empty list
            # 2. AND message is either None or empty string after stripping
            is_initial_state = True  # Start with initial state
            
            if chatbot and len(chatbot) > 0:
                is_initial_state = False
            if msg and msg.strip():
                is_initial_state = False
            
            print("Is initial state:", is_initial_state) 
            
            if image is not None and is_initial_state:
                return """
                <div class="upload-svg-wrapper has-image initial-state" title="Image Attached" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 5L18 7L22 3M12.5 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21H17C17.93 21 18.395 21 18.7765 20.8978C19.8117 20.6204 20.6204 19.8117 20.8978 18.7765C21 18.395 21 17.93 21 17M10.5 8.5C10.5 9.60457 9.60457 10.5 8.5 10.5C7.39543 10.5 6.5 9.60457 6.5 8.5C6.5 7.39543 7.39543 6.5 8.5 6.5C9.60457 6.5 10.5 7.39543 10.5 8.5ZM14.99 11.9181L6.53115 19.608C6.05536 20.0406 5.81747 20.2568 5.79643 20.4442C5.77819 20.6066 5.84045 20.7676 5.96319 20.8755C6.10478 21 6.42628 21 7.06929 21H16.456C17.8951 21 18.6147 21 19.1799 20.7582C19.8894 20.4547 20.4547 19.8894 20.7582 19.1799C21 18.6147 21 17.8951 21 16.456C21 15.9717 21 15.7296 20.9471 15.5042C20.8805 15.2208 20.753 14.9554 20.5733 14.7264C20.4303 14.5442 20.2412 14.3929 19.8631 14.0905L17.0658 11.8527C16.6874 11.5499 16.4982 11.3985 16.2898 11.3451C16.1061 11.298 15.9129 11.3041 15.7325 11.3627C15.5279 11.4291 15.3486 11.5921 14.99 11.9181Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
            elif image is not None and not is_initial_state:
                return """
                <div class="upload-svg-wrapper has-image active-chat" title="Image Attached" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 5L18 7L22 3M12.5 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21H17C17.93 21 18.395 21 18.7765 20.8978C19.8117 20.6204 20.6204 19.8117 20.8978 18.7765C21 18.395 21 17.93 21 17M10.5 8.5C10.5 9.60457 9.60457 10.5 8.5 10.5C7.39543 10.5 6.5 9.60457 6.5 8.5C6.5 7.39543 7.39543 6.5 8.5 6.5C9.60457 6.5 10.5 7.39543 10.5 8.5ZM14.99 11.9181L6.53115 19.608C6.05536 20.0406 5.81747 20.2568 5.79643 20.4442C5.77819 20.6066 5.84045 20.7676 5.96319 20.8755C6.10478 21 6.42628 21 7.06929 21H16.456C17.8951 21 18.6147 21 19.1799 20.7582C19.8894 20.4547 20.4547 19.8894 20.7582 19.1799C21 18.6147 21 17.8951 21 16.456C21 15.9717 21 15.7296 20.9471 15.5042C20.8805 15.2208 20.753 14.9554 20.5733 14.7264C20.4303 14.5442 20.2412 14.3929 19.8631 14.0905L17.0658 11.8527C16.6874 11.5499 16.4982 11.3985 16.2898 11.3451C16.1061 11.298 15.9129 11.3041 15.7325 11.3627C15.5279 11.4291 15.3486 11.5921 14.99 11.9181Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
            else:
                return """
                <div class="upload-svg-wrapper" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """

        image_input.change(
            fn=on_image_upload,
            inputs=[image_input, msg, chatbot],
            outputs=[upload_icon],
            show_progress=False
        )

        def resize_image(img, max_size=800):
            """Resize image while maintaining aspect ratio if either dimension exceeds max_size"""
            if img is None: return None 
            if img.size[0] > max_size or img.size[1] > max_size:
                ratio = min(max_size/img.size[0], max_size/img.size[1])
                new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
                return img.resize(new_size, Image.Resampling.LANCZOS)
            return img

        def user_message(message, chat_history, temp, top_p, min_p, top_k, max_len, rep_penalty, img, system_prompt):
            time.sleep(0.001)  

            # Define SVG HTML generators with different sizes based on state
            def get_initial_svg_html():
                return """
                <div class="send-svg-wrapper" title="Send Message" style="width: 42px; height: 42px; transform: scale(1.2);">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """

            def get_active_svg_html():
                return """
                <div class="send-svg-wrapper" title="Send Message" style="width: 24px; height: 24px; transform: scale(1);">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """

            def get_initial_upload_html():
                return """
                <div class="upload-svg-wrapper" title="Upload Image" style="width: 32px; height: 32px; transform: scale(1.2);" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """

            def get_active_upload_html():
                return """
                <div class="upload-svg-wrapper" title="Upload Image" style="width: 24px; height: 24px; transform: scale(1);" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """

            # If no message and no image, keep initial state
            if not message.strip() and img is None:
                return (
                    message,
                    img,
                    chat_history,
                    gr.update(visible=False),
                    gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]),
                    gr.update(value=get_initial_upload_html(), elem_classes=["custom-upload", "initial-state"]),
                    gr.update(value=get_initial_svg_html(), elem_classes=["custom-send", "initial-state"])
                )

            chat_history = chat_history or []

            if not chat_history or chat_history[0].get("role") != "system":
                chat_history.insert(0, {"role": "system", "content": system_prompt})
            elif chat_history[0].get("role") == "system":
                if chat_history[0]["content"] != system_prompt:
                     chat_history[0]["content"] = system_prompt

            user_content = message.strip() if message else ""
            processed_img = None 
            if img is not None:
                img_resized = resize_image(img) 

                buffered = BytesIO()
                img_resized.save(buffered, format="PNG") 
                img_str = base64.b64encode(buffered.getvalue()).decode()
                img_html = f"<img src='data:image/png;base64,{img_str}' alt='User Upload' style='max-width: 200px; max-height: 200px; display: block; margin-top: 5px;'>"

                if user_content:
                    user_content = f"{user_content}\n{img_html}"
                else:
                    user_content = img_html

                processed_img = None 

            chat_history.append({"role": "user", "content": user_content})
            chat_history.append({"role": "assistant", "content": ""})

            response_stream = mock_chat_response(message, temp, top_p, max_len, img)
            for partial_response in response_stream:
                chat_history[-1]["content"] = partial_response
                yield "", processed_img, chat_history, gr.update(visible=True), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active"]), gr.update(value=get_active_upload_html(), elem_classes=["custom-upload", "active-chat"]), gr.update(value=get_active_svg_html(), elem_classes=["custom-send", "active-chat"])

            # When returning, update to active state
            return (
                "",
                processed_img,
                chat_history,
                gr.update(visible=True),
                gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active"]),
                gr.update(value=get_active_upload_html(), elem_classes=["custom-upload", "active-chat"]),
                gr.update(value=get_active_svg_html(), elem_classes=["custom-send", "active-chat"])
            )

        # Event handlers for message submission
        msg.submit(
            user_message,
            inputs=[msg, chatbot, temperature, top_p, min_p, top_k, max_length, repetition_penalty, image_input, system_prompt],
            outputs=[msg, image_input, chatbot, chatbot, msg, upload_icon, send_button],
            show_progress=False,
            queue=True
        )

        send_button.click(
            user_message,
            inputs=[msg, chatbot, temperature, top_p, min_p, top_k, max_length, repetition_penalty, image_input, system_prompt],
            outputs=[msg, image_input, chatbot, chatbot, msg, upload_icon, send_button],
            show_progress=False,
            queue=True
        )

        # !State for storing chat sessions for demo purposes!
        # !This is a placeholder, we will probably use a database to store the chat sessions!
        chat_sessions = gr.State([])  # List of {id, title, timestamp, messages}
        current_chat_id = gr.State(None)

        def clear_chat(chat_sessions_list, current_chat, chatbot_history):
            # Save current chat if it exists
            if chatbot_history and len(chatbot_history) > 0:
                chat_id = current_chat if current_chat else str(uuid.uuid4())
                
                # Find first user message and extract title
                user_content = next((msg["content"] for msg in chatbot_history if msg["role"] == "user"), "")
                if "<img" in user_content:
                    title = "Image Chat"
                else:
                    title = user_content[:30] + "..." if len(user_content) > 30 else user_content
                
                if not title.strip():
                    title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                new_session = {
                    "id": chat_id,
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "messages": chatbot_history
                }
                
                if not current_chat:
                    chat_sessions_list.append(new_session)
                else:
                    for i, session in enumerate(chat_sessions_list):
                        if session["id"] == current_chat:
                            chat_sessions_list[i] = new_session
                            break
            
            # Generate saved chats HTML
            saved_chats_html = """
            <div class="saved-chats-list" id="saved-chats-list">
            """
            for session in sorted(chat_sessions_list, key=lambda x: x["timestamp"], reverse=True):
                saved_chats_html += f"""
                <div class="saved-chat-item" data-chat-id="{session['id']}" onclick="handleChatClick('{session['id']}')">
                    <div class="chat-title">{session['title']}</div>
                    <div class="chat-timestamp">{datetime.fromisoformat(session['timestamp']).strftime('%Y-%m-%d %H:%M')}</div>
                </div>
                """
            saved_chats_html += "</div>"

            # Keep the original SVG HTML content
            upload_html = f"""
            <div class="upload-svg-wrapper initial-state" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            """

            send_html = f"""
            <div class="send-svg-wrapper initial-state" title="Send Message">
                <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            """
            
            return (
                [],  # Clear chat history
                "You are a helpful AI assistant.",  # Reset system prompt
                gr.update(visible=False),  # Hide chatbot
                gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]),  # Reset input style
                gr.update(value=upload_html, elem_classes=["custom-upload"]),  # Reset upload button with SVG content
                gr.update(value=send_html, elem_classes=["custom-send"]),  # Reset send button with SVG content
                gr.update(value=None, visible=False),  # Clear image input
                chat_sessions_list,
                None,  # Clear current chat ID
                saved_chats_html
            )

        # Load saved chat
        def load_chat(chat_id, chat_sessions_list):
            for session in chat_sessions_list:
                if session["id"] == chat_id:
                    return (
                        session["messages"],  # Load chat history
                        session["messages"][0]["content"] if session["messages"] else "You are a helpful AI assistant.",  # Load system prompt
                        gr.update(visible=True),  # Show chatbot
                        gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active"]),  
                        chat_id  # Set current chat ID
                    )
            return [], "You are a helpful AI assistant.", gr.update(visible=False), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]), None

        # !placeholder for demo purposes!
        def handle_chat_click(raw_value, chat_sessions_list):
            # Extract chat_id from the raw value if it exists
            chat_id = None
            try:
                # The raw_value will be the HTML of the clicked item
                import re
                match = re.search(r'data-chat-id="([^"]+)"', raw_value)
                if match:
                    chat_id = match.group(1)
                    print(f"Found chat ID: {chat_id}") 
                
                if not chat_id:
                    return [], "You are a helpful AI assistant.", gr.update(visible=False), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]), gr.update(), gr.update(), gr.update(value=None, visible=False), None
            
            except Exception as e:
                print(f"Error extracting chat ID: {e}")
                return [], "You are a helpful AI assistant.", gr.update(visible=False), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]), gr.update(), gr.update(), gr.update(value=None, visible=False), None

            # Find the matching session
            matching_session = None
            for session in chat_sessions_list:
                if session["id"] == chat_id:
                    matching_session = session
                    break
            
            if matching_session:
                messages = matching_session["messages"]
                system_prompt_val = messages[0]["content"] if messages else "You are a helpful AI assistant."
                
                initial_upload_html = """
                <div class="upload-svg-wrapper active-chat" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                initial_send_html = """
                <div class="send-svg-wrapper active-chat" title="Send Message">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                return (
                    messages,  # chatbot
                    system_prompt_val,  # system_prompt
                    gr.update(visible=True),  # chatbot visibility
                    gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active"]),  # msg style
                    gr.update(value=initial_upload_html, elem_classes=["custom-upload", "active-chat"]),  # upload_icon
                    gr.update(value=initial_send_html, elem_classes=["custom-send", "active-chat"]),  # send_button
                    gr.update(value=None, visible=False),  # image_input
                    chat_id  # current_chat_id
                )
            
            # Return default values if chat not found
            return (
                [],  # Empty chat history
                "You are a helpful AI assistant.",  # Default system prompt
                gr.update(visible=False),  # Hide chatbot
                gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]),  # Initial input style
                gr.update(value=initial_upload_html, elem_classes=["custom-upload", "initial-state"]),  # Initial upload button
                gr.update(value=initial_send_html, elem_classes=["custom-send", "initial-state"]),  # Initial send button
                gr.update(value=None, visible=False),  # Clear image input
                None  # Clear current chat ID
            )

        # Update the click handler registration to use click instead of select
        saved_chats.click(
            fn=handle_chat_click,
            inputs=[saved_chats, chat_sessions],
            outputs=[chatbot, system_prompt, chatbot, msg, upload_icon, send_button, image_input, current_chat_id],
            show_progress=False
        )

        # Update the new chat button click handler
        new_chat_btn.click(
            clear_chat,
            inputs=[chat_sessions, current_chat_id, chatbot],
            outputs=[chatbot, system_prompt, chatbot, msg, upload_icon, send_button, image_input, chat_sessions, current_chat_id, saved_chats],
            queue=False
        )

        # Stateful SVGs in chat interface and chat history
        js = """
        <script>
            function updateSVGState() {
                const input = document.querySelector('.chat-input textarea');  // Changed to target textarea
                const uploadWrapper = document.querySelector('.upload-svg-wrapper');
                const sendWrapper = document.querySelector('.send-svg-wrapper');
                const uploadContainer = document.querySelector('.block.custom-upload.svelte-11xb1hd');
                const sendContainer = document.querySelector('.block.custom-send.svelte-11xb1hd');
                
                if (input && uploadWrapper && sendWrapper && uploadContainer && sendContainer) {
                    if (input.value.trim()) {
                        uploadWrapper.classList.remove('initial-state');
                        sendWrapper.classList.remove('initial-state');
                        uploadContainer.classList.remove('initial-state');
                        sendContainer.classList.remove('initial-state');
                        
                        uploadContainer.classList.add('active-chat');
                        sendContainer.classList.add('active-chat');
                        
                        input.closest('.chat-input').classList.remove('chat-input-initial');
                        input.closest('.chat-input').classList.add('chat-input-active');
                    } else {
                        uploadWrapper.classList.add('initial-state');
                        sendWrapper.classList.add('initial-state');
                        uploadContainer.classList.add('initial-state');
                        sendContainer.classList.add('initial-state');
                        
                        uploadContainer.classList.remove('active-chat');
                        sendContainer.classList.remove('active-chat');
                        
                        input.closest('.chat-input').classList.remove('chat-input-active');
                        input.closest('.chat-input').classList.add('chat-input-initial');
                    }
                }
            }

            function initializeEventListeners() {
                const input = document.querySelector('.chat-input textarea');
                if (input) {
                    input.addEventListener('input', updateSVGState);
                    setTimeout(updateSVGState, 100);
                    
                    document.addEventListener('click', function(e) {
                        if (e.target.closest('.custom-upload') || e.target.closest('.custom-send')) {
                            setTimeout(updateSVGState, 100);
                        }
                    });
                } else {
                    setTimeout(initializeEventListeners, 500);
                }
            }

            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeEventListeners);
            } else {
                initializeEventListeners();
            }

            document.addEventListener('gradio-loaded', function() {
                initializeEventListeners();
                const uploadContainer = document.querySelector('.block.custom-upload.svelte-11xb1hd');
                const sendContainer = document.querySelector('.block.custom-send.svelte-11xb1hd');
                if (uploadContainer && sendContainer) {
                    uploadContainer.classList.add('initial-state');
                    sendContainer.classList.add('initial-state');
                }
            });

            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.addedNodes.length) {
                        initializeEventListeners();
                    }
                }
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });

            // Update the click handler for saved chats
            function handleChatClick(chatId) {
                const savedChatsContainer = document.getElementById('saved-chats-container');
                if (savedChatsContainer) {
                    // Find the specific chat item
                    const clickedItem = document.querySelector(`[data-chat-id="${chatId}"]`);
                    if (clickedItem) {
                        // Create a temporary container with just the clicked item
                        const tempContainer = document.createElement('div');
                        tempContainer.innerHTML = clickedItem.outerHTML;
                        
                        // Trigger the click event with the specific item's HTML
                        const event = new Event('click', { bubbles: true });
                        savedChatsContainer.innerHTML = tempContainer.innerHTML;
                        savedChatsContainer.dispatchEvent(event);
                        
                        // Restore the original content after a short delay
                        setTimeout(() => {
                            savedChatsContainer.innerHTML = document.querySelector('.saved-chats-list').outerHTML;
                            initializeChatClickHandlers();
                        }, 100);
                    }
                }
            }

            // Initialize click handlers for saved chat items
            function initializeChatClickHandlers() {
                const chatItems = document.querySelectorAll('.saved-chat-item');
                chatItems.forEach(item => {
                    item.onclick = function(e) {
                        e.stopPropagation(); // Prevent event bubbling
                        const chatId = this.getAttribute('data-chat-id');
                        handleChatClick(chatId);
                    };
                });
            }

            // Add to existing observers
            const chatObserver = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.addedNodes.length) {
                        initializeChatClickHandlers();
                    }
                }
            });

            // Observe the saved chats container
            const savedChatsContainer = document.getElementById('saved-chats-container');
            if (savedChatsContainer) {
                chatObserver.observe(savedChatsContainer, {
                    childList: true,
                    subtree: true
                });
            }

            // Initialize on page load
            document.addEventListener('DOMContentLoaded', initializeChatClickHandlers);
            document.addEventListener('gradio-loaded', initializeChatClickHandlers);
        </script>
        """

        gr.HTML(js)

        # Components dictionary
        return {
            'chatbot': chatbot,
            'msg': msg,
            'image_input': image_input,
            'temperature': temperature,
            'top_p': top_p,
            'top_k': top_k,
            'min_p': min_p,
            'max_length': max_length,
            'repetition_penalty': repetition_penalty,
            'system_prompt': system_prompt,
            'model_dropdown': model_dropdown,
            'model_search': model_search,
            'chat_template': chat_template,
            'settings_panel': settings_panel,
            'send_button': send_button,
            'upload_icon': upload_icon,
            'chat_sessions': chat_sessions,
            'current_chat_id': current_chat_id,
            'saved_chats': saved_chats
        }

# If running this file directly (for testing)
# if __name__ == "__main__":
#     chat_ui_dict = create_chat_interface()
#     chat_interface = chat_ui_dict['chatbot'].parent.parent 
#     chat_interface.launch()
