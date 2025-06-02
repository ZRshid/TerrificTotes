#create a cloudwatch metric alarm for specified resources
resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-error-alarm"
  alarm_description   = "triggers when the Lambda has 1 or more errors in 30 secs"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = var.evaluation_periods
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = var.period
  statistic           = "Sum"
  threshold           = var.threshold
  treat_missing_data  = "notBreaching"
  alarm_actions = [aws_sns_topic.lambda_alerts.arn ]

  #to filter/identify a specific resource
  dimensions = {
    FunctionName = aws_lambda_function.extract_handler.function_name
  }

}

resource "aws_sns_topic" "lambda_alerts" {
  name = "lambda-error-alerts"
}

resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "email"
  endpoint  =  var.endpoint
}