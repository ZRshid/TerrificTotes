#create a cloudwatch metric alarm for specified resources
resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-error-alarm"
  alarm_description   = "triggers when the Lambda has 1 or more errors in 5 minutes"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 30
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"

  #to filter/identify a specific resource
  dimensions = {
    FunctionName = aws_lambda_function.extract_handler.function_name
  }

#   alarm_actions = [aws_sns_topic.lambda_alerts.arn] allow for email
}

# resource "aws_sns_topic" "lambda_alerts" {
#   name = "lambda-error-alerts"
# }

# resource "aws_sns_topic_subscription" "email_alert" {
#   topic_arn = aws_sns_topic.lambda_alerts.arn
#   protocol  = "email"
#   endpoint  =  "ncproject_phase@gmail.com"
# }