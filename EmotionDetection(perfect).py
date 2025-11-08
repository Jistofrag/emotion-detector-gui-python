import customtkinter as ctk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ctk.set_appearance_mode("dark")  # Try 'light', 'dark', or 'system'
ctk.set_default_color_theme("green")  # Try 'blue', 'green', 'dark-blue'

class EmotionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Edgy Emotion Detector 🦾")
        self.geometry("900x700")
        self.resizable(False, False)

        # Stunning title
        ctk.CTkLabel(
            self, text="Type a message for instant emotion ➡️", font=("Montserrat", 18, "bold"), text_color="#39FF14"
        ).pack(pady=(22,10))

        # Large text input
        self.input = ctk.CTkTextbox(self, width=340, height=100, font=("Fira Code", 15))
        self.input.pack(pady=4)
        self.input.insert("0.0", "I'm excited to use this! 😄")

        # Analyze button
        ctk.CTkButton(self, text="🔥 Analyze Emotion 🔥", command=self.analyze, fg_color="#1f51ff", hover_color="#6f8cff", font=("Montserrat", 14, "bold")).pack(pady=18)

        # Results - dynamic labels
        self.neg_lbl = ctk.CTkLabel(self, text="", font=("Roboto Mono", 14))
        self.neg_lbl.pack(pady=(5,3))
        self.neu_lbl = ctk.CTkLabel(self, text="", font=("Roboto Mono", 14))
        self.neu_lbl.pack(pady=3)
        self.pos_lbl = ctk.CTkLabel(self, text="", font=("Roboto Mono", 14))
        self.pos_lbl.pack(pady=3)
        self.compound_lbl = ctk.CTkLabel(self, text="", font=("Montserrat", 18, "bold"))
        self.compound_lbl.pack(pady=(18,6))

        # Edgy history panel!
        ctk.CTkLabel(self, text="🕑 History Panel", font=("Montserrat", 13, "italic"), text_color="#b4ffd1").pack(pady=(16,2))
        self.history_box = ctk.CTkTextbox(self, width=340, height=120, font=("Fira Mono", 12))
        self.history_box.pack()
        self.history_box.insert("0.0", "(Your analyzed messages will appear here...)\n")
        self.history_box.configure(state="disabled")

        # Quick clear button
        ctk.CTkButton(self, text="Clear Everything", command=self.clear, fg_color="#ff3131", hover_color="#ff6a6a", font=("Roboto",12)).pack(pady=(12,0))

    def analyze(self):
        text = self.input.get("0.0", "end").strip()
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)

        # Display per-category results
        self.neg_lbl.configure(text=f"😡 Negative: {scores['neg']*100:.1f}%")
        self.neu_lbl.configure(text=f"😐 Neutral: {scores['neu']*100:.1f}%")
        self.pos_lbl.configure(text=f"😄 Positive: {scores['pos']*100:.1f}%")

        # Overall with emoji and fancy display
        if scores['compound'] >= 0.05:
            mood = "POSITIVE 🟢"
            deco = "💚 😄 🚀"
            fontcolor = "#39FF14"
        elif scores['compound'] <= -0.05:
            mood = "NEGATIVE 🔴"
            deco = "💔 😢 ⚡"
            fontcolor = "#FF3131"
        else:
            mood = "NEUTRAL ⚪"
            deco = "😐 🤍 "
            fontcolor = "#cfcfcf"
        self.compound_lbl.configure(text=f"{deco}\n{mood} ({scores['compound']})", text_color=fontcolor)

        # Add to history (enable-write-disable cycle)
        self.history_box.configure(state="normal")
        self.history_box.insert(
            "end",
            f"> {text[:34]+('...' if len(text)>34 else '')}\n   → NEG: {scores['neg']*100:.1f}%, NEU: {scores['neu']*100:.1f}%, POS: {scores['pos']*100:.1f}% → {mood}\n"
        )
        self.history_box.configure(state="disabled")

    def clear(self):
        self.input.delete("0.0", "end")
        self.neg_lbl.configure(text="")
        self.neu_lbl.configure(text="")
        self.pos_lbl.configure(text="")
        self.compound_lbl.configure(text="")
        self.history_box.configure(state="normal")
        self.history_box.delete("0.0", "end")
        self.history_box.insert("0.0", "(Your analyzed messages will appear here...)\n")
        self.history_box.configure(state="disabled")

if __name__ == "__main__":
    app = EmotionApp()
    app.mainloop()

