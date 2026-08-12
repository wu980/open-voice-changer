from pathlib import Path
import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from open_voice_changer.audio import convert_pitch
from open_voice_changer.batch import convert_directory
from open_voice_changer.effects import preset_names


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
        self.batch_mode = ctk.BooleanVar(value=False)
        self.semitones = ctk.DoubleVar(value=0.0)
        self.preset = ctk.StringVar(value="clean")
        self.status = ctk.StringVar(value="Ready")
        self.last_output_path: Path | None = None

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Open Voice Changer",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=3, padx=24, pady=(24, 16), sticky="w")

        mode_switch = ctk.CTkSwitch(
            self,
            text="Batch folder mode",
            variable=self.batch_mode,
            command=self._toggle_mode,
        )
        mode_switch.grid(row=1, column=0, columnspan=3, padx=24, pady=(0, 8), sticky="w")

        self.input_label = ctk.CTkLabel(self, text="Input audio")
        self.input_label.grid(row=2, column=0, padx=24, pady=8, sticky="w")
        input_entry = ctk.CTkEntry(self, textvariable=self.input_path)
        input_entry.grid(row=2, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(self, text="Browse", command=self._choose_input).grid(
            row=2,
            column=2,
            padx=(8, 24),
            pady=8,
        )

        self.output_label = ctk.CTkLabel(self, text="Output file")
        self.output_label.grid(row=3, column=0, padx=24, pady=8, sticky="w")
        output_entry = ctk.CTkEntry(self, textvariable=self.output_path)
        output_entry.grid(row=3, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(self, text="Save as", command=self._choose_output).grid(
            row=3,
            column=2,
            padx=(8, 24),
            pady=8,
        )

        ctk.CTkLabel(self, text="Semitones").grid(row=4, column=0, padx=24, pady=8, sticky="w")
        slider = ctk.CTkSlider(
            self,
            from_=-12,
            to=12,
            number_of_steps=48,
            variable=self.semitones,
            command=self._update_pitch_label,
        )
        slider.grid(row=4, column=1, padx=8, pady=8, sticky="ew")

        self.pitch_label = ctk.CTkLabel(self, text="0.0")
        self.pitch_label.grid(row=4, column=2, padx=(8, 24), pady=8)

        ctk.CTkLabel(self, text="Preset").grid(row=5, column=0, padx=24, pady=8, sticky="w")
        preset_menu = ctk.CTkOptionMenu(
            self,
            values=preset_names(),
            variable=self.preset,
        )
        preset_menu.grid(row=5, column=1, padx=8, pady=8, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=6, column=1, padx=8, pady=(20, 4), sticky="ew")

        self.convert_button = ctk.CTkButton(
            self,
            text="Convert",
            height=40,
            command=self._convert,
        )
        self.convert_button.grid(row=7, column=1, padx=8, pady=(12, 8), sticky="ew")

        self.open_output_button = ctk.CTkButton(
            self,
            text="Open Output",
            height=40,
            state="disabled",
            command=self._open_output_location,
        )
        self.open_output_button.grid(row=7, column=2, padx=(8, 24), pady=(12, 8), sticky="ew")

        status_label = ctk.CTkLabel(self, textvariable=self.status, text_color="gray")
        status_label.grid(row=8, column=0, columnspan=3, padx=24, pady=(12, 24), sticky="w")

    def _choose_input(self) -> None:
        if self.batch_mode.get():
            directory = filedialog.askdirectory(title="Choose input folder")
            if directory:
                self.input_path.set(directory)
                self.output_path.set(str(Path(directory) / "converted"))
            return

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
        if self.batch_mode.get():
            directory = filedialog.askdirectory(title="Choose output folder")
            if directory:
                self.output_path.set(directory)
            return

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

    def _toggle_mode(self) -> None:
        if self.batch_mode.get():
            self.input_label.configure(text="Input folder")
            self.output_label.configure(text="Output folder")
            self.output_path.set(str(Path("outputs")))
            self.open_output_button.configure(state="disabled")
        else:
            self.input_label.configure(text="Input audio")
            self.output_label.configure(text="Output file")
            self.output_path.set(str(Path("outputs") / "converted.wav"))
            self.open_output_button.configure(state="disabled")

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
            self._set_busy(True)
            self.status.set("Converting...")
            self.progress_bar.set(0)
            self.update_idletasks()
            if self.batch_mode.get():
                results = convert_directory(
                    input_dir=input_file,
                    output_dir=output_file,
                    semitones=self.semitones.get(),
                    preset=self.preset.get(),
                    on_progress=self._show_batch_progress,
                )
                message = f"Converted {len(results)} file(s)."
                self.last_output_path = Path(output_file)
                self.progress_bar.set(1)
                self.status.set(message)
                self.open_output_button.configure(state="normal")
                messagebox.showinfo("Done", message)
                return

            result = convert_pitch(
                input_path=input_file,
                output_path=output_file,
                semitones=self.semitones.get(),
                preset=self.preset.get(),
            )
        except Exception as exc:
            self.status.set("Conversion failed")
            self.progress_bar.set(0)
            messagebox.showerror("Conversion failed", str(exc))
            return
        finally:
            self._set_busy(False)

        self.last_output_path = Path(result)
        self.progress_bar.set(1)
        self.status.set(f"Saved: {result}")
        self.open_output_button.configure(state="normal")
        messagebox.showinfo("Done", f"Saved converted audio:\n{result}")

    def _show_batch_progress(self, index: int, total: int, result: Path) -> None:
        if total:
            self.progress_bar.set(index / total)
        self.status.set(f"Converted {index}/{total}: {result.name}")
        self.update_idletasks()

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.convert_button.configure(state=state)

    def _open_output_location(self) -> None:
        if self.last_output_path is None:
            return

        target = self.last_output_path
        folder = target if target.is_dir() else target.parent
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder)
