variable "realm" {}
variable "display_name" {}
variable "enabled" {}

variable "registration_allowed" {
  default = false
}

variable "registration_email_as_username" {
  default = false
}

variable "edit_username_allowed" {
  default = false
}

variable "reset_password_allowed" {
  default = false
}

variable "remember_me" {
  default = false
}

variable "verify_email" {
  default = false
}

variable "login_with_email_allowed" {
  default = true
}

variable "duplicate_emails_allowed" {
  default = false
}

variable "login_theme" {
  default = "keycloak"
}

variable "account_theme" {
  default = "keycloak"
}

variable "admin_theme" {
  default = "keycloak"
}

variable "email_theme" {
  default = "keycloak"
}



