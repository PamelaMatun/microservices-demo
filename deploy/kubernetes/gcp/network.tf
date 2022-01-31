module "network" {
  source  = "terraform-google-modules/network/google"
  version = "4.1.0"

  project_id = var.project

  network_name = "${var.name_prefix}-cne-primary"

  subnets = [
    {
      subnet_region = var.region
      subnet_ip     = "192.168.1.0/24"
      subnet_name   = "${var.name_prefix}-csn-${var.region_infix}-primary"
    }
  ]

  secondary_ranges = {
    "${var.name_prefix}-csn-${var.region_infix}-primary" = [
      {
        ip_cidr_range = "10.0.0.0/22"
        range_name    = "${var.name_prefix}-csr-pod"
      },
      {
        ip_cidr_range = "10.0.4.0/22"
        range_name    = "${var.name_prefix}-csr-service"
      },
    ]
  }
}

/*resource "google_service_networking_connection" "private_vpc_connection" {
  provider = google-beta

  network = module.network.network_self_link
  reserved_peering_ranges = [
  ]
  service = "servicenetworking.googleapis.com"
}*/
