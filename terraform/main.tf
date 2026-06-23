provider "azurerm" {
  features {}

  resource_provider_registrations = "none"
}
# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "capstone-rg"
  location = "East US"
}

# Container Instance (runs your Docker image)
resource "azurerm_container_group" "app" {
  name                = "flask-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"

  container {
    name   = "flask-container"
    image  = "myflaskregistry123.azurecr.io/my-flask-app"
    cpu    = "1"
    memory = "1.5"

    ports {
      port     = 5000
      protocol = "TCP"
    }
  }

  ip_address_type = "Public"

  dns_name_label = "flaskappdemo12345"  # MUST be unique globally

  exposed_port {
    port = 5000
  }
}
