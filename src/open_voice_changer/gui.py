from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from open_voice_changer.audio import convert_pitch


class VoiceChangerApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Open Voice Changer")
        self.geometry("680x360")
        self.minsize(620, 340)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar(value=str(Path("outputs") / "converted.wav"))
        self.semitones = ctk.DoubleVar(value=0.0)
        self.status = ctk.StringVar(value="Ready")

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Open Voice Changer",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=3, padx=24, pady=(24, 16), sticky="w")

        ctk.CTkLabel(self, text="Input audio").grid(row=1, column=0, padx=24, pady=8, sticky="w")
        input_entry = ctk.CTkEntry(self, textvariable=self.input_path)
        input_entry.grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(self, text="Browse", command=self._choose_input).grid(
            row=1,
            column=2,
            padx=(8, 24),
            pady=8,
        )

        ctk.CTkLabel(self, text="Output file").grid(row=2, column=0, padx=24, pady=8, sticky="w")
        output_entry = ctk.CTkEntry(self, textvariable=self.output_path)
        output_entry.grid(row=2, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(self, text="Save as", command=self._choose_output).grid(
            row=2,
            column=2,
            padx=(8, 24),
            pady=8,
        )

        ctk.CTkLabel(self, text="Semitones").grid(row=3, column=0, padx=24, pady=8, sticky="w")
        slider = ctk.CTkSlider(
            self,
            from_=-12,
            to=12,
            number_of_steps=48,
            variable=self.semitones,
            command=self._update_pitch_label,
        )
        slider.grid(row=3, column=1, padx=8, pady=8, sticky="ew")

        self.pitch_label = ctk.CTkLabel(self, text="0.0")
        self.pitch_label.grid(row=3, column=2, padx=(8, 24), pady=8)

        convert_button = ctk.CTkButton(
            self,
            text="Convert",
            height=40,
            command=self._convert,
        )
        convert_button.grid(row=4, column=1, padx=8, pady=(24, 8), sticky="ew")

        status_label = ctk.CTkLabel(self, textvariable=self.status, text_color="gray")
        status_label.grid(row=5, column=0, columnspan=3, padx=24, pady=(12, 24), sticky="w")

    def _choose_input(self) -> None:
        filename = filedialog.askopenfilename(
            title="Choose audio file",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.input_path.set(filename)
            input_file = Path(filename)
            self.output_path.set(str(Path("outputs") / f"{input_file.stem}-converted.wav"))

    def _choose_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="Choose output file",
            defaultextension=".wav",
            filetypes=[
                ("WAV audio", "*.wav"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.output_path.set(filename)

    def _update_pitch_label(self, value: float) -> None:
        self.pitch_label.configure(text=f"{float(value):.1f}")

    def _convert(self) -> None:
        input_file = self.input_path.get().strip()
        output_file = self.output_path.get().strip()

        if not input_file:
            messagebox.showerror("Missing input", "Please choose an input audio file.")
            return

        if not output_file:
            messagebox.showerror("Missing output", "Please choose an output file.")
            return

        try:
            self.status.set("Converting...")
            self.update_idletasks()
            result = convert_pitch(
                input_path=input_file,
                output_path=output_file,
                semitones=self.semitones.get(),
            )
        except Exception as exc:
            self.status.set("Conversion failed")
            messagebox.showerror("Conversion failed", str(exc))
            return

        self.status.set(f"Saved: {result}")
        messagebox.showinfo("Done", f"Saved converted audio:\n{result}")
