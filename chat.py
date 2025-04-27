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
        time.sleep(0.05)  

def create_chat_interface():
    examples = [
        "hello world",
        "what's up?", 
        "this is GradioChat"
    ]

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald")) as chat_interface:
        
        # Main Chat Area
        with gr.Column(scale=10):
            # Header row 
            with gr.Row(elem_classes=["chat-header"], equal_height=True):
                 gr.Markdown("## Welcome to Unsloth Chat")

            # Chat History
            chatbot = gr.Chatbot(
                height=600,
                show_label=False,
                elem_classes=["chat-history", "modern-chat"],
                container=True,
                type="messages",
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
            
            
            MAX_SESSIONS = 10
            sessions_state = gr.State([None]*MAX_SESSIONS)  # Store session data
            
            # System prompt defined before we use it in handlers
            system_prompt = gr.Textbox(
                value="You are a helpful AI assistant.",
                info="Defines the LLM's style of response",
                label="System Prompt", 
                lines=3,
                placeholder="Define the LLM's behavior and role...",
                elem_id="system-prompt-textbox",
                visible=False  
            )
             
            new_chat_btn = gr.Button("New Chat", elem_classes=["new-chat-btn"])
            
            # Create session buttons
            session_buttons = []
            for i in range(MAX_SESSIONS):
                btn = gr.Button(
                    visible=False,
                    elem_classes=["chat-session-btn"],
                )
                session_buttons.append(btn)
            
            current_chat_id = gr.State(None)  
            
            def create_new_chat(sessions, chat_history):
                # Find first available slot
                for i in range(MAX_SESSIONS):
                    if not sessions[i]:
                        title = "New Chat"
                        if chat_history and len(chat_history) > 1:  # Skip system message
                            user_msg = chat_history[1].get("content", "").strip()
                            if user_msg:
                                import re
                                clean_content = re.sub(r'<[^>]+>', '', user_msg).strip()
                                if re.search(r'<img', user_msg, re.IGNORECASE) or clean_content == "":
                                    title = "Image Chat"
                                else:
                                    clean_content = ' '.join(clean_content.split())
                                    title = clean_content[:20] + ('...' if len(clean_content) > 20 else '')
                        sessions[i] = {
                            "id": str(uuid.uuid4()),
                            "title": title,
                            "timestamp": datetime.now().isoformat(),
                            "messages": chat_history if chat_history else []
                        }
                        break
                
                # Sort sessions by timestamp (newest first) and reorder the actual sessions array
                # First, collect all non-None sessions with their original indices
                active_sessions = [(i, session) for i, session in enumerate(sessions) if session]
                # Sort by timestamp, newest first
                active_sessions.sort(key=lambda x: x[1]['timestamp'], reverse=True)
                
                # Create a new sessions array with the correct order
                new_sessions = [None] * MAX_SESSIONS
                for new_idx, (old_idx, session) in enumerate(active_sessions):
                    new_sessions[new_idx] = session
                
                # Update the original sessions array with the new order
                sessions[:] = new_sessions
                
                # Create button updates based on the new order
                button_updates = []
                for i in range(MAX_SESSIONS):
                    if sessions[i]:
                        title = sessions[i]['title']
                        timestamp = datetime.fromisoformat(sessions[i]['timestamp']).strftime('%Y-%m-%d %H:%M')
                        label = f"{title}\n{timestamp}"
                        button_updates.append(gr.update(
                            value=label,
                            visible=True,
                            elem_classes=["chat-session-btn"]
                        ))
                    else:
                        button_updates.append(gr.update(visible=False))
                
                # Clear current chat
                return (
                    sessions,  # sessions state with updated order
                    [],  # clear chatbot
                    "You are a helpful AI assistant.",  # reset system prompt
                    gr.update(visible=False),  # hide chatbot
                    gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]),  # reset input style
                    gr.update(value=None, visible=False),  # clear image
                    *button_updates  # update all buttons
                )

            def load_chat_session(idx, sessions):
                if not sessions[idx]:
                    return [], "You are a helpful AI assistant.", gr.update(visible=False)
                
                session = sessions[idx]
                
                active_upload_html = """
                <div class="upload-svg-wrapper active-chat force-active" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                active_send_html = """
                <div class="send-svg-wrapper active-chat force-active" title="Send Message">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                return (
                    session["messages"],               
                    session["messages"][0]["content"] if session["messages"] else "You are a helpful AI assistant.", 
                    gr.update(visible=True),            
                    gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active", "force-active"]), 
                    gr.update(value=active_upload_html, elem_classes=["custom-upload", "active-chat", "force-active"]),  # upload icon
                    gr.update(value=active_send_html, elem_classes=["custom-send", "active-chat", "force-active"]),      # send button
                    gr.update(value=None, visible=False),  # image input
                    idx                                    # current chat id
                )

            # Event handlers
            new_chat_btn.click(
                create_new_chat,
                inputs=[sessions_state, chatbot],
                outputs=[sessions_state, chatbot, system_prompt, chatbot, msg, image_input] + session_buttons,
                show_progress=False,
                queue=False
            )

            # Add click handlers for each session button
            for i, btn in enumerate(session_buttons):
                btn.click(
                    load_chat_session,
                    inputs=[gr.State(i), sessions_state],
                    outputs=[
                        chatbot,                    # chat messages
                        system_prompt,              # system prompt
                        chatbot,                    # chatbot visibility
                        msg,                        # input box styling
                        upload_icon,                # upload icon
                        send_button,                # send button
                        image_input,                # image input
                        current_chat_id             # current chat ID
                    ],
                    show_progress=False,
                    queue=False
                )

        # Settings panel
        with gr.Column(visible=True, elem_id="settings-panel-column") as settings_panel:
            gr.Markdown("## Settings")
            
            # Create a state to track which accordion is open
            accordion_state = gr.State("none")  # Can be "none", "model", "sampling", or "prompting"
            
            # Model Selection
            model_accordion = gr.Accordion("Model Selection", open=False)
            with model_accordion:
                with gr.Column(elem_classes=["model-selection-controls"]):
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
                    )
                    with gr.Column(scale=2):
                        model_search = gr.Textbox(
                            label="Search",
                            placeholder="Search for a model...",
                            interactive=True,
                        )
                    with gr.Column(scale=2):    
                        hf_token = gr.Textbox(
                            placeholder="Enter your token",
                            label="Hugging Face",
                            interactive=True,
                            scale=1,
                            elem_classes="token-input-model-selection",
                )

            # Sampling Parameters
            sampling_accordion = gr.Accordion("Sampling Parameters", open=False, elem_classes=["sampling-parameters", "sampling-accordion"])
            with sampling_accordion:
                with gr.Row():
                    with gr.Column():
                        temperature = gr.Slider(
                            minimum=0.1, maximum=2.0, value=0.7, step=0.1,
                            label="Temperature", info="Controls randomness (higher = more random)"
                        )
                        top_p = gr.Slider(
                            minimum=0.1, maximum=1.0, value=0.9, step=0.1,
                            label="Top P", info="Limits token selection probability"
                        )
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
            prompting_accordion = gr.Accordion("Prompting", open=False, elem_classes=["prompting-accordion"])
            with prompting_accordion:
                with gr.Row():
                    with gr.Column(scale=2):
                        system_prompt = gr.Textbox(
                            value="You are a helpful AI assistant.",
                            info="Defines the LLM's style of response",
                            label="System Prompt", lines=3,
                            placeholder="Define the LLM's behavior and role..."
                        )                


            def update_accordion_state(current_state, expanded_accordion):
                """Updates accordion states when one is expanded"""
                # Base state where all accordions are closed
                base_state = {
                    "none": False,
                    "model": False,
                    "sampling": False,
                    "prompting": False
                }
                
                # Return all closed
                if expanded_accordion == current_state:
                    new_state = "none"
                else:
                    base_state[expanded_accordion] = True
                    new_state = expanded_accordion
                
                # Boolean states convert to gradio update objects
                return (new_state,) + tuple(gr.update(open=base_state[k]) for k in ["model", "sampling", "prompting"])

            def handle_collapse(state):
                """Handler for collapse events"""
                return (
                    "none",
                    gr.update(open=False),  # model_accordion
                    gr.update(open=False),  # sampling_accordion
                    gr.update(open=False)   # prompting_accordion
                )

            # Handlers for each accordion
            model_accordion.expand(
                fn=update_accordion_state,
                inputs=[accordion_state, gr.State("model")],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

            model_accordion.collapse(
                fn=handle_collapse,
                inputs=[accordion_state],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

            sampling_accordion.expand(
                fn=update_accordion_state,
                inputs=[accordion_state, gr.State("sampling")],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

            sampling_accordion.collapse(
                fn=handle_collapse,
                inputs=[accordion_state],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

            prompting_accordion.expand(
                fn=update_accordion_state,
                inputs=[accordion_state, gr.State("prompting")],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

            prompting_accordion.collapse(
                fn=handle_collapse,
                inputs=[accordion_state],
                outputs=[
                    accordion_state,
                    model_accordion,
                    sampling_accordion,
                    prompting_accordion
                ],
                show_progress=False
            )

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

        def user_message(message, chat_history, temp, top_p, top_k, max_len, rep_penalty, img, system_prompt):

            # Validate input: Check if both message and image are empty
            if not message.strip() and img is None:
                raise gr.Error("Remember to send a message!")

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


            def get_active_upload_html():
                return """
                <div class="upload-svg-wrapper" title="Upload Image" style="width: 24px; height: 24px; transform: scale(1);" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """


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
            inputs=[msg, chatbot, temperature, top_p, top_k, max_length, repetition_penalty, image_input, system_prompt],
            outputs=[msg, image_input, chatbot, chatbot, msg, upload_icon, send_button],
            show_progress=False,
            queue=True
        )

        send_button.click(
            user_message,
            inputs=[msg, chatbot, temperature, top_p, top_k, max_length, repetition_penalty, image_input, system_prompt],
            outputs=[msg, image_input, chatbot, chatbot, msg, upload_icon, send_button],
            show_progress=False,
            queue=True
        )

        # !State for storing chat sessions for demo purposes!
        # !This is a placeholder, we will probably use a database to store the chat sessions!
        chat_sessions = gr.State([])  # List of {id, title, timestamp, messages}

        def clear_chat(chat_sessions_list, current_chat, chatbot_history):
            # Save current chat if it exists
            if chatbot_history and len(chatbot_history) > 0:
                chat_id = current_chat if current_chat else str(uuid.uuid4())
                
                # Find first user message and extract title
                user_content = next((msg["content"] for msg in chatbot_history if msg["role"] == "user"), "")
                
                # Remove any HTML tags for title generation
                if "<img" in user_content:
                    title = "Image Chat"
                else:
                    # Remove HTML tags if any
                    import re
                    clean_content = re.sub(r'<[^>]+>', '', user_content)
                    # Remove newlines and extra spaces
                    clean_content = ' '.join(clean_content.split())
                    # Limit to exactly 20 characters and add ellipsis if needed
                    title = clean_content[:20] + ('...' if len(clean_content) > 20 else '')
                
                if not title.strip():
                    title = f"Chat {datetime.now().strftime('%H:%M')}"
                
                new_session = {
                    "id": chat_id,
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "messages": chatbot_history
                }
                
                if not current_chat:
                    chat_sessions_list.insert(0, new_session)  # Insert at beginning instead of append
                else:
                    for i, session in enumerate(chat_sessions_list):
                        if session["id"] == current_chat:
                            chat_sessions_list[i] = new_session
                            break
            
            # Update dropdown choices
            choices = [(session["title"], session["id"]) 
                      for session in sorted(chat_sessions_list, key=lambda x: x["timestamp"], reverse=True)]
            
            # Keep the original SVG HTML content
            upload_html = """
            <div class="upload-svg-wrapper initial-state" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            """

            send_html = """
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
                chat_sessions_list,  # Updated chat sessions
                None  # Clear current chat ID
            )

        def on_chat_selected(selected_chat_id, chat_sessions_list):
            if not selected_chat_id:
                return [], "You are a helpful AI assistant.", gr.update(visible=False), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]), gr.update(), gr.update(), gr.update(value=None, visible=False), None

            # Find the matching session
            matching_session = None
            for session in chat_sessions_list:
                if session["id"] == selected_chat_id:
                    matching_session = session
                    break
            
            if matching_session:
                messages = matching_session["messages"]
                system_prompt_val = messages[0]["content"] if messages else "You are a helpful AI assistant."
                
                # Always set to active state when chat is selected
                active_upload_html = """
                <div class="upload-svg-wrapper active-chat force-active" title="Upload Image" onclick="document.querySelector('.chat-image-input input[type=\\'file\\']').click()">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                active_send_html = """
                <div class="send-svg-wrapper active-chat force-active" title="Send Message">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.5004 12H5.00043M4.91577 12.2915L2.58085 19.2662C2.39742 19.8142 2.3057 20.0881 2.37152 20.2569C2.42868 20.4034 2.55144 20.5145 2.70292 20.5567C2.87736 20.6054 3.14083 20.4869 3.66776 20.2497L20.3792 12.7296C20.8936 12.4981 21.1507 12.3824 21.2302 12.2216C21.2993 12.082 21.2993 11.9181 21.2302 11.7784C21.1507 11.6177 20.8936 11.5019 20.3792 11.2705L3.66193 3.74776C3.13659 3.51135 2.87392 3.39315 2.69966 3.44164C2.54832 3.48375 2.42556 3.59454 2.36821 3.74078C2.30216 3.90917 2.3929 4.18255 2.57437 4.72931L4.91642 11.7856C4.94759 11.8795 4.96317 11.9264 4.96933 11.9744C4.97479 12.0171 4.97473 12.0602 4.96916 12.1028C4.96289 12.1508 4.94718 12.1977 4.91577 12.2915Z" stroke="#55b685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                """
                
                return (
                    messages,  # chatbot
                    system_prompt_val,  # system_prompt
                    gr.update(visible=True),  # chatbot visibility
                    gr.update(elem_classes=["chat-input", "modern-input", "chat-input-active", "force-active"]),  # msg style - always active
                    gr.update(value=active_upload_html, elem_classes=["custom-upload", "active-chat", "force-active"]),  # upload_icon - always active
                    gr.update(value=active_send_html, elem_classes=["custom-send", "active-chat", "force-active"]),  # send_button - always active
                    gr.update(value=None, visible=False),  # image_input
                    selected_chat_id  # current_chat_id
                )
            
            return [], "You are a helpful AI assistant.", gr.update(visible=False), gr.update(elem_classes=["chat-input", "modern-input", "chat-input-initial"]), gr.update(), gr.update(), gr.update(value=None, visible=False), None

        # Update the new chat button click handler
        new_chat_btn.click(
            clear_chat,
            inputs=[chat_sessions, current_chat_id, chatbot],
            outputs=[chatbot, system_prompt, chatbot, msg, upload_icon, send_button, image_input, chat_sessions, current_chat_id],
            show_progress=False,
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
                    // Check if we have force-active class
                    const isForceActive = input.closest('.chat-input').classList.contains('force-active');
                    
                    if (isForceActive || input.value.trim()) {
                        uploadWrapper.classList.remove('initial-state');
                        sendWrapper.classList.remove('initial-state');
                        uploadContainer.classList.remove('initial-state');
                        sendContainer.classList.remove('initial-state');
                        
                        uploadContainer.classList.add('active-chat');
                        sendContainer.classList.add('active-chat');
                        
                        input.closest('.chat-input').classList.remove('chat-input-initial');
                        input.closest('.chat-input').classList.add('chat-input-active');
                    } else if (!isForceActive) {
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

            const accordionTransition = () => {
                const accordions = document.querySelectorAll('.gradio-accordion');
                accordions.forEach(accordion => {
                    const header = accordion.querySelector('.accordion-header');
                    if (header) {
                        header.addEventListener('click', () => {
                            // First close all accordions
                            accordions.forEach(acc => {
                                if (acc !== accordion && acc.classList.contains('accordion-open')) {
                                    acc.classList.remove('accordion-open');
                                    const content = acc.querySelector('.accordion-content');
                                    if (content) {
                                        content.style.maxHeight = '0px';
                                    }
                                }
                            });
                            
                            // After a small delay, open the clicked accordion if it wasn't already open
                            setTimeout(() => {
                                if (!accordion.classList.contains('accordion-open')) {
                                    accordion.classList.add('accordion-open');
                                    const content = accordion.querySelector('.accordion-content');
                                    if (content) {
                                        content.style.maxHeight = content.scrollHeight + 'px';
                                    }
                                }
                            }, 150); // 150ms delay for smooth transition
                        });
                    }
                });
            };

            document.addEventListener('gradio-loaded', accordionTransition);
            observer.observe(document.body, { childList: true, subtree: true });
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
            'hf_token': hf_token,
            'max_length': max_length,
            'repetition_penalty': repetition_penalty,
            'system_prompt': system_prompt,
            'model_dropdown': model_dropdown,
            'model_search': model_search,
            'settings_panel': settings_panel,
            'send_button': send_button,
            'upload_icon': upload_icon,
            'chat_sessions': chat_sessions,
            'current_chat_id': current_chat_id
        }

def render_chat_buttons(chat_sessions_list, current_chat_id):
    html = '<div class="custom-chat-buttons">'
    for session in sorted(chat_sessions_list, key=lambda x: x["timestamp"], reverse=True):
        active = "active" if session["id"] == current_chat_id else ""
        html += f"""
        <button class="chat-history-btn {active}" 
                onclick="window.setChatDropdown('{session['id']}')">
            <div class="chat-title">{session['title']}</div>
            <div class="chat-timestamp">{datetime.fromisoformat(session['timestamp']).strftime('%Y-%m-%d %H:%M')}</div>
        </button>
        """
    html += "</div>"
    return html