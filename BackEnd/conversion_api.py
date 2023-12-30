from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from conversion_controller import PDFConverter

app = FastAPI()
pdf_converter = PDFConverter()


@app.get("/")
async def root():
    return {"message": "Server is working"}


@app.post("/convert")
async def pdf_to_pdfa(file: UploadFile = File(...)):
    file_contents = await file.read()

    # Call the convert_pdf_to_pdfa method from the PDFConverter instance
    converted_pdf_content = pdf_converter.convert_pdf_to_pdfa(file_contents)

    # Return the converted file for download
    response = StreamingResponse(iter([converted_pdf_content]), media_type="application/pdf")
    response.headers["Content-Disposition"] = f'attachment; filename="converted_pdf.pdf"'

    return response
