from .models import Request
from comment_analysis.lambda_config import check_s3_analyze


def check_analyze(request_id):

    db_check = Request.objects.get(request_display=request_id).analyze_completed
    s3_check = check_s3_analyze(request_id=request_id)
    request = Request.objects.get(request_display=request_id)

    if s3_check == True:
        if db_check == False:
            request.analyze_completed = True
            request.save()
    else:
        if db_check == True:
            request.analyze_completed = False
            request.save()

    db_check = Request.objects.get(request_display=request_id).analyze_completed
    s3_check = check_s3_analyze(request_id=request_id)

    return db_check and s3_check
