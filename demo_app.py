from pathlib import Path
import tempfile

import gradio as gr

from open_voice_changer.audio import convert_pitch
from open_voice_changer.effects import preset_names


def convert_online(input_audio: str | None, semitones: float, preset: str) -> str:
    if input_audio is None:
        raise gr.Error("Please upload an audio file.")

    output_dir = Path(tempfile.mkdtemp(prefix="open-voice-changer-"))
    output_path = output_dir / f"converted-{preset}-{float(semitones):g}.wav"

    result = convert_pitch(
        input_path=input_audio,
        output_path=output_path,
        semitones=semitones,
        preset=preset,
    )
    return str(result)


with gr.Blocks(title="Open Voice Changer Demo") as demo:
    gr.Markdown("# Open Voice Changer Demo")
    gr.Markdown(
        "Upload an audio file, choose a preset, adjust pitch, and preview the converted result."
    )
    gr.Markdown(
        "Privacy note: this online demo processes uploaded audio on the server. "
        "Do not upload private, sensitive, or unauthorized audio."
    )

    with gr.Row():
        input_audio = gr.Audio(type="filepath", label="Input audio")
        output_audio = gr.Audio(label="Output audio")

    with gr.Row():
        preset = gr.Dropdown(choices=preset_names(), value="clean", label="Preset")
        semitones = gr.Slider(-12, 12, value=0, step=0.5, label="Semitones")

    convert_button = gr.Button("Convert", variant="primary")

    convert_button.click(
        fn=convert_online,
        inputs=[input_audio, semitones, preset],
        outputs=output_audio,
    )


if __name__ == "__main__":
    demo.launch()
