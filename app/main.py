from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.aws_services import process_product_image, get_classification_history
from app.evaluation import evaluate_predictions


app = FastAPI(
    title="FastRetail Image Classifier",
    description="Sistema de clasificación automática de imágenes con Amazon Rekognition",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.post("/classify", response_class=HTMLResponse)
async def classify_image(request: Request, file: UploadFile = File(...)):
    allowed_extensions = ["jpg", "jpeg", "png"]

    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Usa JPG, JPEG o PNG."
        )

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío."
        )

    try:
        result = process_product_image(file_bytes, file.filename)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "result": result
        }
    )


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    try:
        items = get_classification_history()
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "items": items
        }
    )


@app.get("/api/history")
def api_history():
    return get_classification_history()


@app.post("/api/classify")
async def api_classify_image(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return process_product_image(file_bytes, file.filename)


@app.get("/api/evaluation-demo")
def api_evaluation_demo():
    """
    Endpoint de demostración para enseñar cómo se mediría la precisión.
    Estos datos pueden sustituirse por resultados reales de pruebas.
    """

    test_cases = [
        {"real": "Calzado", "predicted": "Calzado"},
        {"real": "Ropa superior", "predicted": "Ropa superior"},
        {"real": "Accesorios", "predicted": "Accesorios"},
        {"real": "Bolsos y mochilas", "predicted": "Bolsos y mochilas"},
        {"real": "Ropa inferior", "predicted": "Sin categoría"}
    ]

    return evaluate_predictions(test_cases)