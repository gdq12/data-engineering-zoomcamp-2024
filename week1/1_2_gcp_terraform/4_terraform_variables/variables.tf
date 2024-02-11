variable "bq_dataset_nytaxi" {
  description = "My ny taxi dataset"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "4 gcp bucket"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "my description bucketname"
  default     = "ny-taxi-412905-terra-bucket"
}

variable "location" {
  description = "project location"
  default     = "EU"
}

variable "project" {
  description = "project name"
  default     = "ny-taxi-412905"
}

variable "region" {
  description = "region used for project"
  default     = "europe-west3"
}

variable "credentials" {
  description = "project credentials"
  default     = "/Users/gdq/Documents/ny-taxi-DE-bootcamp-2024.json"
}