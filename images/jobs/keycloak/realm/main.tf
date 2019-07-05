provider "keycloak" {
  client_id = "admin-cli"
}

resource "keycloak_realm" "realm" {
  realm                           = var.realm
  enabled                         = var.enabled
  display_name                    = var.display_name
  registration_allowed            = var.registration_allowed
  registration_email_as_username  = var.registration_email_as_username
  edit_username_allowed           = var.edit_username_allowed
  reset_password_allowed          = var.reset_password_allowed
  remember_me                     = var.remember_me
  verify_email                    = var.verify_email
  login_with_email_allowed        = var.login_with_email_allowed
  duplicate_emails_allowed        = var.duplicate_emails_allowed
  login_theme                     = var.login_theme
  account_theme                   = var.account_theme
  admin_theme                     = var.admin_theme
  email_theme                     = var.email_theme
}
