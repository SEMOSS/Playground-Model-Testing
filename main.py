import streamlit as st
from src.runners.runners import (
    run_selected_tests,
    TestSelections,
    get_available_models,
    available_tests,
)
from src.utils.models import Model
import json

st.set_page_config(
    page_title="AI Model Testing Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    h1 {
        color: #2c3e50;
        padding-bottom: 1rem;
    }
    h2 {
        color: #34495e;
        padding-top: 1rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 AI Model Testing Framework")
st.markdown(
    "**Test multiple AI models across different providers through the SEMOSS API**"
)
st.divider()

with st.sidebar:
    st.header("⚙️ Configuration")

    # Model selection
    st.subheader("Select Models")
    available_models = get_available_models()

    model_selections = {}
    for model in available_models:
        model_selections[model.name] = st.checkbox(
            f"{model.name} ({model.type})", value=True, key=f"model_{model.id}"
        )

    selected_models = [
        model for model in available_models if model_selections[model.name]
    ]

    st.divider()

    # Test selection
    st.subheader("Select Tests")
    test_selections = {}

    test_selections["standard_text_test"] = st.checkbox(
        "Standard Text Test",
        value=True,
        help="Basic text prompt test (e.g., 'What is the capital of France?')",
    )

    test_selections["prompt_with_image_urls"] = st.checkbox(
        "Prompt with Image URLs",
        value=True,
        help="Test image understanding capabilities",
    )

    test_selections["basic_param_values"] = st.checkbox(
        "Basic Param Values Test",
        value=True,
        help="Run test with basic parameter values (e.g., temperature, max_tokens)",
    )

    test_selections["structured_json_test"] = st.checkbox(
        "Structured JSON Test",
        value=True,
        help="Run test with structured json output format",
    )

    st.divider()

    # Confirmation model selection
    st.subheader("Confirmation Model")
    confirmer_model = st.text_input(
        "OpenAI Confirmation Model:",
        value="gpt-4.1-nano",
        help="Model used to validate test responses",
    )

    st.divider()

    run_button = st.button("🚀 Run Tests", use_container_width=True)

# Main content area
if not selected_models:
    st.warning("⚠️ Please select at least one model from the sidebar to begin testing.")
elif not any(test_selections.values()):
    st.warning("⚠️ Please select at least one test to run from the sidebar.")
else:
    if run_button:
        # Create TestSelections object
        selections = TestSelections(**test_selections)

        # Progress tracking
        st.info(f"🔄 Running tests on {len(selected_models)} model(s)...")
        progress_bar = st.progress(0)

        # Run tests
        try:
            results = run_selected_tests(selected_models, selections, confirmer_model)
            progress_bar.progress(100)

            st.success(f"✅ Tests completed successfully for {len(results)} model(s)!")
            st.divider()

            # Display results for each model
            st.header("📊 Test Results")

            for idx, (model_name, test_results) in enumerate(results.items()):
                with st.expander(f"**{model_name}**", expanded=True):
                    # Standard Text Test Results
                    if test_results.standard_text_test:
                        st.subheader("📝 Standard Text Test")
                        result = test_results.standard_text_test

                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**Model:** {result.model_name}")
                        with col2:
                            st.markdown(f"**Client:** {result.client}")
                        with col3:
                            if result.success:
                                st.markdown("**Status:** ✅ Success")
                            else:
                                st.markdown("**Status:** ❌ Failed")

                        st.markdown("**Response:**")
                        st.text_area(
                            "Model Response",
                            value=result.response,
                            height=100,
                            key=f"std_text_{idx}",
                            label_visibility="collapsed",
                        )

                        if result.confirmation_response:
                            st.markdown("**Confirmation:**")
                            st.info(result.confirmation_response)

                        st.divider()

                    # Image URL Test Results
                    if test_results.prompt_with_image_urls:
                        st.subheader("🖼️ Prompt with Image URLs")
                        result = test_results.prompt_with_image_urls

                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**Model:** {result.model_name}")
                        with col2:
                            st.markdown(f"**Client:** {result.client}")
                        with col3:
                            if result.success:
                                st.markdown("**Status:** ✅ Success")
                            else:
                                st.markdown("**Status:** ❌ Failed")

                        st.markdown("**Response:**")
                        st.text_area(
                            "Model Response",
                            value=result.response,
                            height=100,
                            key=f"img_url_{idx}",
                            label_visibility="collapsed",
                        )

                        if result.confirmation_response:
                            st.markdown("**Confirmation:**")
                            try:
                                conf_data = json.loads(result.confirmation_response)
                                if conf_data.get("confirmed"):
                                    st.success(
                                        f"✅ Confirmed: {conf_data.get('confirmation_response', 'N/A')}"
                                    )
                                else:
                                    st.error(
                                        f"❌ Not Confirmed: {conf_data.get('confirmation_response', 'N/A')}"
                                    )
                            except:
                                st.info(result.confirmation_response)

                        st.divider()

                    # Basic Param Values Test Results
                    if test_results.basic_param_values:
                        st.subheader("📐 Basic Param Values Test")
                        result = test_results.basic_param_values

                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**Model:** {result.model_name}")
                        with col2:
                            st.markdown(f"**Client:** {result.client}")
                        with col3:
                            if result.success:
                                st.markdown("**Status:** ✅ Success")
                            else:
                                st.markdown("**Status:** ❌ Failed")

                        st.markdown("**Response:**")
                        st.text_area(
                            "Model Response",
                            value=result.response,
                            height=100,
                            key=f"basic_param_{idx}",
                            label_visibility="collapsed",
                        )

                        if result.confirmation_response:
                            st.markdown("**Confirmation:**")
                            st.info(result.confirmation_response)

                        st.divider()

                    # Structured JSON Test Results
                    if test_results.structured_json_test:
                        st.subheader("📝 Structured JSON Test")
                        result = test_results.structured_json_test

                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**Model:** {result.model_name}")
                        with col2:
                            st.markdown(f"**Client:** {result.client}")
                        with col3:
                            if result.success:
                                st.markdown("**Status:** ✅ Success")
                            else:
                                st.markdown("**Status:** ❌ Failed")

                        st.markdown("**Response:**")
                        st.text_area(
                            "Model Response",
                            value=result.response,
                            height=100,
                            key=f"std_text_{idx}",
                            label_visibility="collapsed",
                        )

                        if result.confirmation_response:
                            st.markdown("**Confirmation:**")
                            st.info(result.confirmation_response)

                        st.divider()

        except Exception as e:
            progress_bar.empty()
            st.error(f"❌ An error occurred while running tests: {str(e)}")
            st.exception(e)
    else:
        # Show configuration summary
        st.info(
            "👈 Configure your test settings in the sidebar and click **Run Tests** to begin."
        )

        # Display current configuration
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Selected Models")
            if selected_models:
                for model in selected_models:
                    st.markdown(f"- **{model.name}** ({model.type})")
            else:
                st.markdown("*No models selected*")

        with col2:
            st.subheader("Selected Tests")
            active_tests = [
                k.replace("_", " ").title() for k, v in test_selections.items() if v
            ]
            if active_tests:
                for test in active_tests:
                    st.markdown(f"- {test}")
            else:
                st.markdown("*No tests selected*")

        st.divider()
        st.markdown(f"**Confirmation Model:** `{confirmer_model}`")
