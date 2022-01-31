module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "18.0.0"

  project_id = var.project
  region     = var.region

  ip_range_pods          = module.network.subnets_secondary_ranges[0].*.range_name[0]
  ip_range_services      = module.network.subnets_secondary_ranges[0].*.range_name[1]
  network                = module.network.network_name
  subnetwork             = module.network.subnets_names[0]

  name            = "${var.name_prefix}-kcl-${var.region_infix}-primary"
  release_channel = "STABLE"

  default_max_pods_per_node       = 32
  enable_vertical_pod_autoscaling = true
  remove_default_node_pool        = true
  skip_provisioners               = true

  node_pools = [
    {
      node_count   = 1
      machine_type = "e2-standard-2"
      name         = "${var.name_prefix}-knp-${var.region_infix}"
    }
  ]

  //grant_registry_access = true
  //registry_project_ids  = [var.registry_project]
}
