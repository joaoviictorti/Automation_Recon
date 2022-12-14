terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "2.25.2"
    }
  }
}

provider "digitalocean" {
 token = var.do_token
}

variable "do_token" {
  type = string
  default = "<token>"
}

resource "digitalocean_ssh_key" "teste" {
    name = "teste"
    public_key = file("~/.ssh/id_rsa.pub")
}

resource "digitalocean_droplet" "Pentest" {
    image  = "ubuntu-18-04-x64"
    name   = "Pentest"
    region = "nyc1"
    size   = "s-1vcpu-1gb" 
    ssh_keys = [digitalocean_ssh_key.teste.fingerprint]
}