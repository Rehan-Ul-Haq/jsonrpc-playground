"""
JSON-RPC Client Interface using Streamlit

This module provides a modern, interactive web interface for testing JSON-RPC 2.0
protocol features including method calls, notifications, and error handling.
Built with Streamlit for easy demonstration and learning purposes.
"""

import json
import uuid
from typing import Any, Dict

import requests
import streamlit as st


class JSONRPCPlaygroundApp:
    """Interactive Streamlit application for JSON-RPC 2.0 learning and testing."""

    def __init__(self, server_url: str = "http://localhost:8080"):
        """Initialize the playground app.

        Args:
            server_url: URL of the JSON-RPC server
        """
        self.server_url = server_url
        self._setup_page_config()

    def _setup_page_config(self):
        """Setup page configuration and styling."""
        st.set_page_config(
            page_title="JSON-RPC Playground",
            page_icon="🧩",
            layout="wide",
            initial_sidebar_state="collapsed",
        )

        st.markdown(
            """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Main container styling */
        .main .block-container {
            max-width: 1200px;
            padding-top: 0.5rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            font-family: 'Inter', sans-serif;
        }
        
        /* header */
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-top: 0;
            margin-bottom: 0.25rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Inter', sans-serif;
        }
        
        .subtitle {
            font-size: 1rem;
            text-align: center;
            margin-top: 0;
            margin-bottom: 0.5rem;
            opacity: 0.8;
            font-weight: 400;
        }
        
        /* Simple developer credit styling */
        .simple-credit {
            text-align: center;
            font-size: 0.85rem;
            color: #777;
            margin-top: 0;
            margin-bottom: 1rem;
            font-weight: 400;
            font-family: 'Inter', sans-serif;
            opacity: 0.8;
        }
        
        /* Modern card styling */
        .stExpander {
            border: 1px solid rgba(103, 126, 234, 0.2);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(103, 126, 234, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            border-radius: 8px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            padding-bottom: 8px;
            margin-bottom: 20px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            font-weight: 500;
            padding: 10px 20px;
            font-size: 15px;
            transition: all 0.2s ease;
            border: 1px solid rgba(128, 128, 128, 0.3);
            background: transparent;
            color: inherit;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            border-color: rgba(128, 128, 128, 0.5);
            background: rgba(128, 128, 128, 0.1);
            transform: translateY(-1px);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(59, 130, 246, 0.1);
            border-color: #3b82f6;
            color: #3b82f6;
            font-weight: 600;
        }
        
        /* Code block styling */
        .stCodeBlock {
            border-radius: 8px;
        }
        
        /* Responsive design - Mobile First Approach */
        
        /* Tablet and larger - columns side by side */
        @media (min-width: 1025px) {
            /* Keep default column behavior for larger screens */
            .stColumns {
                display: flex !important;
                flex-direction: row !important;
            }
            
            .stColumn {
                flex: 1 !important;
                margin-right: 1rem !important;
            }
            
            .stColumn:last-child {
                margin-right: 0 !important;
            }
        }
        
        /* Medium screens (tablets, small laptops) - reduce padding */
        @media (max-width: 1024px) and (min-width: 769px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            /* Keep columns but with tighter spacing */
            .stColumns {
                display: flex !important;
                flex-direction: row !important;
            }
            
            .stColumn {
                flex: 1 !important;
                margin-right: 0.75rem !important;
            }
            
            .stColumn:last-child {
                margin-right: 0 !important;
            }
        }
        
        /* Mobile and small tablets - stack columns vertically */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }
            .main-title {
                font-size: 2.5rem;
            }
            
            /* Force column stacking on mobile */
            .stColumns {
                display: flex !important;
                flex-direction: column !important;
            }
            
            .stColumn {
                width: 100% !important;
                margin-right: 0 !important;
                margin-bottom: 1.5rem !important;
            }
            
            .stColumn:last-child {
                margin-bottom: 0 !important;
            }
            
            /* Responsive tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                flex-wrap: wrap;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 8px 16px;
                font-size: 14px;
                min-width: auto;
                flex: 1;
            }
            
            /* Better spacing for mobile */
            .stExpander {
                margin-bottom: 1rem !important;
            }
            
            .stButton {
                margin-bottom: 0.5rem !important;
            }
            
            .stSelectbox, .stTextInput, .stNumberInput {
                margin-bottom: 1rem !important;
            }
        }
        
        /* Very small mobile devices */
        @media (max-width: 480px) {
            .main-title {
                font-size: 2rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
            
            /* Even more compact spacing */
            .stColumn {
                margin-bottom: 1rem !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 6px 12px;
                font-size: 13px;
            }
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def run(self):
        """Run the main application."""
        self._render_header()
        self._render_learning_tips()

        # Create tabs
        tab1, tab2, tab3 = st.tabs(
            ["🔧 Methods", "📢 Notifications", "💥 Error Scenarios"]
        )

        with tab1:
            self._render_method_tab()
        with tab2:
            self._render_notification_tab()
        with tab3:
            self._render_error_scenarios_tab()

    def _render_header(self):
        """Render the application header."""
        # Main title with gradient
        st.markdown(
            '<div class="main-title">🧩 JSON-RPC Playground</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="subtitle">'
            "Interactive learning tool for JSON-RPC 2.0 protocol"
            "</div>",
            unsafe_allow_html=True,
        )

        # Simple developer credit below tagline
        st.markdown(
            '<div class="simple-credit">Developed by M Rehan ul Haq</div>',
            unsafe_allow_html=True,
        )

    def _render_learning_tips(self):
        """Render the learning tips section."""
        with st.expander("💡 **Quick Learning Tips**", expanded=False):
            st.markdown(
                """
            **🎯 Start Here:**
            1. Begin with the **Method** tab to understand basic request/response
            2. Try the **Notification** tab to see fire-and-forget messaging
            3. Test **Error Scenarios** to understand error handling

            **🔍 What to Notice:**
            - Request structure: `jsonrpc`, `method`, `params`, `id`
            - Response structure: `jsonrpc`, `result`/`error`, `id`
            - Notifications don't have `id` and get no response
            - Error codes follow JSON-RPC 2.0 specification

            **🧑‍🎓 Educational Focus:**
            - These are **learning methods** designed for understanding concepts
            - Simple examples that teach fundamental JSON-RPC principles
            - Each method demonstrates different parameter types and patterns
            - Foundation knowledge that scales to complex real-world systems

            **💼 Real-World Applications:**
            - Blockchain and cryptocurrency APIs (complex calculations)
            - Microservices communication (business logic)
            - IoT device control (sensor data and commands)
            - Financial systems (transactions and reporting)
            """
            )

    def _render_method_tab(self):
        """Render the method testing tab."""
        col1, col2 = st.columns([1, 1])

        with col1:
            self._render_method_instructions()

        with col2:
            method = st.selectbox(
                "Select method",
                ["Select a method", "add", "greet", "get_log"],
                key="method_tab",
            )

            self._render_method_info(method)

            params = self._get_method_params(method)

            if method != "Select a method":
                self._handle_method_request(method, params)

    def _render_method_instructions(self):
        """Render method instructions using native Streamlit components."""
        with st.expander("📚 Understanding JSON-RPC Methods", expanded=True):
            # Main introduction
            st.markdown("### 🎯 What are JSON-RPC Methods?")
            st.info(
                """
            JSON-RPC methods are **remote function calls** that let you execute 
            functions on a server from anywhere on the internet. 
            Think of it like calling a function, but the function lives on another computer!
            """
            )

            # Step-by-step guide
            st.markdown("### 📋 How Method Calls Work")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Every Request Needs:**")
                st.code(
                    '1. jsonrpc: "2.0" (version)\n'
                    "2. method: function name\n"
                    "3. id: unique identifier\n"
                    "4. params: your data (optional)"
                )

            with col2:
                st.markdown("**You'll Get Back:**")
                st.code(
                    'Success: { "result": data, "id": 1 }\nError: { "error": info, "id": 1 }'
                )

            # Interactive flow
            st.markdown("### 🔄 Request-Response Flow")

            flow_col1, flow_col2 = st.columns(2)

            with flow_col1:
                st.markdown("**1️⃣ You Send**")
                st.success("Request with method & params")

            with flow_col2:
                st.markdown("**2️⃣ Server Gets**")
                st.info("Processes your request")

            flow_col3, flow_col4 = st.columns(2)

            with flow_col3:
                st.markdown("**3️⃣ Server Executes**")
                st.warning("Runs the method")

            with flow_col4:
                st.markdown("**4️⃣ You Receive**")
                st.success("Result or error")

            # Learning tips
            st.markdown("### 💡 Learning Tips")
            st.success(
                """
            **Start Simple:** Try `add` or `greet` methods first - they're beginner-friendly!
            
            **Watch the IDs:** Notice how the ID in your request matches the ID in the response
            
            **Experiment:** Try different parameters and see what happens - that's how you learn!
            """
            )

            st.warning(
                """
            **Common Mistakes to Avoid:**
            - Entering text where numbers are expected
            - Forgetting required parameters
            - Not reading error messages carefully
            """
            )

    def _render_method_info(self, method: str):
        """Render information about the selected method using native Streamlit components."""
        if method == "add":
            st.subheader("📊 Add Method", divider="blue")

            col1, col2 = st.columns(2)
            with col1:
                st.info(
                    """
                **Purpose:** Educational example of numeric parameters
                
                **Parameters:**
                - `a` (number) - First number
                - `b` (number) - Second number
                
                **Example:** add(5, 3) → returns 8
                """
                )

            with col2:
                st.success(
                    """
                **Why this matters:**
                - Teaches parameter passing
                - Shows numeric data types
                - Demonstrates basic computation
                
                **Scales to real systems like:**
                - Financial calculations
                - Scientific computations
                - E-commerce pricing
                """
                )

        elif method == "greet":
            st.subheader("👋 Greet Method", divider="green")

            col1, col2 = st.columns(2)
            with col1:
                st.info(
                    """
                **Purpose:** Educational example of string parameters
                
                **Parameters:**
                - `name` (string) - Person's name
                
                **Example:** greet("Alice") → "Hello, Alice!"
                """
                )

            with col2:
                st.success(
                    """
                **Why this matters:**
                - Teaches string handling
                - Shows text processing
                - Demonstrates formatted responses
                
                **Scales to real systems like:**
                - User personalization
                - Message templates
                - Content generation
                """
                )

        elif method == "get_log":
            st.subheader("📋 Get Log Method", divider="orange")

            col1, col2 = st.columns(2)
            with col1:
                st.info(
                    """
                **Purpose:** Educational example of no-parameter methods
                
                **Parameters:** None required
                
                **Example:** get_log() → list of messages
                """
                )

            with col2:
                st.success(
                    """
                **Why this matters:**
                - Teaches parameterless calls
                - Shows data retrieval
                - Demonstrates server state
                
                **Scales to real systems like:**
                - Status monitoring
                - Data analytics
                - Health checks
                """
                )

            st.warning(
                "💡 **Tip:** Use this after sending notifications to see if they were received!"
            )

        elif method == "Select a method":
            st.subheader("👆 Getting Started", divider="rainbow")

            st.info(
                """
            Select a method from the dropdown above to see detailed information about how it works!
            """
            )

            st.markdown("**Available learning methods:**")

            col1, col2 = st.columns(2)

            with col1:
                st.success(
                    """
                **add** 🔢
                
                Learn: Number parameters
                
                Basic math concepts
                """
                )

            with col2:
                st.info(
                    """
                **greet** 👋
                
                Learn: String parameters
                
                Text processing basics
                """
                )

            # Third method gets its own row for better mobile experience
            st.warning(
                """
            **get_log** 📋
            
            Learn: No parameters
            
            Data retrieval concepts
            """
            )

    def _get_method_params(self, method: str) -> Dict[str, Any]:
        """Get parameters for the selected method with educational guidance."""
        params = {}

        if method == "add":
            st.markdown("### 🔢 **Enter Parameters for `add` Method**")

            st.info(
                """
            **🎓 Parameter Learning:**
            • Both parameters are **required** - the method won't work without them
            • JSON-RPC supports numbers (integers and decimals)
            • The server will add these two numbers and return the sum
            • Try different combinations to see how it works!
            """
            )

            col1, col2 = st.columns(2)
            with col1:
                first_number = st.number_input(
                    "First Number (parameter 'a')",
                    value=1,
                    key="a_method",
                    help="This becomes the 'a' parameter in your JSON request",
                )
            with col2:
                second_number = st.number_input(
                    "Second Number (parameter 'b')",
                    value=2,
                    key="b_method",
                    help="This becomes the 'b' parameter in your JSON request",
                )

            params = {"a": first_number, "b": second_number}

            # Show what the JSON will look like
            st.markdown("**📋 This will create the following parameters:**")
            st.code(json.dumps(params, indent=2), language="json")
            st.success(
                f"**🧮 Expected result:** `{first_number} + {second_number} = {first_number + second_number}`"
            )

        elif method == "greet":
            st.markdown("### 👋 **Enter Parameters for `greet` Method**")

            st.warning(
                """
            **🎓 Parameter Learning:**
            • This method takes one **string parameter** called 'name'
            • Strings in JSON are enclosed in quotes: "like this"
            • The server will format this into a greeting message
            • Try names, empty strings, or special characters!
            """
            )

            name = st.text_input(
                "Name (parameter 'name')",
                value="Rehan",
                key="name_method",
                help="Enter any name or text - this becomes the 'name' parameter",
                placeholder="Enter a name to greet...",
            )

            params = {"name": name}

            # Show what the JSON will look like
            st.markdown("**📋 This will create the following parameters:**")
            st.code(json.dumps(params, indent=2), language="json")
            st.success(f"**💬 Expected result:** `Hello, {name}!`")

        elif method == "get_log":
            st.markdown("### 📋 **Parameters for `get_log` Method**")

            st.info(
                """
            **🎓 Parameter Learning:**
            • This method takes **NO parameters** - it's parameter-free!
            • The JSON will either have empty params `{}` or no params field
            • Server methods can work without any input data
            • Perfect example of a "getter" method that just retrieves information
            """
            )

            st.markdown("**📋 This will create the following parameters:**")
            st.code("{}", language="json")
            st.markdown(
                "**📖 Expected result:** All messages that have been logged on the server"
            )
            st.warning(
                "**💡 Tip:** Send some notifications first, then use this method to see them!"
            )

        return params

    def _handle_method_request(self, method: str, params: Dict[str, Any]):
        """Handle method request processing."""
        # Clear previous results when method changes
        if (
            "last_method" not in st.session_state
            or st.session_state["last_method"] != method
        ):
            st.session_state.pop("last_response_method", None)
            st.session_state.pop("last_type_method", None)
            st.session_state["last_method"] = method

        # Create request payload
        payload_key = f"method_{method}_request_{json.dumps(params, sort_keys=True)}"
        if (
            "last_payload_key" not in st.session_state
            or st.session_state["last_payload_key"] != payload_key
        ):
            request_payload = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": str(uuid.uuid4()),
            }
            st.session_state["request_payload"] = request_payload
            st.session_state["last_payload_key"] = payload_key
        else:
            request_payload = st.session_state["request_payload"]

        # Render buttons with educational context
        st.markdown("### 🚀 **Ready to Send Your Method Call?**")
        st.success(
            """
        **🎓 Next Steps:**
        1. **View Raw Request** - See the exact JSON being sent
        2. **Send** - Execute the method on the server
        3. **Analyze Response** - Learn from what comes back
        """
        )

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            view_req_clicked = st.button(
                "🔍 View Raw Request",
                key="view_req_method",
                use_container_width=True,
                type="secondary",
                help="See the exact JSON that will be sent to the server",
            )
        with btn_col2:
            send_clicked = st.button(
                "🚀 Send Method Call",
                key="send_method",
                use_container_width=True,
                type="primary",
                help="Execute the method on the server and get a response",
            )

        # Handle button clicks with educational explanations
        if view_req_clicked:
            st.markdown("### 📄 **Raw JSON Request - What Gets Sent**")
            st.markdown(
                """
                **🎓 Understanding the Request:**
                - This is the exact JSON that will be sent to the server
                - Notice the structure: `jsonrpc`, `method`, `params`, `id`
                - The `id` is automatically generated to track this request
                - Real applications use this same format!
                """
            )
            st.code(json.dumps(request_payload, indent=2), language="json")

            # Add field-by-field explanation
            st.markdown("**🔍 Field-by-Field Breakdown:**")
            st.markdown(
                f"- **`jsonrpc`**: `\"{request_payload['jsonrpc']}\"` (Protocol version)"
            )
            st.markdown(
                f"- **`method`**: `\"{request_payload['method']}\"` (Function to call)"
            )
            st.markdown(
                f"- **`params`**: `{json.dumps(request_payload['params'])}` (Function arguments)"
            )
            st.markdown(
                f"- **`id`**: `\"{request_payload['id']}\"` (Unique request identifier)"
            )

        if send_clicked:
            st.markdown("### 📡 **Sending Request to Server...**")
            with st.spinner("🔄 Executing method call..."):
                self._send_request(request_payload, "method")

        # Display response
        if (
            st.session_state.get("last_type_method") == "request"
            and "last_response_method" in st.session_state
        ):
            self._display_method_response(
                method, st.session_state["last_response_method"]
            )

    def _render_notification_tab(self):
        """Render the notification testing tab."""
        col1, col2 = st.columns([1, 1])

        with col1:
            self._render_notification_instructions()

        with col2:
            self._render_log_management()
            self._render_notification_sender()

    def _render_notification_instructions(self):
        """Render comprehensive notification learning instructions using Streamlit components."""
        with st.expander("📡 Understanding JSON-RPC Notifications", expanded=True):
            # Introduction
            st.markdown("### 🔥 What are Notifications?")
            st.info(
                """
            Notifications are **"fire-and-forget"** messages sent to the server without expecting a response.
            Think of them like sending a postcard - you send it but don't wait for a reply!
            """
            )

            # Key differences
            st.markdown("### 🔍 How They Differ from Methods")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🔔 Notifications:**")
                st.code(
                    "✅ No 'id' field\n✅ No response expected\n✅ Perfect for logging\n✅ Fire-and-forget"
                )

            with col2:
                st.markdown("**📞 Method Calls:**")
                st.code(
                    "✅ Has 'id' field\n✅ Response required\n✅ Perfect for calculations\n✅ Request-response pattern"
                )

            # Step-by-step guide
            st.markdown("### 📋 How to Send Notifications")

            step_col1, step_col2 = st.columns(2)

            with step_col1:
                st.success(
                    """
                **1️⃣ Clear Log**
                
                Optional step
                
                See only new messages
                """
                )

            with step_col2:
                st.info(
                    """
                **2️⃣ Enter Message**
                
                Type your content
                
                Any text works
                """
                )

            step_col3, step_col4 = st.columns(2)

            with step_col3:
                st.warning(
                    """
                **3️⃣ Send**
                
                Fire and forget
                
                No response expected
                """
                )

            with step_col4:
                st.success(
                    """
                **4️⃣ Verify**
                
                Use `get_log` method
                
                Check if received
                """
                )

            # Educational insights
            st.markdown("### 🎓 Learning Insights")
            st.warning(
                """
            **Why Notifications Matter:**
            - Reduce server load (no response needed)
            - Perfect for logging and events
            - Enable asynchronous communication
            - Common in real-time systems
            """
            )

            st.success(
                """
            **💡 Pro Tips:**
            - Notifications are faster than method calls
            - Use for non-critical updates
            - Great for audit trails
            - Server can't report errors back to you
            """
            )

    def _render_log_management(self):
        """Render log management section with educational content."""
        st.markdown("### 🗂️ Log Management")

        # Educational info about log management
        st.info(
            """
        **🎓 Why clear the log?**
        - Helps you see only new messages
        - Makes testing easier
        - Shows the immediate effect of your notification
        - Simulates starting with a clean slate
        """
        )

        with st.container():
            confirm_clear = st.checkbox(
                "✨ Clear log before sending notification",
                key="confirm_clear_log",
                help="This will remove all existing messages from the server log",
            )

            if confirm_clear:
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(
                        "🗑️ Clear Server Log",
                        key="clear_log_btn_notif",
                        use_container_width=True,
                        type="secondary",
                    ):
                        self._clear_log()

                with col2:
                    st.markdown("**📝 This will:**")
                    st.markdown("- Remove all stored messages")
                    st.markdown("- Reset the server log to empty")
                    st.markdown("- Help you see new messages clearly")

    def _render_notification_sender(self):
        """Render notification sender section with enhanced educational content."""
        st.markdown("### 💬 Send Notification")

        # Educational info about the log_message method
        st.info(
            """
        **🎓 About the `log_message` Notification:**
        - This is an educational example of a notification
        - Takes one parameter: `message` (string)
        - Stores your message on the server
        - No response is sent back to you
        """
        )

        message = st.text_input(
            "Enter your message to log:",
            value="",
            key="log_message_tab",
            placeholder="Type a message and press Enter...",
            help="Type your message and press Enter to enable the buttons below",
        )
        
        # Show clear instructions
        if not message.strip():
            st.info("� Type a message above and press **Enter** to enable the buttons below")

        # Always show the UI structure, but disable/enable based on message
        has_message = bool(message.strip())
        
        # Create request payload regardless (for consistency)
        params = {"message": message} if has_message else {"message": ""}
        request_payload = {
            "jsonrpc": "2.0",
            "method": "log_message",
            "params": params,
        }
        
        if has_message:
            # Show parameter structure
            st.markdown("**📋 This will create the following notification:**")
            st.code(json.dumps(params, indent=2), language="json")

            # Notice the difference
            st.warning("**👀 Notice:** No `id` field in notifications!")

            # Action buttons
            st.success("**🚀 Ready to send your notification?**")

        # Always show buttons, but disable them when no message
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            view_req_log_clicked = st.button(
                "🔍 View Raw Request",
                key="view_req_log",
                use_container_width=True,
                type="secondary",
                disabled=not has_message,
                help="See the exact JSON that will be sent (notice: no 'id' field!)",
            )
        with btn_col2:
            send_log_clicked = st.button(
                "📡 Send Notification",
                key="send_log",
                use_container_width=True,
                type="primary",
                disabled=not has_message,
                help="Fire and forget - send message without expecting response",
            )

        # Handle button clicks only if message exists
        if has_message:
            if view_req_log_clicked:
                st.code(json.dumps(request_payload, indent=2), language="json")

            if send_log_clicked:
                self._send_notification(request_payload)

    def _render_error_scenarios_tab(self):
        """Render the error scenarios tab."""
        col1, col2 = st.columns([1, 1])

        with col1:
            self._render_error_instructions()

        with col2:
            self._render_error_scenarios()

    def _render_error_instructions(self):
        """Render comprehensive error scenario learning instructions using Streamlit components."""
        with st.expander("⚠️ Understanding JSON-RPC Error Codes", expanded=True):
            # Introduction
            st.markdown("### 💥 What are JSON-RPC Errors?")
            st.info(
                """
            JSON-RPC errors are **standardized responses** that tell you exactly what went wrong with your request.
            Think of them as helpful error messages that follow a specific format!
            """
            )

            # Error code overview
            st.markdown("### 📋 Standard Error Codes")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🔧 Protocol Errors:**")
                st.code(
                    "-32700: Parse Error (malformed JSON)\n"
                    "-32600: Invalid Request (missing fields)\n"
                    "-32601: Method Not Found"
                )

            with col2:
                st.markdown("**⚠️ Execution Errors:**")
                st.code(
                    "-32602: Invalid Params (wrong types)\n"
                    "-32000: Server Error (application exceptions)\n"
                    "-32000 to -32099: Implementation-defined errors"
                )

            # Educational value
            st.markdown("### 🎓 Why Learn About Errors?")

            error_col1, error_col2 = st.columns(2)

            with error_col1:
                st.success(
                    """
                **🔍 Debug Skills**
                
                Learn to identify problems
                
                Understand error messages
                """
                )

            with error_col2:
                st.warning(
                    """
                **🛠️ Better Code**
                
                Write robust applications
                
                Handle errors gracefully
                """
                )

            # Third benefit gets its own row for better mobile experience
            st.info(
                """
            **📚 Protocol Knowledge**
            
            Understand JSON-RPC spec
            
            Professional development
            """
            )

            # Learning insights
            st.markdown("### 💡 What You'll Learn")
            st.success(
                """
            **Real Error Responses:** See actual JSON-RPC library error responses
            
            **Error Patterns:** Understand what triggers each error type
            
            **Debugging Skills:** Learn to read and interpret error messages
            
            **Best Practices:** Know how to handle errors in your applications
            """
            )

            st.warning(
                """
            **💡 Pro Tip:** These are the **actual errors** you'll encounter in real JSON-RPC applications. 
            Understanding them now will save you debugging time later!
            """
            )

    def _render_error_scenarios(self):
        """Render error scenario selection and testing with enhanced educational content."""
        st.markdown("### 🎯 Select an Error Scenario to Test")

        st.info(
            """
        **🎓 Learning Approach:**
        Each scenario demonstrates a different type of error. Try them all to understand 
        how JSON-RPC handles various problem situations!
        """
        )

        error_scenario = st.selectbox(
            "Choose an error type to trigger:",
            [
                "Select a scenario",
                "🔧 Parse Error (-32700)",
                "📋 Invalid Request (-32600)",
                "❓ Method Not Found (-32601)",
                "⚠️ Invalid Params (-32602)",
                "💥 Server Error (-32000)",
            ],
            key="error_scenario_tab",
            help="Each scenario shows you a different type of JSON-RPC error",
        )

        # Show scenario description
        if error_scenario != "Select a scenario":
            self._show_scenario_description(error_scenario)
            self._handle_error_scenario(error_scenario)

    def _show_scenario_description(self, scenario: str):
        """Show educational description for each error scenario."""
        if scenario == "🔧 Parse Error (-32700)":
            st.warning(
                """
            **🔧 Parse Error (-32700)**
            - **What it is:** JSON syntax is broken
            - **When it happens:** Malformed JSON (missing brackets, commas, etc.)
            - **Real-world cause:** Network corruption, truncated data, coding mistakes
            """
            )
        elif scenario == "📋 Invalid Request (-32600)":
            st.warning(
                """
            **📋 Invalid Request (-32600)**
            - **What it is:** Missing required JSON-RPC fields
            - **When it happens:** No 'jsonrpc' field, wrong format
            - **Real-world cause:** Incorrect client implementation, version mismatch
            """
            )
        elif scenario == "❓ Method Not Found (-32601)":
            st.warning(
                """
            **❓ Method Not Found (-32601)**
            - **What it is:** Calling a method that doesn't exist
            - **When it happens:** Typos in method names, outdated API calls
            - **Real-world cause:** API changes, documentation errors, client bugs
            """
            )
        elif scenario == "⚠️ Invalid Params (-32602)":
            st.warning(
                """
            **⚠️ Invalid Params (-32602)**
            - **What it is:** Wrong parameter types or values
            - **When it happens:** String instead of number, missing required params
            - **Real-world cause:** Input validation failures, type mismatches
            """
            )
        elif scenario == "💥 Server Error (-32000)":
            st.warning(
                """
            **💥 Server Error (-32000)**
            - **What it is:** Application-level exception in your method code
            - **When it happens:** Unhandled exceptions in server methods (RuntimeError, ValueError, etc.)
            - **Real-world cause:** Business logic errors, resource failures, database issues
            """
            )

    def _handle_error_scenario(self, scenario: str):
        """Handle specific error scenario testing with educational flow."""
        # Clear previous results when scenario changes
        if (
            "last_error_scenario" not in st.session_state
            or st.session_state["last_error_scenario"] != scenario
        ):
            if "last_response_error" in st.session_state:
                del st.session_state["last_response_error"]
            st.session_state["last_error_scenario"] = scenario

        st.markdown("---")

        if scenario == "🔧 Parse Error (-32700)":
            self._handle_parse_error()
        elif scenario == "📋 Invalid Request (-32600)":
            self._handle_invalid_request()
        elif scenario == "❓ Method Not Found (-32601)":
            self._handle_method_not_found()
        elif scenario == "⚠️ Invalid Params (-32602)":
            self._handle_invalid_params()
        elif scenario == "💥 Server Error (-32000)":
            self._handle_internal_error()

        # Display error response if available
        if "last_response_error" in st.session_state:
            st.markdown("---")
            self._display_error_response(st.session_state["last_response_error"])

    def _handle_parse_error(self):
        """Handle parse error scenario with enhanced educational content."""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📤 What We're Sending")
            st.info("🔧 **Malformed JSON** - Missing closing brace")
            # Create the malformed JSON string manually for display (missing closing brace)
            malformed_display = '''{
  "jsonrpc": "2.0",
  "method": "add",
  "params": {
    "a": 1,
    "b": 2
  },
  "id": 1'''
            st.code(malformed_display, language="json")
            st.warning("⚠️ Notice the missing `}` at the end - this breaks JSON syntax!")

        with col2:
            st.markdown("#### 🎓 Learning Point")
            st.success(
                """
            **Why This Happens:**
            - Network interruption during transmission
            - Programming errors in JSON construction
            - Copy-paste mistakes in configuration files
            
            **How to Fix:**
            - Validate JSON before sending
            - Use proper JSON libraries
            - Check network integrity
            """
            )

        st.markdown("#### 🚀 Test the Scenario")
        if st.button(
            "Send Malformed JSON",
            key="send_parse_error",
            use_container_width=True,
            type="primary",
        ):
            # Create the same malformed JSON for the actual request (missing closing brace)
            malformed_json = '''{
  "jsonrpc": "2.0",
  "method": "add",
  "params": {
    "a": 1,
    "b": 2
  },
  "id": 1'''
            try:
                resp = requests.post(
                    self.server_url,
                    data=malformed_json,
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )
                try:
                    response = resp.json()
                except ValueError:
                    response = {"error": "Failed to parse server response"}
                st.session_state["last_response_error"] = response
                st.success("✅ Parse error triggered (as expected)")
            except requests.RequestException as e:
                st.session_state["last_response_error"] = {
                    "error": f"Network error: {str(e)}"
                }

    def _handle_invalid_request(self):
        """Handle invalid request scenario with enhanced educational content."""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📤 What We're Sending")
            st.info("📋 **Missing Required Field** - No 'method' field")
            invalid_request = {
                "jsonrpc": "2.0",
                "params": {"a": 1, "b": 2},
                "id": 1,
            }
            st.code(json.dumps(invalid_request, indent=2), language="json")
            st.warning("⚠️ Missing the required `method` field!")

        with col2:
            st.markdown("#### 🎓 Learning Point")
            st.success(
                """
            **JSON-RPC 2.0 Requirements:**
            - Must include `"jsonrpc": "2.0"`
            - Must have a `method` field
            - Should have an `id` for requests
            
            **Common Mistakes:**
            - Missing the method field
            - Empty method name
            - Invalid request structure
            """
            )

        st.markdown("#### 🚀 Test the Scenario")
        if st.button(
            "Send Invalid Request",
            key="send_invalid_request",
            use_container_width=True,
            type="primary",
        ):
            try:
                resp = requests.post(self.server_url, json=invalid_request, timeout=10)
                response = resp.json()
                st.session_state["last_response_error"] = response
                st.success("✅ Invalid request error triggered (as expected)")
            except (requests.RequestException, ValueError) as e:
                st.session_state["last_response_error"] = {
                    "error": f"Network error: {str(e)}"
                }

    def _handle_method_not_found(self):
        """Handle method not found scenario with enhanced educational content."""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📤 What We're Sending")
            st.info("❓ **Non-existent Method** - Calling undefined method")
            method_not_found_request = {
                "jsonrpc": "2.0",
                "method": "this_method_does_not_exist",
                "params": {},
                "id": 1,
            }
            st.code(json.dumps(method_not_found_request, indent=2), language="json")
            st.warning("⚠️ Method `this_method_does_not_exist` is not registered!")

        with col2:
            st.markdown("#### 🎓 Learning Point")
            st.success(
                """
            **Why This Happens:**
            - Typos in method names
            - Outdated client code after API changes
            - Missing method registration on server
            
            **How to Fix:**
            - Check available methods documentation
            - Verify method spelling and case
            - Ensure server has the method implemented
            """
            )

        st.markdown("#### 🚀 Test the Scenario")
        if st.button(
            "Call Non-existent Method",
            key="send_method_not_found",
            use_container_width=True,
            type="primary",
        ):
            try:
                resp = requests.post(
                    self.server_url, json=method_not_found_request, timeout=10
                )
                response = resp.json()
                st.session_state["last_response_error"] = response
                st.success("✅ Method not found error triggered (as expected)")
            except (requests.RequestException, ValueError) as e:
                st.session_state["last_response_error"] = {
                    "error": f"Network error: {str(e)}"
                }

    def _handle_invalid_params(self):
        """Handle invalid params scenario with enhanced educational content."""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📤 What We're Sending")
            st.info("⚠️ **Missing Required Parameter** - Only sending 'a', but 'add' needs both 'a' and 'b'")
            invalid_params_request = {
                "jsonrpc": "2.0",
                "method": "add",
                "params": {"a": 5},  # Missing required parameter 'b'
                "id": 1,
            }
            st.code(json.dumps(invalid_params_request, indent=2), language="json")
            st.warning("⚠️ `add` method requires both 'a' and 'b' parameters!")

        with col2:
            st.markdown("#### 🎓 Learning Point")
            st.success(
                """
            **Parameter Validation Errors:**
            - Missing required parameters
            - Wrong number of parameters  
            - Extra unexpected parameters (method-dependent)
            
            **Best Practices:**
            - Check method signatures before calling
            - Provide all required parameters
            - Use schema validation in production
            """
            )

        st.markdown("#### 🚀 Test the Scenario")
        if st.button(
            "Send Missing Parameter",
            key="send_invalid_params",
            use_container_width=True,
            type="primary",
        ):
            try:
                resp = requests.post(
                    self.server_url, json=invalid_params_request, timeout=10
                )
                response = resp.json()
                st.session_state["last_response_error"] = response
                st.success("✅ Invalid params error triggered (as expected)")
            except (requests.RequestException, ValueError) as e:
                st.session_state["last_response_error"] = {
                    "error": f"Network error: {str(e)}"
                }

    def _handle_internal_error(self):
        """Handle server error (-32000) scenario with enhanced educational content."""
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📤 What We're Sending")
            st.info("💥 **Trigger Server Exception** - Deliberate application error")
            internal_error_request = {
                "jsonrpc": "2.0",
                "method": "cause_internal_error",
                "params": {"trigger": "error"},
                "id": 1,
            }
            st.code(json.dumps(internal_error_request, indent=2), language="json")
            st.warning("⚠️ This will cause a deliberate RuntimeError in the server method!")

        with col2:
            st.markdown("#### 🎓 Learning Point")
            st.success(
                """
            **Server Error (-32000):**
            - Application-level exceptions (RuntimeError, ValueError, etc.)
            - Business logic failures  
            - Database connection issues
            - Resource exhaustion (memory, disk)
            
            **JSON-RPC Library Behavior:**
            - Maps all unhandled exceptions to -32000
            - This is the CORRECT behavior per JSON-RPC 2.0 spec
            - Includes detailed error information in 'data' field
            
            **Error Handling:**
            - Always use try-catch in server methods
            - Log errors for debugging
            - Return meaningful error messages
            """
            )

        st.markdown("#### 🚀 Test the Scenario")
        if st.button(
            "Trigger Server Error",
            key="send_internal_error",
            use_container_width=True,
            type="primary",
        ):
            try:
                resp = requests.post(
                    self.server_url, json=internal_error_request, timeout=10
                )
                response = resp.json()
                st.session_state["last_response_error"] = response
                st.success("✅ Server error triggered (as expected)")
            except (requests.RequestException, ValueError) as e:
                st.session_state["last_response_error"] = {
                    "error": f"Network error: {str(e)}"
                }

    def _send_request(self, payload: Dict[str, Any], request_type: str):
        """Send a JSON-RPC request."""
        try:
            resp = requests.post(self.server_url, json=payload, timeout=10)
            try:
                response = resp.json()
            except ValueError:
                response = resp.text
            st.session_state[f"last_response_{request_type}"] = response
            st.session_state[f"last_type_{request_type}"] = "request"
            st.success("Request sent. See the result below.")
        except requests.RequestException as e:
            st.error(f"Error: {e}")

    def _send_notification(self, payload: Dict[str, Any]):
        """Send a JSON-RPC notification with educational feedback."""
        try:
            requests.post(self.server_url, json=payload, timeout=10)

            # Success notification with educational content
            st.success("🎯 **Notification Sent Successfully!**")

            # Educational explanation
            st.info(
                """
            **🎓 What just happened:**
            - Your notification was sent to the server
            - No response was received (this is normal!)
            - The server processed your message silently
            - Your message is now stored in the server log
            """
            )

            # Next steps guidance
            st.warning(
                """
            **� How to verify it worked:**
            1. Go to the **Method** tab
            2. Select `get_log` method
            3. Click "Send Method Call"
            4. Look for your message in the response
            """
            )

            # Show what was sent
            with st.expander("🔍 See what was sent to the server"):
                st.code(json.dumps(payload, indent=2), language="json")
                st.markdown(
                    "**👀 Notice:** No `id` field - that's what makes it a notification!"
                )

        except requests.RequestException as e:
            st.error(f"❌ **Connection Error:** {e}")
            st.warning(
                "Make sure the JSON-RPC server is running on http://localhost:8000"
            )

    def _clear_log(self):
        """Clear the server log with educational feedback."""
        clear_payload = {
            "jsonrpc": "2.0",
            "method": "clear_log",
            "params": {},
            "id": str(uuid.uuid4()),
        }
        try:
            resp = requests.post(self.server_url, json=clear_payload, timeout=10)
            result = resp.json()

            if "result" in result:
                st.success("🧹 **Log Cleared Successfully!**")
                st.info(
                    """
                **🎓 What happened:**
                - Sent a method call (not notification) to clear the log
                - Server confirmed the log was cleared
                - Now you can send fresh notifications and see them clearly
                """
                )

                with st.expander("🔍 Technical details"):
                    st.markdown("**Request sent:**")
                    st.code(json.dumps(clear_payload, indent=2), language="json")
                    st.markdown("**Response received:**")
                    st.code(json.dumps(result, indent=2), language="json")
                    st.markdown(
                        "**👀 Notice:** This was a method call (has `id`) not a notification!"
                    )
            else:
                st.error("Unexpected response format")

        except (requests.RequestException, ValueError) as e:
            st.error(f"❌ **Error clearing log:** {e}")
            st.warning(
                "Make sure the JSON-RPC server is running on http://localhost:8000"
            )

    def _display_method_response(self, method: str, response: Any):
        """Display method response with educational explanations."""
        st.markdown("### 📬 **Response Analysis - Understanding What Happened**")

        # Success response
        if isinstance(response, dict) and "result" in response:
            st.success("✅ **Success!** Your method call worked perfectly")

            # Special handling for get_log method
            if method == "get_log":
                log_content = response["result"]
                log_lines = [line for line in log_content.strip().split("\n") if line]
                
                if log_lines:
                    # Show clean result like other methods
                    st.success(f"**📊 Result:** {len(log_lines)} message(s) retrieved")
                    
                    # Show the log entries (newest first)
                    for i, entry in enumerate(reversed(log_lines), 1):
                        st.markdown(f"{i}. {entry}")
                else:
                    st.success("**📊 Result:** No messages in log")
                    st.info("Log is empty - send some notifications first!")
            else:
                # For add and greet methods
                st.markdown("**🎯 Result Explanation:**")
                if method == "add":
                    st.markdown(f"**The server calculated:** `{response['result']}`")
                    st.markdown(
                        "**💡 Notice:** The server performed the math and returned just the number"
                    )
                elif method == "greet":
                    st.markdown(f"**The server responded:** `{response['result']}`")
                    st.markdown(
                        "**💡 Notice:** The server formatted your input into a greeting message"
                    )

                # Display the actual result prominently
                st.success(f"**📊 Result:** {response['result']}")

            # Explain the response structure
            st.markdown("**🔍 Response Structure Analysis:**")
            st.markdown(
                """
                - ✅ **`jsonrpc: "2.0"`** - Confirms protocol version
                - ✅ **`result`** - Contains the method's return value
                - ✅ **`id`** - Matches your request ID for tracking
                - ❌ **No `error` field** - Indicates successful execution
                """
            )

        # Error response
        elif isinstance(response, dict) and "error" in response:
            st.error("⚠️ **Something went wrong - Let's learn from it!**")

            error = response["error"]
            st.markdown("**🎓 Error Analysis:**")
            st.markdown(
                f"- **Error Code:** `{error.get('code', 'N/A')}` (Standard JSON-RPC error code)"
            )
            st.markdown(
                f"- **Error Message:** `{error.get('message', 'N/A')}` (Human-readable description)"
            )

            if "data" in error:
                st.markdown(
                    f"- **Additional Info:** `{error['data']}` (Extra details about the error)"
                )

            st.markdown("**💡 What this teaches us:**")
            st.markdown("- Servers can detect and report problems")
            st.markdown("- Error codes help programs handle different error types")
            st.markdown("- The same request structure is used even for errors")

        # Raw response section with explanation
        if st.button("🔍 View Raw JSON Response", key="raw_method"):
            st.markdown("### 📄 **Raw JSON Response - The Actual Data**")
            st.markdown(
                """
                **🎓 Why look at raw JSON?**
                - See exactly what the server sent back
                - Understand the JSON-RPC protocol structure
                - Learn how to parse responses in your own code
                - Compare successful vs error response formats
                """
            )
            st.code(json.dumps(response, indent=2), language="json")

            # Add annotations for the JSON structure
            st.markdown("**🔍 JSON Field Explanations:**")
            if "result" in response:
                st.markdown("- `jsonrpc`: Protocol version (always '2.0')")
                st.markdown("- `result`: The actual data returned by your method")
                st.markdown("- `id`: Links this response to your original request")
            elif "error" in response:
                st.markdown("- `jsonrpc`: Protocol version (always '2.0')")
                st.markdown("- `error`: Object containing error details")
                st.markdown("- `error.code`: Numeric error code (see JSON-RPC spec)")
                st.markdown("- `error.message`: Human-readable error description")
                st.markdown("- `id`: Links this response to your original request")

    def _display_error_response(self, response: Dict[str, Any]):
        """Display error response with enhanced educational content."""
        st.markdown("### 📋 Error Response Analysis")

        if isinstance(response, dict) and "error" in response:
            error = response["error"]
            if isinstance(error, dict):
                error_code = error.get("code", "N/A")
            else:
                # Handle string errors
                st.error(f"Error: {error}")
                return

            # Error code mapping with educational context
            error_info = {
                -32700: {"name": "Parse Error", "icon": "🔧", "color": "error"},
                -32600: {"name": "Invalid Request", "icon": "📋", "color": "error"},
                -32601: {"name": "Method Not Found", "icon": "❓", "color": "warning"},
                -32602: {"name": "Invalid Params", "icon": "⚠️", "color": "warning"},
                -32603: {"name": "Internal Error", "icon": "💥", "color": "error"},
                -32000: {"name": "Server Error", "icon": "💥", "color": "error"},
            }

            error_details = error_info.get(
                error_code, {"name": "Unknown Error", "icon": "❌", "color": "error"}
            )

            # Display error summary with appropriate text sizing
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("**Error Code**")
                st.markdown(f"**{error_code}**")
                st.caption("Standard JSON-RPC error code")

            with col2:
                st.markdown("**Error Type**")
                st.markdown(f"**{error_details['icon']} {error_details['name']}**")
                st.caption("Human-readable error category")

            with col3:
                st.markdown("**Additional Details**")
                if "data" in error:
                    st.markdown("**✅ Yes**")
                    st.caption("Extra error information provided")
                else:
                    st.markdown("**❌ No**")
                    st.caption("No additional error information")

            # Error message
            st.error(
                f"**{error_details['icon']} {error_details['name']}:** {error.get('message', 'No message provided')}"
            )

            # Additional error data if present
            if "data" in error:
                st.warning(f"**Additional Details:** {error['data']}")

            # Educational explanation
            st.info(
                f"""
            **🎓 Understanding this error:**
            - **Code {error_code}** is a standard JSON-RPC 2.0 error
            - **{error_details['name']}** indicates {self._get_error_explanation(error_code)}
            - This helps developers identify and fix the issue
            """
            )
        else:
            st.warning("⚠️ Unexpected response format - not a standard JSON-RPC error")

        # Raw response section
        st.markdown("#### 📄 Raw JSON Response")
        st.code(json.dumps(response, indent=2), language="json")

        # Pro tip
        st.success(
            """
        **💡 Pro Tip:** In production applications, always check the error code to handle 
        different error types appropriately!
        """
        )

    def _get_error_explanation(self, error_code: int) -> str:
        """Get educational explanation for error codes."""
        explanations = {
            -32700: "the JSON syntax is malformed",
            -32600: "required JSON-RPC fields are missing",
            -32601: "the requested method doesn't exist",
            -32602: "the method parameters are invalid",
            -32603: "an internal JSON-RPC infrastructure error occurred",
            -32000: "an application-level exception was thrown in the server method",
        }
        return explanations.get(error_code, "an unknown error condition")


def main():
    """Main entry point for the Streamlit app."""
    # For deployment, use localhost:4000 (server and client run on same host)
    # In production, both server and client run on the same container/service
    server_url = "http://localhost:4000"
    app = JSONRPCPlaygroundApp(server_url)
    app.run()


if __name__ == "__main__":
    main()
