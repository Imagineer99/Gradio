import gradio as gr

# Image processing
import base64
from io import BytesIO

# Mock response to test the chat interface
def mock_chat_response(message, temperature, top_p, max_length, image=None):
    """Mock response function that returns hardcoded responses"""
    if image is not None:
        return "I see you've shared an image! Here's a mock response about it: This appears to be an interesting image."
    
    responses = [
        "That's an interesting point! Let me think about it...",
        "I understand what you're asking. Here's my perspective...",
        "Based on my knowledge, I would say...",
        "That's a great question! Here's what I think...",
    ]
    import random
    return random.choice(responses)

def create_chat_interface():
    # Chat Interface Card
    with gr.Column(elem_classes=["card", "chat-card"]):
        gr.Markdown("## Chat Interface")
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
        # Chat History
        chatbot = gr.Chatbot(
            height=400,
            show_label=False,
            elem_classes=["chat-history"],
            type="messages",
        )
      
        # Input Area
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    placeholder="Type your message here...",
                    show_label=False,
                    elem_classes=["chat-input"],
                )
                system_prompt = gr.Textbox(
                    placeholder="Enter system prompt here...",
                    label="System Prompt",
                    value="You are a helpful AI assistant.",
                    lines=2,
                    interactive=True,
                )
            with gr.Column(scale=1):
                image_input = gr.Image(
                    label="Upload Image",
                    type="pil",
                    elem_classes=["chat-image-input"],
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
                    info="Nucleus sampling threshold",
                )
            with gr.Column():
                max_length = gr.Slider(
                    minimum=50,
                    maximum=2000,
                    value=512,
                    step=50,
                    label="Max Length",
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

    def user_message(message, chat_history, temp, top_p, max_len, rep_penalty, img):
        if message or img is not None:
            # Ensure chat_history is a list if it's None
            chat_history = chat_history or []
            
            # Format user content
            user_content = message.strip() if message else ""
            if img is not None:
                # Convert PIL image to base64 string
                
                # Convert PIL image to base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                img_data = f"<img src='data:image/png;base64,{img_str}'>"
                
                # Create user content with image
                if user_content:
                    user_content = f"{user_content}\n{img_data}"
                else:
                    user_content = img_data
            
            response = mock_chat_response(message, temp, top_p, max_len, img)
            
            # Add messages to chat history
            chat_history.extend([
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": response}
            ])
            
            return "", None, chat_history
        return message, img, chat_history

    # Event handlers
    msg.submit(
        user_message,
        inputs=[msg, chatbot, temperature, top_p, max_length, repetition_penalty, image_input],
        outputs=[msg, image_input, chatbot]
    )

    # Clear chat button
    clear = gr.Button("Clear Chat", elem_classes=["clear-chat-btn"])
    clear.click(lambda: [], None, chatbot, queue=False)

    # Components dictionary
    return {
        'chatbot': chatbot,
        'msg': msg,
        'image_input': image_input,
        'temperature': temperature,
        'top_p': top_p,
        'max_length': max_length,
        'repetition_penalty': repetition_penalty,
        'system_prompt': system_prompt,
        'model_dropdown': model_dropdown,
    }
