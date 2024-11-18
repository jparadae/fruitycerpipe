resource "aws_kinesis_stream" "data_ingest" {
  name             = "fruitycert-inspections-stream"
  shard_count      = 2
  retention_period = 24 # En horas
  tags = {
    Environment = "Production"
    Application = "FruityCert"
  }
}


