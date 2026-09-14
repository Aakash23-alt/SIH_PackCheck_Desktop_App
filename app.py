import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract
import re
from datetime import datetime
import os
import winsound


# ============================================================
# TESSERACT
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================
# ALARM FILE
# ============================================================

ALARM_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "alarm.wav"
)


# ============================================================
# APPLICATION
# ============================================================

class PackCheckApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "COMPLIANCE PACK CHECKING SYSTEM - AI Packaged Commodity Compliance Checker"
        )

        self.root.geometry("1400x850")
        self.root.minsize(1100, 700)

        self.images = []
        self.image_paths = []

        # Alarm state
        self.alarm_running = False

        # Normal colors
        self.normal_bg = "#f4f7fb"

        self.root.configure(
            bg=self.normal_bg
        )

        self._beam_step = 0
        self.create_interface()

    # ========================================================
    # INTERFACE
    # ========================================================

    def create_interface(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.header = tk.Frame(
            self.root,
            bg="#14213d",
            height=90
        )

        self.header.pack(
            fill="x"
        )

        title = tk.Label(
            self.header,
            text="COMPLIANCE PACK CHECKING SYSTEM",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#14213d"
        )

        title.pack(
            pady=(12, 0)
        )

        subtitle = tk.Label(
            self.header,
            text="AI-Powered Packaged Commodity Compliance Checker",
            font=("Segoe UI", 12),
            fg="#dce6f5",
            bg="#14213d"
        )

        subtitle.pack()


        # ----------------------------------------------------
        # MAIN AREA
        # ----------------------------------------------------

        self.main = tk.Frame(
            self.root,
            bg=self.normal_bg
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ====================================================
        # LEFT PANEL
        # ====================================================

        self.left_panel = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid",
            width=420
        )

        self.left_panel.pack(
            side="left",
            fill="both",
            expand=False,
            padx=(0, 10)
        )

        self.left_panel.pack_propagate(False)


        tk.Label(
            self.left_panel,
            text="PRODUCT IMAGES",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#14213d"
        ).pack(
            pady=(15, 5)
        )


        self.count_label = tk.Label(
            self.left_panel,
            text="0 / 6 images added",
            font=("Segoe UI", 10),
            bg="white",
            fg="#555555"
        )

        self.count_label.pack()


        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            self.left_panel,
            bg="white"
        )

        button_frame.pack(
            pady=15
        )


        tk.Button(
            button_frame,
            text="ADD IMAGE",
            command=self.add_image,
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=14,
            height=2,
            bd=0,
            cursor="hand2"
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        tk.Button(
            button_frame,
            text="REMOVE LAST",
            command=self.remove_last,
            font=("Segoe UI", 10, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            width=14,
            height=2,
            bd=0,
            cursor="hand2"
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        tk.Button(
            button_frame,
            text="CLEAR ALL",
            command=self.clear_images,
            font=("Segoe UI", 10, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            width=14,
            height=2,
            bd=0,
            cursor="hand2"
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=8
        )


        # ----------------------------------------------------
        # IMAGE PREVIEW
        # ----------------------------------------------------

        self.preview_frame = tk.Frame(
            self.left_panel,
            bg="#f8fafc"
        )

        self.preview_frame.pack(
            padx=15,
            pady=5,
            fill="both",
            expand=True
        )


        self.preview_label = tk.Label(
            self.preview_frame,
            text=
            "ADD PRODUCT IMAGES\n\n"
            "Image 1 - Front\n"
            "Image 2 - Back\n"
            "Image 3 - Side\n\n"
            "Add images one by one.",
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg="#64748b",
            justify="center"
        )

        self.preview_label.pack(
            expand=True
        )


        # ----------------------------------------------------
        # SCAN BUTTON
        # ----------------------------------------------------

        tk.Button(
            self.left_panel,
            text="SCAN PRODUCT",
            command=self.scan_product,
            font=("Segoe UI", 14, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            width=28,
            height=2,
            bd=0,
            cursor="hand2"
        ).pack(
            pady=15
        )


        # ====================================================
        # RIGHT PANEL
        # ====================================================

        self.right_panel = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )


        tk.Label(
            self.right_panel,
            text="COMPLIANCE INSPECTION REPORT",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#14213d"
        ).pack(
            pady=(15, 8)
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = tk.Label(
            self.right_panel,
            text="WAITING FOR PRODUCT SCAN",
            font=("Segoe UI", 18, "bold"),
            bg="#e2e8f0",
            fg="#475569",
            padx=20,
            pady=12
        )

        self.status_label.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ----------------------------------------------------
        # REPORT
        # ----------------------------------------------------

        self.report_frame = tk.Frame(
            self.right_panel,
            bg="white"
        )

        self.report_frame.pack(
            fill="x",
            padx=20
        )


        self.fields = {}


        field_names = [
            ("Product / Commodity Name", "product_name"),
            ("Maximum Retail Price (MRP)", "mrp"),
            ("Net Quantity", "quantity"),
            ("Manufacturer / Packer / Importer", "manufacturer"),
            ("Manufacturer / Packer Address", "address"),
            ("Date of Manufacture / Packing", "mfg_date"),
            ("Best Before / Use By", "expiry"),
            ("Batch / Lot Number", "batch"),
            ("Consumer Care Details", "consumer"),
            ("Country of Origin", "country")
        ]


        for row, (label_text, key) in enumerate(field_names):

            tk.Label(
                self.report_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#334155",
                anchor="w"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=8,
                pady=5
            )


            value = tk.Label(
                self.report_frame,
                text="Not scanned",
                font=("Segoe UI", 10),
                bg="#f8fafc",
                fg="#64748b",
                anchor="w",
                width=48,
                padx=8,
                pady=4
            )

            value.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=8,
                pady=5
            )

            self.fields[key] = value


        self.report_frame.columnconfigure(
            1,
            weight=1
        )


        # ----------------------------------------------------
        # EXPIRY STATUS
        # ----------------------------------------------------

        self.expiry_status = tk.Label(
            self.right_panel,
            text="Expiry status: Not checked",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#475569"
        )

        self.expiry_status.pack(
            pady=8
        )


        # ----------------------------------------------------
        # MISSING INFORMATION
        # ----------------------------------------------------

        self.missing_label = tk.Label(
            self.right_panel,
            text="Missing / unclear information:\nNone",
            font=("Segoe UI", 10),
            bg="#fff7ed",
            fg="#9a3412",
            justify="left",
            anchor="w",
            padx=12,
            pady=8
        )

        self.missing_label.pack(
            fill="x",
            padx=20,
            pady=8
        )


        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        self.action_label = tk.Label(
            self.right_panel,
            text=
            "Recommended action:\n"
            "Scan a product to begin inspection.",
            font=("Segoe UI", 10),
            bg="#eff6ff",
            fg="#1e40af",
            justify="left",
            anchor="w",
            padx=12,
            pady=8
        )

        self.action_label.pack(
            fill="x",
            padx=20,
            pady=5
        )


        # ----------------------------------------------------
        # OCR
        # ----------------------------------------------------

        tk.Label(
            self.right_panel,
            text="OCR TEXT PREVIEW",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )


        self.ocr_text = tk.Text(
            self.right_panel,
            height=8,
            font=("Consolas", 9),
            bg="#f8fafc",
            fg="#334155",
            wrap="word"
        )

        self.ocr_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )


    # ========================================================
    # ADD IMAGE
    # ========================================================

    def add_image(self):

        if len(self.image_paths) >= 6:

            messagebox.showwarning(
                "Image Limit",
                "Maximum 6 images allowed."
            )

            return


        path = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.webp"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )


        if not path:
            return


        try:

            img = Image.open(path)

            self.image_paths.append(path)
            self.images.append(img.copy())

            self.update_previews()

        except Exception as e:

            messagebox.showerror(
                "Image Error",
                str(e)
            )


    # ========================================================
    # PREVIEW
    # ========================================================

    def update_previews(self):

        self.count_label.config(
            text=f"{len(self.images)} / 6 images added"
        )


        for widget in self.preview_frame.winfo_children():

            widget.destroy()


        if not self.images:

            tk.Label(
                self.preview_frame,
                text=
                "ADD PRODUCT IMAGES\n\n"
                "Image 1 - Front\n"
                "Image 2 - Back\n"
                "Image 3 - Side",
                font=("Segoe UI", 11),
                bg="#f8fafc",
                fg="#64748b",
                justify="center"
            ).pack(
                expand=True
            )

            return


        canvas = tk.Canvas(
            self.preview_frame,
            bg="#f8fafc",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self.preview_frame,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = tk.Frame(
            canvas,
            bg="#f8fafc"
        )


        scroll_frame.bind(
            "<Configure>",
            lambda e:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.thumbnail_refs = []


        for index, img in enumerate(self.images):

            frame = tk.Frame(
                scroll_frame,
                bg="white",
                bd=1,
                relief="solid"
            )

            frame.pack(
                padx=10,
                pady=8,
                fill="x"
            )


            thumbnail = img.copy()

            thumbnail.thumbnail(
                (330, 150)
            )


            photo = ImageTk.PhotoImage(
                thumbnail
            )

            self.thumbnail_refs.append(
                photo
            )


            tk.Label(
                frame,
                image=photo,
                bg="white"
            ).pack(
                pady=5
            )


            tk.Label(
                frame,
                text=f"IMAGE {index + 1}",
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#14213d"
            ).pack(
                pady=(0, 5)
            )


    # ========================================================
    # REMOVE LAST IMAGE
    # ========================================================

    def remove_last(self):

        if not self.image_paths:
            return


        self.stop_alarm()

        self.image_paths.pop()
        self.images.pop()

        self.update_previews()


    # ========================================================
    # CLEAR
    # ========================================================

    def clear_images(self):

        self.stop_alarm()

        self.image_paths.clear()
        self.images.clear()

        self.update_previews()

        self.reset_interface()


    # ========================================================
    # RESET
    # ========================================================

    def reset_interface(self):

        self.stop_alarm()


        self.root.configure(
            bg=self.normal_bg
        )

        self.main.configure(
            bg=self.normal_bg
        )

        self.left_panel.configure(
            bg="white"
        )

        self.right_panel.configure(
            bg="white"
        )


        self.status_label.configure(
            text="WAITING FOR PRODUCT SCAN",
            bg="#e2e8f0",
            fg="#475569"
        )


        for key in self.fields:

            self.fields[key].configure(
                text="Not scanned",
                bg="#f8fafc",
                fg="#64748b"
            )


        self.expiry_status.configure(
            text="Expiry status: Not checked",
            bg="white",
            fg="#475569"
        )


        self.missing_label.configure(
            text="Missing / unclear information:\nNone",
            bg="#fff7ed",
            fg="#9a3412"
        )


        self.action_label.configure(
            text=
            "Recommended action:\n"
            "Scan a product to begin inspection.",
            bg="#eff6ff",
            fg="#1e40af"
        )


        self.ocr_text.delete(
            "1.0",
            tk.END
        )


    # ========================================================
    # OCR
    # ========================================================

    def perform_ocr(self, image_path):

        image = cv2.imread(
            image_path
        )


        if image is None:
            return ""


        rotations = [
            image,
            cv2.rotate(
                image,
                cv2.ROTATE_90_CLOCKWISE
            ),
            cv2.rotate(
                image,
                cv2.ROTATE_180
            ),
            cv2.rotate(
                image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )
        ]


        results = []


        for img in rotations:

            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )


            gray = cv2.resize(
                gray,
                None,
                fx=1.5,
                fy=1.5,
                interpolation=cv2.INTER_CUBIC
            )


            text = pytesseract.image_to_string(
                gray,
                config="--psm 6"
            )


            if text.strip():

                results.append(
                    text
                )


            _, threshold = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY +
                cv2.THRESH_OTSU
            )


            text2 = pytesseract.image_to_string(
                threshold,
                config="--psm 6"
            )


            if text2.strip():

                results.append(
                    text2
                )


        return "\n".join(results)


    # ========================================================
    # PRODUCT NAME
    # ========================================================

    def extract_product_name(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]


        ignored = [
            "MRP",
            "PRICE",
            "NET",
            "WEIGHT",
            "QUANTITY",
            "QTY",
            "MANUFACTURED",
            "MANUFACTURER",
            "PACKED",
            "PACKER",
            "BATCH",
            "LOT",
            "USE BY",
            "BEST BEFORE",
            "EXPIRY",
            "INGREDIENT",
            "INGREDIENTS",
            "ADDRESS",
            "CUSTOMER",
            "CONSUMER",
            "CARE",
            "COUNTRY",
            "ORIGIN",
            "FSSAI",
            "NUTRITION",
            "CALORIES",
            "BARCODE",
            "VEGETARIAN"
        ]


        candidates = []


        for line in lines:

            upper = line.upper()


            if len(line) < 3:
                continue


            if any(
                word in upper
                for word in ignored
            ):
                continue


            if re.search(
                r"\d{1,4}\s?(g|kg|ml|l)\b",
                upper
            ):
                continue


            if re.search(
                r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
                line
            ):
                continue


            if "₹" in line:
                continue


            letters = re.findall(
                r"[A-Za-z]",
                line
            )


            if len(letters) < 3:
                continue


            candidates.append(
                line
            )


        if not candidates:

            return "Not detected"


        candidates.sort(
            key=lambda x: (
                0 if x.isupper() else 1,
                len(x)
            )
        )


        result = candidates[0]


        result = re.sub(
            r"[^A-Za-z0-9&().,'\- ]",
            "",
            result
        )


        return result.strip()


    # ========================================================
    # MRP
    # ========================================================

    def extract_mrp(self, text):

        patterns = [

            r"(?:MRP|M\.R\.P)\s*[:\-]?\s*"
            r"(?:Rs\.?|₹)?\s*"
            r"([0-9]+(?:\.[0-9]{1,2})?)",

            r"(?:MAXIMUM RETAIL PRICE)\s*[:\-]?\s*"
            r"(?:Rs\.?|₹)?\s*"
            r"([0-9]+(?:\.[0-9]{1,2})?)",

            r"(?:₹|Rs\.?)\s*"
            r"([0-9]+(?:\.[0-9]{1,2})?)"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return "₹ " + match.group(1)


        return "Not detected"


    # ========================================================
    # QUANTITY
    # ========================================================

    def extract_quantity(self, text):

        patterns = [

            r"(?:NET\s*(?:WT|WEIGHT|QUANTITY))"
            r"\s*[:\-]?\s*"
            r"([0-9]+(?:\.[0-9]+)?)\s*"
            r"(kg|g|mg|l|ml)",

            r"\b([0-9]+(?:\.[0-9]+)?)\s*"
            r"(kg|g|mg|l|ml)\b"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return (
                    match.group(1)
                    + " "
                    + match.group(2)
                )


        return "Not detected"


    # ========================================================
    # EXPIRY
    # ========================================================

    def extract_expiry_date(self, text):

        patterns = [

            r"(?:USE\s*BY|EXPIRY|EXP|"
            r"BEST\s*BEFORE|BEST\s*BEF)"
            r"\s*[:\-]?\s*"
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",

            r"(?:USE\s*BY|EXPIRY|EXP|"
            r"BEST\s*BEFORE|BEST\s*BEF)"
            r"\s*[:\-]?\s*"
            r"(\d{1,2}[/-]\d{2,4})"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return match.group(1)


        return "Not detected"


    # ========================================================
    # MANUFACTURER
    # ========================================================

    def extract_manufacturer(self, text):

        patterns = [

            r"(?:MANUFACTURED\s*BY|"
            r"MANUFACTURER|"
            r"PACKED\s*BY|"
            r"PACKER)"
            r"\s*[:\-]?\s*(.+)",

            r"(?:MFD\s*BY|MFG\s*BY)"
            r"\s*[:\-]?\s*(.+)"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return (
                    match.group(1)
                    .split("\n")[0]
                    .strip()
                )


        return "Not detected"


    # ========================================================
    # ADDRESS
    # ========================================================

    def extract_address(self, text):

        lines = text.splitlines()


        for i, line in enumerate(lines):

            upper = line.upper()


            if (
                "ADDRESS" in upper
                or "REGISTERED OFFICE" in upper
                or "MANUFACTURED AT" in upper
                or "PACKED AT" in upper
            ):

                if ":" in line:

                    value = line.split(
                        ":",
                        1
                    )[1].strip()


                    if value:
                        return value


                if i + 1 < len(lines):

                    value = lines[i + 1].strip()


                    if value:
                        return value


        return "Not detected"


    # ========================================================
    # MANUFACTURING DATE
    # ========================================================

    def extract_mfg_date(self, text):

        patterns = [

            r"(?:MFD|MFG|MFG\.|PKD|PACKED|"
            r"MANUFACTURED)"
            r"\s*[:\-]?\s*"
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",

            r"(?:DATE\s*OF\s*"
            r"(?:MFG|MANUFACTURE|PACKING))"
            r"\s*[:\-]?\s*"
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return match.group(1)


        return "Not detected"


    # ========================================================
    # BATCH
    # ========================================================

    def extract_batch(self, text):

        pattern = (
            r"(?:BATCH|BATCH\s*NO|LOT|LOT\s*NO)"
            r"\s*[:#\-]?\s*"
            r"([A-Z0-9\-]+)"
        )


        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )


        if match:

            return match.group(1)


        return "Not detected"


    # ========================================================
    # CONSUMER CARE
    # ========================================================

    def extract_consumer(self, text):

        patterns = [

            r"(?:CUSTOMER\s*CARE|"
            r"CONSUMER\s*CARE)"
            r"\s*[:\-]?\s*(.+)",

            r"(?:HELPLINE|TOLL\s*FREE)"
            r"\s*[:\-]?\s*(.+)"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )


            if match:

                return (
                    match.group(1)
                    .split("\n")[0]
                    .strip()
                )


        phone = re.search(
            r"\b[6-9]\d{9}\b",
            text
        )


        if phone:

            return phone.group(0)


        return "Not detected"


    # ========================================================
    # COUNTRY
    # ========================================================

    def extract_country(self, text):

        match = re.search(
            r"(?:COUNTRY\s*OF\s*ORIGIN|"
            r"MADE\s*IN)"
            r"\s*[:\-]?\s*"
            r"([A-Za-z ]+)",
            text,
            re.IGNORECASE
        )


        if match:

            return match.group(1).strip()


        return "Not detected"


    # ========================================================
    # CHECK EXPIRY
    # ========================================================

    def check_expiry(self, expiry_date):

        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d/%m/%y",
            "%d-%m-%y"
        ]


        for fmt in formats:

            try:

                date_value = datetime.strptime(
                    expiry_date,
                    fmt
                ).date()


                today = datetime.now().date()


                if date_value < today:

                    return "EXPIRED"


                return "VALID"


            except ValueError:

                continue


        return "UNKNOWN"


    # ========================================================
    # START ALARM
    # ========================================================

    def start_alarm(self):

        if self.alarm_running:
            return


        if not os.path.exists(ALARM_PATH):

            messagebox.showerror(
                "Alarm File Missing",
                "alarm.wav was not found.\n\n"
                "Please put alarm.wav in the same "
                "folder as app.py."
            )

            return


        try:

            winsound.PlaySound(
                ALARM_PATH,
                winsound.SND_FILENAME |
                winsound.SND_ASYNC |
                winsound.SND_LOOP
            )

            self.alarm_running = True

            print("ALARM STARTED")

        except Exception as e:

            messagebox.showerror(
                "Alarm Error",
                str(e)
            )


    # ========================================================
    # STOP ALARM
    # ========================================================

    def stop_alarm(self):

        try:

            winsound.PlaySound(
                None,
                winsound.SND_ASYNC
            )

        except Exception:
            pass


        self.alarm_running = False

        print("ALARM STOPPED")


    # ========================================================
    # EXPIRED SCREEN
    # ========================================================

    def show_expired_screen(self, expiry_date):

        self.stop_alarm()


        expired_bg = "#fde8e8"
        expired_panel = "#fff5f5"


        # Background
        self.root.configure(
            bg=expired_bg
        )

        self.main.configure(
            bg=expired_bg
        )

        self.left_panel.configure(
            bg=expired_panel
        )

        self.right_panel.configure(
            bg=expired_panel
        )


        # Status
        self.status_label.configure(
            text="⚠ EXPIRED PRODUCT",
            bg="#fecaca",
            fg="#b91c1c"
        )


        # Expiry
        self.expiry_status.configure(
            text=
            f"EXPIRY STATUS: EXPIRED  |  "
            f"Date: {expiry_date}",
            bg=expired_panel,
            fg="#b91c1c"
        )


        self.fields["expiry"].configure(
            text=expiry_date,
            bg="#fee2e2",
            fg="#b91c1c"
        )


        # Action
        self.action_label.configure(
            text=
            "Recommended action:\n"
            "DO NOT ACCEPT / SELL THIS PRODUCT.\n"
            "Product should be removed from sale "
            "and manually verified.",
            bg="#fee2e2",
            fg="#991b1b"
        )


        # Start uploaded alarm
        self.start_alarm()


    # ========================================================
    # VALID SCREEN
    # ========================================================

    def show_valid_screen(self, expiry_date):

        self.stop_alarm()


        self.root.configure(
            bg=self.normal_bg
        )

        self.main.configure(
            bg=self.normal_bg
        )

        self.left_panel.configure(
            bg="white"
        )

        self.right_panel.configure(
            bg="white"
        )


        self.status_label.configure(
            text="✓ PRODUCT DATE VALID",
            bg="#dcfce7",
            fg="#15803d"
        )


        self.expiry_status.configure(
            text=
            f"EXPIRY STATUS: VALID  |  "
            f"Date: {expiry_date}",
            bg="white",
            fg="#15803d"
        )


        self.fields["expiry"].configure(
            text=expiry_date,
            bg="#f0fdf4",
            fg="#15803d"
        )


    # ========================================================
    # SCAN
    # ========================================================

    def scan_product(self):

        if not self.image_paths:

            messagebox.showwarning(
                "No Images",
                "Please add at least one product image."
            )

            return


        self.stop_alarm()


        self.status_label.configure(
            text="SCANNING PRODUCT...",
            bg="#dbeafe",
            fg="#1d4ed8"
        )


        self.root.update_idletasks()


        all_ocr = []


        # ----------------------------------------------------
        # OCR ALL IMAGES
        # ----------------------------------------------------

        for index, path in enumerate(
            self.image_paths
        ):

            text = self.perform_ocr(
                path
            )


            if text:

                all_ocr.append(
                    f"\n===== IMAGE {index + 1} =====\n"
                    + text
                )


        raw_text = "\n".join(
            all_ocr
        )


        # ----------------------------------------------------
        # SHOW OCR
        # ----------------------------------------------------

        self.ocr_text.delete(
            "1.0",
            tk.END
        )


        self.ocr_text.insert(
            tk.END,
            raw_text
        )


        # ----------------------------------------------------
        # EXTRACT INFORMATION
        # ----------------------------------------------------

        product_name = self.extract_product_name(
            raw_text
        )

        mrp = self.extract_mrp(
            raw_text
        )

        quantity = self.extract_quantity(
            raw_text
        )

        expiry = self.extract_expiry_date(
            raw_text
        )

        manufacturer = self.extract_manufacturer(
            raw_text
        )

        address = self.extract_address(
            raw_text
        )

        mfg_date = self.extract_mfg_date(
            raw_text
        )

        batch = self.extract_batch(
            raw_text
        )

        consumer = self.extract_consumer(
            raw_text
        )

        country = self.extract_country(
            raw_text
        )


        # ----------------------------------------------------
        # UPDATE FIELDS
        # ----------------------------------------------------

        values = {
            "product_name": product_name,
            "mrp": mrp,
            "quantity": quantity,
            "manufacturer": manufacturer,
            "address": address,
            "mfg_date": mfg_date,
            "expiry": expiry,
            "batch": batch,
            "consumer": consumer,
            "country": country
        }


        for key, value in values.items():

            if value == "Not detected":

                self.fields[key].configure(
                    text="Not detected",
                    bg="#fff7ed",
                    fg="#c2410c"
                )

            else:

                self.fields[key].configure(
                    text=value,
                    bg="#f8fafc",
                    fg="#334155"
                )


        # ----------------------------------------------------
        # EXPIRY CHECK
        # ----------------------------------------------------

        expiry_status = "UNKNOWN"


        if expiry != "Not detected":

            expiry_status = self.check_expiry(
                expiry
            )


        # ----------------------------------------------------
        # EXPIRED
        # ----------------------------------------------------

        if expiry_status == "EXPIRED":

            self.show_expired_screen(
                expiry
            )


        # ----------------------------------------------------
        # VALID
        # ----------------------------------------------------

        elif expiry_status == "VALID":

            self.show_valid_screen(
                expiry
            )


        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        else:

            self.stop_alarm()

            self.status_label.configure(
                text="NEEDS MANUAL REVIEW",
                bg="#fef3c7",
                fg="#92400e"
            )


            self.expiry_status.configure(
                text="EXPIRY STATUS: Unable to verify",
                bg="white",
                fg="#92400e"
            )


        # ----------------------------------------------------
        # FIND MISSING INFORMATION
        # ----------------------------------------------------

        missing = []


        check_fields = [

            ("Product / Commodity Name",
             product_name),

            ("MRP",
             mrp),

            ("Net Quantity",
             quantity),

            ("Manufacturer / Packer / Importer",
             manufacturer),

            ("Manufacturer / Packer Address",
             address),

            ("Date of Manufacture / Packing",
             mfg_date),

            ("Best Before / Use By",
             expiry),

            ("Batch / Lot Number",
             batch),

            ("Consumer Care Details",
             consumer)
        ]


        for name, value in check_fields:

            if value == "Not detected":

                missing.append(
                    name
                )


        if missing:

            missing_text = (
                "Missing / unclear information:\n"
                +
                "\n".join(
                    "• " + item
                    for item in missing
                )
            )


            self.missing_label.configure(
                text=missing_text,
                bg="#fff7ed",
                fg="#9a3412"
            )


        else:

            self.missing_label.configure(
                text=
                "Missing / unclear information:\n"
                "None detected",
                bg="#f0fdf4",
                fg="#166534"
            )


        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        if expiry_status == "EXPIRED":

            self.status_label.configure(
                text=
                "⚠ POTENTIAL NON-COMPLIANCE - EXPIRED",
                bg="#fecaca",
                fg="#b91c1c"
            )


        elif len(missing) >= 4:

            self.status_label.configure(
                text="POTENTIAL NON-COMPLIANCE",
                bg="#fee2e2",
                fg="#b91c1c"
            )


            self.action_label.configure(
                text=
                "Recommended action:\n"
                "Several declarations could not be detected.\n"
                "Perform manual inspection.",
                bg="#fff7ed",
                fg="#9a3412"
            )


        elif len(missing) > 0:

            self.status_label.configure(
                text="NEEDS MANUAL REVIEW",
                bg="#fef3c7",
                fg="#92400e"
            )


            self.action_label.configure(
                text=
                "Recommended action:\n"
                "Some declarations were not clearly detected.\n"
                "Verify the package manually.",
                bg="#fff7ed",
                fg="#9a3412"
            )


        else:

            self.status_label.configure(
                text="✓ PRELIMINARY COMPLIANT",
                bg="#dcfce7",
                fg="#15803d"
            )


            self.action_label.configure(
                text=
                "Recommended action:\n"
                "Required declarations were detected.\n"
                "Final legal verification should be performed by an inspector.",
                bg="#f0fdf4",
                fg="#166534"
            )


    # ========================================================
    # CLOSE
    # ========================================================

    def close_app(self):

        self.stop_alarm()
        self.bg_animation_running = False

        self.root.destroy()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PackCheckApp(
        root
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close_app
    )

    root.mainloop()