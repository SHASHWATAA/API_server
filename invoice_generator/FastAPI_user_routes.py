from fastapi import APIRouter, Query
from typing import List
from invoice_generator.pdf_generator import main

router = APIRouter()


@router.post("/invoice_generator/generate_invoice")
async def generate_invoice(canvas_days: List[str] = Query(...), cyrus_days: List[str] = Query(...)):
    print("got generation request")
    print(canvas_days)
    print(cyrus_days)
    main(canvas_days, cyrus_days)
    print("completed generation")
    pass

