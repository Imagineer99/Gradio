import gradio as gr
from PIL import Image

# Image processing
import base64
from io import BytesIO

# Mock response to test the chat interface
def mock_chat_response(message, temperature, top_p, max_length, image=None):
    """Mock response function that returns hardcoded responses"""
    if image is not None:
        return "I see you've shared an image!"
    
    responses = [
        "That's an interesting point! Let me think about it...",
        "I understand what you're asking. Here's my perspective...",
        "Based on my knowledge, I would say...",
        "That's a great question! Here's what I think...",
    ]
    import random
    return random.choice(responses)

def create_chat_interface():
    with gr.Blocks() as chat_interface:
        # Combined Model Selection and Chat Interface Card
        with gr.Column(elem_classes=["card", "chat-card"]):
            gr.Markdown("## Chat Interface")
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
                    elem_classes=["model-selection-controls"],
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

            # Chat History
            chatbot = gr.Chatbot(
                height=500,
                show_label=False,
                elem_classes=["chat-history", "modern-chat"],
                container=False,
                type="messages",
                avatar_images=["user.png", "assistant.png"],
            )
            
            # Input Area
            with gr.Row(elem_classes=["chat-input-row"]):
                with gr.Column(scale=8):
                    msg = gr.Textbox(
                        placeholder="Message...",
                        show_label=False,
                        elem_classes=["chat-input", "modern-input"],
                        container=False,
                        
                    )
                with gr.Column(scale=1, elem_classes=["chat-controls"]):
                    image_input = gr.Image(
                        label="",
                        type="pil",
                        elem_classes=["chat-image-input"],
                        show_label=False,
                        container=False,
                        visible=False
                    )
                    upload_icon = gr.HTML(
                        value="""
                        <div class="upload-svg-wrapper" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                            <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" 
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        """,
                        elem_classes=["custom-upload"]
                    )

                    def on_image_upload(image):
                        print("Image uploaded:", image)
                        if image is not None:
                            return """
                            <div class="upload-svg-wrapper" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                                <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M16 5L18 7L22 3M12.5 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21H17C17.93 21 18.395 21 18.7765 20.8978C19.8117 20.6204 20.6204 19.8117 20.8978 18.7765C21 18.395 21 17.93 21 17M10.5 8.5C10.5 9.60457 9.60457 10.5 8.5 10.5C7.39543 10.5 6.5 9.60457 6.5 8.5C6.5 7.39543 7.39543 6.5 8.5 6.5C9.60457 6.5 10.5 7.39543 10.5 8.5ZM14.99 11.9181L6.53115 19.608C6.05536 20.0406 5.81747 20.2568 5.79643 20.4442C5.77819 20.6066 5.84045 20.7676 5.96319 20.8755C6.10478 21 6.42628 21 7.06929 21H16.456C17.8951 21 18.6147 21 19.1799 20.7582C19.8894 20.4547 20.4547 19.8894 20.7582 19.1799C21 18.6147 21 17.8951 21 16.456C21 15.9717 21 15.7296 20.9471 15.5042C20.8805 15.2208 20.753 14.9554 20.5733 14.7264C20.4303 14.5442 20.2412 14.3929 19.8631 14.0905L17.0658 11.8527C16.6874 11.5499 16.4982 11.3985 16.2898 11.3451C16.1061 11.298 15.9129 11.3041 15.7325 11.3627C15.5279 11.4291 15.3486 11.5921 14.99 11.9181Z" 
                                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                            """
                        return upload_icon.value

                    image_input.change(
                        fn=on_image_upload,
                        inputs=[image_input],
                        outputs=[upload_icon],
                        show_progress=False
                    )

        # Sampling Parameters Card
        with gr.Column(elem_classes=["card", "sampling-params"]):
            gr.Markdown("## Sampling Parameters")
            with gr.Row():
                with gr.Column():
                    temperature = gr.Slider(
                        minimum=0.1,
                        maximum=2.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature",
                        info="Controls randomness (higher = more random)",
                    )
                    top_p = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.9,
                        step=0.1,
                        label="Top P",
                        info="Limits token selection to the most likely ones up to probability P",
                    )
                    min_p = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.1,
                        step=0.05,
                        label="Min P",
                        info="Limits token selection by filtering out tokens below probability P",
                    )
                with gr.Column():
                    top_k = gr.Slider(
                        minimum=1,
                        maximum=100,
                        value=40,
                        step=1,
                        label="Top K",
                        info="Limits token selection to the K value",
                    )                
                    max_length = gr.Slider(
                        minimum=50,
                        maximum=2000,
                        value=512,
                        step=50,
                        label="Max New Tokens",
                        info="Maximum response length",
                    )
                    repetition_penalty = gr.Slider(
                        minimum=1.0,
                        maximum=2.0,
                        value=1.1,
                        step=0.1,
                        label="Repetition Penalty",
                        info="Penalizes repeated tokens (higher = less repetition)",
                    )

        # Prompting Card
        with gr.Column(elem_classes=["card", "prompting-card"]):
            gr.Markdown("## Prompting")
            with gr.Row():
                with gr.Column(scale=2):
                    system_prompt = gr.Textbox(
                        value="You are a helpful AI assistant.",
                        info="The system prompt defines the LLM's style of response", 
                        label="System Prompt",
                        lines=3,
                        placeholder="Define the LLM's behavior and role...",
                        elem_classes=["system-prompt-input"],
                    )
                with gr.Column(scale=1):
                    chat_template = gr.Dropdown(
                        choices=[
                            "Auto-Select",
                            "Alpaca",
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
                        label="Chat Template",
                        info="Format of the conversation",
                        interactive=True,   
                        elem_classes=["template-selector"],
                    )

    def resize_image(img, max_size=800):
        """Resize image while maintaining aspect ratio if either dimension exceeds max_size"""
        if img.size[0] > max_size or img.size[1] > max_size:
            ratio = min(max_size/img.size[0], max_size/img.size[1])
            new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
            return img.resize(new_size, Image.Resampling.LANCZOS)
        return img

    def user_message(message, chat_history, temp, top_p, min_p, top_k, max_len, rep_penalty, img, system_prompt):
        if message or img is not None:
            chat_history = chat_history or []
            
            # If chat history is empty, add system message
            if not chat_history:
                chat_history.append({"role": "system", "content": system_prompt})
            
            user_content = message.strip() if message else ""
            if img is not None:
                # Resize image before converting to base64
                img = resize_image(img)
                
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                img_data = f"<img src='data:image/png;base64,{img_str}'>"
                
                if user_content:
                    user_content = f"{user_content}\n{img_data}"
                else:
                    user_content = img_data
            
            response = mock_chat_response(message, temp, top_p, max_len, img)
            
            chat_history.extend([
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": response}
            ])
            
            return "", None, chat_history
        return message, img, chat_history

    # Event handlers
    msg.submit(
        user_message,
        inputs=[msg, chatbot, temperature, top_p, min_p, top_k, max_length, repetition_penalty, image_input, system_prompt],
        outputs=[msg, image_input, chatbot],
        show_progress=False
    )

    # Clear chat button
    clear = gr.Button("Clear Chat", elem_classes=["clear-chat-btn"])
    clear.click(lambda: [], None, chatbot, queue=False)

    # Components dictionary
    return {
        'chatbot': chatbot,
        'model_search': model_search,
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
        'chat_template': chat_template,
    }
