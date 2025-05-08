from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from starlette import status
import io

from src.app.database.db_helper import db_helper
from . import crud
from .schemas import (
    FinancialRecord,
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordUpdatePartial,
)
from .utils import get_current_user

router = APIRouter(prefix="/financial_records", tags=["Financial Records"])


@router.get("/", response_model=list[FinancialRecord])
async def get_financial_records(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Retrieves all financial records belonging to the user."""
    return await crud.get_financial_records(
        session=session,
        user_id=current_user_id,
    )


@router.post("/", response_model=FinancialRecord)
async def create_financial_record(
    financial_record_in: FinancialRecordCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Creates a new financial record for the user."""
    return await crud.create_financial_record(
        session=session,
        financial_record_in=financial_record_in,
        user_id=current_user_id,
    )


@router.get("/{financial_record_id}", response_model=FinancialRecord)
async def get_financial_record(
    financial_record_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Returns financial record if it belongs to the user."""
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )
    if financial_record:
        return financial_record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.put("/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_financial_record(
    financial_record_id: int,
    financial_record_update: FinancialRecordUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Completely updates financial record that belongs to the user."""
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.update_financial_record(
            session=session,
            financial_record=financial_record,
            financial_record_update=financial_record_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.patch("/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_financial_record_partial(
    financial_record_id: int,
    financial_record_update: FinancialRecordUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Partially updates financial record that belongs to the user."""
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.update_financial_record_partial(
            session=session,
            financial_record=financial_record,
            financial_record_update=financial_record_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.delete(
    "/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_financial_record(
    financial_record_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Deletes financial record that belongs to the user."""
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.delete_financial_record(
            session=session, financial_record=financial_record
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.post("/generate-pdf/")
async def generate_pdf_report(
    data: dict,
    current_user_id: int = Depends(get_current_user)
):
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Заголовок
        elements.append(Paragraph("Financial Report", styles['Title']))
        elements.append(Paragraph(f"Period: {data['start_date']} to {data['end_date']}", styles['Normal']))
        
        # Основные транзакции
        elements.append(Paragraph("Transactions", styles['Heading2']))
        table_data = [data['columns']] + data['rows']
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t)
        
        # Статистика
        elements.append(Paragraph("Summary Statistics", styles['Heading2']))
        stats_data = [
            ["Metric", "Amount"],
            ["Total Income", f"{data['stats']['total_income']:.2f}"],
            ["Total Expenses", f"{data['stats']['total_expense']:.2f}"],
            ["Balance", f"{data['stats']['balance']:.2f}"]
        ]
        t = Table(stats_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t)
        
        doc.build(elements)
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="application/pdf")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}"
        )