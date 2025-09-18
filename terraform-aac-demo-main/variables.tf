variable "apic_username" {
  description = "APIC User"
  type        = string
}

variable "apic_password" {
  description = "APIC Password"
  type        = string
  sensitive   = true
}

variable "apic_url" {
  description = "APIC URL"
  type        = string
}
