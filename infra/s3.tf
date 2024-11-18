resource "aws_s3_bucket" "data_storage" {
  bucket = "fruitycert-data-brutos"
  acl    = "private"
  lifecycle_rule {
    enabled = true
    transition {
      days          = 30
      storage_class = "INTELLIGENT_TIERING"
    }
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
