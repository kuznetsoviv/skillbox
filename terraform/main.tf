terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  zone = "ru-central1-a"
}

data "yandex_compute_image" "ubuntu_2204" {
  family = "ubuntu-2204-lts"
}

locals {
  common_instance_config = {
    platform_id = "standard-v1"
    zone        = "ru-central1-a"
    image_id    = data.yandex_compute_image.ubuntu_2204.id
    subnet_id   = yandex_vpc_subnet.skillbox_subnet.id
  }

  instances = {
    test-service = {
      cores     = 2
      memory    = 2
      ssh_key   = "~/.ssh/test_skillbox_rsa.pub"
      labels    = { role = "backend", env = "test" }
      with_lb   = true
    }
    prod-service = {
      cores     = 2
      memory    = 2
      ssh_key   = "~/.ssh/prod_skillbox_rsa.pub"
      labels    = { role = "backend", env = "prod" }
      with_lb   = true
    }
    gitlab-runner = {
      cores     = 2
      memory    = 2
      ssh_key   = "~/.ssh/skillbox_rsa.pub"
      labels    = { role = "gitlabrunner" }
      with_lb   = false
    }
    monitoring = {
      cores     = 2
      memory    = 2
      ssh_key   = "~/.ssh/skillbox_rsa.pub"
      labels    = { role = "monitoring" }
      with_lb   = false
    }
  }
}

resource "yandex_vpc_network" "skillbox_network" {
  name = "skillbox-network"
}

resource "yandex_vpc_subnet" "skillbox_subnet" {
  name           = "skillbox-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.skillbox_network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_compute_instance" "skillbox_instances" {
  for_each = local.instances

  name        = "skillbox-${each.key}"
  platform_id = local.common_instance_config.platform_id
  zone        = local.common_instance_config.zone

  resources {
    cores  = each.value.cores
    memory = each.value.memory
  }

  boot_disk {
    initialize_params {
      image_id = local.common_instance_config.image_id
    }
  }

  network_interface {
    subnet_id = local.common_instance_config.subnet_id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file(each.value.ssh_key)}"
  }

  labels = each.value.labels
}

resource "yandex_lb_target_group" "skillbox_target_groups" {
  for_each = { for k, v in local.instances : k => v if v.with_lb }

  name      = "skillbox-${each.key}-target-group"
  region_id = "ru-central1"

  target {
    subnet_id = yandex_vpc_subnet.skillbox_subnet.id
    address   = yandex_compute_instance.skillbox_instances[each.key].network_interface.0.ip_address
  }
}

resource "yandex_lb_network_load_balancer" "skillbox_load_balancers" {
  for_each = { for k, v in local.instances : k => v if v.with_lb }

  name = "skillbox-${each.key}-load-balancer"

  listener {
    name        = "http-listener"
    port        = 80
    target_port = 8080
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.skillbox_target_groups[each.key].id

    healthcheck {
      name = "http-healthcheck"
      http_options {
        port = 8080
        path = "/health"
      }
    }
  }
}

output "load_balancer_addresses" {
  value = {
    for lb_name, lb in yandex_lb_network_load_balancer.skillbox_load_balancers :
    lb_name => lb.listener[*].external_address_spec[*].address
  }
  description = "Load balancer external addresses"
}

output "external_ip_address_skillbox_service_test" {
  value       = yandex_compute_instance.skillbox_instances["test-service"].network_interface.0.nat_ip_address
  description = "External IP address of test service instance"
}

output "external_ip_address_skillbox_service_prod" {
  value       = yandex_compute_instance.skillbox_instances["prod-service"].network_interface.0.nat_ip_address
  description = "External IP address of prod service instance"
}

output "external_ip_address_skillbox_gitlab_runner" {
  value       = yandex_compute_instance.skillbox_instances["gitlab-runner"].network_interface.0.nat_ip_address
  description = "External IP address of GitLab Runner instance"
}

output "external_ip_address_skillbox_monitoring" {
  value       = yandex_compute_instance.skillbox_instances["monitoring"].network_interface.0.nat_ip_address
  description = "External IP address of monitoring instance"
}