terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  zone      = "ru-central1-a"
}

data "yandex_compute_image" "ubuntu_2204" {
  family = "ubuntu-2204-lts"
}


resource "yandex_compute_instance" "skillbox_vm_gitlab_runner" {
  name        = "skillbox-vm-gitlab-runner"
  platform_id = "standard-v1"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "${data.yandex_compute_image.ubuntu_2204.id}"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.skillbox_subnet.id
    nat = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/skillbox_rsa.pub")}"
  }
}

resource "yandex_compute_instance" "skillbox_vm_service" {
  name        = "skillbox-vm-service"
  platform_id = "standard-v1"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "${data.yandex_compute_image.ubuntu_2204.id}"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.skillbox_subnet.id
    nat = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/skillbox_rsa.pub")}"
  }
}

resource "yandex_vpc_network" "skillbox_network" {
  name = "skillbox-network"
}

resource "yandex_vpc_subnet" "skillbox_subnet" {
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.skillbox_network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_lb_target_group" "skillbox_target_group" {
  name      = "skillbox-target-group"
  region_id = "ru-central1"

  target {
    subnet_id = yandex_vpc_subnet.skillbox_subnet.id
    address   = yandex_compute_instance.skillbox_vm_service.network_interface.0.ip_address
  }
}

resource "yandex_lb_network_load_balancer" "skillbox_balancer" {
  name = "skillbox-balancer"

  listener {
    name = "http-listener"
    port = 80
    target_port = 8080
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.skillbox_target_group.id

    healthcheck {
      name = "http-healthcheck"
      http_options {
        port = 8080
        path = "/health"
      }
    }
  }
}

output "external_ip_address_skillbox_vm_gitlab_runner" {
  value = yandex_compute_instance.skillbox_vm_gitlab_runner.network_interface.0.nat_ip_address
}

output "external_ip_address_skillbox_vm_service" {
  value = yandex_compute_instance.skillbox_vm_service.network_interface.0.nat_ip_address
}

output "skillbox_balancer" {
  value = yandex_lb_network_load_balancer.skillbox_balancer.listener[*].external_address_spec[*].address
}

