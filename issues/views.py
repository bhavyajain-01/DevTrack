from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Reporter,Issue, CriticalIssue, LowPriorityIssue
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def get_issues(request, id=None):
    issue_id = request.GET.get('id')
    status_param = request.GET.get('status')

    with open("issues/issues.json", "r") as file:
        issues = json.load(file)


    if id is None:
        return JsonResponse(issues)
    for issue in issues:
        if issue["id"] == int(id):
            return JsonResponse(issue)
    return JsonResponse({"error": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def post_issues(request):
    data = json.loads(request.body)

    date_text = data.get('created_at')
    real_date = datetime.strptime(date_text, "%Y-%m-%d")

    priority = data.get('priority')



    if priority == 'critical':
        issue = CriticalIssue(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority= priority,
            reporter_id=data.get('reporter_id'),
            created_at = real_date        )


    elif priority == 'low':
        issue = LowPriorityIssue(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority=priority,
            reporter_id=data.get('reporter_id'),
            created_at=real_date
        )
    else:
        issue = Issue(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority= priority,
            reporter_id=data.get('reporter_id'),
            created_at=real_date 
        )
    try:
        issue.validate()
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status =400)
            
    response_data = issue.to_dict()
    response_data['message'] = issue.describe()

    return JsonResponse(response_data, status=201)

def get_Reporter( request, reporter_id):
    with open("issues/Reporter.json","r")as fi:
        reporters= json.load(fi)

        if not reporters:
            return JsonResponse({"error": "Reporters not found"})
        
        for reporter in reporters:
            if reporter["id"] == int(reporter_id):
                return JsonResponse(reporter) 

        return JsonResponse({"error": "Reporter not found"}, status=status.HTTP_404_NOT_FOUND)  

@csrf_exempt
def post_Reporter(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    reporter = Reporter(
        id=data.get('id'),
        name=data.get('name'),
        email=data.get('email'),
        team=data.get('team')
    )
    try:
        reporter.validate()
    except ValueError as e:
            return JsonResponse({"error": str(e)}, status =400)
                
    response_data = reporter.to_dict()
    response_data['message'] = reporter.describe()
    
    # यदि आपके Reporter मॉडल में validate या to_dict मेथड है, तो आप यहाँ जोड़ सकते हैं
    # अभी के लिए हम इसे डिक्शनरी के रूप में रिटर्न कर रहे हैं:
    response_data = {
        "id": reporter.id,
        "name": reporter.name,
        "email": reporter.email,
        "team": reporter.team
    }

    return JsonResponse(response_data, status=201)

             
                  