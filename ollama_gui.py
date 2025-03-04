import gradio as gr
import subprocess

model_options = ["deepseek-r1:1.5b", "deepseek-r1:7b"]


def run_ollama(model, prompt):
    # Remove the prompt from the command arguments.
    command = ["ollama", "run", model]
    print("Running command:", command)

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,  # Enable piping input
            text=True
        )

        # Send the prompt to the process via stdin.
        stdout, stderr = process.communicate(input=prompt, timeout=30)
        print("Return code:", process.returncode)
        print("STDOUT:", stdout)
        print("STDERR:", stderr)

        if process.returncode != 0:
            return f"Error: {stderr.strip()}"
        return stdout.strip() or "No output returned."
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return "Process timed out."
    except Exception as e:
        return f"Exception: {str(e)}"


iface = gr.Interface(
    fn=run_ollama,
    inputs=[
        gr.Dropdown(choices=model_options, label="Select Model"),
        gr.Textbox(lines=5, placeholder="Enter your prompt here", label="Prompt")
    ],
    outputs=gr.Textbox(label="Response"),
    title="Ollama GUI with Gradio",
    description="A simple web interface to interact with your Ollama LLMs."
)

if __name__ == "__main__":
    iface.launch()
