import logging
import subprocess
import tempfile
import os
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PrinterService")

# Note: We are now using CUPS (lp command) for printing to handle locking/queueing better
# The printer should be named 'ThermalPrinter' in CUPS for this to work by default,
# or user can pass the name.

class PrinterService:
    def __init__(self, printer_name="ThermalPrinter"):
        self.printer_name = printer_name
        self.is_mock = False
        self._check_cups()

    def _check_cups(self):
        """Checks if lp command is available."""
        try:
            subprocess.run(["lp", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"CUPS system detected. Target printer: {self.printer_name}")
        except FileNotFoundError:
            logger.warning("CUPS 'lp' command not found. Running in MOCK mode.")
            self.is_mock = True

    def _raw_print_bytes(self, data):
        """Sends raw bytes to the CUPS printer queue."""
        if self.is_mock:
            logger.info(f"[MOCK RAW PRINT] {len(data)} bytes")
            return

        try:
            # We write to a temp file then lp -d PRINTER -o raw FILE
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(data)
                fp.flush()
                filename = fp.name
            
            cmd = ["lp", "-d", self.printer_name, "-o", "raw", filename]
            subprocess.run(cmd, check=True)
            os.remove(filename)
            logger.info("Sent raw job to CUPS")
        except Exception as e:
            logger.error(f"Failed to print via CUPS: {e}")

    def _get_dummy(self):
        """Returns a configured Dummy printer instance."""
        try:
            from escpos.printer import Dummy
            d = Dummy()
            # Initialize printer (optional, depends on printer)
            # d.hw("INIT") 
            return d
        except ImportError:
            logger.error("python-escpos not installed")
            return None

    def print_file(self, file_path):
        """
        Process and print a file. 
        If image/image-like, resize for thermal printer.
        Otherwise send raw bytes.
        """
        d = self._get_dummy()
        if not d: return
        
        try:
            # Try processing as image first to ensure it fits on paper
            # This is critical for mobile screenshots sent as "System Print Documents"
            img = Image.open(file_path)
            max_width = 384 # Standard 58mm width
            w_percent = (max_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
            
            d.image(img)
            d.cut()
            self._raw_print_bytes(d.output)
            
        except (IOError, Exception) as e:
            logger.info("Not a standard image or failed to process, sending raw bytes")
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                self._raw_print_bytes(raw_data)
            except Exception as e2:
                logger.error(f"Failed to print file: {e2}")

