# #create a cloudwatch metric alarm for specified resources
resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-error-alarm"
  alarm_description   = "triggers when the Lambda has 1 or more errors in 30 secs"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 30
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"
  alarm_actions = [ aws_sns_topic.lambda_alerts.arn ]

  #to filter/identify a specific resource
  dimensions = {
    FunctionName = aws_lambda_function.extract_handler.function_name
  }
}

#create alarm, triggers alarm when lambda handler is successful once 
# resource "aws_cloudwatch_metric_alarm" "lambda_success_alarm" {
#   alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-success-alarm"
#   alarm_description   = "triggers when the Lambda has 1 or more success in 30 secs"
#   comparison_operator = "GreaterThanOrEqualToThreshold"
#   evaluation_periods  = 1
#   metric_name         = "SuccessfulExecutions"
#   namespace           = "test/Lambda"
#   period              = 30
#   statistic           = "Sum"
#   threshold           = 1
#   treat_missing_data  = "notBreaching"
#   alarm_actions = [ aws_sns_topic.lambda_alerts.arn ]

#   #to filter/identify a specific resource
#   dimensions = {
#     FunctionName = aws_lambda_function.extract_handler.function_name
#   }
# }

#fancy alarm that just subtracts invocations to errors 
# resource "aws_cloudwatch_metric_alarm" "lambda_success_alarm" {
#   alarm_name          = "lambda-${aws_lambda_function.extract_handler.function_name}-success-alarm"
#   alarm_description   = "Triggers if there are fewer than 1 successful Lambda executions in 3 min"
#   comparison_operator = "LessThanThreshold"
#   evaluation_periods  = 1
#   threshold           = 1
#   treat_missing_data  = "notBreaching"
#   alarm_actions       = [aws_sns_topic.lambda_alerts.arn]

#   metric_query {
#     id = "invocations"
#     metric {
#       metric_name = "Invocations"
#       namespace   = "AWS/Lambda"
#       period      = 10
#       stat        = "Sum"
#       dimensions = {
#         FunctionName = aws_lambda_function.extract_handler.function_name
#       }
#     }
#     return_data = true
#   }

#   metric_query {
#     id = "errors"
#     metric {
#       metric_name = "Errors"
#       namespace   = "AWS/Lambda"
#       period      = 10
#       stat        = "Sum"
#       dimensions = {
#         FunctionName = aws_lambda_function.extract_handler.function_name
#       }
#     }
#     return_data = false
#   }

#   metric_query {
#     id          = "successes"
#     expression  = "invocations - errors"
#     label       = "Successful Invocations"
#     return_data = true
#   }
# }

resource "aws_sns_topic" "lambda_alerts" {
  name = "lambda-error-alerts"
}

resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "email"
  endpoint  =  var.endpoint
}