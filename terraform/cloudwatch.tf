#create a cloudwatch metric alarm for specified resources

resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-error-alarm" #This is the name of the alarm that will appear in AWS Console
  alarm_description   = "triggers when the Lambda has 1 or more errors in 30 secs"  # Tell is a note of what the alarm does
  comparison_operator = "GreaterThanOrEqualToThreshold" #This tells the alarm when to trigger. For instance, the alarm will be triggered if the number of errors is >= Threshol
  evaluation_periods  = var.evaluation_periods #Only checks once before triggering the alarm. CW will only look at 1 period of data before deciding whether to to trigger the alarm .
  metric_name         = "Errors" #This is what we are measuring 
  namespace           = "AWS/Lambda" #This tells AWS to look for a Lambda and not something else like EC2 or S3
  period              = var.period #Check Every 30 seconds 
  statistic           = "Sum" #Sum all those errors within that 30-seond windown. 
  threshold           = var.threshold #Alarm will trigger if we see 1 or more errors
  treat_missing_data  = "notBreaching" #If there is no data, assume nothing went wrong
  alarm_actions = [aws_sns_topic.lambda_alerts.arn ]
  ok_actions    = [aws_sns_topic.lambda_alerts.arn]  # when errors go away - we should be notified 

  dimensions = {
    FunctionName = aws_lambda_function.extract_handler.function_name #This narrows the alarm to only watch the specific Lambda function by name.
  }
}

# Create an SNS topic to send Lambda error alerts
resource "aws_sns_topic" "lambda_alerts" {
  name = "lambda-error-alerts"
}

# Subscribe an email address to the SNS topic to get alert emails
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "email"
  endpoint  = var.endpoint   # Email address to send alerts to
}
