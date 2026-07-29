import pandas as pd
import numpy as np
import joblib
import json
import os
import csv
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from reportlab.pdfgen import canvas
from .forms import HouseForm, CSVUploadForm, DatasetReplaceForm
from .models import Prediction
from .utils import load_model_pipeline


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    total = predictions.count()
    last_pred = predictions.first()
    try:
        with open('models/evaluation.json') as f:
            metrics = json.load(f)
        best_r2 = metrics['Random Forest']['R2_Score']
    except:
        best_r2 = 'N/A'
    return render(request, 'predictor/dashboard.html', {
        'total': total,
        'last_pred': last_pred,
        'best_r2': best_r2,
        'active': 'dashboard'
    })

@login_required
def predict_price(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    prediction = None
    form = HouseForm()

    if request.method == "POST":
        form = HouseForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            try:
                print("FORM DATA:", data)

                pipeline = load_model_pipeline("rf_model.pkl")

                input_df = pd.DataFrame([data])

                predicted_price = pipeline.predict(input_df)[0]

                prediction = round(float(predicted_price), 2)

                print("PREDICTION =", prediction)

                Prediction.objects.create(
                    user=request.user,
                    sqft=data["sqft"],
                    bedrooms=data["bedrooms"],
                    bathrooms=data["bathrooms"],
                    age_of_house=data["age_of_house"],
                    location=data["location"],
                    predicted_price=prediction,
                )

            except Exception as e:
                print("ERROR:", e)
                form.add_error(None, str(e))

    print("RETURNING:", prediction)

    return render(
        request,
        "predictor/predict.html",
        {
            "form": form,
            "prediction": prediction,
            "active": "predict",
        },
    )

@login_required
def history(request):
    preds = Prediction.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(preds, 10)
    page_number = request.GET.get('page')
    preds_page = paginator.get_page(page_number)
    return render(request, 'predictor/history.html', {'predictions': preds_page, 'active': 'history'})

@login_required
def evaluation(request):
    try:
        with open('models/evaluation.json') as f:
            metrics = json.load(f)
    except:
        metrics = {}
    return render(request, 'predictor/evaluation.html', {'metrics': metrics, 'active': 'evaluation'})

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            pipeline = load_model_pipeline('rf_model.pkl')
            predictions = pipeline.predict(df[['sqft','bedrooms','bathrooms','age_of_house','location']])
            df['predicted_price'] = predictions.round(2)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="predicted_prices.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response
    else:
        form = CSVUploadForm()
    return render(request, 'predictor/upload.html', {'form': form, 'active': 'upload'})

@login_required
def download_report(request):
    last_pred = Prediction.objects.filter(user=request.user).order_by('-created_at').first()
    if not last_pred:
        return redirect('predict')
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "House Price Prediction Report")
    p.drawString(100, 730, f"Square Footage: {last_pred.sqft}")
    p.drawString(100, 710, f"Bedrooms: {last_pred.bedrooms}")
    p.drawString(100, 690, f"Bathrooms: {last_pred.bathrooms}")
    p.drawString(100, 670, f"Age: {last_pred.age_of_house} years")
    p.drawString(100, 650, f"Location: {last_pred.location}")
    p.drawString(100, 630, f"Predicted Price: ${last_pred.predicted_price}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf',
                        headers={'Content-Disposition': 'attachment; filename="prediction_report.pdf"'})

# ---------- Admin Views ----------
@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_predictions = Prediction.objects.count()
    total_models = 3
    latest = Prediction.objects.select_related('user').order_by('-created_at')[:5]
    loc_counts = Prediction.objects.values('location').annotate(c=Count('id')).order_by('-c')[:5]
    chart_labels = [item['location'] for item in loc_counts]
    chart_data = [item['c'] for item in loc_counts]
    return render(request, 'predictor/admin_dashboard.html', {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'total_models': total_models,
        'latest_predictions': latest,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })

@staff_member_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    return render(request, 'predictor/admin_users.html', {'users': users_page})

@staff_member_required
def admin_predictions(request):
    predictions = Prediction.objects.select_related('user').order_by('-created_at')
    q = request.GET.get('q')
    if q:
        predictions = predictions.filter(
            models.Q(location__icontains=q) | models.Q(user__username__icontains=q)
        )
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    preds_page = paginator.get_page(page_number)
    return render(request, 'predictor/admin_predictions.html', {
        'predictions': preds_page,
        'search_query': q
    })

@staff_member_required
def admin_models(request):
    try:
        with open('models/evaluation.json') as f:
            metrics = json.load(f)
    except:
        metrics = None
    return render(request, 'predictor/admin_models.html', {'metrics': metrics})

@staff_member_required
def admin_dataset(request):
    message = None
    if request.method == 'POST':
        form = DatasetReplaceForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            with open('house_data.csv', 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            import subprocess
            result = subprocess.run(['python', 'train_model.py'], capture_output=True, text=True)
            if result.returncode == 0:
                message = f"✅ Dataset replaced and models retrained.\n{result.stdout[-300:]}"
            else:
                message = f"⚠️ Dataset saved, but retraining failed: {result.stderr}"
    else:
        form = DatasetReplaceForm()
    return render(request, 'predictor/admin_dataset.html', {'form': form, 'message': message})

@staff_member_required
def admin_reports(request):
    return render(request, 'predictor/admin_reports.html', {'active': 'reports'})

@staff_member_required
def admin_csv_download(request):
    predictions = Prediction.objects.select_related('user').order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_predictions.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Sqft', 'Bedrooms', 'Bathrooms', 'Age', 'Location', 'Predicted Price', 'Date'])
    for p in predictions:
        writer.writerow([p.user.username, p.sqft, p.bedrooms, p.bathrooms, p.age_of_house, p.location, p.predicted_price, p.created_at])
    return response

@staff_member_required
def admin_analytics(request):
    return render(request, 'predictor/analytics.html')


@staff_member_required
def analytics_pdf_report(request):

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="analytics_report.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold",18)

    pdf.drawString(170,800,"Analytics Report")

    total_users = User.objects.count()

    total_predictions = Prediction.objects.count()

    avg_price = Prediction.objects.aggregate(
        Avg('predicted_price')
    )['predicted_price__avg']

    pdf.setFont("Helvetica",12)

    pdf.drawString(80,740,f"Total Users : {total_users}")

    pdf.drawString(80,715,f"Total Predictions : {total_predictions}")

    pdf.drawString(
        80,
        690,
        f"Average House Price : ${round(avg_price or 0,2)}"
    )

    pdf.save()

    return response



@staff_member_required
def admin_pdf_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_predictions.pdf"'

    doc = SimpleDocTemplate(response)

    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>House Price Prediction Report</b>", styles['Title']))

    predictions = Prediction.objects.select_related('user')

    data = [
        [
            "User",
            "Sqft",
            "Bedrooms",
            "Bathrooms",
            "Age",
            "Location",
            "Price"
        ]
    ]

    for p in predictions:

        data.append([
            p.user.username,
            p.sqft,
            p.bedrooms,
            p.bathrooms,
            p.age_of_house,
            p.location,
            f"${p.predicted_price}"
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID',(0,0),(-1,-1),1,colors.grey),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige),

        ('ALIGN',(0,0),(-1,-1),'CENTER')

    ]))

    elements.append(table)

    doc.build(elements)

    return response