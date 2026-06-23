output "app_url" {
  value = "http://${azurerm_container_group.app.fqdn}:5000"
}