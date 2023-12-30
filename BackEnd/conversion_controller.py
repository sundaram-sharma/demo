import os
import subprocess
import re
from shutil import copyfile
from tempfile import NamedTemporaryFile


class PDFConverter:
    def __init__(self, jhove_exec='jhove'):
        self.ghostscript_exec = ['gs', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-sProcessColorModel=DeviceCMYK',
                                 '-sDEVICE=pdfwrite', '-sPDFACompatibilityPolicy=1']
        self.jhove_exec = jhove_exec

    def check_output_from_jhove(self, actual_file):
        output_lines = subprocess.check_output([self.jhove_exec, actual_file]).decode("utf-8").splitlines()
        return any('PDF/A' in line for line in output_lines if re.match('^\s*Profile:', line))

    def convert_pdf_to_pdfa(self, source_file_contents):
        # Check if the source file is already in PDF/A format
        is_pdfa = self.check_output_from_jhove_from_bytes(source_file_contents)

        # Determine the target file contents
        target_file_contents = source_file_contents

        if not is_pdfa:
            # If not, perform the conversion using Ghostscript
            try:
                target_file_contents = subprocess.check_output(
                    self.ghostscript_exec, input=source_file_contents
                )
                print("Converted PDF to PDF/A.")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Command '{e.cmd}' returned with error (code {e.returncode}): {e.output}"
                )

        return target_file_contents

    def check_output_from_jhove_from_bytes(self, file_contents):
        # Convert bytes to a temporary file and use check_output_from_jhove
        with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(file_contents)
            temp_file_path = temp_file.name

        try:
            return self.check_output_from_jhove(temp_file_path)
        finally:
            os.remove(temp_file_path)
# Example Usage:
converter = PDFConverter()