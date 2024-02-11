terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.14.0"
    }
  }
}

provider "google" {
  # project ID and region fetched from GCP project dashboard
  project = "ny-taxi-412905"
  region  = "europe-west3"
  # this can also be set by assigning the path to local var GOOGLE_CREDENTIALS
  credentials = "/Users/gdq/Documents/ny-taxi-DE-bootcamp-2024.json"
}

resource "google_storage_bucket" "demo-bucket" {
  # name must be globally unique across GCP
  name          = "ny-taxi-412905-terra-bucket"
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      # number in days
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}